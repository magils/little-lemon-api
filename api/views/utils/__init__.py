from django.core.paginator import Paginator, EmptyPage
from api.exceptions import PaginationException, UnauthorizedUserGroupException
from enum import Enum


def order_query_result(request, queryset):
    ordering = request.query_params.get("ordering")
    
    if ordering:
        order_cols = ordering.split(",")
        return queryset.order_by(*order_cols)
    else:
        return queryset

def paginate_items(request, items):
    page = request.query_params.get("page", default="1")
    per_page = request.query_params.get("per_page", default="20")
    
    if not page.isnumeric() or int(page) < 1:
        raise PaginationException("Page param value cannot be less than 1 or contains characters.")
    
    if not per_page.isnumeric() or (50 > int(per_page) < 1):
        raise PaginationException(detail="Per Page param value should be between 1 and 50, and cannot contain characters.")
    
    paginator = Paginator(items, per_page=per_page)
    
    try:
        items = paginator.page(number=page)
    except EmptyPage:
        items = []
    
    return items

# TODO: Remove
def check_user_belongs_to_groups(request, group_names, allow_methods, allow_customers=False):
    if allow_customers and not request.user.groups.exists():
        return
    if group_names and request.user.groups.filter(name__in=group_names).exists():
        return
    raise UnauthorizedUserGroupException(detail="User group is not authorized for accessing this endpoint")

def allow_access(rules):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not args:
                raise ValueError("Not args found. An 'request' argument is required.")
            request = args[0]
            user_group_names = [g["name"] for g in request.user.groups.values()]
            
            if not user_group_names:
                user_group_names.append("customer")

            for group_name in user_group_names:
                methods_allowed = rules.get(group_name, [])

                if request.method in methods_allowed:
                    return func(*args, **kwargs)
            raise UnauthorizedUserGroupException(detail="User group is not authorized for accessing this endpoint")            
        return wrapper
    return decorator
