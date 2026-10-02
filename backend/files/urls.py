from rest_framework.routers import DefaultRouter

from files.views import UploadedFileViewSet


router = DefaultRouter()
router.register(
    "files",
    UploadedFileViewSet,
    basename="uploaded-file",
)

urlpatterns = router.urls