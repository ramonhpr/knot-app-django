# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.forms import Form, CharField, IntegerField, ChoiceField, UUIDField
from django.forms.models import model_to_dict

from models import Credentials

from knotpy import *

# Create your views here.

mapCloud = {'1': 'meshblu', '2':'fiware'}

class KnotForm(Form):
    cloud = ChoiceField(choices=((1,'Meshblu'), (2,'Fiware')))
    servername = CharField(label='Hostname', max_length=100)
    port = IntegerField(max_value=0xffff)
    uuid = UUIDField()
    token = CharField(label='Token', max_length=100)

class Knot(View):
    def get(self, request):
        try:
            form = model_to_dict(Credentials.objects.all()[0])
        except:
            form={'servername':'', 'port':'', 'uuid':'', 'token':''}
        return render(request, 'index.html', {'form': KnotForm(form)})

    def post(self, request):
        form = request.POST
        if len(Credentials.objects.all()) > 0:
            Credentials.objects.all()[0].delete()
        print(form)
        cred = Credentials(servername=form.get('servername'), port=form.get('port'),
        uuid=form.get('uuid'), token=form.get('token'), cloud=form.get('cloud'))
        cred.save()
        return render(request, 'index.html', {'form': KnotForm(form)})

class Devices(View):
    def get(self, request):
        cred = model_to_dict(Credentials.objects.all()[0])
        conn = KnotConnection({'servername': cred.get('servername'), 'port':
        cred.get('port'), 'uuid': str(cred.get('uuid')), 'token': cred.get('token')}, protocol='http', cloud=mapCloud[cred.get('cloud')])
        devs = conn.getDevices()
        dev_ids = [dev.get('id') for dev in devs]
        return render(request, 'index.html', { 'devices': devs })

class Sensors(View):
    def get(self, request):
        cred = model_to_dict(Credentials.objects.all()[0])
        conn = KnotConnection({'servername': cred.get('servername'), 'port':
        cred.get('port'), 'uuid': str(cred.get('uuid')), 'token': cred.get('token')}, protocol='http', cloud=mapCloud[cred.get('cloud')])
        sensors = [conn.getSensorDetails(request.GET.get('id'), i) for i in conn.listSensors(request.GET.get('id'))]
        for sensor in sensors:
            try:
                sensor.update({'data':conn.getData(request.GET.get('id'), limit=1)[0]})
            except Exception:
                pass
        print(sensors)
        return render(request, 'index.html', {'sensors': sensors})
