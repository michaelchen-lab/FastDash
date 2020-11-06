import re
import pandas as pd

from .utils import num_millify, num_prettify

global TIME_FRAMES, DISPLAY_TIME_FRAMES

TIME_FRAMES = {
    "Year": "Y",
    "Quarter": "3M",
    "Month": "M"
}

DISPLAY_TIME_FRAMES = {
    "Year": "Y",
    "Quarter": "Q",
    "Month": "M"
}

def line_analytics(df: pd.DataFrame, params: dict) -> dict:
    
    # {'x-axis': {'column': 'timestamp', 'groupby': 'Year'}, 'y-axis': {'column': 'unit_price', 'groupby': 'Sum'}}
    
    x_axis_col = params['X-Axis']['Column']
    x_axis_groupby = params['X-Axis']['Groupby']
    y_axis_col = params['Y-Axis']['Column']
    y_axis_groupby = params['Y-Axis']['Groupby'].lower()
    
    try:
        df[x_axis_col] = pd.to_datetime(df[x_axis_col])
        df[y_axis_col] = pd.to_numeric(df[y_axis_col])
    except:
        return {"error": "Check that the columns have the right data type."}
    
    df.set_index(df[x_axis_col], inplace=True)
    data = df[y_axis_col].resample(TIME_FRAMES[x_axis_groupby]).agg(y_axis_groupby)
    data.index = data.index.to_period(DISPLAY_TIME_FRAMES[x_axis_groupby]).to_series().astype(str)
    data = data.astype(int)
    
    return data.to_dict()

def bar_analytics(df: pd.DataFrame, params: dict) -> dict:
    
    x_axis_col = params['X-Axis']['Column']
    x_axis_filter = params['X-Axis']['Filter']
    y_axis_col = params['Y-Axis']['Column']
    y_axis_groupby = params['Y-Axis']['Groupby'].lower()
    
    try:
        df[x_axis_col] = df[x_axis_col].astype(object)
        df[y_axis_col] = pd.to_numeric(df[y_axis_col])
    except:
        return {"error": "Check that the columns have the right data type."}
    
    data = df[[x_axis_col, y_axis_col]].groupby(x_axis_col).agg(y_axis_groupby)
    data = data.sort_values(by=y_axis_col, ascending=False)
    
    if 'Top' in x_axis_filter:
        return data[y_axis_col].head(int(re.findall('\d+', x_axis_filter)[0])).to_dict()
    else:
        return data[y_axis_col].tail(int(re.findall('\d+', x_axis_filter)[0])).to_dict()

def value_analytics(df: pd.DataFrame, params: dict) -> str:
    
    column = params['Measure']['Column']
    measure = params['Measure']['Metric'].lower()
    format = params['Measure']['Format']
    
    value = df[column].agg(measure)
    if format == "Full Number":
        return num_prettify("{:.2f}".format(value))
    else:
        return num_millify("{:.2f}".format(value))
