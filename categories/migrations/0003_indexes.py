from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_semester_alter_course_name_alter_department_name_and_more'),
    ]

    operations = [
        # University.name index
        migrations.AlterField(
            model_name='university',
            name='name',
            field=models.CharField(db_index=True, max_length=255),
        ),
        # Faculty.name index + composite (university, name)
        migrations.AlterField(
            model_name='faculty',
            name='name',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AddIndex(
            model_name='faculty',
            index=models.Index(fields=['university', 'name'], name='categories_faculty_uni_name_idx'),
        ),
        # Department.name index + composite (faculty, name)
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AddIndex(
            model_name='department',
            index=models.Index(fields=['faculty', 'name'], name='categories_dept_fac_name_idx'),
        ),
        # Course.name index + composite (department, name)
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['department', 'name'], name='categories_course_dept_name_idx'),
        ),
    ]
