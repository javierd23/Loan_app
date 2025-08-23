from django.core.exceptions import ValidationError

from django.db import models
from django.contrib.auth.models import User

from PIL import Image



class UserProfile(models.Model):
    photo = models.ImageField(upload_to="profile_pics/")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.photo:
            img_path = self.photo.path
            img = Image.open(img_path)

            max_size = (1000, 1000)
            img.thumbnail(max_size)  # resizing the image to avoid
            img.save(img_path)

    #relation
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiles')

    #personal info
    nickname = models.CharField(max_length=120, verbose_name="Alias", blank=True)

    birth_date = models.DateField(null=True, blank=True, verbose_name="Fecha de nacimento")
    phone_number = models.CharField(max_length=11, null=True, blank=True, verbose_name="Telefono")
    location = models.CharField(max_length=100, blank=True, verbose_name="Ubicacion")

    # Optional: Social
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    github = models.URLField(blank=True)
    facebook = models.URLField(blank=True)

    photo = models.ImageField(
                              upload_to="profile_pics/", null=True, blank=True,
                              verbose_name="Foto de perfil")

    def __str__(self):
        return self.nickname

