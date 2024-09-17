#!/usr/bin/env python

from bs4 import BeautifulSoup

########################################################################################################################


class HTMLTable(object):
    """Creates a html table based on provides list of header elements and row elements.

    Attributes
    ----------
    table_header : list
        A list of header elements - the heading of each column.
    html_table : str
        The html table

    Methods
    -------
    init_html_table(table_header)
        Generates the first part of the table - the header
    add_html_row(*args)
        Add each provides arguments as column items and finally appends the complete row to the table.
    get_table(*args)
        Finalize and returns the table.
    """

    def __init__(self, table_header):
        """
        Parameters
        ----------
        table_header : list
            A list of header elements - the heading of each column.
        """

        grey = "<td style='background-color: Grey; color: White; font-weight:bold'>"
        purple = "<td style='background-color: Purple; color: White; font-weight:bold'>"
        yellow = "<td style='background-color: Yellow; color: Black; font-weight:bold'>"
        red = "<td style='background-color: Red; color: White; font-weight:bold'>"

        self.table_header = table_header
        self.html_table = ""

        self.disabled_txt = "Disabled"
        self.will_expire_txt = "Will expire"
        self.expired_txt = "Expired"
        self.has_no_expiration = "Has no expiration"
        self.error_txt = "ERROR"

        self.alert_styles = {
            self.disabled_txt: grey,
            self.will_expire_txt: yellow,
            self.expired_txt: red,
            self.has_no_expiration: purple,
            self.error_txt: red
        }

    def init_html_table(self):
        """generates a html table to be used in json output for MS Teams"""

        self.html_table = f"""<table bordercolor='black' border='2'>
    <thead>
    <tr style='background-color: Teal; color: White'>
"""
        for h in self.table_header:
            self.html_table += f"        <th>{h}</th>\n"

        self.html_table += """
    </tr>
    </thead>
    <tbody>
    """

    def add_html_row(self, *args):
        """adds the table rows to the html table

        expected row elements:
            record_name, record_type, vault_name, updated, expires, comment

        Parameters
        ----------
        args : str
            The items which will be added to the current row.
        """

        if not self.html_table:
            return

        html_row = "<tr>"
        for arg in args:
            td = "<td>"
            if arg.startswith(self.disabled_txt):
                td = self.alert_styles.get(self.disabled_txt)
            if arg.startswith(self.will_expire_txt):
                td = self.alert_styles.get(self.will_expire_txt)
            if arg.startswith(self.expired_txt):
                td = self.alert_styles.get(self.expired_txt)
            if arg.startswith(self.has_no_expiration):
                td = self.alert_styles.get(self.has_no_expiration)
            if arg.startswith(self.error_txt):
                td = self.alert_styles.get(self.error_txt)
            arg = arg.replace(". ", "<br>").replace(" (", "<br>(")
            html_row += f"{td}{arg}</td>"
        html_row += "</tr>"

        self.html_table += html_row

    def get_table(self):
        """adding closing html tags and remove plural in days when it should not be used

        Returns
        -------
        html_table : str
            The finalized table.
        """

        if self.html_table:
            self.html_table += "</tbody></table>"
            self.html_table = self.html_table.replace(" 1 days", " 1 day").replace("\n", "")

        return BeautifulSoup(self.html_table, 'html.parser').prettify()


class Markdown(object):
    """Creates a plain text Markdown table from a list (rows) of lists (columns). The header is the first list in the list.

    Attributes
    ----------
    rows : list
        The list of rows to make out the table
    widths : dict
        A dict to store the column widths while parsing the columns for each row.

    Methods
    -------
    set_widths()
        Parses through the values of each column, in each row, in order to set the width of each column.
        Each column will have to be at least the size of the longest value in each column + an additional spacing.
    get_output(*args)
        Parses through each column in each row and adds the Markdown table char, the space and then the value.
        When the header row is done, the Markdown hyphen seperator row which separates the header and rows is added.
        The final result is returned
    """

    def __init__(self, rows):
        """
        Parameters
        ----------
        rows : list
            The list of rows to make ut the table.
        """
        self.rows = rows
        self.widths = {}

    def set_widths(self):
        """Parses through the values of each column, in each row, in order to set the width of each column."""

        for row in self.rows:
            for i, col in enumerate(row):
                cur_w = self.widths.get(i, 0)
                new_w = len(str(col).rstrip()) + 2
                if cur_w < new_w:
                    self.widths[i] = new_w

    def get_output(self, *args):
        """Parses through each column in each row and adds the Markdown table char, the space and then the value.

        Returns
        -------
        output : str
            The finalized table.

        """
        output = ""
        header_line = ""
        for n, row in enumerate(self.rows):
            for i, col in enumerate(row):
                value = f" {str(col).rstrip()} "

                if n == 0:
                    l = "-" * self.widths[i]
                    header_line += f"|{l: <{self.widths[i]}}"

                if n > 0 and i in args:
                    output += f"|{value: >{self.widths[i]}}"
                else:
                    output += f"|{value: <{self.widths[i]}}"

            output += "|\n"

            if header_line:
                output += f"{header_line}|\n"
                header_line = ""

        return output


########################################################################################################################


def dict_to_rows(rows):
    header = []
    result = []
    for row in rows:
        if not header:
            for k in row.keys():
                header.append(k)
            result.append(header)
        current_row = []
        for v in row.values():
            current_row.append(v)
        result.append(current_row)

    return result


def dict_to_csv(rows):
    out = ''
    for row in rows:
        if not out:
            for k in row.keys():
                out += f'"{k}",'
            out = out.rstrip(',')
            out += '\n'
        for v in row.values():
            out += f'"{v}",'
        out = out.rstrip(',')
        out += '\n'
    return out

