#/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

# Create your views here.
from django.http import HttpResponse
from register.models import ArtistInfo, ArtistInfoForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
def index(request):
    """
        This is the basic artist registration page.
        The only things that are really required right now are 
        the username, password, and email.
    """
    errors = '' 
    if request.method == 'POST':
        data = request.POST
        form1 = UserCreationForm(data)
        form2 = ArtistInfoForm(data)
        if form1.is_valid():
            new_user = User(username=data['username'], password=data['password1'])
            new_user.save()
            artist_info = ArtistInfo(bio=data['bio'],website=data['website'], \
                                    birthday=data['birthday'], avatar=data['avatar'], authuser=new_user)
            artist_info.save()
            return HttpResponseRedirect('/manageart/')
        else:
            errors = []
            for form in (form1, form2):
                for k in form.errors:
                    errors.append(form.errors[k])
    form1 = UserCreationForm()
    form2 = ArtistInfoForm()
    context = {'body': '', 'form1': form1, 'form2': form2, 'subtitle': 'User Registration', 'errors':errors}
    return render_to_response('../templates/register.html',\
            context_instance=RequestContext(request, context))



