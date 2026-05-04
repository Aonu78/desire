# Seller Price & Retail Price Implementation Guide

## ✅ COMPLETED TASKS

### 1. Product Model Updates
**File**: `d:\Desiretoys\store\models.py`

✅ Added `seller_price` field - Actual selling price for calculations
✅ Added `retail_price` field - Marked-up price for discount display
✅ Added `get_discount_percentage()` method - Calculate discount %
✅ Added `get_profit_margin()` method - Calculate profit margin

```python
# New fields in Product model:
retail_price = DecimalField(max_digits=8, decimal_places=2, default=0)
seller_price = DecimalField(max_digits=8, decimal_places=2, default=0)
111224488
# New methods:
def get_discount_percentage(self)
def get_profit_margin(self)
```

### 2. Cart Model Enhancements  
**File**: `d:\Desiretoys\store\models.py`

✅ Updated `total_price` property to use `seller_price`
✅ Added `retail_total_price` property for discount calculations
✅ Added `savings` property to show customer savings

```python
# Updated Cart methods:
@property
def total_price(self):
    return self.quantity * self.product.seller_price

@property
def retail_total_price(self):
    return self.quantity * self.product.retail_price

@property
def savings(self):
    return self.retail_total_price - self.total_price
```

### 3. Order Model Enhancement
**File**: `d:\Desiretoys\store\models.py`

✅ Added `unit_price` field to capture price at order time
✅ Added `order_total` property for total calculations
✅ Added `__str__` method for better admin display

```python
# New Order fields:
unit_price = DecimalField(max_digits=8, decimal_places=2, default=0)

# New Order methods:
@property
def order_total(self):
    return self.quantity * self.unit_price
```

### 4. Migrations Created
✅ Migration 0011: Add seller_price and retail_price to Product
✅ Migration 0012: Add unit_price to Order

---

## 📋 AFFECTED FILES - COMPLETE LIST

### A. PYTHON FILES REQUIRING UPDATES

#### 1. **store/views.py** - NEEDS UPDATE
**buy_now function (around Line 184)**

Current code:
```python
total_price = int(quantity) * float(product.price)
```

Should be updated to:
```python
total_price = int(quantity) * float(product.seller_price)
```

Also update Order creation to capture price:
```python
order = Order.objects.create(
    user=user,
    address=addr,
    product=product,
    quantity=quantity,
    unit_price=product.seller_price  # ADD THIS LINE
)
```

#### 2. **store/admin.py** - NEEDS UPDATE
Add new fields to ProductAdmin:

```python
from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller_price', 'retail_price', 'get_discount_percentage', 'is_active')
    list_filter = ('is_active', 'is_featured', 'category')
    search_fields = ('title', 'sku')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'sku', 'category')
        }),
        ('Descriptions', {
            'fields': ('short_description', 'detail_description')
        }),
        ('Pricing & Profit', {
            'fields': ('retail_price', 'seller_price', 'price'),
            'description': 'retail_price: Customer-facing marked-up price | seller_price: Actual selling price | price: Legacy field'
        }),
        ('Images & Media', {
            'fields': ('product_image',)
        }),
        ('Status & Featured', {
            'fields': ('is_active', 'is_featured', 'rating')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Product, ProductAdmin)
```

---

### B. TEMPLATE FILES REQUIRING UPDATES

#### 1. **templates/store/detail.html** - NEEDS UPDATE
**Line 175 - Main Price Display:**
```html
<!-- CURRENT -->
<p class="text-muted lead">RS:{{ product.price }}</p>

<!-- UPDATE TO -->
{% if product.retail_price and product.retail_price > product.seller_price %}
    <p class="text-muted">
        <span style="text-decoration: line-through; color: #999;">RS:{{ product.retail_price }}</span>
        <span style="color: #fd7e14; font-size: 1.3em; font-weight: bold;">RS:{{ product.seller_price }}</span>
        <span style="color: green; font-size: 0.9em;">({{ product.get_discount_percentage }}% OFF)</span>
    </p>
{% else %}
    <p class="text-muted lead">RS:{{ product.seller_price }}</p>
{% endif %}
```

**Line 213 - WhatsApp Button:**
```html
<!-- CURRENT -->
onclick="openWhatsApp('{{ product.title|escapejs }}', '{{ product.price }}', ...)"

<!-- UPDATE TO -->
onclick="openWhatsApp('{{ product.title|escapejs }}', '{{ product.seller_price }}', ...)"
```

**Line 387-388 - Related Products:**
```html
<!-- CURRENT -->
{% if rp.old_price %}

<!-- UPDATE TO -->
{% if rp.retail_price and rp.retail_price > rp.seller_price %}
    <span class="old-price">${{ rp.retail_price }}</span>
    <span class="current-price">${{ rp.seller_price }}</span>
{% else %}
    <span class="current-price">${{ rp.seller_price }}</span>
{% endif %}
```

#### 2. **templates/store/index.html** - NEEDS UPDATE
**Line 569-573 - Featured Products:**
```html
<!-- CURRENT -->
{% if product.old_price %}
    <span class="old-price">${{ product.old_price }}</span>
    <span class="current-price">${{ product.price }}</span>
{% else %}
    <span class="current-price">${{ product.price }}</span>
{% endif %}

<!-- UPDATE TO -->
{% if product.retail_price and product.retail_price > product.seller_price %}
    <span class="old-price">${{ product.retail_price }}</span>
    <span class="current-price">${{ product.seller_price }}</span>
    <span class="discount-badge">{{ product.get_discount_percentage }}% OFF</span>
{% else %}
    <span class="current-price">${{ product.seller_price }}</span>
{% endif %}
```

