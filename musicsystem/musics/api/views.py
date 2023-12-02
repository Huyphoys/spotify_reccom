from rest_framework.response import Response
from musics.cossinesim import onehotencode,tfidf,get_similar_track_ids

from rest_framework import generics
import pandas as pd
from musics.models import Track
from musics.api.serializers import SimilarTrackSerializer,TrackSerializers
from musics.api.paginator import CustomPageNumberPagination



class SimilarTrackListAPIView(generics.ListAPIView):

    queryset = Track.objects.all()
    serializer_class = SimilarTrackSerializer
    
    def list(self, request, *args, **kwargs):
        try:
            track_id = self.kwargs.get('track_id')     

            

            queryset = Track.objects.all()

            

            df = pd.DataFrame.from_records(queryset.values())
            
            
            
            df = pd.concat([df, onehotencode(df, 'artist')], axis=1)

            df = pd.concat([df, onehotencode(df, 'playlist')], axis=1)

            df = pd.concat([df, tfidf(df, 'genres')], axis=1)

            sim_tracks = get_similar_track_ids(df,track_id,50)

            columns = ["id","name","artist","genres","sim_score"]

            sim_tracks=sim_tracks[columns]

            serializer = SimilarTrackSerializer(data=sim_tracks.to_dict(orient='records'), many=True)
            serializer.is_valid(raise_exception=True)  
            serialized_data = serializer.data
            
            return Response(serialized_data)
        
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class TrackListAPIView(generics.ListAPIView):
      
    queryset = Track.objects.all()
    serializer_class = TrackSerializers
    pagination_class = CustomPageNumberPagination



class ListTrackByGenres(generics.ListAPIView):
    serializer_class = TrackSerializers
    

    def list(self, request, *args, **kwargs):
         
        genres = self.kwargs.get('genres')
        
        queryset = Track.objects.filter(genres__contains=genres)
        
        
        paginator = CustomPageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = self.get_serializer(paginated_queryset , many=True)

        return paginator.get_paginated_response(serializer.data)



class ListTrackByArtist(generics.ListAPIView):
    serializer_class = TrackSerializers

    def list(self, request, *args, **kwargs):
        artist_name = self.kwargs.get('artist')
        
        # Burada artist adına göre filtreleme yapılıyor, "iexact" filtreleme kullanılıyor.
        queryset = Track.objects.filter(artist__iexact=artist_name)
        
        paginator = CustomPageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = self.get_serializer(paginated_queryset, many=True)

        return paginator.get_paginated_response(serializer.data)