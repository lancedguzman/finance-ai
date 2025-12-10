from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from .utils import extract_receipt_data
import json

@login_required
def scan_receipt(request):
    if request.method == 'POST' and request.FILES.get('receipt_image'):
        try:
            image = request.FILES['receipt_image']
            
            # Run the OCR utility
            data = extract_receipt_data(image)
            
            if not data['amount'] and not data['date']:
                return JsonResponse({'error': 'Could not detect clear text. Try a clearer image.'}, status=400)

            return JsonResponse({
                'message': 'Scan successful',
                'data': data
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'No image provided'}, status=400)
