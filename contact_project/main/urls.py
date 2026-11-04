from django.urls import path
from main.views import *


app_name = "main"

urlpatterns = [
    path("", contact_list, name="contact_list"),
    path("contacts/search/", contact_search, name="contact_search"),
    path("contacts/add/", contact_add, name="contact_add"),
    path("contacts/<int:pk>/", contact_detail, name="contact_detail"),
    path("contacts/<int:pk>/row/", contact_row, name="contact_row"),
    path("contacts/<int:pk>/edit/", contact_edit, name="contact_edit"),
    path("contacts/<int:pk>/update/", contact_update, name="contact_update"),
    path("contacts/<int:pk>/delete/", contact_delete, name="contact_delete"),
]