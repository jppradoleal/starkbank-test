from rest_framework.routers import DefaultRouter

from payments import views

router = DefaultRouter()
router.register(r"webhook", views.WebhookViewSet, basename="webhook")
urlpatterns = router.urls
