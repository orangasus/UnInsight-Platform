from django.db import models
from django.db.models import Avg

class University(models.Model):
    uni_name = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)


class Professor(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    full_name = models.CharField(max_length=50, blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)

    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)

    universities = models.ManyToManyField('uni_prof.University', related_name='professors')

    def update_rating(self):
        avg_rating = self.courses.aggregate(Avg('avg_course_rating'))['avg_course_rating__avg']
        self.rating = avg_rating or None
        self.save()

    def save(self, *args, **kwargs):
        self.full_name=f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)