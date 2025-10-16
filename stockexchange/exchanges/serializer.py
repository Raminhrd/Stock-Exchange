from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from exchanges.models import *
from decimal import Decimal


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class PortfiloSerializer(ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'company', 'type', 'quantity', 'price', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']

    def validate_price(self, value):
        company_id = self.initial_data.get('company')
        if not company_id:
            raise serializers.ValidationError("Company is required.")

        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            raise serializers.ValidationError("Invalid company selected.")

        current_price = company.current_price
        min_price = current_price * Decimal('0.95')
        max_price = current_price * Decimal('1.05')

        if not (min_price <= value <= max_price):
            raise serializers.ValidationError(
                f"Price must be between {float(min_price):.2f} and {float(max_price):.2f} "
                f"(±5% of current price {current_price})."
            )

        return value
    
class TradeSerializer(ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'