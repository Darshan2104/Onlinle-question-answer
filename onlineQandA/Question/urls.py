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

]
