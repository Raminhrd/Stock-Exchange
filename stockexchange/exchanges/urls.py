from django.urls import path
from .views import (
    CompanyListView,
    PortfolioListView,
    OrderListCreateView,
    ActiveOrdersView,
    TradeListView,
    MyTradesView,
)

urlpatterns = [
    path('companies/', CompanyListView.as_view()),
    path('portfolio/', PortfolioListView.as_view()),
    path('orders/', OrderListCreateView.as_view()),
    path('orders/active/', ActiveOrdersView.as_view()),
    path('trades/', TradeListView.as_view()),
    path('my-trades/', MyTradesView.as_view()),
]