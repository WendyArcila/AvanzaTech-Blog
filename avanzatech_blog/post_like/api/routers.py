from rest_framework.routers import DefaultRouter
from post_like.views import PostLikeViewSet


router = DefaultRouter()

router.register(r'', PostLikeViewSet, basename='likes')

urlpatterns = router.urls
