from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name="register"),
    path('activate/<uidb64>/<token>', user_views.activate,
         name="activate"),
    path('email-send/', user_views.email_send, name="email-send"),
    path('email-validate/', user_views.activation_email, name="email-validate"),
    path('profile/', user_views.profile, name="profile"),
    path('login/', user_views.Login.as_view(template_name='users/login.html', extra_context={'title': 'Login'}),
         name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html', extra_context={'title': 'Logout'}),
         name="logout"),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html',
                                                                 extra_context={'title': 'Password Reset'}),
         name="password_reset"),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name="password_reset_confirm"),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name="password_reset_complete"),
    path('', include('password.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
