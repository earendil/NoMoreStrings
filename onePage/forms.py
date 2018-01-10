from django import forms


class CommitForm(forms.Form):

    case = forms.CharField(label="Case Number", max_length=10,
                           widget=forms.TextInput(attrs={'placeholder': '12345'}))
    message = forms.CharField(label="Commit Message", max_length=100,
                              widget=forms.TextInput(attrs={'placeholder': '(Initials) Message'}))


class StringTest(forms.Form):

    new_string = forms.CharField(label="", label_suffix="", max_length=100,
                                 widget=forms.TextInput(attrs={'placeholder': 'Enter new string:'}))
