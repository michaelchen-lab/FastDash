import json

from django.shortcuts import get_object_or_404

from rest_framework import mixins, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework import status

from core_API.models import Dashboard, Dataset
from .serializers import DashboardSerializer, DatasetSerializer
from .utils import *
from .analytics import *

class DashboardViewSet(viewsets.ModelViewSet):
    #queryset = Dashboard.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    
    serializer_class = DashboardSerializer
    
    def get_queryset(self):
        return self.request.user.Dashboards.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DatasetViewSet(
        mixins.ListModelMixin, 
        mixins.CreateModelMixin, 
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet
    ):
    """
    LIST (GET): 
        - Returns a list of all datasets without raw data
    
    CREATE (POST): 
        - Saves a dataset into static files
    
    RETRIEVE (GET):
        - Returns a particular dataset with 100 rows of raw data
    """
    permission_classes = [
        permissions.IsAuthenticated
    ]
    
    serializer_class = DatasetSerializer
    parser_classes = (JSONParser, FormParser, MultiPartParser)
    
    def get_queryset(self):
        return self.request.user.Datasets.all()
    
    def perform_create(self, serializer):
        # print(serializer.validated_data["file"].temporary_file_path())
    
        # data, columns = get_raw_dataset(serializer.validated_data["file"].temporary_file_path())
        # type_data = generate_type_data(data, columns)
    
        serializer.save(user=self.request.user)
    
    def retrieve(self, request, pk=None):
        queryset = Dataset.objects.all()
        dataset = get_object_or_404(queryset, pk=pk)
        
        dataset_info = DatasetSerializer(dataset).data
        data, columns = get_raw_dataset(dataset)
        
        dataset_info['data'] = data
        if dataset_info['type_data'] == None:
            dataset_info['type_data'] = generate_type_data(data, columns)
        
        return Response(dataset_info)

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def LineAnalyticsView(request, dataset_id):
    
    queryset = request.user.Datasets.all()
    dataset = get_object_or_404(queryset, pk=dataset_id)
    df = get_df(dataset)
    
    graph_params = get_request_params(request)
    print(graph_params)
    data = line_analytics(df, graph_params)
    
    if "error" in data:
        return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(data)

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def BarAnalyticsView(request, dataset_id):
    
    queryset = request.user.Datasets.all()
    dataset = get_object_or_404(queryset, pk=dataset_id)
    df = get_df(dataset)
    
    graph_params = get_request_params(request)
    data = bar_analytics(df, graph_params)
    
    if "error" in data:
        return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(data)

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def ValueAnalyticsView(request, dataset_id):
    
    queryset = request.user.Datasets.all()
    dataset = get_object_or_404(queryset, pk=dataset_id)
    df = get_df(dataset)
    
    graph_params = get_request_params(request)
    data = value_analytics(df, graph_params)
    
    if "error" in data:
        return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(data)

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def ViewDashboardView(request, dashboard_id):
    """
    Returns all templates along with their respective contents
    """
    
    dashboard = Dashboard.objects.get(id=dashboard_id)
    
    return Response(DashboardSerializer(dashboard).data)
        