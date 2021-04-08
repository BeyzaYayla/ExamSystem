from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateExamForm, CreateQuestionForm
from userprofile.decorators import allowed_users
from django.urls import reverse
from .serializers import QuestionSerializer
from django.utils import timezone

# Create your views here.
from .models import Exam, Question, Answer, Score


# creates an exam object with the inputs from form
@login_required
@allowed_users(allowed_roles=['instructor'])
def create_exam(request):
    if request.method == 'POST':
        form = CreateExamForm(request.POST)

        if form.is_valid():
            exam = form.save()
            exam.instructor = request.user
            exam.save()
            return HttpResponseRedirect(reverse('exam:create_question', args=(exam.id, 1,)))
    else:
        form = CreateExamForm()

    return render(request, 'exam/create_exam.html', {'form': form})


# creates question and answer objects with the inputs from form
@login_required
@allowed_users(allowed_roles=['instructor'])
def create_question(request, exam_id, question_num):
    exam = Exam.objects.get(pk=exam_id)

    if request.method == 'POST':
        form = CreateQuestionForm(request.POST)

        if form.is_valid():
            question_text = form.cleaned_data['question_text']

            choice1 = form.cleaned_data["choice1_text"]
            choice1_correctness = form.cleaned_data["choice1_correctness"]

            choice2 = form.cleaned_data["choice2_text"]
            choice2_correctness = form.cleaned_data["choice2_correctness"]

            choice3 = form.cleaned_data["choice3_text"]
            choice3_correctness = form.cleaned_data["choice3_correctness"]

            choice4 = form.cleaned_data["choice4_text"]
            choice4_correctness = form.cleaned_data["choice4_correctness"]

            # creates question in quiz
            question = Question(exam=exam, question=question_text, question_num=question_num)
            question.save()

            # creates answers for questions
            question.answers.create(answer=choice1, isCorrect=choice1_correctness)
            question.answers.create(answer=choice2, isCorrect=choice2_correctness)
            question.answers.create(answer=choice3, isCorrect=choice3_correctness)
            question.answers.create(answer=choice4, isCorrect=choice4_correctness)

            if question_num == exam.numQuestion:
                return redirect('myaccount')
            else:
                return HttpResponseRedirect(reverse('exam:create_question', args=(exam_id, question_num + 1,)))
    else:
        form = CreateQuestionForm()

    if question_num == exam.numQuestion:
        next_submit = "Submit"
    else:
        next_submit = "Next"

    context = {
        'form': form,
        'question_num': question_num,
        'next_submit': next_submit,

    }
    return render(request, 'exam/create_questions.html', context)

# this func shows all questions and answers of the given exam slug with serializers
@login_required
@allowed_users(allowed_roles=['student'])
def take_exam(request, slug):
    exam = get_object_or_404(Exam, slug=slug)
    if Score.objects.filter(student=request.user, exam=exam).exists():
        return HttpResponse('You already took this exam!')
    else:
        if exam.startDate > timezone.now():
            return HttpResponse('Exam have not started yet!')
        elif timezone.now() > exam.endDate:
            return HttpResponse('Exam already finished!')
        else:
            questions = Question.objects.filter(exam=exam)

            serializer = QuestionSerializer(questions, many=True)

            return render(request, 'exam/take_exam.html', {'data': serializer.data, 'exam': exam})


# shows student the result of the exam he just took
@login_required
def result(request, slug):
    correct = 0
    incorrect = 0

    answers = dict(request.POST)
    answers.pop("csrfmiddlewaretoken")

    exam = get_object_or_404(Exam, slug=slug)
    exam.save()

    user = request.user
    user.save()

    for key, value in answers.items():
        if Answer.objects.get(pk=value[0]).isCorrect:
            correct += 1
        else:
            incorrect += 1
    s = Score(correct=correct, incorrect=incorrect)
    s.save()
    s.exam.add(exam)
    s.student.add(user)
    s.save()
    return render(request, 'exam/result.html',
                  {'data': {'exam': exam, 'answers': answers, 'correct': correct, 'incorrect': incorrect}})


# shows all the students and their results that took the exam given to func
@login_required
@allowed_users(allowed_roles=['instructor'])
def scoreboard(request, slug):
    exam = get_object_or_404(Exam, slug=slug)
    scores = Score.objects.filter(exam=exam)
    context = {
        'exam': exam,
        'scores': scores,
    }

    return render(request, 'exam/scoreboard.html', context)
