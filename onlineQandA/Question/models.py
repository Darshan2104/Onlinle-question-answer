from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from taggit.models import Tag
# Create your models here.


class IpModel(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip


class Question(models.Model):
    postby = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    postdate = models.DateTimeField(auto_now_add=True)
    title = models.TextField(null=True)
    description = RichTextField(null=True)
    Tags = TaggableManager(blank=True)
    likes = models.ManyToManyField(User, related_name='que_like')
    views = models.ManyToManyField(
        IpModel, related_name="que_views", blank=True)

    def total_like(self):
        return self.likes.count()

    def total_view(self):
        return self.views.count()

    def __str__(self):
        return self.title

    def get_tag_names(self):
        return [tag.name for tag in Tag.objects.get_for_object(self)]


class Answer(models.Model):
    Qid = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    postby = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    postdate = models.DateTimeField(auto_now_add=True)
    title = models.TextField(null=True)
    description = RichTextField(null=True)
    Tags = TaggableManager(blank=True)
    likes = models.ManyToManyField(User, related_name='ans_like')
    views = models.ManyToManyField(
        IpModel, related_name="ans_views", blank=True)

    def __str__(self):
        return self.title

    def get_tag_names(self):
        return [tag.name for tag in Tag.objects.get_for_object(self)]

    def total_like(self):
        return self.likes.count()

    def total_view(self):
        return self.views.count()
