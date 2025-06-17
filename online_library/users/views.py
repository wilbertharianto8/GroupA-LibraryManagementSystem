from django.http import request, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse
from django.contrib.auth import authenticate, login, mixins
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import UserForm
from django.contrib.auth.models import User, Group
from .forms import ProfileForm
from borrow.models import BorrowRecord
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.db import transaction
from datetime import timedelta
from django.utils.timezone import now

# Create your views here.
class AddUserFormView(generic.TemplateView):
    template_name = 'users/registrationform.html'

    def get(self,request):
        form = UserForm()
        args = {'form':form}
        return render(request,self.template_name,args)

    def post(self,request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # Add user to NormalUser group by default
            normal_group = Group.objects.get(name='NormalUser')
            user.groups.add(normal_group)

            user=authenticate(username=username,password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    messages.success(request, 'Registration successful! Please log in.')
                    return redirect('/users/login')

        return render(request,self.template_name,{'form':form})

@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Changes saved successfully!")
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'users/profile.html', {'form': form})

def is_librarian(user):
    return user.groups.filter(name='Librarian').exists()

@login_required
@user_passes_test(is_librarian)
def promote_user(request, user_id):
    user_to_promote = get_object_or_404(User, id=user_id)

    librarian_group = Group.objects.get(name='Librarian')
    normal_group = Group.objects.get(name='NormalUser')

    # Remove user from normal group if present
    user_to_promote.groups.remove(normal_group)
    # Add user to librarian group
    user_to_promote.groups.add(librarian_group)

    return redirect('users:user_list')  # Redirect to user list or wherever

@login_required
@user_passes_test(is_librarian)
def user_list(request):
    query = request.GET.get('q', '').strip()

    normal_group = Group.objects.get(name='NormalUser')
    librarian_group = Group.objects.get(name='Librarian')

    normal_users = User.objects.filter(groups=normal_group)
    librarians = User.objects.filter(groups=librarian_group)

    if query:
        normal_users = normal_users.filter(
            Q(username__icontains=query)
        )
        librarians = librarians.filter(
            Q(username__icontains=query)
        )

    return render(request, 'users/user_list.html', {
        'normal_users': normal_users,
        'librarians': librarians,
        'query': query,
    })

@login_required
@user_passes_test(is_librarian)
def demote_user(request, user_id):
    user_to_demote = get_object_or_404(User, id=user_id)

    librarian_group = Group.objects.get(name='Librarian')
    normal_group = Group.objects.get(name='NormalUser')

    # Remove user from librarian group
    user_to_demote.groups.remove(librarian_group)
    # Add user back to normal group
    user_to_demote.groups.add(normal_group)

    return redirect('users:user_list')  # Redirect to user list or wherever you want

@login_required
@user_passes_test(is_librarian)
def borrow_request_list(request):
    records = BorrowRecord.objects.filter(
        Q(status='pending') | Q(status='return_requested')
    ).order_by('-borrowed_at')
    return render(request, 'users/request_list.html', {'requests': records})

@login_required
@user_passes_test(is_librarian)
@require_POST
def process_borrow_request(request, record_id, action):
    try:
        record = get_object_or_404(BorrowRecord, id=record_id)
        
        if record.status not in ['pending', 'return_requested']:
            return JsonResponse({'success': False, 'error': 'Request not in a processable state.'}, status=400)

        with transaction.atomic():
            if record.status == 'pending':
                if action == 'approve':
                    record.status = 'approved'
                    if record.book_type == 'physical':
                        if record.book.available_copies <= 0:
                            raise ValueError("No available copies for this book.")
                        record.book.available_copies -= 1
                        record.book.save()
                elif action == 'reject':
                    record.status = 'rejected'
                else:
                    return JsonResponse({'error': 'Invalid action for pending request.'}, status=400)

            elif record.status == 'return_requested':
                if action == 'approve_return':
                    record.status = 'returned'
                    record.returned_at = now().date()

                    late_fee_per_day = 1.00
                    if record.returned_at > record.due_date:
                        days_late = (record.returned_at - record.due_date).days
                        late_fee = days_late * late_fee_per_day
                    else:
                        late_fee = 0.0
                    record.return_rejection_reason = None

                    if record.book_type == 'physical':
                        record.book.available_copies = min(record.book.available_copies + 1, record.book.total_copies)
                        record.book.save()

                elif action == 'reject_return':
                    record.status = 'return_rejected'
                    rejection_reason = request.POST.get('reason', '').strip()
                    if not rejection_reason:
                        return JsonResponse({'success': False, 'error': 'Rejection reason is required.'}, status=400)
                    record.return_rejection_reason = rejection_reason
                else:
                    return JsonResponse({'error': 'Invalid action for return request.'}, status=400)
            
            record.save()
            return JsonResponse({'success': True, 'record_id': record.id})

    except ValueError as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    except Exception as e:
        print(f"Error processing borrow request: {e}")
        return JsonResponse({'success': False, 'error': 'An unexpected error occurred.'}, status=500)