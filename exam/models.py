from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


# Create your models here.

class Exam(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(default='', editable=False, max_length=200, null=False)
    instructor = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    numQuestion = models.IntegerField(verbose_name="Number of questions:")
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + '-' + str(self.id))  # generates unique url
        super(Exam, self).save(*args, **kwargs)

class Question(models.Model):
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)
    question = models.TextField()
    question_num = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.question}"

    def get_answers(self):
        choices = []
        answers = self.answers.all()
        for a in answers:
            choices.append(a.answer)
        return choices

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    answer = models.TextField()
    isCorrect = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.answer}"

    class Meta:
        order_with_respect_to = 'question'


class Score(models.Model):
    exam = models.ManyToManyField(Exam, related_name="exam_scores")
    student = models.ManyToManyField(User, related_name="student_scores")
    correct = models.IntegerField()
    incorrect = models.IntegerField()

    def __str__(self):
        return f"Correct: {self.correct}, Incorrect:{self.incorrect}"
