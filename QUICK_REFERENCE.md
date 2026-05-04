# Quick Reference: Seller Price & Retail Price Implementation

## 📋 COMPLETED ✅

### Models Updated
- ✅ [store/models.py](store/models.py#L46-L89) - Product: Added seller_price, retail_price, discount/profit methods
- ✅ [store/models.py](store/models.py#L101-L128) - Cart: Updated total_price to use seller_price, added retail_total_price & savings
- ✅ [store/models.py](store/models.py#L140-L159) - Order: Added unit_price field, added order_total property

### Migrations Created
- ✅ [0011_add_seller_and_retail_price.py](store/migrations/0011_add_seller_and_retail_price.py)
- ✅ [0012_order_unit_price.py](store/migrations/0012_order_unit_price.py)

### Documentation
- ✅ [PRICE_FIELDS_ANALYSIS.md](PRICE_FIELDS_ANALYSIS.md) - Detailed analysis
- ✅ [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) - Step-by-step guide

---

## 🚀 NEXT STEPS IN ORDER

### 1. Run Migration
```bash
python manage.py migrate
```

### 2. Populate Prices (Django Shell)
```bash
python manage.py shell
from store.models import Product
from decimal import Decimal

for p in Product.objects.filter(seller_price=0):
    p.seller_price = p.price
    p.retail_price = p.price * Decimal('1.20')
    p.save()
```

### 3. Update Python Files (2 files)
- **[store/views.py](store/views.py#L184)** - Line 184: Change `product.price` → `product.seller_price`
  - Also add `unit_price=product.seller_price` in Order.objects.create()
- **[store/admin.py](store/admin.py)** - Add ProductAdmin with new fields

### 4. Update Templates (6 files)
Replace all `product.price` with `product.seller_price` and fix `old_price` references:

| File | Lines | Change |
|------|-------|--------|
| [detail.html](templates/store/detail.html#L175) | 175, 213, 387-388 | Use retail_price & seller_price |
| [index.html](templates/store/index.html#L569) | 569-573 | Replace old_price with retail_price |
| [shop.html](templates/store/shop.html#L421) | 421-425 | Replace old_price with retail_price |
| [category_products.html](templates/store/category_products.html#L422) | 422-425 | Replace old_price with retail_price |
| [orders.html](templates/store/orders.html#L526) | 526, 569 | Use order.unit_price |
| [_product_list.html](templates/store/_product_list.html#L34) | 34 | Use seller_price |

---

## 🔧 QUICK UPDATE SNIPPETS

### Python (views.py)
```python
# Line 184 - Before
total_price = int(quantity) * float(product.price)

# Line 184 - After
total_price = int(quantity) * float(product.seller_price)

# When creating order:
order = Order.objects.create(
    user=user,
    address=addr,
    product=product,
    quantity=quantity,
    unit_price=product.seller_price  # ADD THIS
)
```

### Template (All price displays)
```html
<!-- Before -->
{% if product.old_price %}
    <span class="old-price">${{ product.old_price }}</span>
    <span class="current-price">${{ product.price }}</span>
{% else %}
    <span class="current-price">${{ product.price }}</span>
{% endif %}

<!-- After -->
{% if product.retail_price and product.retail_price > product.seller_price %}
    <span class="old-price">${{ product.retail_price }}</span>
    <span class="current-price">${{ product.seller_price }}</span>
    <span class="discount-badge">{{ product.get_discount_percentage }}% OFF</span>
{% else %}
    <span class="current-price">${{ product.seller_price }}</span>
{% endif %}
```

---

## 📊 Field Usage Cheatsheet

| Use Case | Field | Where |
|----------|-------|-------|
| Show main price to customer | seller_price | All pages |
| Show "original price" (crossed) | retail_price | Product detail, listing |
| Calculate cart total | seller_price | Cart model |
| Calculate discount % | retail_price vs seller_price | Product.get_discount_percentage() |
| Record order price | unit_price | After order creation |
| Show historical order price | unit_price | Orders page |

---

## ✅ Test Checklist

After implementation, verify:
- [ ] Home page shows prices correctly
- [ ] Shop/Category pages show prices with discounts
- [ ] Product detail page shows correct prices
- [ ] Cart calculates with seller_price
- [ ] WhatsApp button has correct price
- [ ] Orders show unit_price not product.price
- [ ] Admin interface displays new fields
- [ ] Existing products are populated with prices
- [ ] Creating new product works with all 3 prices

---

## 📞 Price System Overview

```
RETAIL_PRICE ────────────── (Customer sees this as "original")
       ↓
       └──→ DISCOUNT APPLIED (shown to customer for urgency)
       ↓
SELLER_PRICE ────────────── (What we actually charge)
       ↓
       └──→ PROFIT CALCULATION (seller_price - cost)
       ↓
       └──→ Used for: Cart totals, order calculations
       ↓
UNIT_PRICE (Order) ───────── (Price snapshot at order time)
       ↓
       └──→ Historical accuracy for audit trail
```

---

## 🎯 Key Points

1. **seller_price** = Primary calculation field (use this in most places)
2. **retail_price** = Display field (shows discount effect)
3. **unit_price** = Order history (never changes after purchase)
4. **price** = Legacy field (keep for compatibility or set = seller_price)
5. **get_discount_percentage()** = Calculate discount automatically
6. **get_profit_margin()** = Track your margin

---

## 📝 Files Status

```
✅ COMPLETED:
   └── Models, Migrations, Documentation

⏳ PENDING:
   ├── store/views.py (1 function)
   ├── store/admin.py (ProductAdmin)
   └── 6 Template files

📊 TOTAL IMPACT: 8 files need updates
```

---

**Last Updated**: March 15, 2026 | **Status**: Analysis & Setup Complete 🎉
