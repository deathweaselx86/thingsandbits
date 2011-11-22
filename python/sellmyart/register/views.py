#/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from register.models import ArtistInfo, ArtistInfoForm, UserForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

def add_artist(request):
    """
        This is the basic artist registration page.
        The only things that are really required right now are 
        the username and password. Will flesh this out more later.
    """
    errors = '' 
    if request.method == 'POST':
        data = request.POST
        form1 = UserForm(data)
        form2 = ArtistInfoForm(data)
        if form1.is_valid():
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
    form1 = UserForm()
    form2 = ArtistInfoForm()
    context = {'body': '', 'form1': form1, 'form2': form2, 'subtitle': 'User Registration', 'errors':errors}
    return render_to_response('../templates/register.html',\
            context_instance=RequestContext(request, context))

def mod_artistinfo(request):
    """
        This will allow you to modify a particular user's artist info, but not their username or password.
    """
    pass
        

