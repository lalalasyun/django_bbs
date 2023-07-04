from accounts.form import RegisterForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import CreateView

from django.conf import settings
from django.conf.urls.static import static

from accounts import views

urlpatterns = [
	path('signup/', CreateView.as_view(
        template_name='accounts/signup.html',
		form_class=RegisterForm,
		success_url='/',
	), name='signup'),
	path('login/', LoginView.as_view(
        redirect_authenticated_user = True,
		template_name='accounts/login.html'
    ), name='login'),
	path('logout/',LogoutView.as_view(), name='logout'),
    path('follow/<username>/', views.followUser, name='follow'),
    path('setting/', views.settingUserView, name='setting'),
    path('<username>/', views.userProfileView, name='accounts'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)