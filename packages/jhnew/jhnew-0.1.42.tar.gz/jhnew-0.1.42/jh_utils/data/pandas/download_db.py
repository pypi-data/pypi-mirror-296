from jh_utils.utils.os import create as create_file
import pandas as pd


def table_to_csv(table_name, schema_name, con_engine, directory=''):
    df = pd.read_sql_table(table_name, con=con_engine, schema=schema_name)
    df.to_csv(directory+table_name+'.csv', index=False)


def schema_to_csv(schema_name, db):
    ls_tables = db.get_tables(schema_name)

    folder_name = schema_name
    try:
        create_file(name=folder_name, is_folder=True)
    except Exception:
        print(Exception)
        pass
    for i in ls_tables:
        table_to_csv(table_name=i,
                     con_engine=db.engine(),
                     schema_name=schema_name, directory=folder_name+'/')
    print(0)
