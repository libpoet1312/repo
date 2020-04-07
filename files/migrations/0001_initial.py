# Generated by Django 3.0.4 on 2020-04-06 20:35

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Επιστημονική Περιοχή', max_length=50, verbose_name='Επιστημονική Περιοχή')),
                ('slug', autoslug.fields.AutoSlugField(default=None, editable=False, null=True, populate_from='name', unique=True)),
                ('thumbnail', models.ImageField(null=True, upload_to='Area_Images', verbose_name='Εικόνα Επιστημονικής Περιοχής')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='files.Area')),
            ],
            options={
                'verbose_name': 'Επιστημονική Περιοχή',
                'verbose_name_plural': 'Επιστημονικές Περιοχές',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Όνομα Κατηγορίας', max_length=50, verbose_name='Κατηγορία')),
                ('slug', autoslug.fields.AutoSlugField(default=None, editable=False, null=True, populate_from='name', unique=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='files.Category')),
            ],
            options={
                'verbose_name': 'Κατηγορία',
                'verbose_name_plural': 'Κατηγορίες',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Τίτλος')),
                ('summary', models.TextField(help_text='Περιγραφή του αρχείου', max_length=1000, verbose_name='Περιγραφή')),
                ('slug', autoslug.fields.AutoSlugField(default=None, editable=False, null=True, populate_from='name', unique=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(null=True, upload_to='files', verbose_name='Αρχείο')),
                ('thumbnail', models.ImageField(null=True, upload_to='thumbnail', verbose_name='Εικόνα αρχείου')),
                ('author', models.CharField(help_text='Δημιουργός', max_length=100, verbose_name='Δημιουργός')),
                ('author_email', models.CharField(help_text='email δημιουργού', max_length=100, verbose_name='Email δημιουργού')),
                ('area', models.ManyToManyField(help_text='Επιλέξτε Επιστημονική κατηγορία', to='files.Area', verbose_name='Επιστημονική κατηγορία')),
                ('category', models.ForeignKey(help_text='Επιλέξτε κατηγορία', on_delete=django.db.models.deletion.CASCADE, to='files.Category', verbose_name='Κατηγορία')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('uploader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Αρχείο',
                'verbose_name_plural': 'Αρχεία',
            },
        ),
    ]
