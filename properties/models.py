from django.db import models
from django.contrib.auth.models import User


class Property(models.Model):

    PROPERTY_TYPES = (
        ('Apartment', 'Apartment'),
        ('Villa', 'Villa'),
        ('House', 'House'),
        ('Commercial', 'Commercial'),
    )

    agent = models.ForeignKey(
    User,
    on_delete=models.CASCADE
)

    favorites = models.ManyToManyField(
    User,
    related_name='favorite_properties',
    blank=True
)

    title = models.CharField(
        max_length=200
    )

    location = models.CharField(
        max_length=200
    )

    price = models.IntegerField()

    property_type = models.CharField(
        max_length=100,
        choices=PROPERTY_TYPES
    )
    STATUS_CHOICES = (
    ('Sale', 'Sale'),
    ('Rent', 'Rent'),
)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Sale'
    )
    bedrooms = models.IntegerField(default=1)

    bathrooms = models.IntegerField(default=1)
    area = models.IntegerField(default=1000)

    image = models.ImageField(
        upload_to='property_images/'
    )

    description = models.TextField()
    map_link = models.TextField(
    blank=True,
    null=True
)
    is_featured = models.BooleanField(
    default=False
)

    is_sold = models.BooleanField(
        default=False
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class Inquiry(models.Model):

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.username} - {self.property.title}"

class Review(models.Model):

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField()

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.username} - {self.property.title}"
    

class PropertyImage(models.Model):

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )

    image = models.ImageField(
        upload_to='gallery/'
    )

    def __str__(self):

        return self.property.title
    

class Profile(models.Model):

    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('owner', 'Owner'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='buyer'
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):

        return self.user.username
    
class PropertyVisit(models.Model):

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE
    )

    visitor = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    visit_date = models.DateField()

    visit_time = models.TimeField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.visitor.username} - {self.property.title}"
    
class ChatMessage(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.sender} -> {self.receiver}"

class Notification(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.user.username
    
class RecentlyViewed(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE
    )

    viewed_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ['-viewed_at']

    def __str__(self):

        return f"{self.user.username} viewed {self.property.title}"
class PropertyImage(models.Model):

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to='property_gallery/'
    )

    def __str__(self):

        return self.property.title