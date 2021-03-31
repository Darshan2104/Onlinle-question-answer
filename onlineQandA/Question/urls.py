from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('ask', views.Askquestion, name='Ask-Question'),
    path('update/<int:qid>', views.Updatequestion, name='Update-Question'),
    path('DetailsQUE/<int:qid>', views.Detailquestion, name='Detail-Question'),
    # LIKE
    path('DetailsQUE/<int:qid>/like', views.Questionlike,
         name='Detail-Question-like'),
    #
    path('DetailsQUE/<int:qid>/dislike', views.Questiondislike,
         name='Detail-Question-dislike'),
    path('ans/<int:qid>', views.Addanswer, name='Add-Answer'),
    # List of answers for particular question
    path('Listanswer/<int:qid>', views.listAnswer, name='List-Answer'),
    # View DETailed Answer
    path('Listanswer/<int:qid>/DetailsANS/<int:aid>/',
         views.Detailanswer, name='Detail-Answer'),
    #     LIKE Answerlike
    path('Listanswer/<int:qid>/DetailsANS/<int:aid>/like',
         views.Answerlike, name='Detail-Answer-like'),
    path('Listanswer/<int:qid>/DetailsANS/<int:aid>/dislike',
         views.Answerdislike, name='Detail-Answer-dislike'),
    # Updateanswer
    path('Listanswer/<int:qid>/update/<int:aid>',
         views.Updateanswer, name='Update-Answer'),
    #    Comment section for question
    path('DetailsQUE/<int:qid>/comment', views.QuestionComment,
         name='Detail-Question-comment'),
    path('Listanswer/<int:qid>/DetailsANS/<int:aid>/comment', views.AnswerComment,
         name='Detail-Answer-comment'),
    path('latest', views.Latest, name='Latest-questions'),
    path('mostvoted', views.Mostvoted, name='Mostvotted-questions'),
    path('unanswered', views.Unanswered, name='Unanswered-questions'),
    path('mostviewed', views.Mostviwed, name='Mostviwed-questions'),

    path('latest/<int:qid>', views.Latestans, name='Latest-answers'),
    path('mostvoted/<int:qid>', views.Mostvotedans, name='Mostvotted-answers'),
    path('mostviewed/<int:qid>', views.Mostviwedans, name='Mostviwed-answers'),

]
