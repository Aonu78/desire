import django
from django.contrib.auth.models import User
from store.models import Address, Cart, Category, Order, Product, CompanyInfo
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import HttpResponse
from .forms import RegistrationForm, AddressForm
from django.contrib import messages
from django.views import View
import decimal
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator # for Class Based Views
from .models import Review


# Create your views here.

def home(request):
    categories = Category.objects.filter(is_active=True, is_featured=True)[:3]
    products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'store/index.html', context)


def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.exclude(id=product.id).filter(is_active=True, category=product.category)
    images = product.images.all()
    reviews = product.reviews.filter(approved=True)
    company_info = CompanyInfo.objects.first()  # Get company WhatsApp info

    if request.method == "POST":
        if request.user.is_authenticated:
            rating = request.POST.get("rating")
            comment = request.POST.get("comment")
            image = request.FILES.get("image")

            Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment,
                image=image
            )

            messages.success(request, "Review submitted! Waiting for admin approval.")
            return redirect("store:product-detail", slug=slug)

    context = {
        'product': product,
        'related_products': related_products,
        'images': images,
        'reviews': reviews,
        'company_info': company_info,
    }
    return render(request, 'store/detail.html', context)

def all_categories(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'store/categories.html', {'categories':categories})


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(is_active=True, category=category)
    categories = Category.objects.filter(is_active=True)
    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'store/category_products.html', context)


def cart_redirect(request):
    """Redirect old cart URL to orders page"""
    return redirect('store:orders')


# Authentication Starts Here

class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'account/register.html', {'form': form})
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulations! Registration Successful!")
            form.save()
        return render(request, 'account/register.html', {'form': form})
        

@login_required
def profile(request):
    addresses = Address.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    return render(request, 'account/profile.html', {'addresses':addresses, 'orders':orders})


@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self, request):
        form = AddressForm()
        return render(request, 'account/add_address.html', {'form': form})

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            user=request.user
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            country = form.cleaned_data['country']
            reg = Address(user=user, locality=locality, city=city, state=state, country=country)
            reg.save()
            messages.success(request, "New Address Added Successfully.")
        return redirect('store:profile')


@login_required
def remove_address(request, id):
    a = get_object_or_404(Address, user=request.user, id=id)
    a.delete()
    messages.success(request, "Address removed.")
    return redirect('store:profile')




@login_required
def buy_now(request):
    """Handle order creation with shipping address form"""
    user = request.user
    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        # Get shipping address details from form
        full_name = request.POST.get('full_name').strip()
        phone_number = request.POST.get('phone_number').strip()
        building_no = request.POST.get('building_no').strip()
        locality = request.POST.get('locality').strip()
        province = request.POST.get('province').strip()
        city = request.POST.get('city').strip()
        area = request.POST.get('area').strip()
        address = request.POST.get('address').strip()
        
        try:
            product = get_object_or_404(Product, id=product_id)
            
            # Create or update address
            addr, created = Address.objects.update_or_create(
                user=user,
                defaults={
                    'full_name': full_name,
                    'phone_number': phone_number,
                    'building_no': building_no,
                    'locality': locality,
                    'province': province,
                    'city': city,
                    'area': area,
                    'address': address,
                    'country': 'Pakistan'
                }
            )
            
            # Create order for the product
            order = Order.objects.create(
                user=user,
                address=addr,
                product=product,
                quantity=quantity
            )
            
            # Log the order details to terminal
            total_price = int(quantity) * float(product.price)
            print(f"\n{'='*70}")
            print(f"✅ NEW ORDER CREATED - User: {user.username}")
            print(f"{'='*70}")
            print(f"📍 SHIPPING ADDRESS:")
            print(f"   Full Name: {full_name}")
            print(f"   Phone: {phone_number}")
            print(f"   Building/House No: {building_no}")
            print(f"   Locality/Landmark: {locality}")
            print(f"   Area: {area}")
            print(f"   City: {city}")
            print(f"   Province: {province}")
            print(f"   Full Address: {address}")
            print(f"\n📦 PRODUCT ORDER:")
            print(f"   Product: {product.title}")
            print(f"   SKU: {product.sku}")
            print(f"   Price: ${product.price}")
            print(f"   Quantity: {quantity}")
            print(f"   Total Amount: ${total_price}")
            print(f"   Status: {order.status}")
            print(f"{'='*70}\n")
            
            return redirect('store:orders')
            
        except Exception as e:
            print(f"❌ Error creating order: {str(e)}")
            return redirect('store:home')
    
    return redirect('store:home')











@login_required
def orders(request):
    all_orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    return render(request, 'store/orders.html', {'orders': all_orders})





