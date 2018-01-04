from django.shortcuts import render
from onePage.models import Script

# Make sure each connection has it's own object
uj = None


# Create your views here.
def home_page(request):

    if request.method == 'POST':

        if 'item_text' in request.POST:

            global uj

            try:
                uj = Script(request.POST['item_text'])
                status = "Ready"
            except Exception as e:
                response = []
                status = str(e)
            else:
                response = uj.string_list
                if not response:
                    status = "No strings found"

            return render(request, 'index.html', {
                'items': response,
                'status': status,
            })

        elif 'new_string' in request.POST:
            new_string = request.POST['new_string']
            result = {}

            try:
                old_string = uj.string_list[int(request.POST['old_string'])]
            except IndexError:
                result['text'] = uj.status = "Please try again."
            else:
                uj.replace_text(old_string, new_string)
                result['text'] = old_string.replace("\"", "") + " is now: " + new_string

            result['changes'] = uj.show_diff()
            return render(request, 'index.html', result)

        elif 'commit' in request.POST:

            changes = uj.commit(request.POST['case_number'], request.POST['message'])

            return render(request, 'index.html', {
                'text': 'Commit output:',
                'changes': changes,
            })

        elif 'upload' in request.POST:

            changes = uj.upload()

            return render(request, 'index.html', {
                'text': 'Upload output:',
                'changes': changes,
            })

    return render(request, 'index.html')
