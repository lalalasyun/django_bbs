from django.urls import path
from bbs import views

urlpatterns = [
	path('post/text/new/',views.postTextView, name='post_text'),
    path('post/text/delete/',views.postDeleteTextView, name='delete_post_text'),
    path('post/text/load/',views.getAdditionalPosts, name="get_additional_post"),
    path('setting/timeline/', views.setUserTimeline,name='setting_timeline'),
]