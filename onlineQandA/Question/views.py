from django.shortcuts import render, redirect, get_object_or_404
from Profile.models import Profile
from django.contrib.auth.decorators import login_required
from .models import Question, Answer, IpModel
from taggit.models import Tag
from django.contrib import messages
from .forms import Questiondetails, Answerdetails
from django.urls import reverse
from django.http import HttpResponseRedirect
import datetime


# Create your views here.
def Questionlike(request, qid):
    quest = get_object_or_404(Question, id=request.POST.get('queid'))
    quest.likes.add(request.user)
    return HttpResponseRedirect(reverse('Detail-Question', args=[str(qid)]))


def Questiondislike(request, qid):
    quest = get_object_or_404(Question, id=request.POST.get('queid'))
    quest.likes.remove(request.user)
    return HttpResponseRedirect(reverse('Detail-Question', args=[str(qid)]))

# get ip address


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def home(request):
    quest = Question.objects.all()
    return render(request, 'Questions/home.html', {'quest': quest})


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
    return render(request, 'Questions/DetailQuestion.html', {'quest': quest, 'tagsList': tagsList, 'total_like': total_like, 'total_view': total_view})

# .........................................ANSWERS................................................


def Answerlike(request, qid, aid):
    ans = get_object_or_404(Answer, id=request.POST.get('ansid'))
    ans.likes.add(request.user)
    return HttpResponseRedirect(reverse('Detail-Answer', args=[str(qid), str(aid)]))


def Answerdislike(request, qid, aid):
    ans = get_object_or_404(Answer, id=request.POST.get('ansid'))
    ans.likes.remove(request.user)
    return HttpResponseRedirect(reverse('Detail-Answer', args=[str(qid), str(aid)]))


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
    qobj = Question.objects.get(id=qid)
    qlist = Answer.objects.all().filter(Qid=qobj)
    return render(request, 'Questions/ListAnswer.html', {'qlist': qlist, 'qid': qid})


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
    return render(request, 'Questions/DetailAnswer.html', {'ans': ans, 'tagsList': tagsList, 'qid': qid, 'total_like': total_like, 'total_view': total_view})
