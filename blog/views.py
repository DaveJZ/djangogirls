from django.shortcuts import render, redirect, get_object_or_404
from .models import FoodItem, Transaction

def post_list(request):
    items = FoodItem.objects.all()
    
    # Handling the Transaction FormS
    if request.method == "POST":
        item_id = request.POST.get('item')
        person = request.POST.get('person')
        amount = int(request.POST.get('amount'))
        t_type = request.POST.get('type')
        
        food_item = FoodItem.objects.get(id=item_id)
        
        # Update the stock level based on transaction type
        if t_type == 'DONATE':
            food_item.stock_level += amount
        elif t_type == 'TAKE':
            food_item.stock_level -= amount
        
        food_item.save()
        Transaction.objects.create(item=food_item, person_name=person, quantity=amount, transaction_type=t_type)
        return redirect('post_list')

    return render(request, 'blog/post_list.html', {'items': items})

def item_detail(request, pk):
    item = get_object_or_404(FoodItem, pk=pk)
    # This view allows the front-end to show history/details for one specific food item
    return render(request, 'blog/item_detail.html', {'item': item})
