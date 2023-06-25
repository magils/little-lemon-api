from rest_framework.decorators import api_view,throttle_classes
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.contrib.auth.models import Group, User
from rest_framework.response import Response
from rest_framework import status
from api.serializers import UserSerializer
from api.views.utils import allow_access, paginate_items, order_query_result
import api.views.utils.constants as c

@api_view([c.GET, c.POST])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
@allow_access(
    {
        c.MANAGER: [c.GET, c.POST],
    }
)
def manage_groups(request, group_name):    
    if group_name not in (c.DELIVERY_CREW, c.MANAGER,):
        return Response(
            {"error": f"Invalid user type '{group_name}'"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if request.method == "POST":
        username = request.data.get("username")

        if not username:
            return Response(
                {"message": "Missing required field 'username'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_group = Group.objects.get(name=group_name)
            user = User.objects.get(username=username)
            user_group.user_set.add(user)
            return Response(
                {"message": f"User added to group '{group_name}'"},
                status=status.HTTP_201_CREATED
            )
        except User.DoesNotExist:
            return Response(
                {"message": f"User '{username}' not found"},
                status=status.HTTP_404_NOT_FOUND
            )
    else:
        try:
            users_query = User.objects.filter(groups__name=group_name).order_by("id")
            users = order_query_result(request, users_query)
            pagination_result = paginate_items(request, users)
            users_data = UserSerializer(pagination_result, many=True).data
            return Response(users_data)
        except User.DoesNotExist:
            return Response(
                {"error": "Group does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )


@api_view([c.DELETE])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
@allow_access(
    {
        c.MANAGER: [c.DELETE],
    }
)
def manage_group(request, group_name, pk):
    if group_name not in (c.DELIVERY_CREW, c.MANAGER,):
        return Response(
            {"error": f"Invalid user type '{group_name}'"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        if User.objects.filter(pk=pk, groups__name=group_name):
            user = User.objects.get(pk=pk)
            group = Group.objects.get(name=group_name)
            group.user_set.remove(user)
            resp = {"message": f"User {pk} removed from group '{group_name}'"}
            _status = status.HTTP_204_NO_CONTENT
        else:
            resp = {"message": f"User {pk} does not belong to group '{group_name}'"}
            _status = status.HTTP_400_BAD_REQUEST
    except User.DoesNotExist:
        return Response(
            {"error": f"User ID {pk} does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    return Response(
        resp,
        status=_status
    )

