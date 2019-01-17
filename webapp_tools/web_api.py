import sqlite3
import pandas as pd
from io import BytesIO
from pandas import ExcelWriter

def build_filters(suburb=None,beds=None,prop_type=None,prop_dates=None,state=None):
    filter_str = []
    if suburb is not None:
        filter_str += ["Suburb in ('{}')".format("','".join(suburb))]
    if beds is not None:
        filter_str += ['Beds in ({})'.format(",".join([str(x) for x in beds]))]
    if prop_type is not None:
        filter_str += ["Type in ('{}')".format("','".join(prop_type))]
    if prop_dates is not None:
        filter_str += ["Date between '{}' and '{}'".format(prop_dates[0],prop_dates[1])]
    if state is not None:
        filter_str += ["State in ('{}')".format("','".join(state))]
        
    if len(filter_str):
        filter_str = 'where ' + ' and '.join(filter_str) 
    else:
        filter_str = ''
    return filter_str

def extract_options(**filters):
    # Compile and execute query
    sql = 'select distinct Suburb, Beds, Type, State from auction_data'
    sql = ' '.join([sql,build_filters(**filters)])
    with sqlite3.connect('data/real_estate.db') as db:
        df = pd.read_sql(sql=sql,con=db)
        
    # Sort states
    location_cols = {}
    for state in df.loc[:,'State'].unique():
        location_cols[state] = df.loc[df.loc[:,'State']==state,'Suburb'].unique().tolist()
    
    # Sort remaining
    df = df.drop(['State','Suburb'],axis=1).dropna().drop_duplicates()
    out_col = {'location':location_cols}
    for col in df.columns:
        out_col[col] = sorted(df.loc[:,col].dropna().unique().tolist())
    return out_col

def return_data(**filters):
    sql = 'select distinct Suburb, Address, Price, Beds, Type, Result, Date, Agent, State, url from auction_data'
    sql = ' '.join([sql,build_filters(**filters)])
    with sqlite3.connect('data/real_estate.db') as db:
        df = pd.read_sql(sql=sql,con=db)
    return [x.to_json() for x,_ in df.iterrows()]

def return_excel_output(**filters):
    df = return_data(**filters)
    output = BytesIO()
    writer = ExcelWriter(output,enginer='xlsxwriter')
    df.to_excel(writer,sheetname='Quote Output',index=False)
    writer.save()
    return output.getvalue()