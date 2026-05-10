from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import FoodItem, Transaction

def post_list(request):
    # Getting all the items from the database
    items = FoodItem.objects.all()
    
    #Handling the Transaction FormS
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        item_name = request.POST.get('item_name', '').strip()
        person = request.POST.get('person', '').strip()
        amount_str = request.POST.get('amount', '').strip()
        t_type = request.POST.get('type')
        
        # Check for missing required inputs(Person, Amount, and Type)
        if not person or not amount_str or not t_type:
            messages.error(request, "Please enter your name and the quantity.")
            return redirect('post_list')

        # Ensuring that at least an existing item is selected OR a new name is typed
        if not item_id and not item_name:
            messages.error(request, "Please select an item from the list or type a new name.")
            return redirect('post_list')

        # Type validation and range checking
        try:
            amount = int(amount_str)
            if amount <= 0:
                messages.error(request, "Quantity must be a positive number.")
                return redirect('post_list')
        except ValueError:
            messages.error(request, "Invalid amount. Please enter a whole number.")
            return redirect('post_list')

        # Decide which food item to use
        if item_id:
            # If they chose an item from the dropdown, get it by its ID
            food_item = FoodItem.objects.get(id=item_id)
        elif item_name:
            # If they typed a name instead, check if it exists or create it
            clean_name = item_name.title()
            if FoodItem.objects.filter(name=clean_name).exists():
                food_item = FoodItem.objects.get(name=clean_name)
            else:
                # If it's a 'TAKE' action, we shouldn't create a new item
                if t_type == 'TAKE':
                    messages.error(request, "You cannot 'Take' an item that doesn't exist in the inventory yet.")
                    return redirect('post_list')
                food_item = FoodItem.objects.create(name=clean_name, stock_level=0)
        else:
            return redirect('post_list')

        # Update the stock level based on input
        if t_type == 'DONATE':
            food_item.stock_level = food_item.stock_level + amount
            success_msg = f"Successfully added {amount} units to {food_item.name}."
        elif t_type == 'TAKE':
            if food_item.stock_level < amount:
                messages.error(request, f"Insufficient stock! Only {food_item.stock_level} available.")
                return redirect('post_list')
            
            food_item.stock_level = food_item.stock_level - amount
            success_msg = f"Successfully withdrew {amount} units of {food_item.name}."
        else:
            return redirect('post_list')

        # Save changes and record the transaction
        food_item.save()
        Transaction.objects.create(item=food_item, person_name=person, quantity=amount, transaction_type=t_type)
        messages.success(request, success_msg)

        return redirect('post_list')

    return render(request, 'blog/post_list.html', {'items': items})

def item_detail(request, pk):
    item = get_object_or_404(FoodItem, pk=pk)
    # This view allows the front end to show history/details for one specific food item
    return render(request, 'blog/item_detail.html', {'item': item})

def about(request):
    # A simple view for the about page
    return render(request, 'blog/about.html')

def index(request):
    # This connects the Index.html page
    # We pull the items here, so the home page can show a status update
    items = FoodItem.objects.all()
    return render(request, 'blog/Index.html', {'items': items})

def transaction_history(request):
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'blog/transaction_history.html', {'transactions': transactions})

def clear_history(request):
    if request.method == "POST":
        FoodItem.objects.all().delete()
        messages.success(request, "All inventory items and transaction history have been permanently deleted.")
    return redirect('transaction_history')