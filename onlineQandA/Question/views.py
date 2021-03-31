from django.shortcuts import render, redirect, get_object_or_404
from Profile.models import Profile
from django.contrib.auth.decorators import login_required
from .models import Question, Answer, IpModel, Comment
from taggit.models import Tag
from django.contrib import messages
from .forms import Questiondetails, Answerdetails
from django.urls import reverse
from django.http import HttpResponseRedirect
import datetime


# Create your views here.

# Comment
@login_required
def QuestionComment(request, qid):
    quest = get_object_or_404(Question, id=qid)
    obj = Comment.objects.create(postby=request.user)
    obj.body = request.POST.get('body')
    # conditions for parent comment remaining
    try:
        parent_cid = int(request.POST.get('parentid'))
    except:
        parent_cid = None
    if parent_cid:
        obj.parent = Comment.objects.get(id=parent_cid)
    obj.save()
    quest.comment.add(obj)
    return HttpResponseRedirect(reverse('Detail-Question', args=[str(qid)]))

# AnswerComment


@login_required
def AnswerComment(request, qid, aid):
    ans = get_object_or_404(Answer, id=aid)
    obj = Comment.objects.create(postby=request.user)
    obj.body = request.POST.get('body')

    # conditions for parent comment remaining
    try:
        parent_cid = int(request.POST.get('parentid'))
    except:
        parent_cid = None

    if parent_cid:
        obj.parent = Comment.objects.get(id=parent_cid)

    obj.save()
    ans.comment.add(obj)
    return HttpResponseRedirect(reverse('Detail-Answer', args=[str(qid), str(aid)]))

# Like-Dislike


@login_required
def Questionlike(request, qid):
    quest = get_object_or_404(Question, id=request.POST.get('queid'))
    quest.likes.add(request.user)
    return HttpResponseRedirect(reverse('Detail-Question', args=[str(qid)]))


@login_required
def Questiondislike(request, qid):
    quest = get_object_or_404(Question, id=request.POST.get('queid'))
    quest.likes.remove(request.user)
    return HttpResponseRedirect(reverse('Detail-Question', args=[str(qid)]))


def Latest(request):
    quest = Question.objects.order_by('-id')
    qlike = []
    qview = []
    for q in quest:
        qlike.append(q.likes.count())
        qview.append(q.views.count())

    mix = zip(quest, qlike, qview)
    totalquestions = quest.count()
    totaluser = Profile.objects.all().count()
    return render(request, 'Questions/home.html', {'mix': mix, 'totalquestions': totalquestions, 'totaluser': totaluser})


def Mostvoted(request):
    quest = Question.objects.all()
    qlike = []
    qview = []
    for q in quest:
        qlike.append(q.likes.count())
        qview.append(q.views.count())
    print(quest)
    zipped = zip(quest, qlike, qview)
    mix = sorted(zipped, key=lambda x: -x[1])
    totalquestions = quest.count()
    totaluser = Profile.objects.all().count()
    return render(request, 'Questions/home.html', {'mix': mix, 'totalquestions': totalquestions, 'totaluser': totaluser})


def Mostviwed(request):
    quest = Question.objects.all()
    qlike = []
    qview = []
    for q in quest:
        qlike.append(q.likes.count())
        qview.append(q.views.count())
    print(quest)
    zipped = zip(quest, qlike, qview)
    mix = sorted(zipped, key=lambda x: -x[2])
    totalquestions = quest.count()
    totaluser = Profile.objects.all().count()
    return render(request, 'Questions/home.html', {'mix': mix, 'totalquestions': totalquestions, 'totaluser': totaluser})


def Unanswered(request):
    quest = Question.objects.all()
    qlike = []
    qview = []
    qlist = []
    ans = Answer.objects.all()

    for q in quest:
        qlist.append(q)

    for a in ans:
        if a.Qid in qlist:
            qlist.remove(a.Qid)
    print(qlist)
    for q in qlist:
        qlike.append(q.likes.count())
        qview.append(q.views.count())
    mix = zip(qlist, qlike, qview)
    totalquestions = quest.count()
    totaluser = Profile.objects.all().count()
    return render(request, 'Questions/home.html', {'mix': mix, 'totalquestions': totalquestions, 'totaluser': totaluser})

