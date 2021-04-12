import pandas as pd
import numpy as np
import re
from io import StringIO
import logging
logger = logging.getLogger("pyradigms")
logging.basicConfig(level="ERROR")

person_values = ["1", "2", "3", "1+3", "1+2"]
content_string = "Form"
separators = ["."]
x = []
y = []
z = []
x_sort = []
y_sort = []
filters = {}
ignore = []

def decompose_paradigm(paradigm, z_value=None):
    if not z_value:
        z_value = paradigm.index.name
        
    def get_parameter_values(string, parameters):
        parameter_list = re.split('|'.join(map(re.escape, separators)),string)
        parameter_list = [x for x in parameter_list if x] #Remove leftovers of separation
        new_parameter_list = []
        for param in parameter_list:
            p_hit = False
            for p_v in sorted(person_values, key=len, reverse=True):
                if p_v in param:
                    new_parameter_list += list(filter(None, list(param.partition(p_v))))
                    p_hit = True
                    break
            if not p_hit: new_parameter_list.append(param)
        parameter_list = new_parameter_list
        if len(parameter_list) < len(parameters):
            for i in range(0,len(parameters)-len(parameter_list)):
                parameter_list.append(None)
        elif len(parameter_list) > len(parameters):
            print("ERROR")
            print(parameter_list)
            print(parameters)
        return parameter_list
    
    entries = pd.DataFrame(columns=z+x+y+[content_string])
    for x_string, row in paradigm.iteritems():
        for y_string, form in row.iteritems():
            x_values = get_parameter_values(x_string, x)
            y_values = get_parameter_values(y_string, y)
            param_list = x+y  #List of parameter names
            value_list = x_values+y_values #List of parameter values
            if z:
                param_list += z
                value_list += [z_value]
            param_list += [content_string]
            value_list += [form]
            out_dict = dict(zip(
                    param_list,
                    value_list
                ))
            entries = entries.append(
                out_dict,
                ignore_index=True,
            )
    entries.dropna(subset=[content_string], inplace=True) # …drop rows with no form
    entries.reset_index(drop=True, inplace=True) # reset index
    entries.fillna("",inplace=True)
    return entries

def decompose_from_csv(csvfile):
    dfull = open(csvfile).read()
    return decompose_from_text(dfull)
    
def decompose_from_text(string):
    full = pd.DataFrame(columns=x)
    strings = string.split("\n\n")
    for df_string in strings:
        paradigm = pd.read_csv(StringIO(df_string), dtype=str, index_col=0)
        if paradigm.index.name:
            z_value = paradigm.index.name
        else:
            z_value = ""
        paradigm.index = [str(x) for x in paradigm.index]
        full = full.append(decompose_paradigm(paradigm, z_value=z_value))
    full.reset_index(drop=True, inplace=True)
    return full

def compose_from_text(df_string, csv_output=None):
    entries = pd.read_csv(StringIO(df_string), dtype=str, keep_default_na=False)
    return compose_paradigm(entries, csv_output = csv_output)

def compose_from_csv(csvfile, csv_output=None):
    entries = pd.read_csv(csvfile, dtype=str, keep_default_na=False)
    return compose_paradigm(entries, csv_output = csv_output)

def compose_paradigm(input_df, csv_output = None):
    logger.debug("Composing a new paradigm from entries:")
    df = input_df.copy()
    df.replace(np.nan, "", inplace=True)
    
    logger.debug(df.head())

    for col, values in filters.items():
        df = df[df[col].isin(values)]
    
    for col in ignore:
        df.drop(col, axis=1, inplace=True)
        
    def concat_values(row, values):
        out = ""
        for value in (values):
            out += row[value]
            if row[value] not in person_values: out += separators[0]
        return out.strip(separators[0]).replace(separators[0]+separators[0],separators[0])
    
    logger.debug("Composing y id…")
    new_y_id = separators[0].join(y)
    if len(y) > 1:
        df[new_y_id] = df.apply(concat_values, values=y, axis=1)
    logger.debug(new_y_id)
    
    new_x_id = separators[0].join(x)
    if len(x) > 1: df[new_x_id] = df.apply(concat_values, values=x, axis=1)
    
    new_z_id = separators[0].join(z)
    if len(z) > 1: df[new_z_id] = df.apply(concat_values, values=z, axis=1)
    
    if len(z) > 0:
        z_dict = dict(tuple(df.groupby(new_z_id)))
    else:
        z_dict = {"z": df}

    constructed_paradigms = {}
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    for z_key, df in z_dict.items():
        logger.debug(f"Creating pivot table for {z_key}, using {new_x_id} for x axis and {new_y_id} for y axis")
        out = pd.pivot_table(
            df,
            values=content_string,
            index=new_y_id,
            columns=new_x_id,
            aggfunc=lambda x: "/".join(x)
        )
        out.rename_axis(None, axis="columns", inplace=True) # remove column labels
        if len(z_dict) == 1:
            out.index.name = new_y_id
        else:
            out.index.name = z_key
        
        idx_name = out.index.name
        out.reset_index(inplace=True) # use index as column
        out.replace("", np.nan, inplace=True) # replace all empty strings with NaN, so we can…
        out.dropna(how="all", inplace=True) # …drop rows with no content whatsoever
        out.fillna("", inplace=True) # then add back the empty strings for exporting
        out.set_index(idx_name, drop=True, inplace=True)# then add back the index
        out = out.reindex([value for value in y_sort if value in out.index] + list(set(list(out.index)) - set(y_sort))) # sort index by specified order, put leftovers at the end
        comp_x_sort = x_sort + list(set(list(out.columns)) - set(x_sort))        #sort columns, too
        comp_x_sort = dict(zip(comp_x_sort, range(len(comp_x_sort))))
        out = out[sorted(out.columns, key=lambda x: comp_x_sort[x])]
        constructed_paradigms[z_key] = out
    if csv_output:
        output = []
        for df in constructed_paradigms.values():
            s = StringIO()
            df.to_csv(s, index=True)
            output.append(s.getvalue())
        with open(csv_output, 'w') as file:
            file.write("\n".join(output))
    if len(constructed_paradigms) == 1:
        return constructed_paradigms["z"]
    else:
        return constructed_paradigms
        
        
#TEST CODE
# separators = ["."]
# person_values = ["1", "2", "3", "1+3", "1+2"]
#
# def get_parameter_values(string, parameters):
#     parameter_list = re.split('|'.join(map(re.escape, separators)),string)
#     parameter_list = [x for x in parameter_list if x] #Remove leftovers of separation
#     new_parameter_list = []
#     for param in parameter_list:
#         p_hit = False
#         for p_v in sorted(person_values, key=len, reverse=True):
#             if p_v in param:
#                 new_parameter_list += list(filter(None, list(param.partition(p_v))))
#                 p_hit = True
#                 break
#         if not p_hit: new_parameter_list.append(param)
#     parameter_list = new_parameter_list
#     if len(parameter_list) < len(parameters):
#         for i in range(0,len(parameters)-len(parameter_list)):
#             parameter_list.append(None)
#     elif len(parameter_list) > len(parameters):
#         print("ERROR")
#         print(parameter_list)
#         print(parameters)
#     return parameter_list
#
# a = "1+2PL.IPFV"
# b = ['Person', 'Number', "Aspect"]
# print(get_parameter_values(a, b))