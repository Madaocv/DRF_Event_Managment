from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, EventRegistrationViewSet, HomePageView

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'eventregistration', EventRegistrationViewSet, )

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('api/', include(router.urls)),
]
