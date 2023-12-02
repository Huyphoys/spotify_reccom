from django.urls import path

from musics.api.views import SimilarTrackListAPIView,TrackListAPIView,ListTrackByGenres,ListTrackByArtist


urlpatterns = [
        path('similar_tracks/<str:track_id>/', SimilarTrackListAPIView.as_view(), name='similar_tracks_api'),
        path('tracks/',TrackListAPIView.as_view(),name='track_api'),
        path('track_by_genres/<str:genres>/',ListTrackByGenres.as_view(),name='track_by_genres_api'),
        path('track_by_artist/<str:artist>/', ListTrackByArtist.as_view(),name='track_by_artist_id')
]