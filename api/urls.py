from django.urls import path, include
from api.views import menuitem, cart, orders, groups

urlpatterns = [
    path("menu-items", menuitem.menuitems, name="menu-items"),
    path("categories", menuitem.categories, name="categories"),
    path("categories/<int:pk>", menuitem.category, name="category"),
    path("menu-items/<int:pk>", menuitem.menuitem, name="menu-item"),
    path("cart", cart.cart_menuitems, name="cart-menuitems"),
    path("orders", orders.orders, name="orders"),
    path("orders/<int:pk>", orders.order, name="order"),
    path("groups/<str:group_name>/users", groups.manage_groups, name="groups"),
    path("groups/<str:group_name>/users/<int:pk>", groups.manage_group, name="group-pk"),
    path("auth/", include('djoser.urls')),
    path("auth/", include('djoser.urls.jwt')),
]
