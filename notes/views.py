from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Note, NoteImage, Category
from .forms import NoteForm, SignUpForm
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import UsernameChangeForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


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
    notes = Note.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'note_list.html', {'notes': notes})

@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.owner = request.user
            note.save()
            
            # Handle multiple images
            images = request.FILES.getlist('images')
            for image in images:
                NoteImage.objects.create(note=note, image=image)
            
            messages.success(request, 'Notatka została utworzona.')
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'note_form.html', {'form': form, 'title': 'Nowa notatka'})

@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if note.owner != request.user and not note.is_published:
        messages.error(request, 'Nie masz dostępu do tej notatki.')
        return redirect('note_list')
    return render(request, 'note_detail.html', {'note': note})

@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            
            # Handle multiple images
            images = request.FILES.getlist('images')
            for image in images:
                NoteImage.objects.create(note=note, image=image)
            
            messages.success(request, 'Notatka została zaktualizowana.')
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'note_form.html', {'form': form, 'title': 'Edytuj notatkę'})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, owner=request.user)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Notatka została usunięta.')
        return redirect('note_list')
    return render(request, 'note_confirm_delete.html', {'note': note})

@login_required
def note_publish(request, pk):
    note = get_object_or_404(Note, pk=pk, owner=request.user)
    note.is_published = True
    note.save()
    messages.success(request, 'Notatka została opublikowana.')
    return redirect('note_list')

@login_required
def note_unpublish(request, pk):
    note = get_object_or_404(Note, pk=pk, owner=request.user)
    note.is_published = False
    note.save()
    messages.success(request, 'Notatka została ukryta.')
    return redirect('note_list')

@user_passes_test(lambda u: u.is_superuser)
def admin_delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Notatka została usunięta przez administratora.')
        return redirect('homepage')
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

def homepage(request):
    # Pobierz wszystkie kategorie
    categories = Category.objects.all()
    
    # Pobierz wybraną kategorię z parametrów URL
    category_id = request.GET.get('category')
    selected_category = None
    
    # Pobierz notatki
    published_notes = Note.objects.filter(is_published=True).order_by('-created_at')
    
    # Jeśli wybrano kategorię, przefiltruj notatki
    if category_id and category_id != 'all':
        try:
            selected_category = Category.objects.get(id=category_id)
            published_notes = published_notes.filter(category=selected_category)
        except Category.DoesNotExist:
            pass
    
    context = {
        'published_notes': published_notes,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'homepage.html', context)

@login_required
def account(request):
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nazwa użytkownika została zaktualizowana.')
            return redirect('account')
    else:
        form = UsernameChangeForm(instance=request.user)
    return render(request, 'account.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Konto zostało utworzone! Możesz się teraz zalogować.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def note_delete_image(request, image_id):
    image = get_object_or_404(NoteImage, id=image_id, note__owner=request.user)
    note_id = image.note.id
    image.delete()
    messages.success(request, 'Zdjęcie zostało usunięte.')
    return redirect('note_edit', pk=note_id)
