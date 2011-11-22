#/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

# Create your views here.
from django.http import HttpResponse
from manageart.models import ArtModel
from django.shortcuts import render_to_response

def index(request):
    allArtModels = ArtModel.objects.all()[0]
    template = loader.get_template('../templates/base_generic.html')
    context = Context({'body': allArtModels,})
    return render_to_response('../templates/base_generic.html', \
                              'body': allArtModels,})
