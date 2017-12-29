from django.shortcuts import render, redirect
from onePage.models import Item, Script

uj = Script()


# Create your views here.
def home_page(request):
    if request.method == 'POST':

        if 'item_text' in request.POST:

            uj.update(request.POST['item_text'])

            if uj.status != 'Ready':
                response = []
            else:
                response = uj.string_list

            return render(request, 'index.html', {
                'items': response,
                'status': uj.status,
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
