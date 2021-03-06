from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
# from taggit.managers import TaggableManager
from taggit_selectize.managers import TaggableManager
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from django_comments.models import Comment

# Create your models here.


# Κατηγορία
class Category(MPTTModel):
    name = models.CharField(max_length=50, help_text='Όνομα Κατηγορίας', verbose_name='Κατηγορία')
    slug = AutoSlugField(populate_from='name', unique=True, null=True, default=None)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name
        #return '/'.join([x['name'] for x in self.get_ancestors(include_self=True).values()])

    def get_category_greek(self):
        return '/'.join([x['name'] for x in self.get_ancestors(include_self=True).values()])

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
        #return '/'.join([x['name'] for x in self.get_ancestors(include_self=True).values()])

    def get_name(self):
        return self.name

    def get_area_greek(self):
        return '/'.join([x['name'] for x in self.get_ancestors(include_self=True).values()])

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

    category = models.ForeignKey(Category, help_text='Επιλέξτε κατηγορία', verbose_name='Κατηγορία',
                                 on_delete=models.CASCADE)
    area = models.ManyToManyField(Area, help_text='Επιλέξτε Επιστημονική κατηγορία', verbose_name='Επιστημονική '
                                                                                                  'κατηγορία')
    tags = TaggableManager(blank=True)

    file = models.FileField(upload_to='files', null=True, verbose_name='Αρχείο')
    thumbnail = models.ImageField(upload_to='thumbnail', null=True, verbose_name='Εικόνα αρχείου')

    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    author = models.CharField(max_length=100, help_text='Δημιουργός', verbose_name='Δημιουργός')
    author_email = models.CharField(max_length=100,  help_text='email δημιουργού', verbose_name='Email δημιουργού')
    allow_comments = models.BooleanField('allow comments', default=True)

    ratings = GenericRelation(Rating, related_query_name='foos')


    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        return reverse(
            'file_detail',
            kwargs={'slug': self.slug})

    def get_comments(self):

        return Comment.objects.all().filter(object_pk=self.pk).count()

    def comm(self):
        aggregate = File.objects.aggregate(comment_count=File('comments'))
        return aggregate['comment_count'] + 1

    class Meta:
        verbose_name = 'Αρχείο'
        verbose_name_plural = 'Αρχεία'
