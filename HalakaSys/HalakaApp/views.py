from django.shortcuts import render
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from .models import Contact,Degree
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.utils import timezone
from django.contrib import messages
# commet
# Create your views here.
import git
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update(request):
    if request.method == "POST":
        '''
        pass the path of the diectory where your project will be 
        stored on PythonAnywhere in the git.Repo() as parameter.
        Here the name of my directory is "test.pythonanywhere.com"
        '''
        repo = git.Repo("test.pythonanywhere.com/") 
        origin = repo.remotes.origin

        origin.pull()

        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")

def detailstud(request,id, template_name='detailstud.html'):
    degreesdetaills = Degree.objects.filter(stud_id=id)
    return render(request,template_name,{'degreesdetaills':degreesdetaills})

def show(request):
    degrees2 = Students.objects.filter(staff_id__author = request.user)
    degrees = Degree.objects.filter(stud_id__staff_id__author = request.user, attendance_date = datetime.today())
    #studnames = Students.objects.filter(staff_id__author = request.user),{'studnames':studnames}

    return render(request,"adddegree.html",{'degrees':degrees,'degrees2':degrees2})

def degree_edit(request, id, template_name='edit.html'):
    degree= get_object_or_404(Degree, id=id )
    form = DegreeForm(request.POST or None, instance=degree)
    form.fields['stud_id'].widget = forms.HiddenInput()
    degrees2 = Degree.objects.filter(id=id)
    if form.is_valid():
        form.save()
        return redirect('/adddegree')
    return render(request, template_name, {'form':form,'degrees2':degrees2})

def degree_create(request, template_name='insertdegree.html'):
    form = ExcludedDegreeForm(request.user, request.POST)
    if form.is_valid():
        form.save()
        return redirect('/adddegree')
    else:
       print(form.errors)
    return render(request, template_name, {'form':form})

def degree_create2(request,id, template_name='insertdegree2.html'):
    form = DegreeForm(request.POST)
    #form.fields['stud_id'] = forms.ModelChoiceField(queryset=Students.objects.filter(registration_number=id),label="اسم الطالب ")
    form.fields["stud_id"].queryset =Students.objects.filter(registration_number=id)
    #form.fields['stud_id'].widget = forms.HiddenInput()
    degrees2 = Students.objects.filter(registration_number=id)
    if form.is_valid():
        form.save()
        return redirect('/adddegree')
    else:
       print(form.errors)
    return render(request, template_name, {'form':form,'degrees2':degrees2})



def destroy(request, id):
    degrees = Degree.objects.get(id=id)
    degrees.delete()
    return HttpResponse('Thank you')
    return HttpResponseRedirect('/adddegree', message='تم الحذف')




def base(request):
    return render(request, 'base2.html')

def home(request):
    return render(request, 'home.html')
def register(request):
        registered = False

        if request.method == 'POST':
            profile_form = ProfileForm(request.POST, request.FILES)
            user_form  = UserForm(request.POST, request.FILES)
            if user_form.is_valid() and profile_form.is_valid():
                Students = profile_form.save(commit=False)
                user = user_form.save()

                user.first_name = Students.firstname
                user.last_name = Students.surname+ Students.other_name

                user.save()
                Students = profile_form.save(commit=False)
                Students.author = user
                Students.save()
                success_url = reverse_lazy("thanks2")
                registered = True
            else:
                print(user_form.errors, profile_form.errors)
        else:
            profile_form = ProfileForm()
            user_form = UserForm()


        return render(request, 'registration.html',
                            {'registered':registered,
                             'user_form':user_form,
                             'profile_form':profile_form})
def mydegrees(request):
    try:
        Mydegrees=  Degree.objects.filter(stud_id__author=request.user)

    except Degree.DoesNotExist:
        raise Http404("Poll does not exist")

    return render(request, 'mydegrees.html', {'mydegrees': Mydegrees})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('base'))
            else:
                return HttpResponse("ACCOUNT IS DEACTIVATED")
        else:
            return HttpResponse("Please use correct id and password")
            # return HttpResponseRedirect(reverse('register'))
    else:
        return render(request, 'login.html' )

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("ACCOUNT IS DEACTIVATED")
        else:
               return HttpResponse("Please use correct id and password")
            # return HttpResponseRedirect(reverse('register'))
    else:
        return render(request, 'login.html',{'title': 'تسجيل الدخول', })

def logout_user(request):
    logout(request)
    return render(request, 'logout.html', {
        'title': 'تسجيل الخروج'
    })

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

class ContactView(CreateView):
    model = Contact
    fields = '__all__'
    template_name = 'contact.html'
    success_url = reverse_lazy("thanks2")


def thanks(request):
    return HttpResponse("Thank you! Will get in touch soon.")
def thanks2(request):
    return render(request, 'thanks2.html')