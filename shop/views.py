from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.db import transaction

from .models import Product, Purchase

def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)

class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['product', 'person', 'address']

    def form_valid(self, form):
        self.object = form.save()

        self.dec_for_db(self.object.product)
        
        return redirect('index')

    @staticmethod
    def dec_for_db(product):
        product.count -= 1
        product.save()






