from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core import views

router = DefaultRouter()
router.register('fruits', views.ListFruits)
router.register('sizes', views.ListSizes)
router.register('additionals', views.ListAdditionals)
router.register('orders', views.OrderViewSet)

app_name = 'core'

urlpatterns = [
    path('', include(router.urls)),
]
