"""
Akademik hiyerarşi API endpoint'leri
Üniversite → Fakülte → Bölüm → Ders zinciri için API'ler
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.cache import cache
from django.db.models import Q
from .models import University, Faculty, Department, Course


class UniversityListView(APIView):
    """
    Tüm üniversiteleri listeler (cache'li)
    """
    permission_classes = [AllowAny]

    def get(self, request):
        cache_key = 'api_universities_list'
        universities = cache.get(cache_key)
        
        if not universities:
            universities = University.objects.all().order_by('name')
            universities = [{'id': u.id, 'name': u.name} for u in universities]
            cache.set(cache_key, universities, 60 * 60 * 24)  # 24 saat
        
        return Response(universities)


class FacultyListView(APIView):
    """
    Üniversiteye göre fakülteleri listeler
    """
    permission_classes = [AllowAny]

    def get(self, request):
        university_id = request.GET.get('university_id')
        
        if not university_id:
            return Response({'error': 'university_id parametresi gerekli'}, status=400)
        
        cache_key = f'api_faculties_{university_id}'
        faculties = cache.get(cache_key)
        
        if not faculties:
            faculties = Faculty.objects.filter(university_id=university_id).order_by('name')
            faculties = [{'id': f.id, 'name': f.name} for f in faculties]
            cache.set(cache_key, faculties, 60 * 60 * 12)  # 12 saat
        
        return Response(faculties)


class DepartmentListView(APIView):
    """
    Fakülteye göre bölümleri listeler
    """
    permission_classes = [AllowAny]

    def get(self, request):
        faculty_id = request.GET.get('faculty_id')
        
        if not faculty_id:
            return Response({'error': 'faculty_id parametresi gerekli'}, status=400)
        
        cache_key = f'api_departments_{faculty_id}'
        departments = cache.get(cache_key)
        
        if not departments:
            departments = Department.objects.filter(faculty_id=faculty_id).order_by('name')
            departments = [{'id': d.id, 'name': d.name} for d in departments]
            cache.set(cache_key, departments, 60 * 60 * 12)  # 12 saat
        
        return Response(departments)


class CourseListView(APIView):
    """
    Bölüme göre dersleri listeler
    """
    permission_classes = [AllowAny]

    def get(self, request):
        department_id = request.GET.get('department_id')
        
        if not department_id:
            return Response({'error': 'department_id parametresi gerekli'}, status=400)
        
        cache_key = f'api_courses_{department_id}'
        courses = cache.get(cache_key)
        
        if not courses:
            courses = Course.objects.filter(department_id=department_id).order_by('name')
            courses = [{'id': c.id, 'name': c.name} for c in courses]
            cache.set(cache_key, courses, 60 * 60 * 6)  # 6 saat
        
        return Response(courses)


class CourseGetOrCreateView(APIView):
    """
    Ders oluştur veya bul (not yüklerken yeni ders eklemek için)
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get('name', '').strip()
        department_id = request.data.get('department_id')

        if not name or not department_id:
            return Response({'error': 'name ve department_id gerekli'}, status=400)

        course = Course.objects.filter(
            name__iexact=name, department_id=department_id
        ).first()
        if not course:
            course = Course.objects.create(name=name, department_id=department_id)

        # Cache'i temizle ki yeni ders görünsün
        cache.delete(f'api_courses_{department_id}')

        return Response({'id': course.id, 'name': course.name})


class AcademicSearchView(APIView):
    """
    Text bazlı arama (tüm seviyelerde)
    """
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get('q', '').strip()
        level = request.GET.get('level', 'all')  # all, university, faculty, department, course
        
        if not query or len(query) < 2:
            return Response([])
        
        cache_key = f'api_search_{level}_{query.lower()}'
        results = cache.get(cache_key)
        
        if not results:
            results = []
            
            if level in ['all', 'university']:
                universities = University.objects.filter(name__icontains=query)[:10]
                results.extend([{
                    'id': u.id,
                    'name': u.name,
                    'type': 'university',
                    'level': 1
                } for u in universities])
            
            if level in ['all', 'faculty']:
                faculties = Faculty.objects.filter(name__icontains=query).select_related('university')[:10]
                results.extend([{
                    'id': f.id,
                    'name': f.name,
                    'type': 'faculty',
                    'level': 2,
                    'university_id': f.university_id,
                    'university_name': f.university.name
                } for f in faculties])
            
            if level in ['all', 'department']:
                departments = Department.objects.filter(name__icontains=query).select_related('faculty__university')[:10]
                results.extend([{
                    'id': d.id,
                    'name': d.name,
                    'type': 'department',
                    'level': 3,
                    'faculty_id': d.faculty_id,
                    'faculty_name': d.faculty.name,
                    'university_id': d.faculty.university_id,
                    'university_name': d.faculty.university.name
                } for d in departments])
            
            if level in ['all', 'course']:
                courses = Course.objects.filter(name__icontains=query).select_related('department__faculty__university')[:10]
                results.extend([{
                    'id': c.id,
                    'name': c.name,
                    'type': 'course',
                    'level': 4,
                    'department_id': c.department_id,
                    'department_name': c.department.name,
                    'faculty_id': c.department.faculty_id,
                    'faculty_name': c.department.faculty.name,
                    'university_id': c.department.faculty.university_id,
                    'university_name': c.department.faculty.university.name
                } for c in courses])
            
            cache.set(cache_key, results, 60 * 15)  # 15 dakika cache
        
        return Response(results)

