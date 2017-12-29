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

        elif [i for i in request.POST.keys() if i.isdigit()]:

            new_string = ""
            old_string = ""

            for k, v in request.POST.items():
                if k.isdigit():
                    new_string = v
                    old_string = uj.string_list[int(k)]

            uj.replace_text(old_string, new_string)

            return render(request, 'index.html', {
                'text': old_string.replace("\"", "") + " is now: " + new_string,
                'changes': uj.show_diff()
            })

        elif 'test' in request.POST or 'upload' in request.POST:

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
