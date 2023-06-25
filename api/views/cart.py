from rest_framework.decorators import api_view,throttle_classes
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from django.contrib.auth.models import User
from api.models import Cart, MenuItem
from api.serializers import CartSerializer
from api.views.utils import allow_access, paginate_items, order_query_result
import api.views.utils.constants as c
import traceback


@api_view([c.GET, c.POST, c.DELETE])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
@allow_access(
    {
        c.CUSTOMER: [c.GET, c.POST, c.DELETE]
    }
)
def cart_menuitems(request):
    user = request.user

    if request.method == "POST":
        data_json = request.data

        try:
            item_id = data_json.get("item_id")
            menuitem = MenuItem.objects.get(pk=item_id)
        except MenuItem.DoesNotExist:
            return Response(
                {"message": f"Menu Item {item_id} not found"}
            )

        item_quantity = data_json.get("quantity")
        cart = Cart.objects.filter(user=user, menuitem=menuitem)
        
        if cart:
            cart = cart.first()
            cart.unit_price = menuitem.price
            cart.quantity = item_quantity
            cart.price = (item_quantity * menuitem.price)
        else:
            cart = Cart.objects.create(
                user=user,
                unit_price=menuitem.price,
                quantity=item_quantity,
                menuitem=menuitem,
                price=(item_quantity * menuitem.price),
            )
        cart.save()
        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == "DELETE":
        Cart.objects.filter(user=user).delete()
        return Response({"message": "Cart deleted"}, status=status.HTTP_204_NO_CONTENT)
    else:
        carts_query = Cart.objects.filter(user=user)
        carts = order_query_result(request, carts_query)
        cart_page = paginate_items(request, carts)
        cart_serializer = CartSerializer(cart_page, many=True)
        return Response(cart_serializer.data)
