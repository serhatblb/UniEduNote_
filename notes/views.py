from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import NoteForm
from categories.models import University, Department, Course
import os


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
    return render(request, 'notes/note_list.html', context)


def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note})


@login_required
def download_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    note.download_count += 1
    note.save()

    try:
        file_path = note.file.path
        file_name = os.path.basename(file_path)
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
    except FileNotFoundError:
        raise Http404("Dosya sunucuda bulunamadı.")
@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'dashboard.html')