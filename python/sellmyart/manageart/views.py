#/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

# Create your views here.
from django.http import HttpResponse
from manageart.models import ArtModel, ArtModelForm
from django.shortcuts import render_to_response
from django.template import RequestContext

def add_models(request):
    errors = ''
    if request.method == 'POST':
        form = ArtModelForm(request.POST)
        if form.is_valid():
            new_art = form.save()
    context = {'form':form, } # data goes here, eventually
    return render_to_response('../templates/addartmodels.html', \
            context_instance=RequestContext(request, context))
