from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

STATUS_CHOICES = (
    ('published', 'Published'),
    ('draft', 'Draft'),
)
CATEGORY_CHOICES = (
    ('concert', 'Concert'),
    ('conference', 'Conference'),
    ('meetup', 'Meetup'),
    ('workshop', 'Workshop'),
    ('webinar', 'Webinar'),
)


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    event_time = models.TimeField()
    location = models.CharField(
        max_length=550,
        verbose_name="Адреса/Місце проведення",
        default=''
        )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
        )
    slug = models.SlugField(unique=True, blank=True)
    organizer = models.ForeignKey(
        User,
        related_name='events',
        on_delete=models.CASCADE
        )
    price = models.PositiveIntegerField(null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def registration_count(self):
        return self.registrations.count()

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, related_name='registrations', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='registrations', on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.user.username} registered for {self.event.title}"
