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


BEST_RATE_MODAL_FILE = os.path.join(
    settings.BASE_DIR, 'data', 'best_room_rate_predictor.joblib')

BEST_RATE_MODEL = joblib.load(BEST_RATE_MODAL_FILE)

# Create your views here.


@csrf_exempt
@api_view(http_method_names=["POST"])
def get_best_room_rates(request):
    jdata = json.loads(request.body)
    df = pd.DataFrame([jdata])
    room_rate = BEST_RATE_MODEL.predict(df)
    jdata['optimum_rate'] = str(round(room_rate[0], 2))
    return Response(jdata, status=200)
