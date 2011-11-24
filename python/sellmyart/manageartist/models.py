#/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

from django.db import models
from django.forms import ModelForm, PasswordInput
from manageart.models import ArtModel
from django.contrib.auth.models import User
# Create your models here.

class ArtistInfo(models.Model):
    website = models.URLField(blank=True)
    avatar = models.ImageField(blank=True, upload_to='avatars/')
    bio = models.TextField(blank=True)
    authuser = models.OneToOneField(User, editable=False)
#Deal with client info later when we have invoices and whatever set up

class ArtistInfoForm(ModelForm):
    class Meta:
        model=ArtistInfo

class UserForm(ModelForm):
    class Meta:
        model=User
        fields = ('first_name','last_name','username','email','password')
        widgets = {
                    'password': PasswordInput(),}

