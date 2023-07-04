from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages

from django.conf import settings

from image.models import UploadImage
from accounts.models import MyUser,Follow

from accounts.form import SettingUserForm
from image.form import UploadImageForm,TrimImageForm
from bbs.views import create_timeline_render, get_user_follows, getAliveOrderByUserPosts
# Create your views here.


def userProfileView(request,username):
    user = get_object_or_404(MyUser, username = username)
    follows = []
    is_follow = []
    if request.user.is_authenticated:
        followed_by = get_object_or_404(MyUser,username =request.user.username)
        is_follow = Follow.objects.filter(followed_by = followed_by,followed_to = user)
    follows = Follow.objects.filter(Q(followed_by = user) | Q(followed_to = user))

    posts, next = getAliveOrderByUserPosts(user,5)
    user_follows = get_user_follows(user)

    setting_form = None
    if user == request.user:
        setting_form = SettingUserForm(instance = user)

    image = None
    if hasattr(user,'trim_image'):
        image = get_object_or_404(UploadImage,upload_by = user)
    
    return render(request, "accounts/profile.html", {
                                                        "page_user":user, 
                                                        "posts":posts,
                                                        "post_next":next,
                                                        "follow_names":user_follows,
                                                        "follows":follows,
                                                        "is_follow":is_follow,
                                                        "setting_form":setting_form,
                                                        'upload_form': UploadImageForm(),
                                                        'trim_form':TrimImageForm(),
                                                        'image':image,
                                                        'image_size':400
                                                    }
    )

@require_POST
def followUser(request,username):
    event = request.POST["event"]
    json = { "error":True, "content":{}}
    if not request.user.is_authenticated:
        json["redirect"] = f"{settings.LOGIN_URL}?next=/accounts/{username}"
        return JsonResponse(json)
    
    if username == request.user.username:
        return JsonResponse(json)
	
    followed_to = get_object_or_404(MyUser,username =username)
    followed_by = get_object_or_404(MyUser,username =request.user.username)

    follows = Follow.objects.filter(followed_to = followed_to, followed_by = followed_by)

    if event == "follow" and not follows:
        form = Follow(followed_to = followed_to, followed_by = followed_by)
        form.save()
        json["error"]   = False
        messages.add_message(request, messages.SUCCESS,"フォローしました。")

    if event == "unfollow" and follows:
        follows[0].delete()
        json["error"]   = False
        messages.add_message(request, messages.SUCCESS,"フォロー解除しました。")

    follows = Follow.objects.filter(Q(followed_by = followed_to) | Q(followed_to = followed_to))
    is_follows = Follow.objects.filter(followed_to = followed_to, followed_by = followed_by)

    json["content"]["profile"] = render_to_string("accounts/profile_detail.html",{"page_user":followed_to, "follows":follows, "is_follow":is_follows},request)

    json["content"]["timeline"] = create_timeline_render(request)
    json["content"]["messages"] = render_to_string("bbs/messages.html",None,request)

    return JsonResponse(json)


@require_POST
def settingUserView(request):
    user = get_object_or_404(MyUser,username =request.user.username)
    form = SettingUserForm(request.POST,instance = user)
    if form.is_valid():
        form.save()
    return redirect("accounts",username = user.username)