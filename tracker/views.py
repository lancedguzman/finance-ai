from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.shortcuts import render
from .models import Category, Transaction
from .forms import TransactionForm
import json

def transaction_list(request):
    # Get all transactions, newest first
    transactions = Transaction.objects.select_related('category').all().order_by('-date')
    
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


def add_transaction(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data sent from Vue
            data = json.loads(request.body)
            
            # Use the Django Form to validate input
            form = TransactionForm(data)
            
            if form.is_valid():
                # Save to database
                transaction = form.save()
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


def delete_transaction(request, id):
    if request.method == 'DELETE':
        try:
            # Note: Your model uses 'transaction_id' as the primary key
            transaction = Transaction.objects.get(transaction_id=id)
            transaction.delete()
            return JsonResponse({'message': 'Deleted successfully'})
        except Transaction.DoesNotExist:
            return JsonResponse({'error': 'Transaction not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid method'}, status=405)


@ensure_csrf_cookie 
def index(request):
    # Pass categories to the frontend so Vue can list them in the dropdown
    categories = list(Category.objects.values('id', 'name', 'type'))
    return render(request, 'index.html', {'categories': categories})
