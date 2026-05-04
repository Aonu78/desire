from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField  # Add this import at the top of the file
from ckeditor_uploader.fields import RichTextUploadingField


class Address(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150, verbose_name="Full Name", blank=True, null=True)
    phone_number = models.CharField(max_length=20, verbose_name="Phone Number", blank=True, null=True)
    building_no = models.CharField(max_length=150, verbose_name="Building / House No / Floor / Street", blank=True, null=True)
    locality = models.CharField(max_length=150, verbose_name="Colony / Suburb / Locality / Landmark")
    province = models.CharField(max_length=150, verbose_name="Province", blank=True, null=True)
    city = models.CharField(max_length=150, verbose_name="City")
    area = models.CharField(max_length=150, verbose_name="Area", blank=True, null=True)
    address = models.TextField(verbose_name="Address Description", blank=True, null=True)
    state = models.CharField(max_length=150, verbose_name="State", blank=True, null=True)
    country = models.CharField(max_length=150, verbose_name="Country", default="Pakistan")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        ordering = ('-updated_at',)

    def __str__(self):
        return f"{self.full_name} - {self.city}" if self.full_name else self.locality


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="Category Title")
    slug = models.SlugField(max_length=55, verbose_name="Category Slug")
    description = models.TextField(blank=True, verbose_name="Category Description")
    category_image = models.ImageField(upload_to='category', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160)
    sku = models.CharField(max_length=255, unique=True)
    short_description = models.TextField()
    detail_description = RichTextField(blank=True, null=True)
    detail_description = RichTextUploadingField(blank=True, null=True)
    product_image = models.ImageField(upload_to='product', blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True, verbose_name="Brand Name")
    sizes = models.TextField(blank=True, null=True, verbose_name="Available Sizes", help_text="Enter sizes separated by comma (e.g., S, M, L, XL or 36, 38, 40)")
    retail_price = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="Retail/Marked-up price shown to customers")
    seller_price = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="Actual selling price (base price for calculation)")
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Display price (use seller_price for calculations)")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0, help_text="Product rating from 0 to 5 stars")
    delivery_time = models.TextField(blank=True, null=True, verbose_name="Delivery Time Info", help_text="Estimated delivery time range (e.g., 2-3 working days)")
    refund_and_return_policy = models.TextField(blank=True, null=True, verbose_name="Refund & Return Policy", help_text="Information about return and refund policies")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    enable_facebook_share = models.BooleanField(default=True, verbose_name="Enable Facebook Share")
    enable_twitter_share = models.BooleanField(default=True, verbose_name="Enable Twitter/X Share")
    enable_pinterest_share = models.BooleanField(default=True, verbose_name="Enable Pinterest Share")
    enable_linkedin_share = models.BooleanField(default=True, verbose_name="Enable LinkedIn Share")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title
    
    def get_discount_percentage(self):
        """Calculate discount percentage between retail and seller price"""
        if self.retail_price and self.retail_price > 0:
            discount = ((self.retail_price - self.seller_price) / self.retail_price) * 100
            return round(discount, 1)
        return 0
    
    def get_profit_margin(self):
        """Calculate profit margin based on seller price"""
        if self.seller_price and self.seller_price > 0:
            margin = self.seller_price - self.price
            return round(margin, 2)
        return 0
    
    def get_average_rating(self):
        """Calculate average rating from approved reviews"""
        approved_reviews = self.reviews.filter(approved=True)
        if approved_reviews.count() > 0:
            total = sum(review.rating for review in approved_reviews)
            return round(total / approved_reviews.count(), 1)
        return self.rating

# Add this model after Product model and before ProductImage model

class ProductSpecification(models.Model):
    """Dynamic product specifications matching admin panel requirements"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specifications")
    spec_key = models.CharField(max_length=100, verbose_name="Specification Key")
    spec_value = models.CharField(max_length=500, verbose_name="Specification Value")
    display_order = models.IntegerField(default=0, verbose_name="Display Order")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Product Specification"
        verbose_name_plural = "Product Specifications"
        ordering = ('display_order', 'id')
        unique_together = ['product', 'spec_key']  # Prevent duplicate keys per product
    
    def __str__(self):
        return f"{self.product.title} - {self.spec_key}: {self.spec_value[:50]}"
# ✅ PRODUCT GALLERY MODEL
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_gallery/")

    def __str__(self):
        return f"{self.product.title} Image"


# ✅ REVIEW MODEL (ADMIN APPROVAL)
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    image = models.ImageField(upload_to="review_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        """Calculate total using seller_price (actual selling price)"""
        return self.quantity * self.product.seller_price
    
    @property
    def retail_total_price(self):
        """Calculate total using retail_price (marked-up price) for discount calculation"""
        return self.quantity * self.product.retail_price
    
    @property
    def savings(self):
        """Calculate total savings (retail - actual)"""
        return self.retail_total_price - self.total_price

    def __str__(self):
        return str(self.user)


STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="Price per unit at time of order")
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default="Pending")
    
    @property
    def order_total(self):
        """Calculate order total based on unit_price captured at order time"""
        return self.quantity * self.unit_price
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

# Your existing CompanyInfo model is fine, but let's ensure it has a method to get WhatsApp number
class CompanyInfo(models.Model):
    whatsapp_number = models.CharField(max_length=20, verbose_name="WhatsApp Number", help_text="Enter phone number with country code (e.g., +923451234567)")
    company_name = models.CharField(max_length=100, default="Desiretoys")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company Information"
        verbose_name_plural = "Company Information"

    def __str__(self):
        return self.company_name
    
    def get_whatsapp_number(self):
        """Return cleaned WhatsApp number"""
        # Remove any non-numeric characters except +
        import re
        cleaned = re.sub(r'[^\d+]', '', self.whatsapp_number)
        return cleaned