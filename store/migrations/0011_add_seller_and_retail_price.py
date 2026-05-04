# Generated migration for adding seller_price and retail_price fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_product_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='retail_price',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Retail/Marked-up price shown to customers', max_digits=8),
        ),
        migrations.AddField(
            model_name='product',
            name='seller_price',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Actual selling price (base price for calculation)', max_digits=8),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Display price (use seller_price for calculations)', max_digits=8),
        ),
    ]
