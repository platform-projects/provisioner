import logging, json, os, sys, time, re

import constants 
import writer_hana as hana
import writer_csv as csv

logger = logging.getLogger('writer')
        
def write_list(list_data, args=None):
    if list_data is None or len(list_data) == 0:
        logger.error(f'invalid list passed to write_list: target {args.format}.')
        return

    if args.format == "hana":
        hana.write_list(list_data, args)
    elif args.format == "csv":
        csv.write_list(list_data, args)
    elif args.format == "json":
        write_json(list_data, args)
    elif args.format == "text":
        if args.output is not None:
            args.output_handle = open(args.output, "w")
        else:
            args.output_handle = sys.stdout

        write_list_text(list_data, args)
        
        if args.output is not None:
            args.output_handle.close()
    else:
        logger.warn(f"Invalid target for output: {format}")

def write_json(object, prefix):
    """
        Write out the provided object to the specified file.
    """

    # Ensure the working directory exists before trying to write
    # this file.

    json_path = os.path.join(Path(__file__).parent.absolute(), "working")

    if not os.path.exists(json_path):
        os.mkdir(json_path)

    json_file = os.path.join(json_path, f"{json_name}.json")

    with open(json_file, "w") as outfile:
        outfile.write(json.dumps(object, indent = 4)) # With pretty print

def lookup_value(data, field):
    return_value = data
    
    if isinstance(field, str):
        if field not in data:
            return_value = None
        else:
            return_value = data[field]
    else:
        for path_spec in field["path"].strip().split("."):
            if path_spec not in return_value:
                # logger.error(f"lookup_value: invalid path - {path_spec}")
                return_value = ""
            else:
                return_value = return_value[path_spec]
        
    if isinstance(return_value, str):
        format_spec = field["format"]
        format = format_spec[-1]
        width = int(format_spec[0:-1])
        
        if len(return_value) > 0 and return_value != "" and format == "e":
            return_value = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(return_value[0:10])))

        if len(return_value) > 0 and return_value != "" and format == "g":
            return_value = str(int(return_value) / constants.CONST_GIGABYTE)

        return_value = (return_value + " " * width)[:width]
    
    return return_value

def recurse_format(data, fields):
    x = 1
        
def write_list_text(list_data, args):
    if list_data is None:
        logger.warning(f"write_list_text: {args.command} - empty list")
        return

    if isinstance(list_data, dict):
        list_data = [ list_data ]

    if args.command not in constants.templates:
        logger.error(f"write_list_text: {args.command} template not found.")
        return
    
    template = constants.templates[args.command]

    # Loop over each item and build output lines based on the template.
    
    for item in list_data:
        for row in template["rows"]:
            if row["type"] == "row":
                fields = re.findall("\\{(.*?)\\}", row["layout"]);
                values = {}
            
                for field in fields:
                    values[field] = lookup_value(item, template["fields"][field])
                
                output_row = row["layout"].format(**values)
                args.output_handle.write(output_row)
            elif row["type"] == "list":
                row_data = lookup_value(item, row["path"])

                # list_fields = re.findall("\\{(.*?)\\}", row["layout"]);
                # list_values = {}
                
                # for list_field in list_fields:
                #     list_values[list_field] = lookup_value(row_data, template["fields"][list_field])
                
                # output_row = row["layout"].format(**values)
                # args.output_handle.write(output_row)
                                                  
# if isinstance(item, str) or isinstance(item, int):
#     str_indent = '.' * (indent + 2)
#     args.output_handle.write("{}{}\n".format(str_indent, item))

#     continue

# for key in item.keys():
#     if isinstance(item[key], list) or isinstance(item[key], dict):
#         # Recurse this list object
#         write_list_text(item[key], args, indent=indent + 2)
#     else:
#         # Test to see if the value is actually a JSON string.  If the
#         # following conversion does not fail, process the string as
#         # a nested object.

#         try:
#             json_obj = json.loads(item[key])

#             if isinstance(json_obj, list) or isinstance(json_obj, dict):
#                 write_list_text(json_obj, args, indent=indent + 2)

#                 continue
#         except:
#             pass           