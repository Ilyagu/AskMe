"""AskNagdimaev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from myapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("hot/", views.hot_questions, name="hot_questions"),
    path("tag/<str:name>/", views.tag, name="questions_by_tag"),
    path("question/<int:pk>/", views.answers_for_question, name="answers_for_question"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("ask/", views.new_question, name="new_question"),
    path("settings/", views.settings, name="settings"),
    path("votes/", views.votes, name="votes"),
    path("correct/", views.is_correct, name="correct"),
    # path("static_page/", views.static_page, name="static_page"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
