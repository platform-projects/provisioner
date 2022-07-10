import logging

import session_config

logger = logging.getLogger("writer_csv")

def recurse_columns(columns, list_data, param_name):
    csv_name = param_name.lower()

    # Lazy instantiation of the column list - we may see
    # not see the same csv in every pass through lists.
    
    if csv_name not in columns:
        columns[csv_name] = { "columns": [], "file_handle" : None }

    # Search through all the rows because some columns are not consistently
    # returned by the URL/REST queries.  Looping over all the rows helps ensure
    # we capture all the possible columns (attributes).
        
    for row in list_data:
        row_column_names = row.keys()

        for column_name in row_column_names:
            if column_name.find("@") != -1:  # Exclude metadata columns.
                continue

            # For each column we add, record the name of the column.
            # DWC queries are sometimes inconsistent about columns and we
            # can use this list to ensure all columns are accounted for
            # across all rows in the CSV file.

            if column_name not in columns[csv_name]["columns"]:
                columns[csv_name].append(column_name)

                if isinstance(row[column_name], list):
                    recurse_columns(columns, row[column_name], csv_name + "_" + column_name)

def write_csv(columns, list_data, param_name):
    csv_name = param_name.lower()
    csv_file = csv_name + ".csv"

    if csv_name not in columns:
        logger.warn(f"write_csv passed unexpected CSV object name: {csv_name}")

    if columns[csv_name]["file_handle"] is None:
        # Open the file and output the heading row for this file.

        columns[csv_name]["file_handle"] = open(csv_file, "w")

        heading_line = ""
        comma = ""

        for heading in columns[csv_name]["columns"]:
            heading_line += comma + '"' + columns[csv_name]["columns"][heading] + '"'
            comma = ","

        columns[csv_name]["file_handle"].write(f"{heading_line}\n")

    for row in list_data:
        row_column_names = row.keys()
    
def write_list(list_data, args):
    logger.setLevel(session_config.log_level)

    columns = recurse_columns(list_data, args.prefix)

    write_csv(columns, list_data, args.prefix)

    # Every sub-list may have generated an open file, close them all.
    
    for csv_name in columns:
        if columns[csv_name]["file_handle"] is not None and columns[csv_name]["file_handle"].closed == False:
            columns[csv_name]["file_handle"].close()