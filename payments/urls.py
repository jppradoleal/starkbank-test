from django.urls import path
from payments import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"webhook", views.WebhookViewSet, basename="webhook")
urlpatterns = router.urls
