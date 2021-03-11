from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from PIL import Image
# Create your models here.

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='Profile_pic')
    gender = models.CharField(choices=GENDER_CHOICES,
                              max_length=10, default='Male')
    Address = models.TextField(null=True, blank=True)
    education = models.TextField(null=True, blank=True)
    skill = TaggableManager(blank=True)
    about = models.TextField(null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Profile, self).save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
