from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import RequestForm, TokenForm
from .models import Request, Token
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from parties.models import User
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views import View
import random
# web3 imports
import json
from web3 import Web3

PUBLIC_KEY = "0xE71115Ed8904541C08DeCB032877e2D85f527e61"
PRIVATE_KEY = "ad601d0aee9345d7c1891c2b722f6c1bec9fbc51ddc4a646daa83566eb7da427"

URL = "HTTP://127.0.0.1:8545"

web3 = Web3(Web3.HTTPProvider(URL))

address = Web3.toChecksumAddress("0xd8D2Af9EDB2186CDce2d7371bEabC9298043C97d")

contract_abi = """[
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "string",
				"name": "signature",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "receiver",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "token",
				"type": "string"
			}
		],
		"name": "NewToken",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "signature",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "receiver",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "token",
				"type": "string"
			}
		],
		"name": "saveToken",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "signature",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "receiver",
				"type": "string"
			}
		],
		"name": "getToken",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "signToToken",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "tokens",
		"outputs": [
			{
				"internalType": "string",
				"name": "signature",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "receiver",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "token",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "tokenToOwner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]"""
abi = json.loads(contract_abi)


contract = web3.eth.contract(address=address, abi=abi)

web3.eth.defaultAccount = web3.eth.accounts[0]


def SaveToken(signature, receiver, token):
    # Send a transaction to save a new token
    tx_hash = contract.functions.saveToken(signature, receiver, token).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)

    print("Transaction confirmed!")


def GetToken(signature, receiver):
    # Call the getToken function
    result = contract.functions.getToken(signature, receiver).call()
    print(result)


def request_form(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chain:request_sent')
    else:
        form = RequestForm()
    return render(request, "chain/request_form.html", {"form": form})


def request_list(request):
    # Retrieve all the requests that match the Ds_name of the logged-in user
    requests = Request.objects.filter(Ds_name=request.user.username)

    context = {
        'requests': requests
    }

    return render(request, 'chain/request_list.html', context)

'''class RequestDetailView(View):
    def get(self, request, pk):
        # get the request object based on the pk
        request_obj = get_object_or_404(Request, pk=pk)
        
        # get the next and previous requests
        next_request = Request.objects.filter(pk__gt=pk, Ds_name=request_obj.Ds_name).order_by('pk').first()
        prev_request = Request.objects.filter(pk__lt=pk, Ds_name=request_obj.Ds_name).order_by('-pk').first()

        context = {
            'request': request_obj,
            'next_request': next_request,
            'prev_request': prev_request,
        }
        return render(request, 'chain/request_detail.html', context)'''

def create_token(request):
    if request.method == 'POST':
        form = TokenForm(request.POST)
        if form.is_valid():
            # Create a new Token object from the form data
            signature = form.cleaned_data['signature']
            receiver = form.cleaned_data['receiver']
            token = str(random.randint(0, 9999))
            expiry_date = form.cleaned_data['expiry_date_choice']
            user = User.objects.get(username=receiver)
            email = user.email
            token_obj = Token(signature=signature, receiver=receiver, token=token, expiry_date=expiry_date)
            token_obj.save()
            

            # Send a transaction to save a new token
            tx_hash = contract.functions.saveToken(signature, receiver, token).transact()
            web3.eth.waitForTransactionReceipt(tx_hash)
            
			
            print("Transaction confirmed!")
            send_mail('Token is created', str(token_obj), 'settings.EMAIL_HOST_USER', [email])
            return redirect('chain:token_created')
    else:
        form = TokenForm()

    return render(request, 'chain/create_token.html', {'form': form})

def token_list(request):
    tokens = Token.objects.all()

    context = {
        'tokens': tokens
    }

    return render(request, 'chain/token_list.html', context)

def token_created(request):
    return render(request, 'chain/token_created.html')

def request_sent(request):
    return render(request, 'chain/request_sent.html')


        