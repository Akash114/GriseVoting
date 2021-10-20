import json
import os

from django.http import JsonResponse, Http404
from web3 import Web3
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Question, Choice,UserInfo
from pathlib import Path


def voting(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request,'voting.html',context)


def verification(request):
    if request.is_ajax():
        data=json.loads(request.body.decode('UTF-8'))
        request.session['address'] = data['address']
        balanc = balance(data['address'])
        return HttpResponse(json.dumps({'balance': balanc}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'msg': 'request type is not allowed !!'}), content_type="application/json")


def balance(add):
    script_location = Path(__file__).absolute().parent
    file_location = script_location / 'GriseToken.json'
    file = open(file_location,encoding='utf-8')
    w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org:443'))

    currentAbis = json.loads(file.read())

    # print(currentAbis)
    address1 = '0xb359e4290573a3974616b7c26ea86939689b9ec4'

    address = w3.toChecksumAddress(address1)
    contract = w3.eth.contract(address=address, abi=currentAbis['abi'])

    token_balance = contract.functions.balanceOf(w3.toChecksumAddress(add[0])).call()
    print(token_balance)
    return token_balance


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'details.html', {'question': question})


# Get question and display results


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', {'question': question})

# Vote for a question choice


def vote(request, question_id):
    # print(request.POST['choice'])
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'details.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        address = request.session.get('address')
        Userinfo = UserInfo()
        Userinfo.question = question
        Userinfo.selected_choice = selected_choice
        Userinfo.address = address
        Userinfo.balance = balance(address)
        Userinfo.save()
        return HttpResponseRedirect(reverse('results', args=(question.id,)))
