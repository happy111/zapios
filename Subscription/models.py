from django.db import models
from Configuration.models import CurrencyMaster
from django.core.validators import MaxValueValidator, MinValueValidator
 
 
class SubscriptionPlanType(models.Model):
    plan_name = models.CharField(
        max_length=30,
        verbose_name='Subscription Type')
    currency = models.ForeignKey(
        CurrencyMaster, 
        on_delete=models.CASCADE,
        related_name='subscription_plan_currency', 
        blank=True,
        null=True,
        verbose_name="Currency")
    membership_status = models.CharField(
        choices=(('Yearly', 'Yearly'),
        ('Monthly', 'Monthly')),
        max_length=20,
        verbose_name="Plan Type",
        null=True,blank=True)
    cost = models.FloatField(validators=[
            MinValueValidator(0.0)
        ],
        verbose_name='Amount',
        null=True,blank=True)
    user_limit = models.PositiveIntegerField(default=3)
    orders_limit = models.PositiveIntegerField(default=50)
    outlet_limit = models.PositiveIntegerField(default=1)
    product_limit = models.PositiveIntegerField(default=50)
    active_status = models.BooleanField(
        default=1,
        verbose_name="Is Active")
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
        verbose_name='Creation Date')
    updated_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Updation Date')
    isRecommended = models.BooleanField(default=0)
    is_customer_segmentation = models.BooleanField(default=False)
    is_video_product = models.BooleanField(default=False)
    is_custom_domain = models.BooleanField(default=False)
    is_zone_delivery = models.BooleanField(default=False)
    is_support_chat = models.BooleanField(default=False)
    is_eion_plan = models.BooleanField(default=False)
    class Meta:
        verbose_name ="   Subscription Plan"
        verbose_name_plural ="   Subscription Plan"

    def __str__(self):
        return str(self.plan_name)


class SubscriptionPaymentModel(models.Model):
    subscription = models.ForeignKey(
        SubscriptionPlanType, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True)
    payment_id = models.CharField(
        max_length=250, 
        blank=True, 
        null=True)
    key = models.CharField(
        max_length=250, 
        blank=True, 
        null=True)
    secret = models.CharField(
        max_length=250, 
        blank=True, 
        null=True)
    cost = models.FloatField(validators=[
            MinValueValidator(0.0)
        ],
        null=True, blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
        verbose_name='Creation Date')
    updated_at = models.DateTimeField(
        blank=True, 
        null=True, 
        verbose_name='Updation Date')

class Gatewaypayments(models.Model):
    
    company = models.ForeignKey(
            'Brands.Company', 
            on_delete=models.CASCADE,
            verbose_name='Company payments',)

    subscription = models.ForeignKey(
        SubscriptionPlanType, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True)

    receipt_id = models.CharField(
        max_length=255,
        verbose_name='Razorpay Receipt Id',
        unique=True,
        null=True,blank=True)
    razorpay_payment_id = models.CharField(
        max_length=255,
        verbose_name='Razorpay Payment Id',
        unique=True,
        null=True,blank=True)
    razorpay_order_id = models.CharField(
        max_length=255,
        verbose_name = 'Razorpay Order Id', 
        unique=True,null=True,
        blank=True)
    razorpay_signature = models.CharField(
        max_length=255,
        verbose_name = 'Razorpay Signature', 
        unique=True,null=True,
        blank=True)
    amount = models.FloatField(
        max_length=35,
        verbose_name='Amount',
        blank=True,null=True)
    is_successful = models.BooleanField(
        default=0,
        verbose_name="Is Successful")
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation Date')

    class Meta:
        verbose_name = ' Customer Razorpay Payment History'
        verbose_name_plural = 'Customer Razorpay Payment History'

    def __str__(self):
        return self.receipt_id



