from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.db import IntegrityError
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


@login_required(login_url='user_management:login')
def add_category(request):
    """View to add a new category via JSON."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            cat_type = data.get('type')

            if not name or not cat_type:
                return JsonResponse({'error': 'Name and Type are required'}, status=400)

            # Create the category linked to the user
            category = Category.objects.create(
                user=request.user,
                name=name,
                type=cat_type
            )
            
            # Return the new category data so Vue can update the list immediately
            return JsonResponse({
                'message': 'Success',
                'category': {
                    'id': category.id,
                    'name': category.name,
                    'type': category.type
                }
            })
        except IntegrityError:
            return JsonResponse({'error': 'Category with this name already exists.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
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
