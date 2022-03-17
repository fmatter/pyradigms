import pandas as pd
import numpy as np
import re
from io import StringIO
import logging
from clldutils.loglib import Logging, get_colorlog
import sys
from attrs import define, Factory
from typing import List, Dict

person_values = ["1", "2", "3", "1+3", "1+2"]
content_string = "Form"
# separators = ["."]
x = []
y = []
z = []
x_sort = []
y_sort = []
sort_orders = {}
filters = {}
ignore = []


@define
class Pyradigm:
    entries: pd.DataFrame = None
    x: List[str] = Factory(list)
    y: List[str] = Factory(list)
    z: List[str] = Factory(list)
    x_sort: List[str] = Factory(list)
    y_sort: List[str] = Factory(list)
    sort_orders: Dict = Factory(dict)
    filters: Dict = Factory(dict)
    ignore: List[str] = Factory(list)
    separators: List[str] = Factory(list)
    log_level: str = None
    logger = get_colorlog(__name__, sys.stdout, level="DEBUG")
    joiner = "/"
    content_string: str = "Form"

    def __attrs_post_init__(self):
        if self.log_level is not None:
            self.logger.setLevel(self.log_level)
        if self.separators is None or self.separators == []:
            self.separators = ["."]

    @property    
    def parameters(self):
        l = list(self.entries.columns)
        l.remove(self.content_string)
        return l

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame, format="wide", **kwargs):
        """Create a new Pyradigm from a pandas dataframe.

        :param df: a pandas dataframe containing the data in wide/unstacked format

        :return: a Pyradigm object
        """

        if format=="wide":
            return cls(entries=df, **kwargs)
        elif format=="long":
            print(df)
            return df
        elif format=="paradigm":
            return cls(entries=cls.decompose_paradigm(cls, paradigm=df,**kwargs), **kwargs)

    @classmethod
    def from_csv(cls, path, format="wide", **kwargs):
        """Create a new Pyradigm from a CSV file.

        :param path: a path to a CSV file containing the data in wide/unstacked format

        :return: a Pyradigm object
        """
        df = pd.read_csv(path, keep_default_na=False, dtype=str)
        if format=="wide":
            return cls(entries=df, **kwargs)
        elif format=="long":
            print(df)
            print(df.pivot(index="Form", columns="Parameter")["Value"])
        elif format=="paradigm":
            df.set_index(df.columns[0], inplace=True)
            return cls(entries=cls.decompose_paradigm(cls, paradigm=df,**kwargs), **kwargs)
    
    def decompose_paradigm(self, paradigm, x, y, separators=["."], z_value=None, **kwargs):
        if not z_value:
            z_value = paradigm.index.name
    
        entries = pd.DataFrame(columns=z + x + y + [content_string])
        for x_string, row in paradigm.iteritems():
            for y_string, form in row.iteritems():
                x_values = get_parameter_values(x_string, x, separators)
                y_values = get_parameter_values(y_string, y, separators)
                param_list = x + y  # List of parameter names
                value_list = x_values + y_values  # List of parameter values
                if z:
                    param_list += z
                    value_list += [z_value]
                param_list += [content_string]
                value_list += [form]
                out_dict = dict(zip(param_list, value_list))
                entries = entries.append(
                    out_dict,
                    ignore_index=True,
                )
        entries.dropna(subset=[content_string], inplace=True)  # …drop rows with no form
        entries.reset_index(drop=True, inplace=True)  # reset index
        entries.fillna("", inplace=True)
        return entries

    @classmethod
    def from_text(cls, text, x_sep=",", y_sep="\n"):
        """Create a new Pyradigm from a string.

        :param text: a string containing the data in wide/unstacked format
        :param x_sep: how "cells" are horizontally separated
        :param y_sep: how "cells" are vertically separated

        :return: a Pyradigm object
        """
        df = pd.read_csv(StringIO(text), sep=x_sep, lineterminator=y_sep)
        return cls(df)

    def to_markdown(self, format="paradigm", **kwargs):
        if format == "long":
            out = self.to_long()
        elif format == "paradigm":
            out = self.compose_paradigm(**kwargs)
        elif format == "wide":
            out = self.entries
        return out.to_markdown()

    def to_long(self):
        return pd.melt(self.entries, id_vars=self.content_string, value_vars=self.parameters, var_name="Parameter", value_name="Value").drop_duplicates()

    def compose_paradigm(
        self,
        input_df=None,
        csv_output=None,
        multi_index=False,
        x=None,
        y=None,
        z=None,
        x_sort=None,
        y_sort=None,
        filters=None,
        ignore=None,
        separators=None,
        joiner=None,
        content_string=None
    ):
        if input_df is None:
            input_df = self.entries
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        if z is None:
            z = self.z
        if x_sort is None:
            x_sort = self.x_sort
        if y_sort is None:
            y_sort = self.y_sort
        if filters is None:
            filters = self.filters
        if ignore is None:
            ignore = self.ignore
        if separators is None:
            separators = self.separators
        if joiner is None:
            joiner = self.joiner
        if content_string is None:
            content_string = self.content_string

        df = input_df.copy()
        df.replace(np.nan, "", inplace=True)
        self.logger.debug("Composing a new paradigm from entries:\n" + _short_repr(df))


        # cast parameters to list
        def listify(var):
            if type(var) != list:
                return [var]
            else:
                return var

        x = listify(x)
        y = listify(y)
        z = listify(z)
            
        # check if all axes have valid parameters
        parameters = {"x": x, "y": y, "z": z}
        for k, v in parameters.items():
            remainders = set(v) - set(df.columns)
            if len(remainders) > 0:
                self.logger.error(f"{k} axis contains inexistent parameter(s): {', '.join(remainders)}")
                return None

        # make sure that "Form" or whatever other content string is present
        if content_string not in df.columns:
            self.logger.error(f"String {content_string} is not found in dataframe columns")
            return None


        filter_string = "\n".join(
            [f"\t{k}: {', '.join(v)}" for k, v in filters.items()]
        )
        self.logger.debug(f"Filtering parameters:\n" + filter_string + "\n")
        for col, values in filters.items():
            if type(values) != list:
                values = [values]
            df = df[df[col].isin(values)]
        self.logger.debug("New entries:\n" + _short_repr(df))

        if len(ignore) > 0:
            self.logger.debug(f"Ignoring parameters:\n" + ", ".join(ignore))
            for col in ignore:
                df.drop(col, axis=1, inplace=True)
                self.logger.debug("New entries:\n" + _short_repr(df))

        def concat_values(row, values):
            out = ""
            for value in values:
                out += row[value]
                if row[value] not in person_values:
                    out += separators[0]
            return out.strip(separators[0]).replace(
                separators[0] + separators[0], separators[0]
            )

        new_y_id = separators[0].join(y)
        self.logger.debug(f"New y id: [{new_y_id}]")
        if len(y) > 1 and not multi_index:
            df[new_y_id] = df.apply(concat_values, values=y, axis=1)

        new_x_id = separators[0].join(x)
        self.logger.debug(f"New x id: [{new_x_id}]")
        if len(x) > 1 and not multi_index:
            df[new_x_id] = df.apply(concat_values, values=x, axis=1)

        new_z_id = separators[0].join(z)
        if len(z) > 1:
            self.logger.debug(f"New z id: [{new_z_id}]")
            df[new_z_id] = df.apply(concat_values, values=z, axis=1)

        if len(z) > 0:
            z_dict = dict(tuple(df.groupby(new_z_id)))
        else:
            z_dict = {"z": df}

        constructed_paradigms = {}
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        for z_key, df in z_dict.items():
            self.logger.debug(
                f"Creating pivot table for [{z_key}], using [{new_x_id}] for x axis and [{new_y_id}] for y axis"
            )
            if multi_index:
                out = pd.pivot_table(
                    df,
                    values=content_string,
                    index=y,
                    columns=x,
                    aggfunc=lambda x: joiner.join(x),
                )
            else:
                out = pd.pivot_table(
                    df,
                    values=content_string,
                    index=new_y_id,
                    columns=new_x_id,
                    aggfunc=lambda x: joiner.join(x),
                )
            if not multi_index:
                out.rename_axis(
                    None, axis="columns", inplace=True
                )  # remove column labels
            if len(z_dict) == 1:
                out.index.name = new_y_id
            else:
                out.index.name = z_key

            if multi_index:
                idx_name = out.index.names
            else:
                idx_name = out.index.name
            out.reset_index(inplace=True)  # use index as column
            out.replace(
                "", np.nan, inplace=True
            )  # replace all empty strings with NaN, so we can…
            out.dropna(how="all", inplace=True)  # …drop rows with no content whatsoever
            out.fillna(
                "", inplace=True
            )  # then add back the empty strings for exporting
            out.set_index(idx_name, drop=True, inplace=True)  # then add back the index
            out.index.name = ""
            if not multi_index:
                out = out.reindex(
                    [value for value in y_sort if value in out.index]
                    + list(set(list(out.index)) - set(y_sort))
                )  # sort index by specified order, put leftovers at the end
                comp_x_sort = x_sort + list(
                    set(list(out.columns)) - set(x_sort)
                )  # sort columns, too
                comp_x_sort = dict(zip(comp_x_sort, range(len(comp_x_sort))))
                out = out[sorted(out.columns, key=lambda x: comp_x_sort[x])]
            else:
                new_indices = []
                for lvl_c in range(0, out.index.nlevels):
                    values = out.index.get_level_values(y[lvl_c])
                    if y[lvl_c] in sort_orders:
                        new_indices.append(
                            pd.CategoricalIndex(
                                values, categories=sort_orders[y[lvl_c]], ordered=True
                            )
                        )
                    else:
                        new_indices.append(pd.CategoricalIndex(values))
                out.set_index(new_indices, inplace=True)
                out.sort_index(inplace=True)

                new_columns = []
                for lvl_c in range(0, out.columns.nlevels):
                    values = out.columns.get_level_values(x[lvl_c])  # != ""
                    if x[lvl_c] in sort_orders:
                        new_columns.append(
                            pd.CategoricalIndex(
                                values, categories=sort_orders[x[lvl_c]], ordered=True
                            )
                        )
                    else:
                        new_columns.append(pd.CategoricalIndex(values))
                out.columns = new_columns
                out.sort_index(inplace=True, axis=1)
                # print(out.columns.to_frame())
                # print(out.columns)
                # s = pd.Series(out.columns)
                # s = s.fillna('unnamed:' + (s.groupby(s.isnull()).cumcount() + 1).astype(str))
                # out.columns = s

            constructed_paradigms[z_key] = out
        if csv_output:
            output = []
            for df in constructed_paradigms.values():
                s = StringIO()
                df.to_csv(s, index=True)
                output.append(s.getvalue())
            with open(csv_output, "w") as file:
                file.write("\n".join(output))
        if len(constructed_paradigms) == 1:
            return constructed_paradigms["z"]
        else:
            return constructed_paradigms


def get_parameter_values(string, parameters, separators):
    parameter_list = re.split("|".join(map(re.escape, separators)), string)
    parameter_list = [x for x in parameter_list if x]  # Remove leftovers of separation
    new_parameter_list = []
    for param in parameter_list:
        p_hit = False
        for p_v in sorted(person_values, key=len, reverse=True):
            if param.startswith(p_v):
                new_parameter_list += list(filter(None, list(param.partition(p_v))))
                p_hit = True
                break
        if not p_hit:
            new_parameter_list.append(param)
    parameter_list = new_parameter_list
    if len(parameter_list) < len(parameters):
        for i in range(0, len(parameters) - len(parameter_list)):
            parameter_list.append(None)
    elif len(parameter_list) > len(parameters):
        print("ERROR")
        print(parameter_list)
        print(parameters)
    return parameter_list


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
    return compose_paradigm(entries, csv_output=csv_output)


def compose_from_csv(csvfile, csv_output=None):
    entries = pd.read_csv(csvfile, dtype=str, keep_default_na=False)
    return compose_paradigm(entries, csv_output=csv_output)


def _short_repr(df):
    return df.head().to_string() + f"\n({len(df)} entries)"


# TEST CODE
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
