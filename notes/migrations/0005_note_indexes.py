from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_bookmark_report'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='note',
            index=models.Index(fields=['-uploaded_at'], name='notes_note_uploaded_idx'),
        ),
        migrations.AddIndex(
            model_name='note',
            index=models.Index(fields=['-likes'], name='notes_note_likes_idx'),
        ),
        migrations.AddIndex(
            model_name='note',
            index=models.Index(fields=['-download_count'], name='notes_note_dl_idx'),
        ),
        migrations.AddIndex(
            model_name='note',
            index=models.Index(fields=['university', '-uploaded_at'], name='notes_note_uni_date_idx'),
        ),
        migrations.AddIndex(
            model_name='note',
            index=models.Index(fields=['department', '-uploaded_at'], name='notes_note_dept_date_idx'),
        ),
        migrations.AddIndex(
            model_name='note',
            index=models.Index(fields=['course', '-uploaded_at'], name='notes_note_course_date_idx'),
        ),
    ]
