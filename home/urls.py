from django.contrib import admin
from django.urls import path
from home import views

# Setting url paths.
urlpatterns = [
    path("",views.index,name="home"),
    path("next_page",views.next_page),
    path("last_page",views.next_page_data_submit),
    path("preview_video",views.preview_video)
]