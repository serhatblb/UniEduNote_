from django.db import models

class University(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Faculty(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="faculties")
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name  # 🔹 Eskiden "Karabük Üniversitesi - Mühendislik Fakültesi" oluyordu


class Department(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="departments")
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name  # 🔹 Sadece bölüm adı yazsın


class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses")
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name  # 🔹 Karışıklığı önledik


class Semester(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
