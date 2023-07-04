from django.shortcuts import render,get_object_or_404,redirect
from django.views.decorators.http import require_POST,require_GET
from django.contrib.auth.decorators import login_required

from image.form import UploadImageForm,TrimImageForm

from image.models import UploadImage
from accounts.models import  MyUser

from django_bbs import settings

from PIL import Image
from datetime import datetime
import hashlib
import os
# Create your views here.
IMAGE_SIZE = 400

@require_GET
def topView(request):
    user = request.user
    image = None
    context = {
        'upload_form': UploadImageForm(),
        'trim_form':TrimImageForm(),
        }
    if hasattr(user,'trim_image'):
        image = get_object_or_404(UploadImage,upload_by = user)
        context['image'] = image
        context['image_size'] = IMAGE_SIZE
    return render(request,"image/top.html",context)

@require_GET
def profileView(request,username):
    user = get_object_or_404(MyUser,username = username)
    context = {'page_user':user}
    if hasattr(user,'trim_image'):
        context['image'] = get_object_or_404(UploadImage,upload_by = user)
    return render(request,"user/profile.html",context)

@require_GET
def userListView(request):
    users = MyUser.objects.all()
    images = UploadImage.objects.filter(upload_by__in = users)
    return render(request,"user/list.html",{'users':images})

@login_required(login_url='/login/')
@require_POST
def uploadImageView(request):
    user = get_object_or_404(MyUser,pk = request.user.pk)
    if hasattr(user,'trim_image'):
        image = get_object_or_404(UploadImage,upload_by = user)
        image.image.delete()
        image.is_edited = False
        form = UploadImageForm(request.POST, request.FILES, instance=image)
    else:
        form = UploadImageForm(request.POST, request.FILES)

    if form.is_valid():
        form.upload_by = user
        form.save()

        image = get_object_or_404(UploadImage, upload_by = user)
        filename = f"images/user/{upload_to_uuid(user, image.image)}"

        user.image.delete()
        trimImage(image, filename)

        user.image = filename
        user.save()
    return redirect('accounts',username = user.username)

@login_required(login_url='/login/')
@require_POST
def deleteImageView(request):
    user = get_object_or_404(MyUser,pk = request.user.pk)
    image = get_object_or_404(UploadImage,upload_by = user)
    user.image.delete()
    image.delete()
    return redirect('accounts',username = user.username)


def upload_to_uuid(instance, filename):
    current_time = datetime.now()
    pre_hash_name = '%s%s%s' % (instance.pk, filename, current_time)
    hs_filename = '%s.%s' % (hashlib.md5(pre_hash_name.encode()).hexdigest(), 'webp')
    return hs_filename

@login_required(login_url='/login/')
@require_POST
def trimImageView(request):
    user = get_object_or_404(MyUser,pk = request.user.pk)
    image = get_object_or_404(UploadImage, upload_by = user)
    image.is_edited = True
    form = TrimImageForm(request.POST, instance=image)
    if form.is_valid():
        form.save()
        image = get_object_or_404(UploadImage, upload_by = user)
        
        filename = f"images/user/{upload_to_uuid(user, image.image)}"
        user.image.delete()
        trimImage(image, filename)

        user.image = filename
        user.save()
    return redirect('accounts',username = user.username)

def trimImage(image, filename):
    img = Image.open(image.image.path)
    zoom = (image.zoom / 100) + 1

    front_zoom = IMAGE_SIZE / img.height
    WIDTH = int(img.width * front_zoom * zoom)
    HEIGHT = int(img.height * front_zoom * zoom)
    img = img.resize((WIDTH, HEIGHT))
    left, upper = abs(image.position_x), abs(image.position_y)
    right, lower = left + IMAGE_SIZE, upper + IMAGE_SIZE
    img = img.crop((left, upper, right, lower))
    img.save(os.path.join(settings.MEDIA_ROOT, filename))