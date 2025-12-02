import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Note
from .forms import NoteForm
from categories.models import University, Department, Course
from django.views.decorators.http import require_POST
from django.shortcuts import redirect

# 📤 Not yükleme
@login_required
def upload_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/upload_note.html', {'form': form})


# 📋 Not listesi (filtreli)
def note_list(request):
    notes = Note.objects.all().order_by('-uploaded_at')

    university = request.GET.get('university')
    department = request.GET.get('department')
    course = request.GET.get('course')

    if university:
        notes = notes.filter(university__id=university)
    if department:
        notes = notes.filter(department__id=department)
    if course:
        notes = notes.filter(course__id=course)

    universities = University.objects.all()
    departments = Department.objects.all()
    courses = Course.objects.all()

    context = {
        'notes': notes,
        'universities': universities,
        'departments': departments,
        'courses': courses,
    }
    request.session['last_notes_list_url'] = request.get_full_path()
    return render(request, 'notes/note_list.html', context)


# 🔍 Not detay
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note})


# 📥 Not indirme
@login_required
def download_note(request, pk):
    note = get_object_or_404(Note, pk=pk)

    # İndirme sayısını artır
    note.download_count += 1
    note.save()

    # ESKİ KODUN (Bunu sil):
    # try:
    #     file_path = note.file.path
    #     return FileResponse(open(file_path, 'rb')...)
    # except...

    # YENİ KOD (Bunu yapıştır):
    if note.file:
        # Dosya Cloudinary'de olduğu için direkt URL'sine yönlendiriyoruz
        return redirect(note.file.url)
    else:
        # Dosya yoksa hata ver
        raise Http404("Dosya bulunamadı.")


# 🏠 Dashboard
@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'dashboard.html')


# ✏️ Not düzenleme
@login_required(login_url="/login/")
def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == "POST":
        note.title = request.POST.get("title")
        note.description = request.POST.get("description")
        if "file" in request.FILES:
            note.file = request.FILES["file"]
        note.save()
        messages.success(request, "Not başarıyla güncellendi.")
        return redirect("note_detail", pk=note.pk)
    return render(request, "notes/edit_note.html", {"note": note})

# ✏ Not silme
@login_required(login_url='/login/')
@require_POST
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.delete()
    messages.success(request, "Not silindi.")
    redirect_url = request.session.get('last_notes_list_url', '/notes/')
    return redirect(redirect_url)