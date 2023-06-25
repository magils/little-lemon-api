from api.models import MenuItem, Category
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.response import Response
from api.serializers import CategorySerializer, MenuItemSerializer
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework import status
from api.views.utils import allow_access, paginate_items, order_query_result
import api.views.utils.constants as c

@api_view([c.GET, c.POST])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
@allow_access(
    {
        c.DELIVERY_CREW: [c.GET],
        c.CUSTOMER: [c.GET],
        c.MANAGER: [c.GET, c.POST],
    }
)
def menuitems(request):
    if request.method == c.POST:
        json_data = JSONParser().parse(request)
        serializer = MenuItemSerializer(data=json_data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(
                {"error": f"Invalid data. Cause: '{serializer.errors}'"}
            )
    else:
        menuitems_query = MenuItem.objects.all()
        menuitems = order_query_result(request, menuitems_query)
        page_result = paginate_items(request, menuitems)
        serializer = MenuItemSerializer(page_result, many=True)

        return Response(serializer.data)


@api_view([c.GET, c.PUT, c.PATCH, c.DELETE])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
@allow_access(
    {
        c.DELIVERY_CREW: [c.GET],
        c.CUSTOMER: [c.GET],
        c.MANAGER: [c.GET, c.PUT, c.PATCH, c.DELETE],
    }
)
def menuitem(request, pk):
    try:
        menu_item = MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return Response({"error": f"MenuItem '{pk}' not found "}, status=status.HTTP_404_NOT_FOUND)

    if request.method == c.PUT:
        serializer = MenuItemSerializer(menu_item, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return Response({"error": f"Invalid JSON payload. Cause: {serializer.errors}"})
    elif request.method == c.DELETE:
        menu_item.delete()
        return Response({"message": f"MenuItem {pk} deleted"}, status=status.HTTP_204_NO_CONTENT)
    elif request.method == c.PATCH:
        serializer = MenuItemSerializer(menu_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"error": f"Invalid request data. Cause: {serializer.errors}"})
    else:
        serializer = MenuItemSerializer(menu_item)
        return Response(serializer.data)

@api_view([c.GET, c.POST])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
@allow_access(
    {
        c.DELIVERY_CREW: [c.GET],
        c.CUSTOMER: [c.GET],
        c.MANAGER: [c.GET, c.POST],
    }
)
def categories(request):
    if request.method == c.POST:
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(
                {"error": f"Invalid data. Cause: '{serializer.errors}'"}
            )
    else:
        categories_query = Category.objects.all()
        categories = order_query_result(request, categories_query)
        page_result = paginate_items(request, categories)
        serializer = CategorySerializer(page_result, many=True)

        return Response(serializer.data)

@api_view([c.GET])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
@allow_access(
    {
        c.DELIVERY_CREW: [c.GET],
        c.CUSTOMER: [c.GET],
        c.MANAGER: [c.GET],
    }
)
def category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({"error": f"Category '{pk}' not found "}, status=status.HTTP_404_NOT_FOUND)

    serializer = CategorySerializer(category)

    return Response(serializer.data)