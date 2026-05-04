from django.contrib import admin
from .models import Address, Category, Product, Cart, Order, ProductImage, Review, CompanyInfo, ProductSpecification


class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'locality', 'city', 'state', 'country')
    list_filter = ('city', 'state', 'country')
    search_fields = ('locality', 'city', 'state', 'country')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active', 'is_featured', 'updated_at')
    list_editable = ('slug', 'is_active', 'is_featured')
    prepopulated_fields = {"slug": ("title",)}


class ProductSpecificationInline(admin.TabularInline):
    """Inline for product specifications - appears on product edit page"""
    model = ProductSpecification
    extra = 5
    fields = ['spec_key', 'spec_value', 'display_order', 'is_active']
    ordering = ['display_order']
    classes = ['collapse']
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        return formset


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'category', 'seller_price', 'is_active', 'is_featured')
    list_editable = ('category', 'is_active', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured', 'brand')
    search_fields = ('title', 'sku', 'brand')
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProductImageInline, ProductSpecificationInline]
    
    fieldsets = (
        ('Product Information', {
            'fields': ('title', 'slug', 'sku', 'category', 'product_image')
        }),
        ('Product Details', {
            'fields': ('brand', 'sizes', 'short_description', 'detail_description'),
            'classes': ('wide',)
        }),
        ('Pricing', {
            'fields': ('price', 'seller_price', 'retail_price'),
            'description': 'Set the prices for this product. seller_price is actual selling price, retail_price is marked-up price'
        }),
        ('Delivery Information', {
            'fields': ('delivery_time',),
            'description': 'Information about estimated delivery time',
            'classes': ('collapse',)
        }),
        ('Refund & Return Policy', {
            'fields': ('refund_and_return_policy',),
            'description': 'Terms and conditions for returns and refunds',
            'classes': ('collapse',)
        }),
        ('Specifications', {
            'fields': (),
            'description': 'Product specifications can be added in the "Product Specifications" section below',
            'classes': ('collapse',)
        }),
        ('Share Options', {
            'fields': ('enable_facebook_share', 'enable_twitter_share', 'enable_pinterest_share', 'enable_linkedin_share'),
            'description': 'Enable or disable sharing on social media platforms'
        }),
        ('Status & Ratings', {
            'fields': ('rating', 'is_active', 'is_featured'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'approved', 'created_at')
    list_filter = ('approved', 'rating')
    list_editable = ('approved',)


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    list_editable = ('quantity',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'status', 'ordered_date')
    list_editable = ('quantity', 'status')
    list_filter = ('status', 'ordered_date')


class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'spec_key', 'spec_value', 'display_order', 'is_active')
    list_filter = ('is_active', 'product__category')
    search_fields = ('product__title', 'spec_key', 'spec_value')
    list_editable = ('display_order', 'is_active')
    list_per_page = 20


admin.site.register(Address, AddressAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(CompanyInfo)
admin.site.register(ProductSpecification, ProductSpecificationAdmin)