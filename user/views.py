from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse, reverse_lazy

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeForm
from django.contrib import messages

from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from .forms import SignUpForm, EditProfileForm, EditUserForm
from .models import Profile

# Create your views here.

def registration(request):
    if request.user.is_authenticated:
        return redirect('blog:index')
    
    else:
        form = SignUpForm()
        if request.method == 'POST':
            form = SignUpForm(request.POST or None)
            if form.is_valid():
                form.save()
                
                username = form.cleaned_data.get('username')
                user = User.objects.get(username=username)
                Profile.objects.create(user=user)
                
                first_name = form.cleaned_data.get('first_name')
                messages.success(request, 'Account successfully created, enjoy ' + first_name)
                
                login(request, user)
                return redirect('user:profile', id=user.id)
                
        context = {
            'form': form
        }
        return render(request, 'user/registration.html', context)



def loginview(request):
    if request.user.is_authenticated:
        return redirect('blog:index')
    
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
        
            user = authenticate(request, username=username, password=password)
        
            if user is not None:
                login(request, user)
                messages.info(request, 'Logged in successfully!')
                return redirect('blog:index')
            else:
                messages.error(request, 'Username or Password is incorrect')
            
        context = {
        
        }
        return render(request, 'user/login.html', context)
 
 

def logoutview(request):
    logout(request)
    messages.info(request, 'Logged out successfully!')
    return redirect('blog:index')
 


@login_required(login_url='user:login')
def userprofile(request, id):
    user = User.objects.get(id=id)
    profile_details = Profile.objects.get(user=user)
    total_post = user.author.count()
    published_post = user.author.filter(is_published=True)
    unpublished_post = user.author.filter(is_published=False)
   
    context = {
        'user':user,
        'profile': profile_details,
        'total_post':total_post,
        'published_post': published_post,
        'unpublished_post': unpublished_post,
    }
    return render(request, "user/user_profile.html", context)
    



@login_required(login_url='user:login')
def edit_user(request):
    user = User.objects.get(username=request.user)
    form = EditUserForm(request.POST or None, instance = user)
    
    if request.method == "POST":
        #form = EditUserForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Settings changed successfully")
            return redirect('user:profile', id=request.user.id)
    
    context = {
        'form':form
    }
    return render(request, "user/edit_user.html", context)




    
@login_required(login_url='user:login')
def edit_user_profile(request):
    #user = User.objects.get(username=request.user)
    profile_details = Profile.objects.get(user=request.user)
    form = EditProfileForm(request.POST, request.FILES, instance = profile_details)
    
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance = profile_details)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect('user:profile',  id=request.user.id)
    
    context = {
        'form':form
    }
    return render(request, "user/edit_user_profile.html", context)
    
    

    
def change_password(request):
    form = PasswordChangeForm(data=request.POST or None, user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Password changed successfully")
            update_session_auth_hash(request, form.user)
            return redirect('user:profile',  id=request.user.id)
    context = {
        'form': form,
    }
    return render(request, 'user/change_password.html', context)
    
    
    
    
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "user/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("user:password_reset_done")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="user/password/password_reset.html", context={"password_reset_form":password_reset_form})