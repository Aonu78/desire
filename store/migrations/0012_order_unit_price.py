# Generated migration for adding unit_price field to Order model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_add_seller_and_retail_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Price per unit at time of order', max_digits=8),
        ),
    ]
