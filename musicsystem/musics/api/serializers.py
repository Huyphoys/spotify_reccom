from rest_framework import serializers
from musics.models import Track




    
class  SimilarTrackSerializer(serializers.Serializer):

    id = serializers.CharField()
    name = serializers.CharField()
    artist = serializers.CharField()
    genres = serializers.CharField()
    sim_score = serializers.FloatField()



class TrackSerializers(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id','name','genres','artist']