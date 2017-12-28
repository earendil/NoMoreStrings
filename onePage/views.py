from django.shortcuts import render, redirect
from onePage.models import Item, Script


# Create your views here.
def home_page(request):

    if request.method == 'POST':

        if 'item_text' in request.POST:

            uj = Script(request.POST['item_text'])
            # uj.update_path()
            uj.get_source()
            uj_source = uj.get_source()
            string_list = uj.get_strings()
            print(uj.uj)
            print(string_list)
            return render(request, 'index.html', {
                'items': string_list,
            })

        elif [i for i in request.POST.keys() if i.isdigit()]:

            uj2 = Script('7979')
            uj2.get_source()
            string_list = uj2.get_strings()

            new_string = ""
            old_string = ""

            for k, v in request.POST.items():
                if k.isdigit():
                    new_string = v
                    old_string = string_list[int(k) - 1]

            uj2.text = uj2.text.replace(old_string, f'"{new_string}"')

            uj2.set_source()

            return render(request, 'index.html', {
                'text': old_string + " is now: " + new_string,
                'items': string_list,
                'script': uj2.text
            })

    return render(request, 'index.html')
