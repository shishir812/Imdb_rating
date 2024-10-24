from django.urls import path
from .views import WatchListAV, WatchListDetailAV, StreamPlatformAV, StreamPlatformDetailAV, ReviewList, ReviewDetail, ReviewCreate,WatchListGV

urlpatterns = [
    path('watch/', WatchListAV.as_view(), name='watch-list'),
    path('watchlist/', WatchListGV.as_view(), name='watch-list-gv'),

    path('watch/<int:pk>/', WatchListDetailAV.as_view(), name='watch-detail'),
    path('stream/', StreamPlatformAV.as_view(), name='stream-platform'),
    path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(), name='stream-platform-detail'),

    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/review/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail')

]