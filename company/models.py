from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images", default='images/user.jpg')
    bio = models.TextField(null=True, blank=True)
    twitter = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        name = str(self.first_name)
        if self.last_name:
            name += ' ' + str(self.last_name)
        return name


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/%s/' % self.slug

class Tag(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name

class Post(models.Model):
    ACTIVE = 'active'
    DRAFT = 'draft'

    CHOICE_STATUS = (
        (ACTIVE, 'Active'),
        (DRAFT, 'Draft')
    )

    category = models.ForeignKey(Category, null=True, blank=True, related_name='posts', on_delete=models.CASCADE)
    headline = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(blank=True, null=True)
    sub_headline = models.CharField(max_length=255, null=True, blank=True)
    intro = models.CharField(max_length=255, blank=True, null=True)
    thumbnail = models.ImageField(upload_to='images', null=True, blank=True)
    body = RichTextUploadingField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)
    status = models.CharField(max_length=10, choices=CHOICE_STATUS, default=ACTIVE)

    class Meta:
       ordering = ('-created',)

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return '/%s/%s/' % (self.category.slug, self.slug)

    def save(self, *args, **kwargs):

        if self.slug == None:
            slug = slugify(self.headline)

            has_slug = Post.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                count += 1
                slug = slugify(self.headline) + '-' + str(count)
                has_slug = Post.objects.filter(slug=slug).exists()

            self.slug = slug

        super().save(*args, **kwargs)


class PostComment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.body

    @property
    def created_dynamic(self):
        now = timezone.now()
        return now
