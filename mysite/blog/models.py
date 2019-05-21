from django.db import models
from django.utils import timezone

class Article(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    meta_description = models.CharField(max_length=200)
    body = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=200)
    views = models.PositiveIntegerField(default=0)
    show = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_date']

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def category_list(self):
        return self.category.split(";")

    def __str__(self):
        return self.title
