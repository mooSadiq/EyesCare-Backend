from django.urls import path
from . import mobile_api

urlpatterns = [
    path('plan/', mobile_api.PlanListView.as_view(), name='plan-list'),
]
