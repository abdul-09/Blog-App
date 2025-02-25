from django.urls import path, include
from wagtail.admin import urls as wagtail_admin_urls
from wagtail.documents import urls as wagtail_docs_urls
from .views import *
from wagtail import urls as wagtail_urls

urlpatterns = [
    path('cms/', include(wagtail_admin_urls)),
    path('documents/', include(wagtail_docs_urls)),
    path('search/', article_search, name='article_search'),
    path('', include(wagtail_urls)),

]