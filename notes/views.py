from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Note
from .forms import NoteForm, SignUpForm
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('note_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def note_list(request):
    notes = Note.objects.filter(owner=request.user)
    return render(request, 'notes/note_list.html', {'notes': notes})

@login_required
def note_create(request):
    form = NoteForm(request.POST or None)
    if form.is_valid():
        note = form.save(commit=False)
        note.owner = request.user
        note.save()
        return redirect('note_list')
    return render(request, 'notes/note_form.html', {'form': form})

@login_required
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk, owner=request.user)
    form = NoteForm(request.POST or None, instance=note)
    if form.is_valid():
        form.save()
        return redirect('note_list')
    return render(request, 'notes/note_form.html', {'form': form})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, owner=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'notes/note_confirm_delete.html', {'note': note})

@user_passes_test(lambda u: u.is_superuser)
def admin_delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect(reverse('note_list'))
    return render(request, 'notes/admin_note_confirm_delete.html', {'note': note})

@user_passes_test(lambda u: u.is_superuser)
def admin_note_list(request):
    query = request.GET.get('q', '')
    notes = Note.objects.all().select_related('owner')
    if query:
        notes = notes.filter(
            Q(title__icontains=query) | Q(owner__username__icontains=query)
        )
    return render(request, 'notes/admin_note_list.html', {'notes': notes, 'query': query})

@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('note_list')
    return render(request, 'notes/user_confirm_delete.html', {'user_obj': user})