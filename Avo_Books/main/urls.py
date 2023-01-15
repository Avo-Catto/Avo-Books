from django.urls import path
from .views import home, search_results

urlpatterns = [
    path('', home),
    path('search-results/', search_results)
]
