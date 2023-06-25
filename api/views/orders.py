from rest_framework.decorators import api_view,throttle_classes
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.response import Response
from api.exceptions import InvalidUserTypeException, BadRequestException
from api.models import Order, Cart, OrderItem
from api.serializers import OrderItemSerializer, OrderSerializer, OrderUpdateSerializer
from django.db import transaction
from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import status
from api.views.utils import allow_access, paginate_items, order_query_result
import api.views.utils.constants as c

@transaction.atomic
@api_view([c.GET, c.POST])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
@allow_access(
    {
        c.CUSTOMER: [c.GET, c.POST],
        c.DELIVERY_CREW: [c.GET],
        c.MANAGER: [c.GET],
    }
)
def orders(request):
    user = request.user

    if request.method == c.POST:
        cart_items = Cart.objects.filter(user=user)

        if len(cart_items) == 0:
            return Response(
                {
                    "error": "Your cart is empty. You need a least one item to create an order."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        order_total = sum([c.price for c in cart_items])
        order = Order(user=user, date=datetime.now(), total=order_total)
        order.save()

        for a in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                menuitem=a.menuitem,
                quantity=a.quantity,
                unit_price=a.unit_price,
                price=a.price,
            )
            order_item.save()

        Cart.objects.filter(user=user).delete()
        order_serializer = OrderSerializer(order)

        return Response(order_serializer.data)
    else:
        user_groups = [g["name"] for g in user.groups.values()]
        
        if c.MANAGER in user_groups:
            orders_query = Order.objects.all()
        elif c.DELIVERY_CREW in user_groups:
            orders_query = Order.objects.filter(delivery_crew=user)
        else:
            orders_query = Order.objects.filter(user=user)

        orders = order_query_result(request, orders_query)
        page_result = paginate_items(request, orders)
        order_serializer = OrderSerializer(page_result, many=True)

        return Response(order_serializer.data)



@transaction.atomic
@api_view([c.GET, c.PATCH, c.PUT, c.DELETE])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
@allow_access(
    {
        c.CUSTOMER: [c.GET],
        c.DELIVERY_CREW: [c.PUT, c.PATCH],
        c.MANAGER: [c.PUT, c.PATCH, c.DELETE],
    }
)
def order(request, pk):
    user = request.user
    user_group_names = [g["name"] for g in request.user.groups.values()]

    try:
        if request.method in [c.PUT, c.PATCH]:
            order = Order.objects.get(pk=pk)
            request_data = request.data
            delivery_crew_id = request_data.get("delivery_crew")

            if delivery_crew_id and not User.objects.filter(pk=delivery_crew_id, groups__name=c.DELIVERY_CREW).exists():
                raise InvalidUserTypeException("Invalid Delivery Crew ID")
            
            if c.DELIVERY_CREW in user_group_names and "delivery_crew" in request_data:
                raise BadRequestException(f"User is not allow to modify property 'delivery_crew'.")
 
            serializer = OrderUpdateSerializer(order, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                order_serializer = OrderSerializer(order)
                return Response(order_serializer.data)
            else:
                raise BadRequestException(f"Invalid request data. Cause: {serializer.errors}")
        elif request.method == c.DELETE:
            order = Order.objects.get(pk=pk)
            order.delete()
            return Response({"message": f"Order {pk} deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            order = Order.objects.get(pk=pk, user=user)
            order_serializer = OrderSerializer(order)
            return Response(order_serializer.data)
    except Order.DoesNotExist:
        raise BadRequestException(f"Order ID {pk} does not exist")
