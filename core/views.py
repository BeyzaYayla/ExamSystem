from django.shortcuts import render

# Create your views here.

from exam.models import Exam

#shows the frontpage
def frontpage(request):
    exam_list = Exam.objects.all()
    return render(request, 'core/frontpage.html', {'exam_list': exam_list})
