import pandas as pd

def read_data(csv, required_fields):
    csv_df = pd.read_csv(csv)
    for col in required_fields:
        if col not in set(csv_df.columns.values):
            raise Exception(f'{csv} missing required columns.')
    
    return csv_df

def clean_data_strip(df):
    str_cols = [col for col, dt in df.dtypes.items() if dt == 'object']
    for col in str_cols:
            df[col] = df[col].str.strip()
    return df

def clean_data_lower(df):
    str_cols = [col for col, dt in df.dtypes.items() if dt == 'object']
    for col in str_cols:
            df[col] = df[col].str.lower()
    return df

def clean_data(df, flag_lower):
    df_cleaned = clean_data_strip(df)
    if flag_lower:
        df_cleaned = clean_data_lower(df_cleaned)
    return df_cleaned

def write_logs(output_file, log_stream):
    log = open(output_file, 'w+')
    log.writelines(log_stream)
    log.close()
