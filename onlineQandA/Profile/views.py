from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from Question.models import Question, Answer
from .forms import ProfileUpdateForm, UserRegistrationForm, UserUpdateForm
from taggit.models import Tag
# from django.views.generic import CreateView

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} registered successfully!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'Profile/register.html', {'form': form})


# Add and update are same
@login_required
def editprofile(request):

    try:
        profile = request.user.profile
    except:
        profile = Profile(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('/profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    # context = {
    #     'u_form': u_form,
    #     'p_form': p_form
    # }
    # print(u_form,p_form)
    return render(request, 'Profile/edit_Profile.html', {'u_form': u_form, 'p_form': p_form})


@login_required
def profile(request):
    u_info = request.user
    p_info = Profile.objects.get(user=u_info)
    tagsList = []
    for tag in p_info.skill.all():
        tagsList.append(tag.name)
    # Count total star of all qustion by this user and send it
    quest = Question.objects.filter(postby=u_info)
    ans = Answer.objects.filter(postby=u_info)
    qlike = []
    qview = []
    alike = []
    aview = []
    for q in quest:
        qlike.append(q.likes.count())
        qview.append(q.views.count())

    for a in ans:
        alike.append(a.likes.count())
        aview.append(a.views.count())
    quests = zip(quest, qlike, qview)
    anss = zip(ans, alike, aview)
    context = {
        'u_info': u_info,
        'p_info': p_info,
        'tagsList': tagsList,
        'quests': quests,
        'anss': anss,
        'quest': quest,
        'ans': ans,
    }
    return render(request, 'Profile/viewprofile.html', context)
