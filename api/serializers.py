from rest_framework import serializers
from django.contrib.auth.models import User, Group
from api.models import *

# TODO: Change this
# Creating serializers manually just for practicing
class CategorySerializer(serializers.Serializer):
    slug = serializers.SlugField()
    title = serializers.CharField(max_length=255)


# Using model serializers from now on
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class UserRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(required=False, max_length=250)
    password = serializers.CharField(required=True, max_length=2048)
    first_name = serializers.CharField(required=True, max_length=255)
    last_name = serializers.CharField(required=True, max_length=255)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "groups",
            "date_joined"
        )
        extra_kwargs = {
            "username": {"required": True}
        }


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "status",
            "delivery_crew"
        ]
        extra_kwargs = {
            "status": {
                "required": True
            },
            "delivery_crew": {
                "required": True
            }
        }