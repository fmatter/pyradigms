"""This is the main pyradigms module"""
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


__author__ = "Florian Matter"
__email__ = "florianmatter@gmail.com"
__version__ = "0.1.0"


handler = colorlog.StreamHandler(None)
handler.setFormatter(
    colorlog.ColoredFormatter("%(log_color)s%(levelname)-7s%(reset)s %(message)s")
)
log = logging.getLogger(__name__)
log.propagate = True
log.addHandler(handler)
log.setLevel(logging.INFO)


person_values = ["1", "2", "3", "1+3", "1+2"]


def _format_person_values(string, sep):
    for val in person_values:
        if val in string:
            string = string.replace(val + sep, val)
    return string


def _listify(var):
    if not isinstance(var, list) and not isinstance(var, tuple):
        return [var]
    return var


def _get_parameter_values(string, parameters, separators):
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
    """Pyradigm instances hold the data from which paradigms are created, as well as
    parameters and methods used to generate them.
    """

    entries: pd.DataFrame = None
    """The data in a wide format pandas DataFrame"""
    x: List[str] = Factory(list)
    """The parameters to be represented on the x axis"""
    y: List[str] = Factory(list)
    """The parameters to be represented on the y axis"""
    z: List[str] = Factory(list)
    """The parameters to be represented on the z axis"""
    sort_orders: Dict = Factory(dict)
    """Pass parameter names as keys, ordered value lists as values.
    Example: ``{"Number": ["SG", "DU", "PL"]}``"""
    filters: Dict = Factory(dict)
    """Pass parameter names as keys, value lists to be filtered as values.
    Example: ``{"Number": ["SG", "DU"]}``"""
    ignore: List[str] = Factory(list)
    """Parameters which will be ignored completely."""
    with_multi_index = False
    """If False, the value labels for categories sharing an axis will be joined in
    single cells.
    If True, a pandas ``MultiIndex`` will be used."""
    separators = ["."]
    """The first item is used to concatenate labels of values combined in a column or
    row label.
    Subsequent items are only used when decomposing paradigms."""
    category_joiner = " / "
    """The string used to concatenate labels of categories combined on an axis."""
    print_column: str = "Form"
    """The column in wide format which holds the values in the cells
    (usually forms or IDs)"""
    output_folder = None
    """The folder into which generated paradigms will be written."""

    @property
    def _parameters(self):
        parlist = list(self.entries.columns)
        parlist.remove(self.print_column)
        return parlist

    @property
    def _short_repr(self):
        return self.entries.head().to_string() + f"\n({len(self.entries)} entries)"

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame, data_format="wide", **kwargs):
        """Create a new Pyradigm from a pandas dataframe.

        Args:
            df (DataFrame): a pandas dataframe containing the data in wide format

        Returns:
            a :class:`.Pyradigm` object
        """

        if data_format == "wide":
            return cls(entries=df, **kwargs)
        if data_format == "long":
            out = df.pivot(index="ID", columns="Parameter", values="Value")
            out.columns.name = None
            return cls(entries=out, **kwargs)
        if data_format == "paradigm":
            return cls(entries=cls.decompose_paradigm(cls, paradigm=df, **kwargs))
        log.error(f"Invalid format: {data_format}")
        sys.exit(1)

    @classmethod
    def from_csv(cls, path, data_format="wide", **kwargs):
        """Create a new Pyradigm object from a CSV file.

        Args:
            path (str): path to the CSV file to be read
            data_format (str):
                * ``"wide"`` (default): Parameters in columns, entries in rows.
                * ``"long"``: Columns: ID, Parameter, Value
                * ``"paradigm"``: Decompose a paradigm by specifying at least x and y\
         (kwargs are passed to :meth:`.Pyradigm.decompose_paradigm`)

        Returns:
            a :class:`.Pyradigm` object
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
        """Create a new Pyradigm object from a string.

        Args:
            text (str): a string containing the data in wide format
            x_sep (str): how columns are separated
            y_sep (str): how rows are separated

        Returns:
            a :class:`.Pyradigm` object
        """
        df = pd.read_csv(
            StringIO(text), sep=x_sep, lineterminator=y_sep, index_col=0, dtype=str
        )
        return cls(df)

    def decompose_paradigm(self, paradigm, z_value=None, **kwargs):  # noqa
        """Decompose a paradigm by specifying the parameters shown on the x and y axes.

        Args:
            paradigm (DataFrame): The paradigm as a pandas DataFrame.
                Note: the y axis labels of the **must be the index**, not the first
                column. To achieve that, use
                ``pd.read_csv("file.csv", dtype=str, index_col=0)``
                or ``df.set_index()``
            x (list): The parameters shown on the x axis (columns)
            y (list): The parameters shown on the y axis (index)
            separators (list): Strings by which x and y labels (combined categories)
                will be split.
            print_column (str): Name of the column where paradigm cells will be stored.
            z_value (str): if a z parameter is specified for the paradigm to be
                decomposed, you can assign a value manually.

        Returns: a `pandas DataFrame\
        <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_ object
        """
        x = _listify(kwargs.get("x", self.x))
        y = _listify(kwargs.get("y", self.y))
        z = _listify(kwargs.get("z", self.z))
        separators = kwargs.get("separators", self.separators)
        print_column = kwargs.get("print_column", "Form")
        z_value = z_value or paradigm.index.name

        # gather all parameter names from the defined axes
        # + the name of what's in the cells
        entries = pd.DataFrame(columns=z + x + y + [print_column])

        for i, (x_string, col) in enumerate(paradigm.items()):
            for y_string, form in col.items():
                x_values = _get_parameter_values(x_string, x, separators)
                y_values = _get_parameter_values(y_string, y, separators)
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

    def to_markdown(self, data_format="paradigm", pyd_kwargs=None, **kwargs):
        """Print a markdown representation of the data. **kwargs are passed to pandas'\
        `to_markdown <https://pandas.pydata.org/docs/reference\
