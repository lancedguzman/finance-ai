import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from user_management.models import Profile
from tracker.models import Transaction, Category

def send_telegram_reply(chat_id, text):
    """Helper to send text back to Telegram"""
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending telegram message: {e}")


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        try:
            # Parse incoming JSON
            data = json.loads(request.body)
            message = data.get('message', {})
            chat_id = message.get('chat', {}).get('id')
            print(f"--- MY CHAT ID: {message.get('chat', {}).get('id')} ---")
            text = message.get('text', '').strip()

            if not text:
                return JsonResponse({'status': 'ok'})

            # Strict Format Check: "Name Amount Category"
            parts = text.split()
            
            # We expect exactly 3 parts. 
            if len(parts) != 3:
                error_msg = (
                    "⚠️ Format Error.\n"
                    "Please use: Name Amount Category\n"
                    "Example: Coffee 150 Food"
                )
                send_telegram_reply(chat_id, error_msg)
                return JsonResponse({'status': 'ok'})

            name, amount_str, category_name = parts

            # Validate Amount
            try:
                amount = float(amount_str)
            except ValueError:
                send_telegram_reply(chat_id, f"⚠️ Error: '{amount_str}' is not a valid number.")
                return JsonResponse({'status': 'ok'})

            # Get User (Default to first user/superuser for personal bot)
            # In a multi-user app, you would map chat_id to request.user
            try:
                # We look for a Profile (not UserProfile)
                profile = Profile.objects.get(telegram_chat_id=str(chat_id))
                user = profile.user
            except Profile.DoesNotExist:
                send_telegram_reply(chat_id, "⛔ Error: Telegram account not linked. Ask admin to add your Chat ID.")
                return JsonResponse({'status': 'ok'})
            # Find Category (Case Insensitive)
            # Category model has fields: user, name
            category = Category.objects.filter(user=user, name__iexact=category_name).first()
            
            if not category:
                # Optional: List available categories to help the user
                available = ", ".join([c.name for c in Category.objects.filter(user=user)])
                send_telegram_reply(chat_id, f"⚠️ Error: Category '{category_name}' not found.\nAvailable: {available}")
                return JsonResponse({'status': 'ok'})

            # Save Transaction
            # Transaction model has: user, date, name, amount, category
            Transaction.objects.create(
                user=user,
                date=timezone.now().date(), # Automatically log date
                name=name,
                amount=amount,
                category=category
            )

            # 7. Success Reply
            reply = f"✅ Saved!\nItem: {name}\nCost: ₱{amount}\nCat: {category.name}"
            send_telegram_reply(chat_id, reply)

        except Exception as e:
            print(f"Bot Error: {e}")
            
        return JsonResponse({'status': 'ok'})
    
    return JsonResponse({'status': 'error'}, status=400)
