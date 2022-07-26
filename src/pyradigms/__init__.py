"""Docstring describing pyradigms"""
import logging
import re
import sys
from io import StringIO
from pathlib import Path
from typing import Dict
from typing import List
import colorlog
import numpy as np
import pandas as pd
from attrs import Factory
from attrs import define


handler = colorlog.StreamHandler(None)
handler.setFormatter(
    colorlog.ColoredFormatter("%(log_color)s%(levelname)-7s%(reset)s %(message)s")
)
log = logging.getLogger(__name__)
log.propagate = True
log.addHandler(handler)


person_values = ["1", "2", "3", "1+3", "1+2"]


def format_person_values(string, sep):
    for val in person_values:
        if val in string:
            string = string.replace(val + sep, val)
    return string


# cast parameters to list
def listify(var):
    if not isinstance(var, list) and not isinstance(var, tuple):
        return [var]
    return var


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
        log.warning(f"Fewer values ({parameter_list}) than specified: {parameters}")
        for i in range(0, len(parameters) - len(parameter_list)):
            del i
            parameter_list.append(None)
    elif len(parameter_list) > len(parameters):
        log.error(f"More values than specified: {parameters} {parameter_list}")
        sys.exit(1)
    return parameter_list


@define
class Pyradigm:
    """A pyradigm instance holds the data underlying paradigms, as well as parameters
    and methods used to generate them.

    """

    entries: pd.DataFrame = None
    x: List[str] = Factory(list)
    y: List[str] = Factory(list)
    z: List[str] = Factory(list)
    x_sort: List[str] = Factory(list)
    y_sort: List[str] = Factory(list)
    sort_orders: Dict = Factory(dict)
    filters: Dict = Factory(dict)
    ignore: List[str] = Factory(list)
    with_multi_index = False
    separators = ["."]
    value_joiner = "."
    category_joiner = " / "
    print_column: str = None
    output_folder = None

    def __attrs_post_init__(self):
        if not self.print_column:
            self.print_column = "Form"

    @property
    def parameters(self):
        parlist = list(self.entries.columns)
        parlist.remove(self.print_column)
        return parlist

    def _short_repr(self, df):
        return df.head().to_string() + f"\n({len(df)} entries)"

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame, data_format="wide", **kwargs):
        """Create a new Pyradigm from a pandas dataframe.

        :param df: a pandas dataframe containing the data in wide/unstacked format

        :return: a Pyradigm object
        """

        if data_format == "wide":
            return cls(entries=df, **kwargs)
        if data_format == "long":
            out = df.pivot(index="ID", columns="Parameter", values="Value")
            out.columns.name = None
            return cls(entries=out, **kwargs)
        if data_format == "paradigm":
            return cls(
                entries=cls.decompose_paradigm(cls, paradigm=df, **kwargs), **kwargs
            )
        log.error(f"Invalid format: {data_format}")
        sys.exit(1)

    @classmethod
    def from_csv(cls, path, data_format="wide", **kwargs):
        """Create a new Pyradigm from a CSV file.

        :param path: a path to a CSV file containing the data in wide/unstacked format

        :return: a Pyradigm object
        """
        if data_format in ["wide", "long"]:
            df = pd.read_csv(path, keep_default_na=False, dtype=str)
        elif data_format == "paradigm":
            df = pd.read_csv(path, keep_default_na=False, dtype=str, index_col=0)
        else:
            log.error(f"Invalid format: {data_format}")
            sys.exit(1)
        return cls.from_dataframe(df, data_format=data_format, **kwargs)

    @classmethod
    def from_text(cls, text, x_sep=",", y_sep="\n"):
        """Create a new Pyradigm from a string.

        :param text: a string containing the data in wide/unstacked format
        :param x_sep: how "cells" are horizontally separated
        :param y_sep: how "cells" are vertically separated

        :return: a Pyradigm object
        """
        df = pd.read_csv(
            StringIO(text), sep=x_sep, lineterminator=y_sep, index_col=0, dtype=str
        )
        return cls(df)

    def decompose_paradigm(self, paradigm, z_value=None, **kwargs):  # noqa
        """Important: the y axis labels must be the index, not the first column"""
        x = listify(kwargs.get("x", self.x))
        y = listify(kwargs.get("y", self.y))
        z = listify(kwargs.get("z", self.z))
        separators = kwargs.get("separators", self.separators)
        print_column = kwargs.get("print_column", "Form")
        z_value = z_value or paradigm.index.name

        # gather all parameter names from the defined axes
        # + the name of what's in the cells
        entries = pd.DataFrame(columns=z + x + y + [print_column])

        for i, (x_string, col) in enumerate(paradigm.iteritems()):
            for y_string, form in col.iteritems():
                x_values = get_parameter_values(x_string, x, separators)
                y_values = get_parameter_values(y_string, y, separators)
                param_list = x + y  # List of parameter names
                value_list = x_values + y_values  # List of parameter values
                if z:
                    param_list += z
                    value_list += [z_value]
                param_list += [print_column]
                value_list += [form]
                entries = pd.concat(
                    [
                        entries,
                        pd.DataFrame(dict(zip(param_list, value_list)), index=[i]),
                    ]
                )

        entries.dropna(subset=[print_column], inplace=True)  # …drop rows with no form
        entries.reset_index(drop=True, inplace=True)  # reset index
        entries.fillna("", inplace=True)
        return entries

    def to_markdown(self, data_format="paradigm", **kwargs):
        if data_format == "long":
            out = self.to_long()
            return out.to_markdown(index=False, **kwargs)
        if data_format == "paradigm":
            out = self.compose_paradigm(**kwargs)
            if isinstance(out, dict):
                mds = []
                for z, x in out.items():
                    x.index.name = z
                    mds.append(x.to_markdown(**kwargs))
                return "\n\n".join(mds)
        if data_format == "wide":
            return self.entries.to_markdown(index=False, **kwargs)
        log.error(f"Unknown format '{data_format}'.")
        sys.exit(1)

    def to_long(self):
        if "ID" not in self.entries.columns:
            self.entries[  # pylint: disable=unsupported-assignment-operation
                "ID"
            ] = self.entries.apply(lambda x: f"{x.name}-{x[self.print_column]}", axis=1)
        return pd.melt(
            self.entries,
            id_vars="ID",
            value_vars=self.parameters + [self.print_column],
            var_name="Parameter",
            value_name="Value",
        )

    def compose_paradigm(  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
        self, csv_output=None, **kwargs
    ):
        input_df = kwargs.get("input_df", self.entries)
        with_multi_index = kwargs.get("with_multi_index", self.with_multi_index)
        x = kwargs.get("x", self.x)
        y = kwargs.get("y", self.y)
        z = kwargs.get("z", self.z)
        filters = kwargs.get("filters", self.filters)
        ignore = listify(kwargs.get("ignore", self.ignore))
        separators = kwargs.get("separators", self.separators)
        value_joiner = kwargs.get("value_joiner", self.value_joiner)
        category_joiner = kwargs.get("category_joiner", self.category_joiner)
        print_column = kwargs.get("print_column", self.print_column)
        sort_orders = kwargs.get("sort_orders", self.sort_orders)
        output_folder = kwargs.get("output_folder", self.output_folder)
        if output_folder:
            output_folder = Path(output_folder)

        df = input_df.copy()
        df.replace(np.nan, "", inplace=True)
        log.debug(f"Composing a new paradigm from entries:\n{self._short_repr(df)}")

        # get a sensible default sort order for a given parameter (order in the input)
        def get_sort_order(parameter):
            val_list = list(df[parameter])
            val_list = [i for n, i in enumerate(val_list) if i not in val_list[:n]]
            log.debug(f"New sort order for {parameter}: {val_list}")
            return val_list

        x = listify(x)
        y = listify(y)
        z = listify(z)

        # check if all axes have valid parameters
        parameters = {"x": x, "y": y, "z": z}
        for k, v in parameters.items():
            remainders = set(v) - set(df.columns)
            if len(remainders) > 0:
                rstring = ", ".join(remainders)
                log.error(f"{k} axis contains inexistent parameter(s): {rstring}")
                sys.exit(1)

        # make sure that "Form" or whatever other column to print is present
        if print_column not in df.columns:
            log.error(f"'{print_column}' not found in dataframe columns")
            sys.exit(1)

        # inform user if there are columns they did not give directions for
        leftover_columns = set(df.columns) - set(x + y + z + [print_column])
        if len(leftover_columns) > 0:
            log.info(
                "You did not specify what should happen"
                " to the following columns/fields/parameters: %s",
                "\t".join(leftover_columns),
            )

        # only for debugging purposes
        filter_string = "\n".join(
            [f"\t{k}: {', '.join(v)}" for k, v in filters.items()]
        )
        log.debug(f"Filtering parameters:\n{filter_string}\n")

        # filter rows by fitler arg
        for col, values in filters.items():
            values = listify(values)
            df = df[df[col].isin(values)]
        log.debug("Filtered entries:\n%s", self._short_repr(df))

        # drop irrelevant columns
        if len(ignore) > 0:
            log.debug(f"""Ignoring parameters:\n{", ".join(ignore)}""")
            for col in ignore:
                df.drop(col, axis=1, inplace=True)
                log.debug("New entries:\n%s", self._short_repr(df))

        # join columns for the y axis
        def concat_values(row, values):
            out = ""
            for value in values:
                out += row[value]
                if row[value] not in person_values:
                    out += separators[0]
            return out.strip(separators[0]).replace(
                separators[0] + separators[0], separators[0]
            )

        new_z_id = separators[0].join(z)
        if len(z) > 1:
            df[new_z_id] = df.apply(concat_values, values=z, axis=1)

        if len(z) > 0:
            z_dict = dict(tuple(df.groupby(new_z_id)))
        else:
            z_dict = {"z": df}

        constructed_paradigms = {}
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        for z_key, df in z_dict.items():
            log.debug(
                f"Creating pivot table for x={x}, y={y}, cell values: {print_column}"
            )
            out = pd.pivot_table(
                df,
                values=print_column,
                index=y,
                columns=x,
                aggfunc=category_joiner.join,
            )

            # drop empty rows
            idx_name = out.index.names
            out.reset_index(inplace=True)  # use index as column
            out.replace(
                "", np.nan, inplace=True
            )  # replace all empty strings with NaN, so we can…
            out.dropna(how="all", inplace=True)  # …drop rows with no content whatsoever
            out.fillna(
                "", inplace=True
            )  # then add back the empty strings for exporting
            out.set_index(idx_name, drop=True, inplace=True)  # then add back the index

            # for those parameters lacking a specified sort order, establish a default
            for parameter in out.index.names + out.columns.names:
                df_sort = get_sort_order(parameter)
                if parameter not in sort_orders:
                    sort_orders[parameter] = df_sort
                elif set(sort_orders[parameter]) != set(df_sort):
                    log.error(
                        f"Specified order {sort_orders[parameter]} for parameter "
                        f"'{parameter}' does not cover all values: {df_sort}"
                    )
                    sys.exit(1)

            # sort x and y axis
            new_indices = []
            for idx in y:
                values = out.index.get_level_values(idx)
                new_indices.append(
                    pd.CategoricalIndex(
                        values, categories=sort_orders[idx], ordered=True
                    )
                )
            out.set_index(new_indices, inplace=True)
            out.sort_index(level=[c for c in sort_orders if c in y], inplace=True)

            new_columns = []
            for col in x:
                values = out.columns.get_level_values(col)
                new_columns.append(
                    pd.CategoricalIndex(
                        values, categories=sort_orders[col], ordered=True
                    )
                )
            out.columns = new_columns
            out.sort_index(
                level=[c for c in sort_orders if c in x], inplace=True, axis=1
            )

            if not with_multi_index:
                log.debug("Flattening multiindices")

                new_colindex_name = category_joiner.join(x)
                out.columns = [
                    format_person_values(value_joiner.join(col).strip(), value_joiner)
                    for col in out.columns.values
                ]
                out.columns.name = new_colindex_name

                new_index_name = category_joiner.join(y)
                out.index = [
                    format_person_values(
                        value_joiner.join(listify(col)).strip(), value_joiner
                    )
                    for col in out.index.values
                ]
                out.index.name = new_index_name

            constructed_paradigms[z_key] = out

        if csv_output:
            log.debug(f"Writing to {csv_output}")
            output = []
            for z_key, df in constructed_paradigms.items():
                s = StringIO()
                df.to_csv(s, index=True)
                output.append(s.getvalue())
            with open(csv_output, "w", encoding="utf-8") as file:
                file.write("\n".join(output))

        if output_folder:
            log.debug(f"Saving CSV files to {output_folder}")
            for z_key, df in constructed_paradigms.items():
                if z_key == "z":
                    filename = "generated_paradigm.csv"
                    idx_label = ""
                else:
                    filename = z_key + ".csv"
                    idx_label = z_key
                df.to_csv(output_folder / filename, index=True, index_label=idx_label)

        if len(constructed_paradigms) == 1:
            return list(constructed_paradigms.values())[0]
        return constructed_paradigms
