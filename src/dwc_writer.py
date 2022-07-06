import logging
import json
import os
import sys

import dwc_config as config
import dwc_utility as utility
import dwc_writer_hana as hana
import dwc_writer_csv as csv

logger = logging.getLogger('writer')
        
def write_list(list_data, args=None):
    if list_data is None or len(list_data) == 0:
        logger.error(f'invalid list passed to write_list: target {target}.')
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

def write_list_text(list_data, args, indent=0):
    if list_data is None:
        logger.warning("write_list_text: empty list")
        return

    if isinstance(list_data, dict):
        list_data = [ list_data ]

    indent_space = '.' * indent

    for item in list_data:
        # Now loop over the keys looking for arrays of items.  If there is a template
        # for the list, produce output.

        if args.prefix is not None:
            args.output_handle.write("{}{}:\n".format(indent_space, args.prefix))

        if isinstance(item, str) or isinstance(item, int):
            str_indent = '.' * (indent + 2)
            args.output_handle.write("{}{}\n".format(str_indent, item))

            continue

        for key in item.keys():
            if isinstance(item[key], list) or isinstance(item[key], dict):
                # Recurse this list object
                write_list_text(item[key], args, indent=indent + 2)
            else:
                # Test to see if the value is actually a JSON string.  If the
                # following conversion does not fail, process the string as
                # a nested object.

                try:
                    json_obj = json.loads(item[key])

                    if isinstance(json_obj, list) or isinstance(json_obj, dict):
                        write_list_text(json_obj, args, indent=indent + 2)

                        continue
                except:
                    pass

                args.output_handle.write(f'{indent_space}{key}: {item[key]}\n')