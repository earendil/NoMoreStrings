from django import forms


class CommitForm(forms.Form):

    case = forms.CharField(label="Case Number", max_length=10)
    message = forms.CharField(label="Commit Message", max_length=100)
