from rest_framework import viewsets, permissions, filters, status, mixins
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from .models import Event, EventRegistration
from .serializers import EventSerializer, EventRegistrationSerializer
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django_filters.rest_framework import DjangoFilterBackend
import logging
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from pprint import pformat

logger = logging.getLogger(__name__)

from django.utils import timezone
from django.views.generic import ListView
from .models import Event

class HomePageView(ListView):
    model = Event
    template_name = "index.html"
    context_object_name = "events"
    paginate_by = 5

    def get_queryset(self):
        queryset = Event.objects.all()
        self.category = self.request.GET.get('category', '')
        self.location = self.request.GET.get('location', '')
        self.price_from = self.request.GET.get('price_from', '')
        self.price_to = self.request.GET.get('price_to', '')
        self.filter_time = self.request.GET.get('filter-time', '')


        if self.category:
            queryset = queryset.filter(category=self.category)
        if self.location:
            queryset = queryset.filter(location__icontains=self.location)
        if self.price_from:
            queryset = queryset.filter(price__gte=self.price_from)
        if self.price_to:
            queryset = queryset.filter(price__lte=self.price_to)
        if self.filter_time == 'today':
            queryset = queryset.filter(date=timezone.now().date())
        elif self.filter_time == 'this_week':
            start_of_week = timezone.now().date()
            end_of_week = start_of_week + timezone.timedelta(days=7)
            queryset = queryset.filter(date__range=[start_of_week, end_of_week])
        elif self.filter_time == 'this_month':
            start_of_month = timezone.now().date().replace(day=1)
            next_month = start_of_month + timezone.timedelta(days=32)
            end_of_month = next_month.replace(day=1) - timezone.timedelta(days=1)
            queryset = queryset.filter(date__range=[start_of_month, end_of_month])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()

        if 'page' in query_params:
            del query_params['page']

        context['query_string'] = query_params.urlencode()
        context["location"] = self.location
        context["category"] = self.category
        context["price_from"] = self.price_from
        context["price_to"] = self.price_to
        context["filter_time"] = self.filter_time
        context["order_by"] = self.request.GET.get('order_by', '')
        return context


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'location', 'price']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['date', 'price']

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        if Event.objects.filter(title=title).exists():
            raise ValidationError("Event with this title already exists")
        serializer.save(organizer=self.request.user)



class EventRegistrationViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(operation_summary="Create an Event Registration")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Delete an Event Registration")
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({"detail": "You do not have permission to delete this registration."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        user = self.request.user
        event = serializer.validated_data.get('event')

        if EventRegistration.objects.filter(user=user, event=event).exists():
            raise ValidationError("You are already registered for this event.")

        serializer.save(user=self.request.user)
        registration = serializer.instance

        logger.info(
            f'Registration for event "{registration.event.title}" has been made by user {registration.user.email}. '
            f'An email notification should be sent to the organizer {registration.event.organizer.email}.'
        )
