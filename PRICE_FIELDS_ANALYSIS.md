# Price Fields Analysis and Implementation Guide

## Summary
Added two new price fields to the Product model:
- **seller_price**: Actual selling/base price for calculations (recommended for use in cart, order total)
- **retail_price**: Marked-up price shown to customers (creates discount illusions)
- **price**: Existing field maintained for display purposes

---

## 1. PRODUCT MODEL CHANGES ✅ COMPLETED

### Location: `d:\Desiretoys\store\models.py` (Lines 46-89)

**New Fields Added:**
```python
retail_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
seller_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
price = models.DecimalField(max_digits=8, decimal_places=2)  # Updated with help_text
```

**New Utility Methods Added:**
- `get_discount_percentage()` - Calculates discount between retail_price and seller_price
- `get_profit_margin()` - Calculates profit margin (seller_price - price)
- `get_average_rating()` - Existing method maintained

---

## 2. FILES THAT USE PRODUCT PRICING

### A. PYTHON FILES

#### 1. `d:\Desiretoys\store\models.py`
- **Cart Model** (Line 107-108): Uses `product.price` in `total_price` property
  - **Action Needed**: Should use `seller_price` instead for accurate calculations
  
- **Order Model** (Lines 114-121): References product via ForeignKey
  - **Action Needed**: May need to store price at time of order

**Recommendation for Cart & Order:**
```python
# In Cart model
@property
def total_price(self):
    return self.quantity * self.product.seller_price  # Use seller_price

# Consider adding price snapshot to Order
class Order(models.Model):
    # ... existing fields ...
    price_at_order = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    # Store the actual price at time of order in case prices change
```

#### 2. `d:\Desiretoys\store\views.py`
**Uses in buy_now function (Line 184):**
- Line 184: `total_price = int(quantity) * float(product.price)`
- Line 200: `print(f"   Price: ${product.price}")`
- Line 202: `print(f"   Total Amount: ${total_price}")`

**Action**: Should be updated to use `seller_price`:
```python
# Current (Line 184)
total_price = int(quantity) * float(product.price)

# Recommended
total_price = int(quantity) * float(product.seller_price)
```

---

### B. TEMPLATE FILES (Front-end)

#### 1. `d:\Desiretoys\templates\store\detail.html`
- **Line 175**: Displays `{{ product.price }}`
- **Line 213**: WhatsApp button passes `{{ product.price }}`
- **Line 387-388**: Uses `{{ rp.old_price }}` and `{{ rp.price }}`

**Current Issue**: Template references `old_price` which doesn't exist in model
**Recommendation**:
```html
<!-- Update WhatsApp price passing -->
onclick="openWhatsApp('{{ product.title|escapejs }}', '{{ product.seller_price }}', ...)"

<!-- For discount display -->
{% if product.retail_price and product.retail_price > product.seller_price %}
    <span class="old-price">${{ product.retail_price }}</span>
    <span class="current-price">${{ product.seller_price }}</span>
{% else %}
    <span class="current-price">${{ product.seller_price }}</span>
{% endif %}
```

#### 2. `d:\Desiretoys\templates\store\index.html`
- **Line 569-573**: Uses `product.old_price` and `product.price`
- **Line 536-539**: Shopping cart and price display

**Action**: Replace `old_price` with `retail_price`
```html
<!-- Old code (won't work) -->
{% if product.old_price %}
    <span class="old-price">${{ product.old_price }}</span>

<!-- New code -->
{% if product.retail_price %}
    <span class="old-price">${{ product.retail_price }}</span>
    <span class="current-price">${{ product.seller_price }}</span>
```

#### 3. `d:\Desiretoys\templates\store\shop.html`
- **Line 421-425**: References `product.old_price` and `product.price`
- **Line 393**: Product listing with prices

**Action**: Same as index.html - replace `old_price` with `retail_price`

#### 4. `d:\Desiretoys\templates\store\category_products.html`
- **Line 422-425**: Uses `product.old_price` and `product.price`
- **Line 393**: Product info section

**Action**: Same update pattern for discount display

#### 5. `d:\Desiretoys\templates\store\orders.html`
- **Line 526**: `{{ order.product.price|floatformat:2 }}`
- **Line 569**: `{{ order.product.price|floatformat:2 }}`

**Action**: Update to use `seller_price` since that's the actual charged price:
```html
{{ order.product.seller_price|floatformat:2 }}
```

#### 6. `d:\Desiretoys\templates\store\_product_list.html`
- **Line 34**: `<p class="small text-muted">${{ product.price }}</p>`

**Action**: Update to display `seller_price`:
```html
<p class="small text-muted">${{ product.seller_price }}</p>
```

---

## 3. RECOMMENDED PRICING STRATEGY

### Three-Tier Price System:
1. **retail_price** - Original/suggested retail price (shown struck-through for discount effect)
2. **seller_price** - Actual selling price (primary display price, used for calculations)
3. **price** - Can be used for special display or kept for backward compatibility

### Usage Guidelines:

