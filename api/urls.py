from django.urls import path

from . import views

urlpatterns = [
    path('', views.review, name='index'),
    path('<int:review_id>/', views.one_review, name='review' )
]