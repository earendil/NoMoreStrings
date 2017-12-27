from django.shortcuts import render, redirect
from onePage.models import Item, Script


# Create your views here.
def home_page(request):

    if request.method == 'POST':

        uj = Script(request.POST['item_text'])
        uj.get_source()
        # print(uj.input)
        # print(uj.text)

        # Item.objects.create(text=request.POST['item_text'])
        # return redirect('/')

        return render(request, 'index.html', {
            'items': uj.get_strings(),
        })

    # items = Item.objects.all()

    return render(request, 'index.html')
