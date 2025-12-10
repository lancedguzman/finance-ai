from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Category, Transaction
from .forms import TransactionForm
import json

@login_required(login_url='user_management:login')
def transaction_list(request):
    """View all transactions as JSON for Vue frontend."""
    # Get all transactions, newest first
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    
    data = []
    for t in transactions:
        data.append({
            'id': t.transaction_id,
            'date': t.date,
            'name': t.name,
            'amount': float(t.amount),
            'category': t.category.name,
            'type': t.category.type, 
        })
        
    return JsonResponse(data, safe=False)


@login_required(login_url='user_management:login')
def add_transaction(request):
    """View to add a new transaction via JSON from Vue frontend."""
    if request.method == 'POST':
        try:
            # Parse the JSON data sent from Vue
            data = json.loads(request.body)
            
            # Use the Django Form to validate input
            form = TransactionForm(data)
            
            if form.is_valid():
                # Save to database
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                return JsonResponse({
                    'message': 'Success', 
                    'id': transaction.transaction_id
                })
            else:
                # Return validation errors (e.g., "Date is invalid")
                return JsonResponse({'errors': form.errors}, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'error': 'Invalid method'}, status=405)


@login_required(login_url='user_management:login')
def delete_transaction(request, id):
    """View to delete a transaction by ID via JSON from Vue frontend."""
    if request.method == 'DELETE':
        try:
            # Note: Your model uses 'transaction_id' as the primary key
            transaction = Transaction.objects.get(transaction_id=id, user=request.user)
            transaction.delete()
            return JsonResponse({'message': 'Deleted successfully'})
        except Transaction.DoesNotExist:
            return JsonResponse({'error': 'Transaction not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid method'}, status=405)


@ensure_csrf_cookie
@login_required(login_url='user_management:login') 
def index(request):
    """View to render the main tracker page with categories."""
    # Pass categories to the frontend so Vue can list them in the dropdown
    categories = Category.objects.filter(user=request.user)
    cat_list = list(categories.values('id', 'name', 'type'))

    context = {
        'categories': cat_list
    }

    return render(request, 'index.html', context)
