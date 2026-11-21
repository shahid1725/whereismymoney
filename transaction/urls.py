from rest_framework.routers import DefaultRouter

from transaction.views import TransactionViewSet


router = DefaultRouter()
router.register('', TransactionViewSet, basename='transaction')

urlpatterns = router.urls
