from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    #path('', views.home),
    path('',views.ProductView.as_view(),name="home"),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('removecart/', views.remove_cart, name='remove_cart'),
    path('pluscart/', views.plus_cart, name='plus_cart'),
    path('minuscart/', views.minus_cart, name='minus_cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('pick/', views.pick, name='pick'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('Laptop/', views.Laptop, name='Laptop'),
    path('Laptop/<slug:data>', views.Laptop, name='Laptopdata'),
    path('Jeans/', views.Jeans, name='Jeans'),
    path('Jeans/<slug:data>', views.Jeans, name='Jeansdata'),
    path('TopWear/', views.TopWear, name='TopWear'),
    path('TopWear/<slug:data>', views.TopWear, name='TopWeardata'),
    path('CovidMedicine/', views.CovidMedicine, name='CovidMedicine'),
    path('Mask/', views.Mask, name='Mask'),
    path('Sanitizer/', views.Sanitizer, name='Sanitizer'),
    path('KitchenEssential/', views.KitchenEssential, name='KitchenEssential'),
    path('KitchenEssential/<slug:data>', views.KitchenEssential, name='KitchenEssentialdata'),
    path('Grocery/', views.Grocery, name='Grocery'),
    path('Grocery/<slug:data>', views.Grocery, name='Grocerydata'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout2/', views.checkout2, name='checkout2'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('pickpaymentdone/', views.pickpayment_done, name='pickpaymentdone'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    path('shopregistration/', views.ShopRegistrationView.as_view(), name="shopregistration"),
    path('registration/', views.CustomerRegistrationView.as_view(), name="customerregistration"),
    path('searchbar/',views.searchbar,name='searchbar')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
