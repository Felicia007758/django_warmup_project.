from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    selected_choices = request.POST.getlist('choices')  # supports multiple selections
    if not selected_choices:
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select any choices.",
        })
    for choice_id in selected_choices:
        choice = question.choice_set.get(pk=choice_id)
        choice.votes += 1
        choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
