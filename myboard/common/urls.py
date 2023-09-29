from django.contrib.auth import views as auth_views
from django.urls import path,include
from . import views

app_name = 'common'
urlpatterns = [
  path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
  path('signup/', views.signup, name='signup'),
]
# LoginView는 registration이라는 템플릿 디렉터리에서 login.html 파일을 찾는다
# registration/login.html 템플릿 파일을 작성하거나 따로 작성해서 연동