/api/pandas.DataFrame.to_markdown.html>`_ and to\
        `tabulate <https://pypi.org/project/tabulate/>`_, so you can use ``tablefmt``.

        Args:
            data_format (str):
                * ``"paradigm"`` (default): The data rendered as a paradigm.
                * ``"wide"``: Parameters in columns, entries in rows.
                * ``"long"``: Columns: ID, Parameter, Value
            pyd_kwargs (dict): Any parameters to be passed to\
            :meth:`.Pyradigm.compose_paradigm` if ``data_format=="paradigm"``

        Returns:
            A markdown string.
        """
        pyd_kwargs = pyd_kwargs or {}
        if data_format == "long":
            out = self.to_long()
            return out.to_markdown(index=False, **kwargs)
        if data_format == "paradigm":
            out = self.compose_paradigm(**pyd_kwargs)
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
        """Arrange the entries in\
        `long <https://en.wikipedia.org/wiki/Wide_and_narrow_data#Narrow>`_ format.
        If there is no column ``ID``, one will be created.

        Returns: a `pandas DataFrame <https://pandas.pydata.org\
/docs/reference/api/pandas.DataFrame.html>`_ object"""
        if "ID" not in self.entries.columns:
            self.entries[  # pylint: disable=unsupported-assignment-operation
                "ID"
            ] = self.entries.apply(lambda x: f"{x.name}-{x[self.print_column]}", axis=1)
        return pd.melt(
            self.entries,
            id_vars="ID",
            value_vars=self._parameters + [self.print_column],
            var_name="Parameter",
            value_name="Value",
        )

    def _print_cell_string(self, series, category_joiner):
        return category_joiner.join(series.unique())

    def compose_paradigm(  # pylint: disable=too-many-locals
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements
        self,
        csv_output=None,
        **kwargs,
    ):
        """The central function of pyradigms, creating paradigms. In addition to the list
        below, **you can pass any
        argument described for the** :class:`.Pyradigm` **class**.

        Args:
            csv_output (str): CSV file to save paradigm to.

        Returns:
           If one paradigm is generated, a pandas DataFrame.
           If multiple paradigms are generated, a dict of DataFrames."""
        input_df = kwargs.get("input_df", self.entries)
        with_multi_index = kwargs.get("with_multi_index", self.with_multi_index)
        x = kwargs.get("x", self.x)
        y = kwargs.get("y", self.y)
        z = kwargs.get("z", self.z)
        filters = kwargs.get("filters", self.filters)
        ignore = _listify(kwargs.get("ignore", self.ignore))
        separators = kwargs.get("separators", self.separators)
        category_joiner = kwargs.get("category_joiner", self.category_joiner)
        print_column = kwargs.get("print_column", self.print_column)
        sort_orders = kwargs.get("sort_orders", self.sort_orders)
        output_folder = kwargs.get("output_folder", self.output_folder)
        decorate_x = kwargs.get("decorate_x", lambda x: x)
        decorate_y = kwargs.get("decorate_y", lambda y: y)
        decorate = kwargs.get("decorate", lambda x: x)
        if output_folder:
            output_folder = Path(output_folder)

        df = input_df.copy()
        df.replace(np.nan, "", inplace=True)
        log.debug(f"Composing a new paradigm from entries:\n{self._short_repr}")

        # get a sensible default sort order for a given parameter (order in the input)
        def get_sort_order(parameter):
            if parameter in filters:
                return filters[parameter]
            val_list = list(dict.fromkeys(list(df[parameter])))
            log.debug(f"New sort order for {parameter}: {val_list}")
            return val_list

        x = _listify(x)
        y = _listify(y)
        z = _listify(z)

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
        leftover_columns = set(df.columns) - set(x + y + z + [print_column]) - set(ignore)
        if len(leftover_columns) > 0:
            log.info(
                "You did not specify what should happen"
                " to the following columns/fields/parameters: %s",
                ", ".join(leftover_columns),
            )

        # only for debugging purposes
        filter_string = "\n".join(
            [f"\t{k}: {', '.join(v)}" for k, v in filters.items()]
        )
        log.debug(f"Filtering parameters:\n{filter_string}\n")

        # filter rows by filter arg
        for col, values in filters.items():
            values = _listify(values)
            df = df[df[col].isin(values)]
        log.debug("Filtered entries:\n%s", self._short_repr)

        # drop irrelevant columns
        if len(ignore) > 0:
            log.debug(f"""Ignoring parameters:\n{", ".join(ignore)}""")
            df.drop(columns=ignore, inplace=True)
            log.debug("New entries:\n%s", df)

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
            df[print_column] = df[print_column].map(decorate)
            out = pd.pivot_table(
                df,
                values=print_column,
                index=y,
                columns=x,
                aggfunc=lambda x: self._print_cell_string(x, category_joiner),
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
                    log.info(f"Guessing order {df_sort} for parameter {parameter}")
                    sort_orders[parameter] = df_sort
                elif set(df_sort) - set(sort_orders[parameter]) != set():
                    log.warning(
                        f"Specified order {sort_orders[parameter]} for parameter "
                        f"'{parameter}' does not cover all values: {set(df_sort) - set(sort_orders[parameter])}."
                    )
                    log.info(f"Guessing order {df_sort} for parameter {parameter}")
                    sort_orders[parameter] = df_sort

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
                    decorate_x(_format_person_values(
                        separators[0].join(col).strip(), separators[0]
                    ))
                    for col in out.columns.values
                ]
                out.columns.name = new_colindex_name

                new_index_name = category_joiner.join(y)
                out.index = [
                    decorate_y(_format_person_values(
                        separators[0].join(_listify(col)).strip(), separators[0]
                    ))
                    for col in out.index.values
                ]
                out.index.name = new_index_name

            constructed_paradigms[z_key] = out

        if csv_output:
            log.debug(f"Writing to {csv_output}")
            output = []
            for z_key, df in constructed_paradigms.items():
                s = StringIO()
                df.to_csv(s, index=True, index_label="")
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
