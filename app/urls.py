from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from django.urls import re_path

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:page_number>', views.index, name='page'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('ask', views.ask, name='ask'),
    path('login/', views.log_in, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('profile/edit', views.edit_profile, name='edit'),
    path('popular_tags/<int:tag_id>/', views.popular_tags, name='popular_tags'),
    path('hot/', views.hot, name='hot'),
    path('like/', views.like_question, name='like'),
    path('like/answer/', views.like_answer, name='like_answer'),
    path('answer_correct/', views.answer_correct, name='answer_correct'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)