from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import University, Department, Course, Note
from .forms import NoteUploadForm, UserUpdateForm, ProfileUpdateForm

# Email Verification Imports
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

# --- ANASAYFA & ARAMA ---
def home(request):
    universities = University.objects.all()
    # İstatistikler için sayılar
    context = {
        'universities': universities,
        'total_notes': Note.objects.count(),
        'total_users': University.objects.count() * 150 # Fake rakam, dolu görünsün :)
    }
    return render(request, 'index.html', context)

def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Course.objects.filter(Q(name__icontains=query) | Q(code__icontains=query))
    return render(request, 'search_results.html', {'query': query, 'results': results})

# --- AKADEMİK DETAYLAR ---
def department_detail(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    courses = department.courses.all()
    return render(request, 'department_detail.html', {'department': department, 'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    notes = course.notes.filter(is_approved=True).order_by('-created_at')
    return render(request, 'course_detail.html', {'course': course, 'notes': notes})

# --- NOT İŞLEMLERİ ---
@login_required
def upload_note(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = NoteUploadForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.uploader = request.user
            note.course = course
            # Puan Kazandır
            request.user.profile.points += 5
            request.user.profile.save()
            note.save()
            messages.success(request, f'Tebrikler! Not yüklendi ve 5 Puan kazandın! 🎉')
            return redirect('course_detail', course_id=course.id)
    else:
        form = NoteUploadForm()
    return render(request, 'upload_note.html', {'form': form, 'course': course})

# --- KULLANICI İŞLEMLERİ ---
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False # Pasif olarak oluştur
            user.save()
            
            # Email Gönderme İşlemi
            current_site = get_current_site(request)
            mail_subject = 'UniEduNote Hesabını Aktifleştir'
            message = render_to_string('registration/email_confirmation_message.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            
            messages.success(request, 'Hesabın oluşturuldu! Lütfen e-posta adresine gelen linke tıklayarak hesabını aktifleştir.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Hesabın başarıyla aktif edildi! Şimdi giriş yapabilirsin.')
        return redirect('login')
    else:
        messages.error(request, 'Aktivasyon linki geçersiz veya süresi dolmuş!')
        return redirect('signup')

@login_required
def profile(request):
    # Profil yoksa oluştur (Eski kullanıcılar veya hata durumları için)
    if not hasattr(request.user, 'profile'):
        from .models import Profile
        Profile.objects.create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profilin başarıyla güncellendi!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_notes': Note.objects.filter(uploader=request.user)
    }
    return render(request, 'users/profile.html', context)