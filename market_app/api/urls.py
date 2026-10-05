from django.urls import path, include
from .views import market_single_view, sellers_view, product_view, product_single_view, seller_single_view, MarketsClassbasedView,  SellerOfMarketList, ProductViewSet
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('market/', MarketsClassbasedView.as_view()),
    path('market/<int:pk>/', market_single_view),
    path('market/<int:pk>/seller/', SellerOfMarketList.as_view()),
    path('seller/', sellers_view),
    path('seller/<int:pk>/', seller_single_view, name='seller_single'),
    path('product/', product_view),
    path('product/<int:pk>/', product_single_view),
]