from django import forms
from django.forms import ModelForm, Textarea
from .models import Question, Answer

# forms

# postby = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
# postdate = models.DateTimeField(auto_now_add=True)
# title = models.TextField(null=True)
# description = RichTextField(null=True)
# Tags = TaggableManager()
# countstar = models.CharField(max_length=10)


class Questiondetails(ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'description', 'Tags')
        widgets = {
            'title': Textarea(attrs={'cols': 50, 'rows': 2}),
        }


class Answerdetails(ModelForm):
    class Meta:
        model = Answer
        fields = ('title', 'description', 'Tags')
        widgets = {
            'title': Textarea(attrs={'cols': 50, 'rows': 2}),
        }
