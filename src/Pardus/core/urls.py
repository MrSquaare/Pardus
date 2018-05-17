#
# Documentation Django sur la distribution des URLs :
# https://docs.djangoproject.com/fr/2.0/topics/http/urls/
#

from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from core import views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("<int:id>-<slug:slug>/", views.ArticleRead.as_view(), name="article_read"),
    path("<int:year>/<int:month>/", views.DateFilter.as_view(), name="date_filter"),
    path("categories/", views.Categories.as_view(), name="categories"),
    path("categories/<int:id>/", views.CategoriesFilter.as_view(), name="categories_filter"),
    path("contact/", views.Contact.as_view(), name="contact"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(redirect_field_name="next"), name="logout"),
    path("register/", views.Register.as_view(), name="register"),
    re_path(r"^profile/(?:(?P<id>[1-9]+)/)?$", views.Profile.as_view(), name="profile"),
    path("settings/", views.Settings.as_view(), name="settings"),
    path("search/", views.search, name="search"),
]
