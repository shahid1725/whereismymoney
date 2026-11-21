from rest_framework.routers import DefaultRouter

from account.views import AccountViewSet


router = DefaultRouter()
router.register('', AccountViewSet, basename='account')

urlpatterns = router.urls
