from django import forms

class QuestionForm(forms.Form):
    id=forms.IntegerField()
    question=forms.CharField(required=True,max_length=100)
    answer=forms.BooleanField(required=False)
    comment=forms.CharField(required=True,max_length=100)

class DeleteForm(forms.Form):
    id=forms.IntegerField()

