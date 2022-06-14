from django.shortcuts import render
from django.http import JsonResponse
from .models import SbrCurrentsessions
from django.core.cache import cache

import logging
logger = logging.getLogger(__name__)

# default cache time for the APIs
LIST_CACHE_TIMEOUT = 60

# Create your views here.


def get_msisdn(request, ip):
    # return HttpResponseRedirect(reverse('all-borrowed'))
    # change ip from str to int
    temp = ip.split(".")
    if len(temp) != 4:
        return JsonResponse({'api': 'get-msisdn', 'rc': -1, 'error': 'input not an ipv4 address'})
    try:
        int_ip = int(temp[0]) * 16777216 + int(temp[1]) * \
            65536 + int(temp[2]) * 256 + int(temp[3])
    except Exception as e:
        return JsonResponse({'api': 'get-msisdn', 'rc': -1, 'error': 'input not an ipv4 address', 'exception_class': str(e.__class__.__name__),  'exception': str(e)})
    theresult = cache.get('get-msisdn ip=%s' % int_ip)
    if not theresult:
        try:
            theresult = SbrCurrentsessions.objects.get(sbr_ipv4address=int_ip)
        except Exception as e:
            return JsonResponse({'api': 'get-msisdn', 'rc': 1, 'error': 'object not found', 'exception_class': str(e.__class__.__name__), 'exception': str(e)})
        cache.set('get-msisdn ip=%s' % int_ip, theresult, LIST_CACHE_TIMEOUT)
    return JsonResponse({'api': 'get-msisdn', 'rc': 0, 'msisdn': theresult.sbr_username})


def get_ip(request, msisdn):
    # return HttpResponseRedirect(reverse('all-borrowed'))
    # change ip from string to int
    try:
        int(msisdn)
    except Exception as e:
        return JsonResponse({'api': 'get-ip', 'rc': -1, 'error': 'input not msisdn', 'exception_class': str(e.__class__.__name__), 'exception': str(e)})
    theresult = cache.get('get-ip msisdn=%s' % msisdn)
    if not theresult:
        try:
            theresult = SbrCurrentsessions.objects.get(sbr_username=msisdn)
        except Exception as e:
            return JsonResponse({'api': 'get-ip', 'rc': 1, 'error': 'object not found', 'exception_class': str(e.__class__.__name__), 'exception': str(e)})
        cache.set('get-ip msisdn=%s' % msisdn, theresult, LIST_CACHE_TIMEOUT)
    # change int ip to str
    int_ip = theresult.sbr_ipv4address
    ip = str(int_ip//16777216) + "." + str(int_ip % 16777216//65536) + "." + \
        str(int_ip % 16777216 % 65536//256) + "." + \
        str(int_ip % 16777216 % 65536 % 256)
    return JsonResponse({'api': 'get-ip', 'rc': 0, 'ip': ip})

from django.core.checks.database import check_database_backends

def healthcheck(request):
    """ app healthcheck example """

    theout = {'api': 'healthcheck', 'rc': 0}
    theout['is_health'] = True

    databases = ['aaa-1', 'aaa-2']
    theout['database'] = {}
    for db in databases:
        theout['database'][db] = {}
        try:
            checkresult = check_database_backends([db])
            if not checkresult:
               theout['database'][db]['is_health'] = True
            else:
                theout['database'][db]['is_health'] = False
                theout['database'][db]['error'] = checkresult
                theout['is_health'] = False
        except Exception as e:
            theout['database'][db]['is_health'] = False
            theout['database'][db]['exception'] = {}
            theout['database'][db]['exception']['class'] = str(e.__class__.__name__)
            theout['database'][db]['exception']['desc'] = str(e)
            theout['is_health'] = False

    return JsonResponse(theout)
