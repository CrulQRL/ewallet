from django.urls import path, include
from . import utils
from . import views

router = utils.OptionalSlashRouter()
router.register('', views.CustomerViewSet)

urlpatterns = [
 path('', include(router.urls))
]