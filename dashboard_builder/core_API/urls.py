from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register("dashboard", DashboardViewSet, "dashboards")
router.register("dataset", DatasetViewSet, "datasets")

urlpatterns = [
    path('', include(router.urls)),
    path('view/dashboard/<str:dashboard_id>/', ViewDashboardView),
    path('analytics/line/<str:dataset_id>/', LineAnalyticsView),
    path('analytics/bar/<str:dataset_id>/', BarAnalyticsView),
    path('analytics/value/<str:dataset_id>/', ValueAnalyticsView),
]