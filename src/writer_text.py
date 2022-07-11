import logging, re, time, sys

import constants, session_config

logger = logging.getLogger("write_text")

def json_path(data, field):
    if not isinstance(field, str) or len(field.strip()) == 0:
        logger.error("json_value: invalid JSON spec".format(str(field)))
        return None
    
    json_value = None
    
    path_specs = field.strip().split(".")  # We want to be able to index the path as we loop
    
    for path_indx in range(0, len(path_specs)):
        path_spec = path_specs[path_indx]
        
        if path_spec == "$":
            json_value = data
        elif path_spec.startswith("*"):  # Expecting a dictionary
            array_spec = re.search(r"\[(.*?)\]", path_spec)  # Maybe a list of subscripts

            # We must be on a dictionary or array.
            if isinstance(json_value, list):
                return json_value
            
            if isinstance(json_value, dict):
                dict_value = []
                
                for key in json_value.keys():
                    dict_value.append({ "key" : key, "value" : json_value[key] })
                    
                return dict_value
        elif path_spec.find("[") != -1 and path_spec.endswith("]"):
            array_spec = re.search(r"\[(.*?)\]", path_spec)
            path_spec = path_spec[0:path_spec.find("[")]

            json_value = json_value[path_spec]  # Pull out the array
            
            if array_spec.group(1) != "*":
                array_index = int(array_spec.group(1))
                
                if len(json_value) == 0 or array_index > len(json_value) - 1:
                    json_value = None
                else:
                    json_value = [ json_value[array_index] ]                
        else:
            if path_spec not in json_value:
                logger.debug(f"json_value: invalid path - {path_spec}")
                json_value = None
                break
            else:
                if json_value is None:
                    logger.debug(f"json_value: invalid path {path_spec}")
                    break
                
                json_value = json_value[path_spec]
    
    return json_value
    
def lookup_value(data, field):
    # Get the requested value - invalid lookups always return a None value.
    
    lookup_value = None
    
    if isinstance(field, dict):  # Did we get a field specification that includes a path?
        if "path" in field:
            lookup_value = json_path(data, field["path"])
        else:
            logger.debug("lookup_value: path not found")  # Must include a "path" attribute
    elif isinstance(field, str):
        # Specific "path" not included in a field definition - should really just call json_path
        lookup_value = json_path(data, field)
    else:
        logger.debug(f"lookup_value: path not found: {field}")

    # We have value, handle type conversion and formatting.
    
    if isinstance(lookup_value, str) or isinstance(lookup_value, bool) or isinstance(lookup_value, int):
        if isinstance(lookup_value, bool) or isinstance(lookup_value, int):
            lookup_value = str(lookup_value)
            
        if "format" in field:
            format_spec = field["format"]
            format = format_spec[-1]
            width = int(format_spec[0:-1])
            
            if len(lookup_value) > 0 and lookup_value != "" and format == "e":
                lookup_value = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(lookup_value[0:10])))

            if len(lookup_value) > 0 and lookup_value != "" and format == "g":
                lookup_value = str(int(lookup_value) / constants.CONST_GIGABYTE) + " GB"

            lookup_value = (lookup_value + " " * width)[:width]
    elif isinstance(lookup_value, list):
        if "aggregate" not in field:
            logger.warning("aggregate value missing")
        else:
            aggr_value = ""
            comma = ""
            
            for item in lookup_value:
                aggr_value += comma + json_path(item, field["aggregate"])
                comma = ", "
            
            lookup_value = aggr_value
            
    return lookup_value

def recurse_format(data, template, output_handle):
    for item in data:
        for row in template["rows"]:
            if row["type"] == "row":
                fields = re.findall("\\{(.*?)\\}", row["layout"]);
                values = {}
            
                for field in fields:
                    values[field] = lookup_value(item, template["fields"][field])
                
                output_row = row["layout"].format(**values)
                output_handle.write(output_row)
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

def write_list(list_data, args):
    logger.setLevel(session_config.log_level)

    if args.output is not None:
        output_handle = open(args.output, "w")
    else:
        output_handle = sys.stdout
    
    if list_data is None:
        logger.warning(f"write_list_text: {args.command} - empty list")
        return

    if isinstance(list_data, dict):
        list_data = [ list_data ] # We love lists

    if args.command not in constants.templates:
        logger.error(f"write_list_text: {args.command} template not found.")
        return
    
    template = constants.templates[args.command]

    # Loop over each item and build output lines based on the template.

    recurse_format(list_data, template, output_handle)
    
    if args.output is not None:
        output_handle.close()
