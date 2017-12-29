from django.shortcuts import render, redirect
from onePage.models import Item, Script

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

        elif 'test' in request.POST:

            uj.commit()

            return render(request, 'index.html', {
                'text': 'Yes there is something',
                'changes': 'You clicked a button.'
            })

        elif 'upload' in request.POST:

            return render(request, 'index.html', {
                'text': 'Yes there is something',
                'changes': 'You clicked a button.'
            })

    return render(request, 'index.html')
