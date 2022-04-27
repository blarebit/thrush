"""Product URLs."""
from django.urls import include, path
from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from .views import CartViewSet, UserCartViewSet
from account.views import UserViewSet

router = routers.DefaultRouter()
router.register("cart", CartViewSet, basename="cart")
# router.register("carts/<user_pk>", UserCartViewSet, basename="user_cart")
# router.register("users", UserViewSet, basename="users")

# cart_router = nested_routers.NestedDefaultRouter(router, "cart", lookup="cart")
# cart_router.register("users", UserViewSet, basename="users_cart_products")

# cart_router = nested_routers.NestedDefaultRouter(router, "users", lookup="users")
# cart_router.register("carts", UserCartViewSet, basename="users_cart_products")

urlpatterns = [
    path("", include(router.urls)),
    # path("", include(cart_router.urls)),
    path('carts/<user_pk>/', UserCartViewSet.as_view({'get': 'list'}), name='user_cart-detail'),
]
