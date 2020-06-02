from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.core.cache import cache 

import time
import datetime
from datetime import timezone

import random
import string

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def index(request):    
    while True:
        alias = randomString()
        if cache.get('c-' + alias) is None:
            break
    return render(request, 'index.html', {'alias': alias })
       

@csrf_exempt
def send(request):
    # print(request.POST)
    d = request.POST.get("d", "")
    alias = request.POST.get("a", "")
    room = request.POST.get("r", "")
    
    # save info about this frame 
    cache.set('c-' + alias, d) 
    dt = datetime.datetime.now()
    timestamp = int(dt.replace(tzinfo=timezone.utc).timestamp())
    cache.set('l-' + alias, timestamp)
    o_dic = cache.get('r-' + room)
    if o_dic is None:
        o_dic = {}
        
    dic = {}
    res = {}
    
    # get other webcams frame
    for o_a in o_dic.keys(): 
        if a == o_a:
            pass
            #continue
        last_seen = int(cache.get('l-' + o_a))
        if timestamp - last_seen > 3:
            dic.pop(o_a, None)
            continue
        
        dic[o_a] = 1
        res[o_a] = cache.get('c-' + o_a)
    
    dic[a] = 1
    cache.set('r-' + room, dic)

    return JsonResponse(res)
