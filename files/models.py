from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager

# Create your models here.


# Κατηγορία
class Category(MPTTModel):
    name = models.CharField(max_length=50, help_text='Όνομα Κατηγορίας', verbose_name='Κατηγορία')
    slug = AutoSlugField(populate_from='name', unique=True, null=True, default=None)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = 'Κατηγορίες'
        verbose_name = 'Κατηγορία'


# Επιστημονική Περιοχή
class Area(MPTTModel):
    name = models.CharField(max_length=50, help_text='Επιστημονική Περιοχή', verbose_name='Επιστημονική Περιοχή')
    slug = AutoSlugField(populate_from='name', unique=True, null=True, default=None)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    thumbnail = models.ImageField(upload_to='Area_Images', null=True, verbose_name='Εικόνα Επιστημονικής Περιοχής')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Επιστημονική Περιοχή'
        verbose_name_plural = 'Επιστημονικές Περιοχές'


# Το αρχείο
class File(models.Model):
    """Model representing a File """
    name = models.CharField(max_length=200, verbose_name='Τίτλος')
    summary = models.TextField(max_length=1000, help_text='Περιγραφή του αρχείου', verbose_name='Περιγραφή')

    slug = AutoSlugField(populate_from='name', unique=True, null=True, default=None)

    # Foreign Key used because a file can only have one author, but authors can have multiple files
    # Author as a string rather than object because it hasn't been declared yet in the file

    # Date of uploading the file #
    dateCreated = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(Category, help_text='Επιλέξτε κατηγορία', verbose_name='Κατηγορία', on_delete=models.CASCADE)
    area = models.ManyToManyField(Area, help_text='Επιλέξτε Επιστημονική κατηγορία', verbose_name='Επιστημονική κατηγορία')
    tags = TaggableManager()

    file = models.FileField(upload_to='files', null=True, verbose_name='Αρχείο')
    thumbnail = models.ImageField(upload_to='thumbnail', null=True, verbose_name='Εικόνα αρχείου')

    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    author = models.CharField(max_length=100, help_text='Δημιουργός', verbose_name='Δημιουργός')
    author_email = models.CharField(max_length=100,  help_text='email δημιουργού', verbose_name='Email δημιουργού')


    def __str__(self):
        """String for representing the Model object."""
        return self.name

    class Meta:
        verbose_name = 'Αρχείο'
        verbose_name_plural = 'Αρχεία'
