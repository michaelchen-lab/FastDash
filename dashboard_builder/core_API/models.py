from django.db import models
from accounts_API.models import User

from .utils import upload_file

class Dashboard(models.Model):
    ''' Dashboard's analytics data is stored here '''
    user = models.ForeignKey(User, related_name="Dashboards", on_delete=models.CASCADE, null=True)
    
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    data = models.JSONField()

class Dataset(models.Model):
    ''' Dataset's name and data types are stored here '''
    user = models.ForeignKey(User, related_name="Datasets", on_delete=models.CASCADE, null=True)
    
    title = models.CharField(max_length=100)
    type_data = models.JSONField(null=True)
    #file = models.FileField(upload_to=upload_file)
    file = models.FileField()
    
    # How to convert file to pandas #
    # from django.core.files import File
    # f = open(dataset.file.url, 'r')
    # file = File(f)
    # df = pd.read_csv(file)
