import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Note
from .forms import NoteForm
from categories.models import University, Faculty, Department, Course
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.http import JsonResponse
from users.models import Notification

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


# 📋 Not listesi (filtreli) - Pagination ile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def note_list(request):
    sort_by = request.GET.get('sort', 'newest')

    if sort_by == 'popular':
        ordering = '-download_count'
    elif sort_by == 'liked':
        ordering = '-likes'
    else:
        ordering = '-uploaded_at'  # Varsayılan: En yeni

    # N+1 query problemini çözmek için select_related ve prefetch_related kullan
    notes = Note.objects.select_related(
        'user', 'university', 'faculty', 'department', 'course'
    ).prefetch_related(
        'comments', 'likes_set'
    ).order_by(ordering)

    university = request.GET.get('university')
    department = request.GET.get('department')
    course = request.GET.get('course')

    if university:
        notes = notes.filter(university__id=university)
    if department:
        notes = notes.filter(department__id=department)
    if course:
        notes = notes.filter(course__id=course)

    # Pagination: Sayfa başına 20 not
    paginator = Paginator(notes, 20)
    page = request.GET.get('page', 1)
    
    try:
        notes_page = paginator.page(page)
    except PageNotAnInteger:
        notes_page = paginator.page(1)
    except EmptyPage:
        notes_page = paginator.page(paginator.num_pages)

    universities = University.objects.all().order_by('name')
    departments = Department.objects.all().order_by('name')
    courses = Course.objects.all().order_by('name')

    context = {
        'notes': notes_page,
        'universities': universities,
        'departments': departments,
        'courses': courses,
        'sort_by': sort_by,
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

    try:
        if note.file:
            note.download_count += 1
            note.save()

            # BİLDİRİM GÖNDER (Kendi notunu indirince gitmesin)
            if note.user != request.user:
                Notification.objects.create(
                    user=note.user,  # Notun sahibine
                    message=f"Tebrikler! '{note.title}' başlıklı notun {request.user.username} tarafından indirildi. 🎉"
                )

            return redirect(note.file.url)
    except Exception as e:
        messages.error(request, "Dosya bulunamadı.")

    return redirect('note_detail', pk=pk)

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

def load_faculties(request):
    university_id = request.GET.get('university')
    faculties = Faculty.objects.filter(university_id=university_id).order_by('name')
    return JsonResponse(list(faculties.values('id', 'name')), safe=False)

def load_departments(request):
    faculty_id = request.GET.get('faculty')
    departments = Department.objects.filter(faculty_id=faculty_id).order_by('name')
    return JsonResponse(list(departments.values('id', 'name')), safe=False)

def load_courses(request):
    department_id = request.GET.get('department')
    courses = Course.objects.filter(department_id=department_id).order_by('name')
    return JsonResponse(list(courses.values('id', 'name')), safe=False)