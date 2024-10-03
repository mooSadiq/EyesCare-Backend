from django.urls import path
from . import mobile_api
from . import subscription

urlpatterns = [
    path('plan/', mobile_api.PlanListView.as_view(), name='plan-list'),
    path('plan/<int:pk>/', subscription.SubscribeToPlan.as_view(), name='plan-subscripe'),
]
