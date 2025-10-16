from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Company, Portfolio, Order, Trade
from .serializer import CompanySerializer, PortfolioSerializer, OrderSerializer, TradeSerializer
from rest_framework.response import Response
from rest_framework import status
from .serializer import SignUpSerializer



class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"})
        return Response(serializer.errors)
    

class CompanyListView(ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]


class PortfolioListView(ListAPIView):
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)


class OrderListCreateView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "message": "Order created successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    
class ActiveOrdersView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Order.objects.filter(status='active')

        order_type = self.request.query_params.get('type')
        company_id = self.request.query_params.get('company')

        if order_type in ['buy', 'sell']:
            queryset = queryset.filter(type=order_type)

        if company_id:
            queryset = queryset.filter(company_id=company_id)

        if order_type == 'buy':
            queryset = queryset.order_by('-price')
        elif order_type == 'sell':
            queryset = queryset.order_by('price')

        return queryset


class TradeListView(ListAPIView):
    queryset = Trade.objects.all().order_by('-timestamp')
    serializer_class = TradeSerializer
    permission_classes = [AllowAny]


class MyTradesView(ListAPIView):
    serializer_class = TradeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Trade.objects.filter(buyer=user).union(Trade.objects.filter(seller=user)).order_by('-timestamp')

