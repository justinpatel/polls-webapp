from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import Question, Choice
from django.utils import timezone

from django.contrib import messages

# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')

    return render(request, 'polls/index.html', {
        "latest_question_list": latest_question_list
    })

def detail(request, question_id):
    q = get_object_or_404(Question ,pk=question_id)
    return render(request, 'polls/detail.html', {
        "question": q
    })

def results(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {
        'q':q
    })

def vote(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = q.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html",{
            "question":q,
            "msg":"You didnt select any choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        print(q.id)
        return HttpResponseRedirect(reverse("results", args=(q.id,)))

def makepoll(request):
    if request.method == "POST":
        q_text = request.POST['q_text']
        choices = request.POST['choices']
        if q_text and choices:
            choices_list = choices.split(',')
            q = Question.objects.create(question_text=q_text, pub_date= timezone.now())
            for choice in choices_list:
                Choice.objects.create(question=q, choice_text=choice)
            messages.success(request, "Successfully added")
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'polls/makepoll.html',{
                "q_text": "Please fill up"
            })
    return render(request, 'polls/makepoll.html',{
        "q_text": "Please fill up"
    })