from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="user_profile")
    phone_number = models.CharField(max_length=20, blank=True)
    max_score = models.IntegerField(default=0)

    def serialize(self):
        p = self
        u = p.user
        return {
            "user_id": u.id,
            "username": u.username,
            "phone_number": p.phone_number,
            "max_score": p.max_score,
        }


class Skin(models.Model):
    id = models.IntegerField(primary_key=True)
    profile = models.ManyToManyField(Profile, through="UserSkins")
    path_png = models.CharField(max_length=240)

    def serialize(self):
        s = self
        return {
            "skin_id": s.id,
            "path": s.path_png,
        }


class UserSkins(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    skin = models.ForeignKey(Skin, on_delete=models.CASCADE)


class Score(models.Model):
    name = models.CharField(max_length=240)
    score = models.IntegerField(default=0)
