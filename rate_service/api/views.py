from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

import json
import joblib
import pandas as pd
import os

from api.models import Event
from api.serializers import EventSerializer



BEST_RATE_MODAL_FILE = os.path.join(settings.BASE_DIR, 'data','best_room_rate_predictor.joblib')

BEST_RATE_MODEL =  joblib.load(BEST_RATE_MODAL_FILE)

# Create your views here.
@csrf_exempt
def event_list(request):
    events = Event.objects.all()
    event_list = []
    for event in events:
        event_list.append({
            'event_name': event.event_name,
            'event_code': event.event_code,
            'event_type_name': event.event_type_name,
            'event_type_code': event.event_type_code,
            'event_demography': event.event_demography,
            'event_demography_code': event.event_demography_code,
            'event_show_time_code': event.show_time_code,
        })
    return JsonResponse({'events':event_list})

@csrf_exempt
@api_view(http_method_names=["POST"])
def event_create(request):
    serializer = EventSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)


@csrf_exempt
@api_view(http_method_names=["POST"])
def get_best_room_rates(request):
    jdata = json.loads(request.body)
    df = pd.DataFrame([jdata])
    room_rate = BEST_RATE_MODEL.predict(df)
    jdata['optimum_rate'] = str(round(room_rate[0],2))
    return Response(jdata, status=200)
