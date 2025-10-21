from django.http import HttpResponse

from .models import Order, OrderLineItem
from products.models import Product

import stripe 
import json
import time

class StripeWH_Handler: 
    """ Handles Stripe webhooks """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """ Handle a generic/unknown/unexpected webhook event"""

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
    
    def handle_payment_intent_succeeded(self, event):
        """ Handle the payment_intent.succeeded webhook event from Stripe """

        intent = event.data.object
        pid = intent.id
        basket = intent.metadata.basket
        save_info = intent.metadata.save_info

        # get the Charge object
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )

        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)

        # Clean data in shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None 

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name_iexact=shipping_details.name,
                    email_iexact=billing_details.email,
                    phone_number_iexact=shipping_details.phone,
                    street_address1_iexact=shipping_details.address.street_address1,
                    street_address2_iexact=shipping_details.address.street_address2,
                    town_or_city_iexact=shipping_details.address.city,
                    postcode_iexact=shipping_details.address.postal_code,
                    country_iexact=shipping_details.address.country,
                    grand_total=grand_total,
                    original_basket=basket,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
            if order_exists:
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in databse',
                    status=200)
            else:
                order = None
                try:
                    order = Order.objects.create(
                        full_name=shipping_details.name,
                        email=billing_details.email,
                        phone_number=shipping_details.phone,
                        street_address1_iexact=shipping_details.address.street_address1,
                        street_address2_iexact=shipping_details.address.street_address2,
                        town_or_city_iexact=shipping_details.address.city,
                        postcode_iexact=shipping_details.address.postal_code,
                        country_iexact=shipping_details.address.country,
                        grand_total=grand_total,
                        original_basket=basket,
                        stripe_pid=pid,
                    )
                    for item_id, item_data in json.loads(basket).items():
                        product = Product.objects.get(id=item_id)
                        if isinstance(item_data, int):
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=item_data, 
                            )
                            order_line_item.save()
                except Exception as e:
                    if order:
                        order.delete()
                    return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200
        )
    
    def handle_payment_intent_payment_failed(self, event):
        """ Handle the payment_intent.failed webhook event from Stripe """

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )