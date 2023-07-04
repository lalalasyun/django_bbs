from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render,get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from bbs.form import PostForm
from bbs.models import Post
from accounts.models import MyUser,Follow

from django.contrib import messages
from django.conf import settings

from bbs.form import PostForm

def getAliveOrderByPosts(limit=10):
	posts = Post.objects.alive().order_by("-posted_at")[:limit+1]
	return (posts[:limit],len(posts) > limit)

def getAliveOrderByUserPosts(user=None, limit=10):
	posts = Post.objects.alive().filter(posted_by=user).order_by("-posted_at")[:limit+1]
	return (posts[:limit],len(posts) > limit)

def get_user_follows(user):
	follow_names = [user]
	follows = Follow.objects.filter(followed_by = user)
	for follow in follows:
		follow_names.append(follow.followed_to)
	return follow_names

def getAliveOrderByFollowsUserPosts(request,limit=10):
	posts, next = getAliveOrderByPosts(limit)
	if not request.user.is_authenticated:
		return posts, next, None
	
	user = get_object_or_404(MyUser,username =request.user.username)

	follows = get_user_follows(user)
	if user.view_timeline == "all":
		return posts, next, follows
	
	posts = Post.objects.alive().filter(posted_by__in = follows).order_by("-posted_at")[:limit+1]
	return (posts[:limit], len(posts) > limit, follows)

def create_timeline_render(request, limit=10):
	posts,next,follows = getAliveOrderByFollowsUserPosts(request,limit)
	user = get_object_or_404(MyUser,username =request.user.username)
	return render_to_string("bbs/timeline.html",{"posts":posts, "post_next":next, "follow_names":follows ,"user":user},request)

# Create your views here.
def topView(request):
	posts,next,follows = getAliveOrderByFollowsUserPosts(request)
	return render(request, "bbs/top.html",{"posts":posts,"post_next":next,"post_form":PostForm(),"follow_names":follows})

@require_POST
def postTextView(request):
	json = { "error":True, "content":{}}
	if not request.user.is_authenticated:
		json["redirect"] = f"{settings.LOGIN_URL}?next={settings.LOGIN_REDIRECT_URL}"
		return JsonResponse(json)
	
	form = PostForm(request.POST)

	if not form.is_valid():
		print("Validation Error")
		messages.add_message(request, messages.ERROR,"投稿に失敗しました。")
		json["content"]["timeline"] = create_timeline_render(request)
		json["content"]["messages"] = render_to_string("bbs/messages.html",None,request)

		return JsonResponse(json)
	
	post = form.save(commit = False)
	post.posted_by = request.user
	post.save()
	json["error"]   = False

	messages.add_message(request, messages.SUCCESS,"投稿しました。")
	json["content"]["timeline"] = create_timeline_render(request)
	json["content"]["messages"] = render_to_string("bbs/messages.html",None,request)
	
	return JsonResponse(json)

@require_POST
def postDeleteTextView(request):
	json = { "error":True, "content":{}}
	if not request.user.is_authenticated:
		json["redirect"] = f"{settings.LOGIN_URL}?next={settings.LOGIN_REDIRECT_URL}"
		return JsonResponse(json)
	
	
	post = Post.objects.get(pk = request.POST["post_id"])
	
	if not post or request.user != post.posted_by:
		messages.add_message(request, messages.WARNING,"削除に失敗しました。。")
	else:
		post.delete()
		json["error"]   = False
	
	messages.add_message(request, messages.INFO,"削除しました。")
	json["content"]["timeline"] = create_timeline_render(request)
	json["content"]["messages"] = render_to_string("bbs/messages.html",None,request)
	
	return JsonResponse(json)

@require_POST
def getAdditionalPosts(request):
	json = { "error":True, "content":{}}
	limit = int(request.POST["post_limit"]) + 10
	json["content"]["timeline"] = create_timeline_render(request,limit)
	json["error"]   = False

	return JsonResponse(json)

@require_POST
def setUserTimeline(request):
	select = request.POST["select"]
	json = { "error":True, "content":{}}
	if not request.user.is_authenticated:
		json["redirect"] = f"{settings.LOGIN_URL}?next=/"
		return JsonResponse(json)
	user = get_object_or_404(MyUser,username =request.user.username)
	if select in ["follow","all"]:
		user.view_timeline = select
		user.save()
		json["error"]   = False
	json["content"]["timeline"] = create_timeline_render(request)

	return JsonResponse(json)