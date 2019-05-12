from django.urls import include,path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register('login',views.LoginViewSet,base_name='login')
router.register('profile',views.ProfilesViewSet)
router.register('fighter',views.FighterViewSet)
urlpatterns = [
    path('',include(router.urls))
]