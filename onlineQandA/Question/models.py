from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from taggit.models import Tag
from django.utils.timezone import now
# Create your models here.


class IpModel(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip


class Comment(models.Model):
    postby = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    body = models.TextField(blank=False)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='replies', null=True)
    timestamp = models.DateTimeField(default=now)

    class Meta:
        # sort comments in chronological order by default
        ordering = ('timestamp',)

    def __str__(self):
        return self.body[0:10]+"...."+" by "+self.postby.username


class Question(models.Model):
    postby = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    postdate = models.DateTimeField(auto_now_add=True)
    title = models.TextField(null=True)
    description = RichTextField(null=True)
    Tags = TaggableManager(blank=True)
    likes = models.ManyToManyField(User, related_name='que_like')
    views = models.ManyToManyField(
        IpModel, related_name="que_views", blank=True)
    comment = models.ManyToManyField(
        Comment, related_name='que_comment', null=True)

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
    comment = models.ManyToManyField(
        Comment, related_name='ans_comment', null=True)

    def __str__(self):
        return self.title

    def get_tag_names(self):
        return [tag.name for tag in Tag.objects.get_for_object(self)]

    def total_like(self):
        return self.likes.count()

    def total_view(self):
        return self.views.count()
