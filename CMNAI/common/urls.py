from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
# from final import views as final_views


app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),

]