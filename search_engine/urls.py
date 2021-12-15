from django.contrib import admin
from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="Home"),
    path("submit_site/", submit_site, name="submit site"),
    path("search", search_results, name="search"),
    re_path(r"^search(.csrfmiddlewaretoken=[a-zA-Z0-9.].q=[a-zA-Z0-9])$",search_results, name="search_results")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
