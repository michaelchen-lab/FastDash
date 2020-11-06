import os, json
import math
import re
from decimal import Decimal
import pandas as pd
from django.core.files import File

def remove_exponent(d):
    """Remove exponent."""
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()

def num_millify(n, precision=2, drop_nulls=True, prefixes=[]):
    """Humanize number."""
    millnames = ['', 'K', 'M', 'B', 'T', 'P', 'E', 'Z', 'Y']
    if prefixes:
        millnames = ['']
        millnames.extend(prefixes)
    n = float(n)
    millidx = max(0, min(len(millnames) - 1,
                         int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))
    result = '{:.{precision}f}'.format(n / 10**(3 * millidx), precision=precision)
    if drop_nulls:
        result = remove_exponent(Decimal(result))
    return '{0}{dx}'.format(result, dx=millnames[millidx])


def num_prettify(amount, separator=','):
    """Separate with predefined separator."""
    orig = str(amount)
    new = re.sub("^(-?\d+)(\d{3})", "\g<1>{0}\g<2>".format(separator), str(amount))
    if orig == new:
        return new
    else:
        return num_prettify(new)

def get_templates():
    """
    Return all templates (and their contents)
    This is a temporary solution. To be moved to AWS S3.
    """
    path_to_json = "./core_API/static/dashboard_templates"
    
    ## JSON files
    json_filenames = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    
    json_data = []
    for filename in json_filenames:
        f = open(path_to_json+"/"+filename, "r")
        json_data.append(json.load(f))
    
    return dict(zip(json_filenames, json_data))

def upload_file(instance, filename):
    """'
    Upload user's file to STATIC
    """
    print(filename)
    
    return "./user_data/datasets/{0}_{1}".format(instance.user.id, filename)

def get_raw_dataset(dataset):
    """
    Get 100 rows of data from Dataset object
    """
    # f = open(dataset.file.url, 'r', encoding="utf8")
    # file = File(f)
    # df = pd.read_csv(file).head(100)
    
    df = pd.read_csv(dataset.file.url)
    df.fillna(0, inplace=True)
    df = df.head(50)
    
    # data = {
        # "columns": df.columns.tolist(), 
        # "data": df.values.tolist()
    # }
    
    columns, data = df.columns.tolist(), df.to_dict('records')
    return data, columns

def generate_type_data(data, columns):
    """
    Generate type data (numerical, categorical, etc) based on given data.
    """
    df = pd.DataFrame(data, columns=columns)
    dtypes = df.convert_dtypes().dtypes.to_dict()
    
    translate_dtypes = {
        'string':'categorical', 
        'float64':'numerical', 
        'Int64':'numerical'
    }
    
    dtypes = {col: translate_dtypes[dtype.name] for col,dtype in dtypes.items()}
    
    return dtypes

def get_df(dataset):
    # f = open("."+dataset.file.url, 'r', encoding="utf8")
    # file = File(f)
    # df = pd.read_csv(file)
    df = pd.read_csv(dataset.file.url)
    df.fillna(0, inplace=True)
    
    return df

def get_request_body(request):
    
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    
    return body

def get_request_params(request):
    return json.loads(request.query_params.dict()['0'])
    