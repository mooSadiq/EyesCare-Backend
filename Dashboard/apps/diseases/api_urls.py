from django.urls import path
from . import api_mobile

urlpatterns = [
    path('', api_mobile.DiseaseListView.as_view(), name='diseases-list'),
    path('search/', api_mobile.DiseaseListSearchView.as_view(), name='diseases-search'),
]
