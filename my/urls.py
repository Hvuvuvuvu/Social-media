from django.urls import path

from . import views
from .views import PubList, PubDetailView, PubCreateView, PubDeleteView, PubEditView, PubPublishView, CommentCreateView

urlpatterns = [
    path('my_pubs/', views.user_pub, name='user_pub'),
    path('kk/', PubList.as_view(), name='pub_list'),
    path('<int:pk>/', PubDetailView.as_view(), name='pub_detail'),
    path('pub_add/', PubCreateView.as_view(), name='pub_add'),
    path('pub_delete/<int:pk>', PubDeleteView.as_view(), name='pub_delete'),
    path('<int:pk>/edit/', PubEditView.as_view(), name='pub_edit'),
    path('<int:pk>/publish/', PubPublishView.as_view(), name='pub_publish'),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path('<int:pk>/add_comment/', CommentCreateView.as_view(), name='add_comment'),
    path('', PubList.as_view(), name='pub_list'),
    ]