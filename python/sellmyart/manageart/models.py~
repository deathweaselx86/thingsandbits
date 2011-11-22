#/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User


class ArtModel(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=200)
    artist_id = models.ManyToManyField(User)
    date_modified = models.DateTimeField(auto_now_add=True)
    number_repros = models.IntegerField()
    repros_sold = models.IntegerField(default=0)
    original_available = models.BooleanField(default=False)
    media = models.CharField(max_length=400, default="Graphite")

    def __unicode__(self):
        return ' '.join((self.title, self.media))

class ArtModelForm(ModelForm):
    class Meta:
        model = ArtModel
