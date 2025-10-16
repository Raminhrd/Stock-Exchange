from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Order, Trade, Portfolio, Company


@receiver(post_save, sender=Order)
def match_orders(sender, instance, created, **kwargs):
    if not created:
        return

    order = instance
    company = order.company

    if order.type == 'buy':
        opposite_orders = Order.objects.filter(
            company=company, type='sell', status='active'
        ).order_by('price', 'created_at')
    else:
        opposite_orders = Order.objects.filter(
            company=company, type='buy', status='active'
        ).order_by('-price', 'created_at')

    for opposite in opposite_orders:
        if order.remaining_quantity == 0:
            break 

        if order.type == 'buy' and order.price >= opposite.price:
            deal_price = order.price 
        elif order.type == 'sell' and opposite.price >= order.price:
            deal_price = opposite.price
        else:
            continue

        traded_quantity = min(order.remaining_quantity, opposite.remaining_quantity)

        if order.type == 'buy':
            buyer = order.user
            seller = opposite.user
        else:
            buyer = opposite.user
            seller = order.user

        with transaction.atomic():
            Trade.objects.create(
                buyer=buyer,
                seller=seller,
                company=company,
                price=deal_price,
                quantity=traded_quantity
            )

            order.remaining_quantity -= traded_quantity
            opposite.remaining_quantity -= traded_quantity

            order.status = 'done' if order.remaining_quantity == 0 else 'partial'
            opposite.status = 'done' if opposite.remaining_quantity == 0 else 'partial'

            order.save(update_fields=['remaining_quantity', 'status'])
            opposite.save(update_fields=['remaining_quantity', 'status'])

            company.current_price = deal_price
            company.save(update_fields=['current_price'])

            update_portfolios(buyer, seller, company, traded_quantity, deal_price)


def update_portfolios(buyer, seller, company, quantity, price):

    seller_portfolio, _ = Portfolio.objects.get_or_create(user=seller, company=company)
    if seller_portfolio.quantity >= quantity:
        seller_portfolio.quantity -= quantity
        seller_portfolio.save(update_fields=['quantity'])

    buyer_portfolio, _ = Portfolio.objects.get_or_create(user=buyer, company=company)
    total_cost = (buyer_portfolio.avg_price * buyer_portfolio.quantity) + (price * quantity)
    buyer_portfolio.quantity += quantity
    buyer_portfolio.avg_price = total_cost / buyer_portfolio.quantity
    buyer_portfolio.save(update_fields=['quantity', 'avg_price'])