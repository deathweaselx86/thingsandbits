#/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from manageartist.models import ArtistInfo, ArtistInfoForm, UserForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm 


from django.contrib.auth import authenticate, login

def add_artist(request):
    """
        This is the basic artist registration page.
        The only things that are really required right now are 
        the username and password.

        I could use django.contrib.auth.forms.UserCreationForm, but
        that doesn't have enough info on it for me so I'm mocking
        this up.
    """
    errors = '' 
    if request.method == 'POST':
        data = request.POST
        form1 = UserForm(data)
        form2 = ArtistInfoForm(data)
        if form1.is_valid() and data['password'] == data['password2']:
            new_user = form1.save()
            artist_info = form2.save(commit=False)
            artist_info.authuser = new_user
            artist_info.save()
            return HttpResponseRedirect('/manageart/')
        else:
            errors = []
            for form in (form1, form2):
                for k in form.errors:
                    errors.append(form.errors[k])
            errors = ' '.join(errors)
    form1 = UserForm()
    form2 = ArtistInfoForm()
    context = {'body': '', 'form1': form1, 'form2': form2, 'subtitle': 'User Registration', 'errors':errors}
    return render_to_response('../templates/register.html',\
            context_instance=RequestContext(request, context))

def login_artist(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/manageart/')
        #A custom inactive login view redirect goes here.
            else:
                raise Http404()
        else:
             #A custom bad username/password view goes here.
             raise Http404()
            
    form = AuthenticationForm()
    context = {'form':form}
    return render_to_response('../templates/login.html',\
           context_instance=RequestContext(request,context))

def logout_artist(request):
    logout(request)
    return HttpResponseRedirect('/')

def mod_artistinfo(request):
    """
        This will allow you to modify a particular user's artist info, but not their username or password.
    """
    pass
        

