from django.urls import path
from django.core.exceptions import PermissionDenied
from . import views


def permission_denied_view(request):
    raise PermissionDenied


urlpatterns = [

    path('', views.home, name='home'),
    path('base', views.base, name='base'),
    path('home', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('contact/', views.ContactView.as_view(), name="contact"),
    path('mydegrees/', views.mydegrees, name="mydegrees"),
    path('403/', permission_denied_view),
    path('adddegree', views.show,name="adddegree"),
    path('edit/<int:id>', views.degree_edit, name='edit'),
    path('delete/<int:id>', views.destroy),
    path('insertdegree', views.degree_create, name='insertdegree'),
    path('detailstud/<int:id>', views.detailstud, name='detailstud'),
    path('insertdegree2/<int:id>', views.degree_create2, name='insertdegree2'),
    path('password/', views.change_password, name='password'),
    path("thanks/", views.thanks, name="thanks"),
    path("thanks2/", views.thanks2, name="thanks2"),
     path("update_server/", views.update, name="update"),
]



