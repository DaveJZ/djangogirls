from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import FoodItem, Transaction

def post_list(request):
    items = FoodItem.objects.all()
    
    #Handling the Transaction FormS
    if request.method == "POST":
        item_id = request.POST.get('item', '').strip()
        person = request.POST.get('person', '').strip()
        amount_str = request.POST.get('amount', '').strip()
        t_type = request.POST.get('type')
        
        #Check for missing required inputs
        if not all([item_id, person, amount_str, t_type]):
            messages.error(request, "Please enter info in all boxes. Please check your input.")
            return redirect('post_list')

        #Type validation and range checking
        try:
            amount = int(amount_str)
            if amount <= 0:
                messages.error(request, "Quantity must be a positive number.")
                return redirect('post_list')
        except ValueError:
            messages.error(request, "Invalid amount. Please enter a whole number.")
            return redirect('post_list')

        # Retrieve object check
        food_item = get_object_or_404(FoodItem, id=item_id)
        
        # Update the stock level based on transaction type
        if t_type == 'DONATE':
            food_item.stock_level += amount
        elif t_type == 'TAKE':
            if food_item.stock_level < amount:
                messages.error(request, f"Not enough {food_item.name} in stock!")
                return redirect('post_list')
            food_item.stock_level -= amount
            
        # Final check for valid transaction type and save
        if t_type in ['DONATE', 'TAKE']:
            food_item.save()
            Transaction.objects.create(item=food_item, person_name=person, quantity=amount, transaction_type=t_type)
            messages.success(request, f"Stock updated for {food_item.name}.")
        else:
            messages.error(request, "Invalid transaction type.")
            
        return redirect('post_list')

    return render(request, 'blog/post_list.html', {'items': items})

def item_detail(request, pk):
    item = get_object_or_404(FoodItem, pk=pk)
    # This view allows the front end to show history/details for one specific food item
    return render(request, 'blog/item_detail.html', {'item': item})