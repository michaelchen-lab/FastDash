from rest_framework import serializers
from core_API.models import Dashboard, Dataset

class DashboardSerializer(serializers.ModelSerializer):
	class Meta:
		model = Dashboard
		fields = "__all__"

class DatasetSerializer(serializers.ModelSerializer):
    #file = serializers.FilePathField(required=True)
    
    class Meta:
        model = Dataset
        fields = ("id", "title","type_data", "file")
        #fields = "__all__"