#### 3. **templates/store/shop.html** - NEEDS UPDATE
**Line 421-425 - Product Pricing:**
Same update as index.html above

#### 4. **templates/store/category_products.html** - NEEDS UPDATE
**Line 422-425 - Product Pricing:**
Same update as index.html above

#### 5. **templates/store/orders.html** - NEEDS UPDATE
**Line 526 & 569:**
```html
<!-- CURRENT -->
<div class="product-price">${{ order.product.price|floatformat:2 }}</div>

<!-- UPDATE TO -->
<div class="product-price">${{ order.unit_price|floatformat:2 }}</div>
```

Or if you want to show summary:
```html
<div class="product-price">
    Unit Price: ${{ order.unit_price|floatformat:2 }}
    <br>
    Total: ${{ order.order_total|floatformat:2 }}
</div>
```

#### 6. **templates/store/_product_list.html** - NEEDS UPDATE
**Line 34:**
```html
<!-- CURRENT -->
<p class="small text-muted">${{ product.price }}</p>

<!-- UPDATE TO -->
<p class="small text-muted">${{ product.seller_price }}</p>
```

---

## 🚀 NEXT STEPS - EXECUTION GUIDE

### Step 1: Run Migrations
```bash
python manage.py migrate
```

### Step 2: Populate Existing Product Data
Since new products will have `seller_price=0` by default, you need to populate them:

**Option A: Using Django Shell**
```bash
python manage.py shell

from store.models import Product

# For each product, set seller_price = current price
for product in Product.objects.all():
    if product.seller_price == 0:
        product.seller_price = product.price
        product.retail_price = product.price * 1.20  # Example: 20% retail markup
        product.save()
```

**Option B: Create Management Command**
Create file: `store/management/commands/populate_prices.py`
```python
from django.core.management.base import BaseCommand
from store.models import Product
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate seller_price and retail_price for existing products'

    def handle(self, *args, **options):
        updated = 0
        for product in Product.objects.filter(seller_price=0):
            product.seller_price = product.price
            product.retail_price = product.price * Decimal('1.20')  # 20% markup
            product.save()
            updated += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated} products')
        )
```

Then run:
```bash
python manage.py populate_prices
```

### Step 3: Update admin.py
Edit `d:\Desiretoys\store\admin.py` to add ProductAdmin configuration

### Step 4: Update views.py
Update the `buy_now` function to use `seller_price` and capture it in Order

### Step 5: Update Templates
Update all 6 template files (detail.html, index.html, shop.html, category_products.html, orders.html, _product_list.html)

### Step 6: Test Everything
- Test product detail page (check price display & discount)
- Test cart calculations
- Test order creation
- Test admin interface
- Test WhatsApp button with correct price
- Check home page and shop page pricing

---

## 📊 PRICE FIELD REFERENCE GUIDE

| Field | Location | Shows To | Used For | Type |
|-------|----------|----------|----------|------|
| **price** | Product | - | Legacy/Backward compat | DecimalField |
| **seller_price** | Product | Buyer (actual price) | Calculations, Order total | DecimalField |
| **retail_price** | Product | Display (struck-through) | Discount effect | DecimalField |
| **unit_price** | Order | Admin, History | Order tracking | DecimalField |

### Example Scenario:
- **retail_price** = $200 (what we tell customer is "original price")
- **seller_price** = $149 (what we actually charge)
- **price** = $149 (match seller_price or use for special pricing)
- **Discount shown** = 25.5% OFF
- **Cart total** = quantity × seller_price
- **Order captured** = unit_price (seller_price at time of order)

---

## ⚠️ IMPORTANT NOTES

### Data Loss Prevention:
- The old `price` field is still there - no data is lost
- New fields have `default=0`, so existing products will show as unpriced
- **You MUST populate prices** before making site live

### Price History:
- Orders store `unit_price` - historical accuracy maintained
- If product price changes, old orders show what was actually charged
- Cart uses current `seller_price` - dynamic pricing

### Admin Experience:
- Make pricing fields clearly labeled in admin
- Show discount percentage calculated from retail vs seller
- Consider adding a "Duplicate Price from Another Product" feature

### Test Cases:
1. ✅ Product with retail_price > seller_price (discount shown)
2. ✅ Product with no retail_price (no discount shown)
3. ✅ Cart total uses seller_price
4. ✅ Order total uses unit_price captured at order time
5. ✅ WhatsApp button shows seller_price
6. ✅ Price change doesn't affect old orders

---

## 📁 FILES CREATED/MODIFIED SUMMARY

### Created Files:
✅ `PRICE_FIELDS_ANALYSIS.md` - Detailed analysis of all affected files
✅ `store/migrations/0011_add_seller_and_retail_price.py` - Add price fields
✅ `store/migrations/0012_order_unit_price.py` - Add order unit_price

### Modified Files:
✅ `store/models.py` - Updated Product, Cart, Order models

### Files Still Needing Updates:
⏳ `store/views.py` - Update buy_now() function
⏳ `store/admin.py` - Configure ProductAdmin display
⏳ `templates/store/detail.html` - Update price display
⏳ `templates/store/index.html` - Update price display
⏳ `templates/store/shop.html` - Update price display
⏳ `templates/store/category_products.html` - Update price display
⏳ `templates/store/orders.html` - Update price display
⏳ `templates/store/_product_list.html` - Update price display

---

## 🎯 RECOMMENDED UPDATE ORDER
1. Run migrations
2. Populate existing product prices
3. Update admin.py first (for testing)
4. Update views.py (critical for order creation)
5. Update templates (in order: detail → index → shop → category → orders → list)
6. Comprehensive testing
7. Deploy to production

---

Generated: March 15, 2026
Status: ✅ Analysis Phase Complete
Next: 🚀 Implementation Phase
