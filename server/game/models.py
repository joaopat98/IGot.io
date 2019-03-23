from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="user_profile")
    phone_number = models.CharField(max_length=20, blank=True)
    max_score = models.IntegerField(default=0)
    current_skin = models.CharField(max_length=100, default="default")

    def serialize(self):
        p = self
        u = p.user
        return {
            "user_id": u.id,
            "username": u.username,
            "phone_number": p.phone_number,
            "max_score": p.max_score,
            "current_skin": p.current_skin
        }


class Skin(models.Model):
    profile = models.ManyToManyField(Profile, through="UserSkins")
    path_png = models.CharField(max_length=240)
    slang = models.CharField(max_length=100)

    def serialize(self):
        s = self
        return {

            "skin_id": s.id,
            "path": s.path_png,
            "slang": s.slang
        }


class UserSkins(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    skin = models.ForeignKey(Skin, on_delete=models.CASCADE)


class Score(models.Model):
    name = models.CharField(max_length=240)
    score = models.IntegerField(default=0)
