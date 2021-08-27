from django.urls import path
from django.contrib.auth import views as auth_views
from review import views


app_name = 'review'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),                                        # 홈(리뷰목록)
    path('create/', views.reviewCreate, name='review_create'),                  # 리뷰등록
    path('modify/<int:review_id>/', views.reviewModify, name='review_modify'),  # 리뷰수정
    path('delete/<int:review_id>/', views.reviewDelete, name='review_delete'),  # 리뷰삭제
    path('<int:review_id>/', views.reviewDetail, name='review_detail'),         # 리뷰상세조회
    path('like/<int:review_id>/', views.like_review, name='like_review'),  # 좋아요
    path('unlike/<int:review_id>/', views.unlike_review, name='unlike_review'),  # 싫어요
]
