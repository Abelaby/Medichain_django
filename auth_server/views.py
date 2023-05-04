from django.shortcuts import render,get_object_or_404

from django.utils import timezone
from chain.models import Token
from django.http import HttpResponse, Http404
import os
from django.conf import settings
import mimetypes
import os
from django.conf import settings
from django.http import HttpResponse, Http404


def token_detail(request):
    if request.method == 'POST':
        token_number = request.POST['token_number']
        expiry_date = request.POST['expiry_date']
        try:
            token = Token.objects.get(token=token_number, expiry_date=expiry_date)
            token_valid = True
        except Token.DoesNotExist:
            token_valid = False
            token = None
        context = {
            'token': token,
            'token_valid': token_valid,
            'error': 'Invalid token or expiry date. Please try again.' if not token_valid else None
        }
        return render(request, 'auth_server/verify.html', context)
    else:
        return render(request, 'auth_server/verify.html')



def download_file(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/octet-stream")
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response


