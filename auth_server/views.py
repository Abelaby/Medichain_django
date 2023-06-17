from django.shortcuts import render

from django.utils import timezone
from chain.models import Token
from django.http import HttpResponse
import os
from django.conf import settings
import os
from chain.views import contract



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

        if token_valid:
            # Fetch the token using the getToken function of the contract instance
            signature = token.signature
            receiver = token.receiver
            fetched_token = contract.functions.getToken(signature, receiver)

            # Perform verification logic with the fetched_token
            
            # Add the verification result to the context dictionary
            context = {
                'token': token,
                'token_valid': token_valid,
                'fetched_token': fetched_token,
                'error': None
            }
        else:
            context = {
                'token': token,
                'token_valid': token_valid,
                'fetched_token': None,
                'error': 'Invalid token or expiry date. Please try again.'
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


