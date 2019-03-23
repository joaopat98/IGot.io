from django.apps import apps
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

Skin = apps.get_model("game", "Skin")
UserSkin = apps.get_model("game", "UserSkins")


def homepage(request):
    return render(request, 'index.html')


@login_required
def shop(request):
    skins = {}
    for skin in Skin.objects.all():
        skins[skin.slang] = skin.path_png

    userskins = list(map(lambda s: s.skin.slang, UserSkin.objects.filter(profile=request.user.user_profile)))

    return render(request, 'shop.html', {"skin_list": skins, "user_skins": userskins})

@login_required
def select_skin(request, skin):
    userskins = list(map(lambda s: s.skin.slang, UserSkin.objects.filter(profile=request.user.user_profile)))
    if skin in userskins:
        request.user.user_profile.current_skin = skin
        request.user.user_profile.save()
    return redirect(shop)


@login_required
def pay_mobile(request, skin):
    data = {'value': 1, 'skin': skin}
    return render(request, 'pay_mobile.html', data);

@login_required
def logout_view(request):
    logout(request)
    return redirect(homepage)
