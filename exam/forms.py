from django import forms
from django.core.exceptions import ValidationError
from .models import Exam


class CreateExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'
        exclude = ('instructor', 'slug')


class CreateQuestionForm(forms.Form):
    question_text = forms.CharField(max_length=300, label="Question Text",
                                    widget=forms.Textarea())

    choice1_text = forms.CharField(max_length=300, label="Choice 1",
                                   widget=forms.TextInput())
    choice1_correctness = forms.BooleanField(required=False,
                                             widget=forms.CheckboxInput())

    choice2_text = forms.CharField(max_length=300, label="Choice 2",
                                   widget=forms.TextInput())
    choice2_correctness = forms.BooleanField(required=False,
                                             widget=forms.CheckboxInput())

    choice3_text = forms.CharField(max_length=300, label="Choice 3",
                                   widget=forms.TextInput())
    choice3_correctness = forms.BooleanField(required=False,
                                             widget=forms.CheckboxInput())

    choice4_text = forms.CharField(max_length=300, label="Choice 4",
                                   widget=forms.TextInput())
    choice4_correctness = forms.BooleanField(required=False,
                                             widget=forms.CheckboxInput())

    # makes sure that exactly one answer is selected to be true
    def clean(self):

        choice1_answer = self.cleaned_data["choice1_correctness"]
        choice2_answer = self.cleaned_data["choice2_correctness"]
        choice3_answer = self.cleaned_data["choice3_correctness"]
        choice4_answer = self.cleaned_data["choice4_correctness"]

        answer_list = [choice1_answer, choice2_answer, choice3_answer, choice4_answer]

        true_count = 0
        for answer in answer_list:
            if answer:
                true_count += 1

        if true_count != 1:
            raise ValidationError('Must have exactly one correct answer')

        return self.cleaned_data
