from django.shortcuts import render
from onePage.models import Script
from .forms import CommitForm, StringTest

uj = None


# Create your views here.
def home_page(request):

    global uj

    if request.method == 'POST':

        if 'item_text' in request.POST:

            try:
                uj = Script(request.POST['item_text'])
                status = "Ready"
                request.session['uj_number'] = request.POST['item_text']
            except Exception as e:
                response = []
                status = str(e)
            else:
                response = uj.account_list
                if not response:
                    status = "No strings found"

            return render(request, 'index.html', {
                'items': response,
                'status': status,
                'form': StringTest()
            })

        elif 'new_string' in request.POST:

            session = request.session.get('uj_number', '')

            if session != uj.uj_number:
                uj = Script(session)

            form = StringTest(request.POST)

            if form.is_valid():

                new_string = form.cleaned_data['new_string']

                result = {}

                try:
                    old_string = uj.string_list[int(request.POST['old_string'])]
                except IndexError:
                    result['text'] = uj.status = "Please try again."
                else:
                    uj.replace_text(old_string, new_string)
                    result['text'] = old_string.replace("\"", "").replace("\'", "")
                    result['text1'] = new_string

                result['changes'] = uj.show_diff()
                result['can_commit'] = 'True'
                result['form'] = CommitForm()

                request.session['uj_text'] = uj.text

                return render(request, 'index.html', result)

        elif 'commit' in request.POST:

            session_num = request.session.get('uj_number', '')
            session_text = request.session.get('uj_text', '')

            if session_num != uj.uj_number:
                uj = Script(session_num, update=False)

            if session_text != uj.text:

                return render(request, 'index.html', {
                    'message': 'There has been an issue establishing your session, please try again',
                    'changes': 'Please report it to your technical team.',
                })

            form = CommitForm(request.POST)

            if form.is_valid():

                changes = uj.commit(form.cleaned_data['case'], form.cleaned_data['message'])

            else:

                changes = "Unable to commit due to incorrect data."

            return render(request, 'index.html', {
                'message': 'Commit output:',
                'changes': changes,
                'can_upload': 'True',
            })

        elif 'upload' in request.POST:

            session_num = request.session.get('uj_number', '')
            session_text = request.session.get('uj_text', '')

            if session_num != uj.uj_number:
                uj = Script(session_num)

            if session_text != uj.text:

                return render(request, 'index.html', {
                    'message': 'There has been an issue establishing your session, please try again',
                    'changes': 'Please report it to your technical team.',
                })

            changes = uj.upload()

            return render(request, 'index.html', {
                'message': 'Upload output:',
                'changes': changes,
            })

    return render(request, 'index.html')
