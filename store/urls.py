from store.forms import LoginForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'store'


urlpatterns = [
    path('', views.home, name="home"),
    # URL for Direct Checkout (Buy Now)
    path('checkout/', views.buy_now, name="buy-now"),
    path('orders/', views.orders, name="orders"),
    path('cart/', views.cart_redirect, name="cart"),  # Redirect cart to orders

    #URL for Products
    path('product/<slug:slug>/', views.detail, name="product-detail"),
    path('categories/', views.all_categories, name="all-categories"),
    path('shop/', views.shop, name="shop"),
    
    # New Pages for Footer Links
    path('about/', views.about_page, name="about"),
    path('contact/', views.contact_page, name="contact"),
    path('contact/submit/', views.contact_submit, name="contact_submit"),
    path('faq/', views.faq_page, name="faq"),
    
    # New Policy & Info Pages
    path('returns-policy/', views.returns_policy, name="returns_policy"),
    path('shipping-info/', views.shipping_info, name="shipping_info"),
    path('payment-methods/', views.payment_methods, name="payment_methods"),
    path('privacy-policy/', views.privacy_policy, name="privacy_policy"),
    
    # This should be LAST - catches any other slug for categories
    path('<slug:slug>/', views.category_products, name="category-products"),

    # URL for Authentication
    path('accounts/register/', views.RegistrationView.as_view(), name="register"),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='account/login.html', authentication_form=LoginForm), name="login"),
    path('accounts/profile/', views.profile, name="profile"),
    path('accounts/add-address/', views.AddressView.as_view(), name="add-address"),
    path('accounts/remove-address/<int:id>/', views.remove_address, name="remove-address"),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name="logout"),

    path('accounts/password-change/', auth_views.PasswordChangeView.as_view(template_name='account/password_change.html', form_class=PasswordChangeForm, success_url='/accounts/password-change-done/'), name="password-change"),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), name="password-change-done"),

    path('accounts/password-reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html', form_class=PasswordResetForm, success_url='/accounts/password-reset/done/'), name="password-reset"),
    path('accounts/password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name="password_reset_done"),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html', form_class=SetPasswordForm, success_url='/accounts/password-reset-complete/'), name="password_reset_confirm"),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name="password_reset_complete"),

    path('product/test/', views.test, name="test"),
]