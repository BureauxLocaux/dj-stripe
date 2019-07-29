# Generated by Django 2.2.2 on 2019-07-03 09:58

from django.db import migrations, models
import django.db.models.deletion
import djstripe.enums
import djstripe.fields


def fix_djstripepaymentmethod_index_name_forwards(apps, schema_editor):
    # Altering the index is required because while we changed the name of old PaymentMethod model to
    # DjStripePaymentMethod, the migrations didn't update the names of index.
    # In the current migration, we create a new PaymentMethod model, hence before creating it, its
    # better to rename the old index.
    if schema_editor.connection.vendor == 'postgresql':
        migrations.RunSQL(
            'ALTER INDEX djstripe_paymentmethod_id_0b9251df_like rename TO djstripe_paymentmethod_legacy_id_0b9251df_like',
        )


def fix_djstripepaymentmethod_index_name_backwards(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        migrations.RunSQL(
            'ALTER INDEX djstripe_paymentmethod_legacy_id_0b9251df_like rename TO djstripe_paymentmethod_id_0b9251df_like',
        )


class Migration(migrations.Migration):

    dependencies = [
        ('djstripe', '0004_auto_20190612_0850'),
    ]

    operations = [
        migrations.RunPython(fix_djstripepaymentmethod_index_name_forwards, fix_djstripepaymentmethod_index_name_backwards),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('djstripe_id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('id', djstripe.fields.StripeIdField(max_length=255, unique=True)),
                ('livemode', models.NullBooleanField(default=None, help_text='Null here indicates that the livemode status is unknown or was previously unrecorded. Otherwise, this field indicates whether this record comes from Stripe test mode or live mode operation.')),
                ('created', djstripe.fields.StripeDateTimeField(blank=True, help_text='The datetime this object was created in stripe.', null=True)),
                ('metadata', djstripe.fields.JSONField(blank=True, help_text='A set of key/value pairs that you can attach to an object. It can be useful for storing additional information about an object in a structured format.', null=True)),
                ('description', models.TextField(blank=True, help_text='A description of this object.', null=True)),
                ('djstripe_created', models.DateTimeField(auto_now_add=True)),
                ('djstripe_updated', models.DateTimeField(auto_now=True)),
                ('billing_details', djstripe.fields.JSONField(help_text='Billing information associated with the PaymentMethod that may be used or required by particular types of payment methods.')),
                ('card', djstripe.fields.JSONField(help_text='If this is a card PaymentMethod, this hash contains details about the card.')),
                ('card_present', djstripe.fields.JSONField(help_text='If this is an card_present PaymentMethod, this hash contains details about the Card Present payment method.')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_methods', to='djstripe.Customer')),
            ],
            options={
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaymentIntent',
            fields=[
                ('djstripe_id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('id', djstripe.fields.StripeIdField(max_length=255, unique=True)),
                ('livemode', models.NullBooleanField(default=None, help_text='Null here indicates that the livemode status is unknown or was previously unrecorded. Otherwise, this field indicates whether this record comes from Stripe test mode or live mode operation.')),
                ('created', djstripe.fields.StripeDateTimeField(blank=True, help_text='The datetime this object was created in stripe.', null=True)),
                ('metadata', djstripe.fields.JSONField(blank=True, help_text='A set of key/value pairs that you can attach to an object. It can be useful for storing additional information about an object in a structured format.', null=True)),
                ('djstripe_created', models.DateTimeField(auto_now_add=True)),
                ('djstripe_updated', models.DateTimeField(auto_now=True)),
                ('amount', djstripe.fields.StripeQuantumCurrencyAmountField(help_text='Amount intended to be collected by this PaymentIntent.')),
                ('amount_capturable', djstripe.fields.StripeQuantumCurrencyAmountField(help_text='Amount that can be captured from this PaymentIntent.')),
                ('amount_received', djstripe.fields.StripeQuantumCurrencyAmountField(help_text='Amount that was collected by this PaymentIntent.')),
                ('canceled_at', models.DateTimeField(default=None, help_text='Populated when status is canceled, this is the time at which the PaymentIntent was canceled. Measured in seconds since the Unix epoch.', null=True)),
                ('cancellation_reason', models.CharField(help_text='User-given reason for cancellation of this PaymentIntent, one of duplicate, fraudulent, requested_by_customer, or failed_invoice.', max_length=255, null=True)),
                ('capture_method', models.CharField(help_text='Capture method of this PaymentIntent, one of automatic or manual.', max_length=255)),
                ('client_secret', models.CharField(help_text='The client secret of this PaymentIntent. Used for client-side retrieval using a publishable key. Please refer to our automatic confirmation quickstart guide to learn about how client_secret should be handled.', max_length=255)),
                ('confirmation_method', models.CharField(help_text='Confirmation method of this PaymentIntent, one of manual or automatic.', max_length=255)),
                ('currency', djstripe.fields.StripeCurrencyCodeField(help_text='Three-letter ISO currency code', max_length=3)),
                ('description', models.TextField(default='', help_text='An arbitrary string attached to the object. Often useful for displaying to users.')),
                ('last_payment_error', djstripe.fields.JSONField(help_text='The payment error encountered in the previous PaymentIntent confirmation.')),
                ('next_action', djstripe.fields.JSONField(help_text='If present, this property tells you what actions you need to take in order for your customer to fulfill a payment using the provided source.')),
                ('on_behalf_of', models.CharField(help_text='The account (if any) for which the funds of the PaymentIntent are intended. See the PaymentIntents Connect usage guide for details.', max_length=255)),
                ('payment_method_types', djstripe.fields.JSONField(help_text='The list of payment method types (e.g. card) that this PaymentIntent is allowed to use.')),
                ('receipt_email', models.CharField(help_text='Email address that the receipt for the resulting payment will be sent to.', max_length=255)),
                ('statement_descriptor', models.CharField(help_text='Extra information about a PaymentIntent. This will appear on your customer’s statement when this PaymentIntent succeeds in creating a charge.', max_length=255)),
                ('status', models.CharField(help_text='Status of this PaymentIntent, one of requires_payment_method, requires_confirmation, requires_action, processing, requires_capture, canceled, or succeeded. You can read more about PaymentIntent statuses here.', max_length=255)),
                ('transfer_data', djstripe.fields.JSONField(help_text='The data with which to automatically create a Transfer when the payment is finalized. See the PaymentIntents Connect usage guide for details.')),
                ('transfer_group', models.CharField(help_text='A string that identifies the resulting payment as part of a group. See the PaymentIntents Connect usage guide for details.', max_length=255)),
                ('customer', models.ForeignKey(help_text='ID of the Customer this PaymentIntent is for if one exists.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='djstripe.Customer')),
                ('invoice', models.ForeignKey(help_text='ID of the invoice that created this PaymentIntent, if it exists.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='djstripe.Invoice')),
                ('payment_method', models.ForeignKey(help_text='ID of the payment method used in this PaymentIntent.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='djstripe.PaymentMethod')),
            ],
            options={
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
    ]
