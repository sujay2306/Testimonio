from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from datetime import date
import json
from web3 import Web3, HTTPProvider

global details

def readDetails():
    global details
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'ForensicEvidenceContract.json' #forensic contract code
    deployed_contract_address = '0x30B7BE3B6E801480462e09C8cacA67D5203612ec' #hash address to access forensiccontract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    details = contract.functions.getData().call()
    if len(details) > 0:
        if 'empty' in details:
            details = details[5:len(details)]

def saveDataBlockChain(currentData):
    global details
    global contract
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'ForensicEvidenceContract.json'
    deployed_contract_address = '0x30B7BE3B6E801480462e09C8cacA67D5203612ec'
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails()
    details+=currentData
    msg = contract.functions.setEvidenceDetails(details).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(msg)

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})
def About(request):
    if request.method == 'GET':
       return render(request, 'About.html', {})
def Admin(request):
    if request.method == 'GET':
       return render(request, 'Admin.html', {})

def AddEvidence(request):
    if request.method == 'GET':
       return render(request, 'AddEvidence.html', {})

def AdminLogin(request):
    if request.method == 'POST':
      username = request.POST.get('t1', False)
      password = request.POST.get('t2', False)
      if username == 'admin' and password == 'admin':
       context= {'data':'welcome '+username}
       return render(request, 'AdminScreen.html', context)
      else:
       context= {'data':'login failed'}
       return render(request, 'Admin.html', context)

def ViewEvidence(request):
    if request.method == 'GET':
        global details
        readDetails()
        print("p det "+details)
        arr = details.split("\n")
        output = ''
        font = "<font size=3 color=black>"
        for i in range(len(arr)-1):
            array = arr[i].split("$");
            output+="<tr><td>"+font+array[0]+"</td>"
            output+="<td>"+font+array[1]+"</td>"
            output+="<td>"+font+array[2]+"</td>"
            output+="<td>"+font+array[3]+"</td>"
            output+="<td>"+font+array[4]+"</td>"
            output+="<td>"+font+array[5]+"</td>"
            output+="<td>"+font+array[6]+"</td>"
        context= {'data':output}
        return render(request, 'ViewEvidence.html', context)

def AddEvidenceAction(request):
    if request.method == 'POST':
        rid = request.POST.get('t1', False)
        crime_type = request.POST.get('t2', False)
        desc = request.POST.get('t3', False)
        evidence = request.POST.get('t4', False)
        area = request.POST.get('t5', False)
        witness = request.POST.get('t6', False)
        today = date.today()
        data = rid+"$"+crime_type+"$"+desc+"$"+evidence+"$"+area+"$"+witness+"$"+str(today)+"\n"
        saveDataBlockChain(data)
        context= {'data':'Evidence details saved in Blockchain'}
        return render(request, 'AddEvidence.html', context)