# get ip address


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def home(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query is None:
            quest = Question.objects.all()
        else:
            quest = Question.objects.filter(title__icontains=query)
    else:
        quest = Question.objects.all()

    qlike = []
    qview = []
    for q in quest:
        qlike.append(q.likes.count())
        qview.append(q.views.count())

    mix = zip(quest, qlike, qview)
    totalquestions = quest.count()
    totaluser = Profile.objects.all().count()
    totalanswers = Answer.objects.all().count()
    return render(request, 'Questions/home.html', {'quest': quest, 'totaluser': totaluser, 'totalquestions': totalquestions, 'totalanswers': totalanswers, 'mix': mix})


@login_required
def Askquestion(request):
    if request.method == 'POST':
        q_form = Questiondetails(request.POST, request.FILES)
        if q_form.is_valid():
            q_form.save()
            obj = q_form.instance
            obj.postby = request.user
            obj.postdate = datetime.datetime.now()
            obj.save()
            messages.success(request, f'Your Question has been Added!!!')
            return redirect('/')
    else:
        q_form = Questiondetails()
        return render(request, 'Questions/AskQuestion.html', {'q_form': q_form})


@login_required
def Updatequestion(request, qid):
    quest = Question.objects.get(id=qid)
    # tagsList = []
    # for tag in quest.Tags.all():
    #     tagsList.append(tag.name)
    if request.method == 'POST':
        q_form = Questiondetails(
            request.POST, request.FILES, instance=quest)
        if q_form.is_valid():
            q_form.save()
            messages.success(request, f'Your Question has been updated !!!')
            return redirect('Detail-Question', qid=qid)
        # else:
        #     return redirect('/ask')
    else:
        q_form = Questiondetails(instance=quest)
    return render(request, 'Questions/UpdateQuestion.html', {'q_form': q_form, 'qid': qid})


def Detailquestion(request, qid):
    quest = Question.objects.get(id=qid)
    total_like = quest.total_like()
    tagsList = []
    for tag in quest.Tags.all():
        tagsList.append(tag.name)

    ip = get_client_ip(request)
    if not IpModel.objects.filter(ip=ip).exists():
        IpModel.objects.create(ip=ip)
    quest.views.add(IpModel.objects.get(ip=ip))
    total_view = quest.total_view()
    comments = quest.comment.all().order_by('-timestamp')
    alist = Answer.objects.filter(Qid=qid)
    totalans = alist.count()
    return render(request, 'Questions/DetailQuestion.html', {'quest': quest, 'tagsList': tagsList, 'total_like': total_like, 'total_view': total_view, 'totalans': totalans, 'comments': comments})

# .........................................ANSWERS................................................


@login_required
def Answerlike(request, qid, aid):
    ans = get_object_or_404(Answer, id=request.POST.get('ansid'))
    ans.likes.add(request.user)
    return HttpResponseRedirect(reverse('Detail-Answer', args=[str(qid), str(aid)]))


@login_required
def Answerdislike(request, qid, aid):
    ans = get_object_or_404(Answer, id=request.POST.get('ansid'))
    ans.likes.remove(request.user)
    return HttpResponseRedirect(reverse('Detail-Answer', args=[str(qid), str(aid)]))


@login_required
def Addanswer(request, qid):
    if request.method == 'POST':
        a_form = Answerdetails(request.POST, request.FILES)
        if a_form.is_valid():
            a_form.save()
            obj = a_form.instance
            quest = Question.objects.get(id=qid)
            obj.Qid = quest
            obj.postby = request.user
            obj.postdate = datetime.datetime.now()
            obj.save()
            messages.success(request, f'Your Answer has been Added!!!')
            return redirect('Detail-Question', qid=str(qid))
    else:
        a_form = Answerdetails()
        return render(request, 'Questions/AddAnswer.html', {'a_form': a_form})


@login_required
def Updateanswer(request, qid, aid):
    ans = Answer.objects.get(id=aid)
    # quest =Question.objects.get(id=qid)
    if request.method == 'POST':
        a_form = Answerdetails(
            request.POST, request.FILES, instance=ans)
        if a_form.is_valid():
            a_form.save()
            messages.success(request, f'Your Answer has been updated !!!')
            return redirect('Detail-Answer', aid=aid, qid=qid)
        # else:
        #     return redirect('/ask')
    else:
        a_form = Answerdetails(instance=ans)
    return render(request, 'Questions/UpdateAnswer.html', {'a_form': a_form, 'aid': aid, 'qid': qid})


def listAnswer(request, qid):
    quest = Question.objects.get(id=qid)

    if request.method == 'GET':
        query = request.GET.get('query')
        if query is None:
            ans = Answer.objects.filter(Qid=quest)
        else:
            ans = Answer.objects.filter(
                title__icontains=query).filter(Qid=quest)
    else:
        ans = Answer.objects.filter(Qid=quest)

    alike = []
    aview = []
    for a in ans:
        alike.append(a.likes.count())
        aview.append(a.views.count())

    mix = zip(ans, alike, aview)
    totalans = ans.count()
    return render(request, 'Questions/ListAnswer.html', {'qid': qid, 'mix': mix, 'totalans': totalans})


def Detailanswer(request, qid, aid):
    ans = Answer.objects.get(id=aid)
    total_like = ans.total_like()
    tagsList = []
    for tag in ans.Tags.all():
        tagsList.append(tag.name)

    ip = get_client_ip(request)
    if not IpModel.objects.filter(ip=ip).exists():
        IpModel.objects.create(ip=ip)
    ans.views.add(IpModel.objects.get(ip=ip))
    total_view = ans.total_view()
    comments = ans.comment.all().order_by('-timestamp')
    return render(request, 'Questions/DetailAnswer.html', {'ans': ans, 'tagsList': tagsList, 'qid': qid, 'total_like': total_like, 'total_view': total_view, 'comments': comments})


def Latestans(request, qid):

    temp = Answer.objects.filter(Qid=qid)
    ans = temp.order_by('-id')
    alike = []
    aview = []
    for a in ans:
        alike.append(a.likes.count())
        aview.append(a.views.count())

    mix = zip(ans, alike, aview)
    totalans = ans.count()
    return render(request, 'Questions/ListAnswer.html', {'mix': mix, 'qid': qid, 'totalans': totalans})


def Mostvotedans(request, qid):

    temp = Answer.objects.filter(Qid=qid)
    ans = temp.order_by('-id')
    alike = []
    aview = []
    for a in ans:
        alike.append(a.likes.count())
        aview.append(a.views.count())
    zipped = zip(ans, alike, aview)
    mix = sorted(zipped, key=lambda x: -x[1])
    totalans = ans.count()
    return render(request, 'Questions/ListAnswer.html', {'mix': mix, 'qid': qid, 'totalans': totalans})


def Mostviwedans(request, qid):
    temp = Answer.objects.filter(Qid=qid)
    ans = temp.order_by('-id')
    alike = []
    aview = []
    for a in ans:
        alike.append(a.likes.count())
        aview.append(a.views.count())
    zipped = zip(ans, alike, aview)
    mix = sorted(zipped, key=lambda x: -x[2])
    totalans = ans.count()
    return render(request, 'Questions/ListAnswer.html', {'mix': mix, 'qid': qid, 'totalans': totalans})