def shop(request):
    # Search and category filtering
    q = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True)

    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        except Category.DoesNotExist:
            category = None

    if q:
        products = products.filter(Q(title__icontains=q) | Q(short_description__icontains=q))

    # paginate
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': categories,
        'query': q,
        'selected_category': category_slug,
        'page_obj': page_obj,
    }

    # If AJAX request, return only the product list partial
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('store/_product_list.html', context, request=request)
        return HttpResponse(html)

    return render(request, 'store/shop.html', context)





def test(request):
    return render(request, 'store/test.html')






from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CompanyInfo  # If you have this model

# Add these new view functions at the end of your views.py

def about_page(request):
    """Display about us page"""
    # Get company info if you have the model
    company_info = None
    try:
        company_info = CompanyInfo.objects.first()
    except:
        pass
    
    context = {
        'company_info': company_info,
    }
    return render(request, 'store/about.html', context)


def contact_page(request):
    """Display contact page"""
    company_info = None
    try:
        company_info = CompanyInfo.objects.first()
    except:
        pass
    
    context = {
        'company_info': company_info,
    }
    return render(request, 'store/contact.html', context)


def contact_submit(request):
    """Handle contact form submission"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you can add code to:
        # 1. Save to database (if you create a Contact model)
        # 2. Send email notification
        # 3. Log the contact request
        
        # For now, just show success message
        messages.success(request, f'Thank you {name}! We have received your message and will contact you soon.')
        
        # Optional: Print to console for testing
        print(f"\n📧 NEW CONTACT FORM SUBMISSION")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Phone: {phone}")
        print(f"Subject: {subject}")
        print(f"Message: {message}")
        print("-" * 50)
        
    return redirect('store:contact')


def faq_page(request):
    """Display FAQ page"""
    # Hardcoded FAQs - you can move these to a model later if needed
    faq_categories = [
        {
            'id': 'orders',
            'name': 'Orders',
            'questions': [
                {
                    'question': 'How do I place an order?',
                    'answer': 'To place an order, simply browse our products, click on the item you want, select your preferred options, and click "Add to Cart." Then go to your cart and follow the checkout process to complete your order.'
                },
                {
                    'question': 'Can I modify or cancel my order?',
                    'answer': 'You can modify or cancel your order within 2 hours of placing it. Please contact our customer support immediately with your order number for assistance.'
                },
                {
                    'question': 'How do I track my order?',
                    'answer': 'Once your order is shipped, you\'ll receive a tracking number via email and SMS. You can use this number to track your order on our website or the courier\'s website.'
                },
            ]
        },
        {
            'id': 'shipping',
            'name': 'Shipping',
            'questions': [
                {
                    'question': 'What are your shipping charges?',
                    'answer': 'Shipping charges vary based on your location and order value. Orders above Rs. 2000 qualify for free shipping. You can see the exact shipping cost at checkout.'
                },
                {
                    'question': 'How long does delivery take?',
                    'answer': 'Delivery typically takes 3-5 business days for major cities and 5-7 business days for other areas.'
                },
                {
                    'question': 'Do you deliver internationally?',
                    'answer': 'Currently, we only deliver within Pakistan. We\'re working on expanding our services internationally in the future.'
                },
            ]
        },
        {
            'id': 'returns',
            'name': 'Returns & Refunds',
            'questions': [
                {
                    'question': 'What is your return policy?',
                    'answer': 'We offer a 7-day return policy. If you\'re not satisfied with your purchase, you can return it within 7 days of delivery for a full refund or exchange.'
                },
                {
                    'question': 'How do I initiate a return?',
                    'answer': 'To initiate a return, contact our customer support with your order number and reason for return. We\'ll guide you through the process.'
                },
                {
                    'question': 'How long do refunds take?',
                    'answer': 'Once we receive your returned item, refunds are processed within 3-5 business days.'
                },
            ]
        },
        {
            'id': 'payment',
            'name': 'Payment',
            'questions': [
                {
                    'question': 'What payment methods do you accept?',
                    'answer': 'We accept Cash on Delivery, Credit/Debit Cards, Easypaisa, JazzCash, and Bank Transfers.'
                },
                {
                    'question': 'Is Cash on Delivery available?',
                    'answer': 'Yes, Cash on Delivery is available for all orders across Pakistan.'
                },
                {
                    'question': 'Is it safe to pay online?',
                    'answer': 'Yes, we use secure payment gateways and encryption to protect your payment information.'
                },
            ]
        },
    ]
    
    context = {
        'faq_categories': faq_categories,
    }
    return render(request, 'store/faq.html', context)


# Add these new view functions at the end of your views.py

def returns_policy(request):
    """Display Returns Policy page"""
    return render(request, 'store/returns_policy.html')

def shipping_info(request):
    """Display Shipping Information page"""
    return render(request, 'store/shipping_info.html')

def payment_methods(request):
    """Display Payment Methods page"""
    return render(request, 'store/payment_methods.html')

def privacy_policy(request):
    """Display Privacy Policy page"""
    return render(request, 'store/privacy_policy.html')