| Field | Use Case | Example |
|-------|----------|---------|
| `retail_price` | Show as "old price" for discount effect | "$199" (struck-through) |
| `seller_price` | All calculations (cart, order, total) | "$149" (current price) |
| `price` | Backward compatibility OR special pricing | Can match seller_price |
| `get_discount_percentage()` | Display discount badge | "25% OFF" |

---

## 4. MIGRATION STATUS ✅ COMPLETED

**File**: `d:\Desiretoys\store\migrations\0011_add_seller_and_retail_price.py`

**Changes Applied**:
- Adds `retail_price` field with default=0
- Adds `seller_price` field with default=0
- Updates `price` field help_text

---

## 5. CHECKLIST FOR FULL IMPLEMENTATION

### Phase 1: Model & Database ✅
- [x] Add seller_price field to Product model
- [x] Add retail_price field to Product model
- [x] Update price field help text
- [x] Add utility methods (get_discount_percentage, get_profit_margin)
- [x] Create migration file

### Phase 2: Update Calculations ⚠️ PENDING
- [ ] Update Cart.total_price to use seller_price
- [ ] Update views.py buy_now() to use seller_price
- [ ] Consider adding price_at_order to Order model
- [ ] Update Order creation logic to capture price snapshot

### Phase 3: Update Frontend Templates ⚠️ PENDING
- [ ] Update detail.html (discount display, WhatsApp button)
- [ ] Update index.html (replace old_price with retail_price)
- [ ] Update shop.html (replace old_price with retail_price)
- [ ] Update category_products.html (replace old_price with retail_price)
- [ ] Update orders.html (use seller_price)
- [ ] Update _product_list.html (use seller_price)

### Phase 4: Django Admin Updates ⚠️ PENDING
- [ ] Update admin.py ProductAdmin to display new fields
- [ ] Add inline help text for admin users
- [ ] Consider adding discount percentage display in admin

### Phase 5: Testing ⚠️ PENDING
- [ ] Test cart calculations with seller_price
- [ ] Test order creation with correct pricing
- [ ] Test discount display in templates
- [ ] Test WhatsApp message with correct price
- [ ] Test admin interface

---

## 6. IMPORTANT NOTES

### Backward Compatibility:
- **Old Price Field**: The `price` field is kept as-is. Consider:
  - Setting it to equal `seller_price` during migration
  - OR keep it for backward compatibility

### Data Migration Needed:
When you apply migrations, existing products will have:
- `retail_price = 0`
- `seller_price = 0`
- `price = (existing value)`

**Action**: You'll need to populate these fields for existing products (either via Django shell or custom management command)

### Admin Interface:
Update `d:\Desiretoys\store\admin.py` to make these fields editable:
```python
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'sku', 'category')
        }),
        ('Pricing', {
            'fields': ('retail_price', 'seller_price', 'price'),
            'description': 'retail_price: Marked-up price | seller_price: Actual selling price | price: Display price'
        }),
        # ... other fields
    )
```

---

## 7. FILES REQUIRING UPDATES (Summary Table)

| File | Line(s) | Current Code | Action |
|------|---------|--------------|--------|
| models.py | 107-108 | `product.price` | Use `product.seller_price` |
| views.py | 184, 200, 202 | `product.price` | Use `product.seller_price` |
| detail.html | 175, 213, 387-388 | `product.price`, `old_price` | Use `retail_price` & `seller_price` |
| index.html | 569-573 | `old_price` | Replace with `retail_price` |
| shop.html | 421-425 | `old_price` | Replace with `retail_price` |
| category_products.html | 422-425 | `old_price` | Replace with `retail_price` |
| orders.html | 526, 569 | `product.price` | Use `product.seller_price` |
| _product_list.html | 34 | `product.price` | Use `product.seller_price` |

---

## 8. HELPFUL TEMPLATE SNIPPETS

### Display Product Price with Discount:
```html
<div class="product-price">
    {% if product.retail_price and product.retail_price > product.seller_price %}
        <span class="old-price">${{ product.retail_price }}</span>
        <span class="current-price">${{ product.seller_price }}</span>
        <span class="discount-badge">{{ product.get_discount_percentage }}% OFF</span>
    {% else %}
        <span class="current-price">${{ product.seller_price }}</span>
    {% endif %}
</div>
```

### Update WhatsApp Message:
```html
onclick="openWhatsApp('{{ product.title|escapejs }}', '{{ product.seller_price }}', '{{ company_info.whatsapp_number|default:"" }}')"
```

---

## 9. EXECUTION ORDER FOR UPDATES

1. **Run migrations**: `python manage.py migrate`
2. **Update admin.py** with new fields
3. **Populate existing products** with price data
4. **Update models.py** (Cart.total_price)
5. **Update views.py** (buy_now function)
6. **Update all templates** in order: detail.html → index.html → shop.html → category_products.html → orders.html → _product_list.html
7. **Test thoroughly** across all pages
8. **Update Order model** (optional but recommended)

---

Generated: March 15, 2026
Analysis Complete ✅
