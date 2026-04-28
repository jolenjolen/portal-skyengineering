from django.shortcuts import render, redirect, get_object_or_404
from core.models import TblUser
from .models import Message

def get_current_user(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    try:
        return TblUser.objects.get(id=user_id)
    except TblUser.DoesNotExist:
        return None

def inbox(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    messages = Message.objects.filter(recipient=user, status='sent').order_by('-created_at')
    return render(request, 'messaging/inbox.html', {'messages': messages})

def sent(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    messages = Message.objects.filter(sender=user, status='sent').order_by('-created_at')
    return render(request, 'messaging/sent.html', {'messages': messages})

def drafts(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    messages = Message.objects.filter(sender=user, status='draft').order_by('-created_at')
    return render(request, 'messaging/drafts.html', {'messages': messages})

def new_message(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    users = TblUser.objects.exclude(id=user.id)
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        action = request.POST.get('action')
        recipient = TblUser.objects.get(id=recipient_id)
        status = 'sent' if action == 'send' else 'draft'
        Message.objects.create(
            sender=user,
            recipient=recipient,
            subject=subject,
            body=body,
            status=status
        )
        return redirect('inbox') if status == 'sent' else redirect('drafts')
    return render(request, 'messaging/new_message.html', {'users': users})

def view_message(request, pk):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    message = get_object_or_404(Message, id=pk)
    if not message.is_read and message.recipient == user:
        message.is_read = True
        message.save()
    return render(request, 'messaging/view_message.html', {'message': message})