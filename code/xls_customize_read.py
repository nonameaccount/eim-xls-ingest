import json
import pandas as pd
import xls_format


# zip_xxxxx_xxxx = lambda x: (str(int(x)//10000).zfill(5)+ "-" + str(int(x)%1000).zfill(4))
# round_2 = lambda x: ("{:.2f}".format(x))

def transpose_extract_data_as_csv(dir, file, sheet_name, skiprows, nbrofdatarows, nbr_cells_merged_for_column,
                                  table_name):
    dest = dir + table_name.replace(" ", "_")
    df = pd.read_excel(file, sheet_name=sheet_name, header=None, index_col=None, skiprows=skiprows, nrows=nbrofdatarows)
    df.apply(pd.Series.first_valid_index)
    df = df.fillna(method='ffill', axis=1)
    table_start = nbr_cells_merged_for_column - 2
    table_end = nbr_cells_merged_for_column - 1

    df_new = df[[table_start, table_end]].T
    print(df_new.index)
    print(df_new.columns)
    out = df_new.to_csv(dest, header=None, index=False)
    return out


def extract_data_as_csv(dir, file, sheet_name, cols, skiprows, table_name, dtype, converters, skipfooter, header,
                        csv_delimiter=","):
    dest = dir + table_name.replace(" ", "_")
    df = pd.read_excel(file, sheet_name=sheet_name, usecols=cols, skiprows=skiprows, skipfooter=skipfooter,
                       header=header,
                       dtype=dtype,
                       converters=converters
                       )
    df.fillna(method='ffill', axis=0)
    df.columns = df.columns.map(lambda x: x.replace("-", "_").replace(" ", "_").replace("(", "").replace(")", ""))
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.dropna(inplace=True)
    out = df.to_csv(dest, sep=csv_delimiter, index=False)
    return out


f = open('/Users/riley/git/EIM/eim-xls-ingest/config/process.config_json', "r")

execution_details = json.loads(f.read())

file = execution_details["s3_bucket_in"] + execution_details["s3_bucket_in_file"]
dir = execution_details["s3_bucket_out"]

for p in execution_details['processing']:
    if p["source_type"] == "merged-special":
        transpose_extract_data_as_csv(dir, file, p['sheet_name'], p['skiprows'], p['nbrofdatarows'],
                                      p['nbr_cells_merged_for_column'], p['table_name'])
    else:
        if 'converters' in p:
            converters = {}
            for k, v in p['converters'].items():
                converters[k] = xls_format.converter(v)
        else:
            converters = {}
        if 'dtype' in p:
            dtype = {}
            for k, v in p['dtype'].items():
                if v == 'round_2':
                    dtype[k] = xls_format.round_2
        else:
            dtype = {}

        if 'skipfooter' in p:
            skipfooter = p['skipfooter']
        else:
            skipfooter = 0

        if 'skiprows' in p:
            skiprows = p['skiprows']
        else:
            skiprows = 0

        if 'header' in p:
            header = p['header']
        else:
            header = 0

        extract_data_as_csv(dir, file, p['sheet_name'], p['cols'], skiprows, p['table_name'], dtype, converters,
                            skipfooter, header)
