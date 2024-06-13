from django.contrib import admin
from django.urls import path, include
from labex import views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'labs', views.LabViewset)
router.register(r'appointments', views.AppointmentViewSet, basename='appointment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),

    path('login/', obtain_auth_token),
    path('robot/change_controller/', views.change_controller),
    path('robot/change_command/', views.change_command)
]
