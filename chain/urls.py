from django.urls import path
from . import views

app_name = "chain"

urlpatterns = [
    path("request-form/", views.request_form, name="request_form"),
    path("request-list/", views.request_list, name="request_list"),
    path('', views.create_token, name='create_token'),
    path('tokens/', views.token_list, name='token_list'),
    path('token-created/',views.token_created, name='token_created'),
    path('request-sent',views.request_sent, name="request_sent"),

]

