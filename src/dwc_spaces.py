import logging
import os

import dwc_cmdparse as cmdparse
import dwc_config as config
import dwc_utility as utility
import dwc_writer as writer

logger = logging.getLogger("spaces")

def process(space_args):
    """Subprocessor for the "spaces" commands."""

    logger.setLevel(config.log_level)

    if space_args.subcommand == "list":
        spaces_list(space_args)
    elif space_args.subcommand == "create":
        spaces_create(space_args)
    elif space_args.subcommand == "delete":
        spaces_delete(space_args)
    elif space_args.subcommand == "bulk":
        process_bulk(space_args)
    elif space_args.subcommand == "member":
        process_members(space_args)

def spaces_create(space_args):
    utility.start_timer("spaces_create")

    # The user could have specified a label name instead of
    # of a space name - fix it to be a functional space name.

    space_name = config.dwc.validate_space_id(space_args.spaceName)

    if space_name is None:
        logger.error(f'Create space {space_args.spaceName} - invalid space name')
        return

    space_label = config.dwc.validate_space_label(space_args.spaceName, space_args.label)

    if space_label is None:
        logger.warn(f'Create space {space_args.spaceName} - invalid space label {space_args.label} - defaulting to {space_name}')
        
    # Set defaults for disk and ram.  These can be overridden by
    # a template or by command line values (--disk, --memory).

    assigned_storage = config.CONST_DEFAULT_SPACE_STORAGE
    assigned_ram = config.CONST_DEFAULT_SPACE_MEMORY

    # Check to see if the space already exists.

    space_def = config.dwc.get_space(space_name)

    # If the user specified "--force" this may be overridden
    delete_flag = False

    # Check to see if the space objects (or empty object) as the
    # space_name as a dictionary object - this only valid when
    # a real space is returned.

    if space_name in space_def:
        if space_args.force == False:
            logger.warning(f'Create space: {space_args.spaceName} already exists - specify force.')
            return
        else:
            delete_flag = True

    # If a template was specified, make sure it exists.  If there is no template,
    # compose a minimal space defintion.

    if space_args.template is None:
        new_space_def = {}
        new_space_def[space_name] = {}
        new_space_def[space_name]["spaceDefinition"] = {}
        new_space_def[space_name]["spaceDefinition"]["label"] = space_label
        new_space_def[space_name]["spaceDefinition"]["assignedStorage"] = assigned_storage
        new_space_def[space_name]["spaceDefinition"]["assignedRam"] = assigned_ram
        new_space_def[space_name]["spaceDefinition"]["enableDataLake"] = False
        new_space_def[space_name]["spaceDefinition"]["priority"] = 5
        new_space_def[space_name]["spaceDefinition"]["members"] = []   # We will add members shortly.
    else:
        template_def = config.dwc.get_space(space_args.template)

        if template_def is None:
            logger.error("Create space {}: template space {} not found.".format(space_args.space, space_args.template))
            return

        new_space_def = {}
        new_space_def[space_name] = {}

        # Copy the space definition from the template
        new_space_def[space_name]["spaceDefinition"] = template_def[space_args.template]["spaceDefinition"]
        new_space_def[space_name]["spaceDefinition"]["label"] = space_label
        new_space_def[space_name]["spaceDefinition"]["members"] = []   # We will add members shortly

    # Set values if there are command line arguments for 
    # disk and memory.
    if space_args.disk is not None:
        assigned_storage = int(float(space_args.disk) * config.CONST_GIGABYTE)
        new_space_def[space_name]["spaceDefinition"]["assignedStorage"] = assigned_storage

    if space_args.memory is not None:
        assigned_ram = int(float(space_args.memory) * config.CONST_GIGABYTE)
        new_space_def[space_name]["spaceDefinition"]["assignedRam"] = assigned_ram

    # Add members to the space definition.

    users = config.dwc.get_users(space_args.users)

    if len(users) == 0:    
        logger.warning("Create space {} found no matching DWC users.".format(space_name))
        
    for user in users:
        new_space_def[space_name]["spaceDefinition"]["members"].append(
                    { "name" : user["userName"], "type" : "user" }
                )

    # If we need to force the creation of the space, delete the existing space first.

    if delete_flag:
        logger.warning("Create space: {} forced recreate - deleting space.".format(space_name))

        config.dwc.spaces_delete_cli(space_name)

    # The space is ready to be created, call the CLI to do the operation.

    config.dwc.spaces_create_cli('create', new_space_def)

    logger.debug(utility.log_timer("spaces_create", "Space {} creation complete.".format(space_name)))

def spaces_delete(space_args):
    utility.start_timer("spaces_delete")

    for space_name in config.dwc.get_space_names(space_args.spaceName):
        config.dwc.spaces_delete_cli(space_name)

    logger.debug(utility.log_timer("spaces_delete"))

def process_bulk(space_args):
    # A file with a list of spaces for the bulk operation is required.

    if not os.path.exists(space_args.filename):
        logger.error("spaces_bulk: file not found: {}".format(space_args.filename))
        return

    # Load the file - should be a CSV file

    with open(space_args.filename, "r") as file:
        bulk_text = file.readlines()

    # Remove the header line by clipping starting at the skip value.
    bulk_text = bulk_text[int(space_args.skip):]

    if space_args.bulk_subcommand == "create":
        spaces_bulk_create(space_args, bulk_text)
    elif space_args.bulk_subcommand == "delete":
        spaces_bulk_delete(space_args, bulk_text)

def spaces_bulk_create(space_args, bulk_text):
    CONST_SPACE_NAME = 0
    CONST_LABEL = 1
    CONST_DISK = 2
    CONST_MEMORY = 3
    CONST_TEMPLATE = 4
    CONST_FORCE = 5
    CONST_USERS = 6

    for text in bulk_text:
        text = text.strip()

        # Skip comment lines - I WANTED THE ABILITY TO COMMENT - so shoot me.
        if text[0] == '#':
            continue

        # Build the arguments to pass to the spaces_create routine.
        create_args = [ "spaces", "create" ]

        # Split the row into expected columns.
        arg_row = text.split(",")

        space_name = arg_row[CONST_SPACE_NAME]
        space_label = arg_row[CONST_LABEL]
        space_disk = arg_row[CONST_DISK]
        space_memory = arg_row[CONST_MEMORY]
        space_template = arg_row[CONST_TEMPLATE]
        space_force = arg_row[CONST_FORCE]

        # Pass along the force option, if present.
        # Note: command line argument overrides individual spaces in the CSV

        if space_args.force:
            create_args.append("--force")
        else:
            if isinstance(space_force, str) and len(space_force) > 0:
                if space_force.lower() == "true":
                    create_args.append("--force")
                else:
                    logger.warning("spaces_bulk_create: invalid force argument, should be \"true\" or empty - defaulting to false.")

        # Pass along the template specified on the command line.
        # Note: command line argument overrides individual templates in the CSV
        # Note: we do not validate the template - that occurs during the
        #       create operation.

        if space_args.template is not None:
            create_args.append('--template')
            create_args.append(space_args.template)
        else:
            if space_template is not None:
                if isinstance(space_template, str) and len(space_template) > 0:
                    create_args.append('--template')
                    create_args.append(space_template)

        # Process a label if present in the CSV
        # Note: we do not validate the label name - that occurs during
        #       the create operation.

        if space_label is not None and len(space_label) > 0:
            create_args.append("--label")
            create_args.append(space_label)

        # Note: if disk or memory is not specified for this space
        #       then the values will set to defaults or to the template
        #       values (if specified).

        if space_disk is not None and len(space_disk) > 0:
            create_args.append("--disk")
            create_args.append(space_disk)

        if space_memory is not None and len(space_memory) > 0:
            create_args.append("--memory")
            create_args.append(space_memory)

        # Add in the NON-OPTIONAL space name
        create_args.append(space_name)

        # Add in the NON-OPTIONAL list of users
        for user in arg_row[CONST_USERS:]:
            create_args.append(user.strip())

        spaces_create(cmdparse.parse(create_args))

def spaces_bulk_delete(args):
    if not os.path.exists(args.csv):
        logger.error("spaces_bulk_delete: CSV file {} not found".format(args.csv))
        return

    # Load the file - should be a CSV file

    with open(args.csv, "r") as file:
        spaces_text = file.readlines()

    # Remove the header line.
    spaces_text = spaces_text[args.skip:]

    for space in spaces_text:
        space_args = space.split(",")
        space_name = space_args[0]

        config.dwc.spaces_delete_cli(space_name)

def spaces_list(space_args):
    utility.start_timer("spaces_list")

    # Get the list of all spaces.  This query returns a list of spaces with 
    # only a few attributes per space.
    
    spaces = config.dwc.get_space_list(space_args.spaceName, space_args.wildcard)

    # Capture this list of spaces to a file so we can visually review if needed.
    utility.write_json("space-list", spaces)  
    
    # Now loop over the spaces list and do additional queries to get all the details for each space.

    space_list = []
    
    # Keep track of whether the current (logged in) DWC user is a member of a space.  To
    # capture ALL the details we need to be a space member.  Setting this flag, per space, let's
    # us know when we need to call the DWC CLI to punch our admin user into the space.

    spaces_needing_member = {}
    
    for current_space in spaces:
        space_name = current_space["name"]  # This is the technical name for the space.
        space_id = current_space["id"]

        logger.debug(f"starting space list for {space_name}")
        
        # Get the space details (including members/dbusers/connections/etc) from DWC
        space = config.dwc.get_space(space_name)

        # For us to be able to pull more data/business builder information, we need to ensure
        # the DWC current user is a member of the space.  This is done via the offical API.
        # To use the API, we need a definition of the Space as a JSON file.  Write
        # out the original definition to be used if we need to remove our membership
        # after the data extract is complete.
        
        config.dwc.write_space_json(space)
        
        # Pull out the space details from the query results.
        space_def = space[space_name]["spaceDefinition"]

        # Compose the space row to be written to the output.  This is a
        # combination of all the short space query attributes (shallow copy) 
        # and the detailed query attributes (python update).
        
        new_space = current_space.copy()   # Shallow copy of the slim version to start a new object
        new_space.update(space_def)        # Add the detailed space attributes

        space_list.append(new_space)       # Add this completed space to the list.
        
        # Assume the administrative user doing this operation is not a member of this space.  
        spaces_needing_member[space_name] = True 
        
        if len(new_space["members"]) > 0:  # Do we have members?
            for member in new_space["members"]:
                # Are we a member of the space?
                if member["name"] == config.dwc.get_user_info()["userName"]:
                    spaces_needing_member[space_name] = False

                # Add some referential integrity.
                member["spaceId"] = space_id

        # Enrich the dbusers with spaceId values for referential integrity.
        if isinstance(new_space["dbusers"], list) and len(new_space["dbusers"]) > 0:
            for dbuser in new_space["dbusers"]:
                dbuser["spaceId"] = space_id

                # For each data access user in the space, find the objects that exist in that schema

                for object in config.dwc.get_dbuser_objects(space_name, dbuser):
                    if "objects" not in dbuser["spaceId"]:
                        dbuser["spaceId"]["objects"] = []
                    
                    dbuser["spaceId"]["objects"].append(object)
 
        # Ask for any connections defined for this space.
        # NOTE: this query uses ID and not SPACE_NAME 
 
        # for connection in config.dwc.get_connections(space_id):
        #     if "connections" not in new_space:
        #         new_space["connections"] = []

        #     # Add the primary key to spaces.
        #     connection["spaceId"] = space_id  

        #     new_space["connections"].append(connection)

        # Ask for additional categories of objects that may be associated with each space.
        # These data are only available for members of the space - we may need to add ourselves.
    
        # Check to see if the current user is a member of this space.  We can't collect
        # info on various object types if we are not a member.
        
        # if spaces_needing_member[space_id]:
        #     # Adjust the Space definition to include this user - we must have sufficient
        #     # DWC privilege to do this operation.
        
        #     space_def[space_name]["spaceDefinition"]["members"].append({ 'name' : userInfo["user"]["userName"], 'type' : 'user' })
        #     # Get ready for calling the API by writing the updated space definition 
        #     # to a JSON file (as needed by the API)    

        #     json_file = os.path.join("working", "{}-add-member.json".format(space_name))
        #     utility.write_json(json_file, space_def)

        # Pump out the data builder objects

        db_objects = config.dwc.get_data_builder_objects(space_name)

        if db_objects is not None and "value" in db_objects:
            for db_object in db_objects["value"]:
                if "data_builder" not in new_space:  # Lazy add to the object
                    new_space["data_builder"] = []
            
                db_object["spaceId"] = space_id

                new_space["data_builder"].append(db_object)

        # Pump out the remote tables list
        
        for remote_table in config.dwc.get_remote_tables(space_name):
            if "remote_tables" not in new_space:  # Lazy add to the object
                new_space["remote_tables"] = []
            
            remote_table["spaceId"] = space_id

            new_space["remote_tables"].append(remote_table)

        # Pump out the business builder objects
        
        # bb_query = p.business_builder_query.replace("{space_name}", space_name)

        # business_builder_string = dwc.post(urls["businessbuilder"], bb_query).text
        # logr.info(elapsedTime.format("Business Builder query for space {}".format(space_name), dwc.getelapsed()))

        # if len(business_builder_string) > 0:
        #     business_builder_objects = json.loads(business_builder_string)
            
        #     if business_builder_objects["@odata.count"] > 0:
        #         for business_builder_object in business_builder_objects["Content"]:
        #             business_builder_object["space_name"] = space_name
                    
        #             business_builder_list.append(business_builder_object)

    if len(space_list) == 0:
        logger.warn("spaces_list: No spaces found.")

        return

    writer.write_list(space_list, args=space_args)

def process_members(space_args):
    if space_args.member_subcommand == "list":
        members_list(space_args)
    else:
        members_action(space_args)

def members_list(space_args):
    space_list = config.dwc.get_space_list(space_args.spaceName, wildcard=space_args.no_wildcard)

    members_list = None
    convert_list = True

    for space in space_list:
        space_name = space["name"]

        space = config.dwc.get_space(space_name)
        space_def = space[space_name]["spaceDefinition"]

        if members_list is None:
            members_list = space_def["members"]
        else:
            if convert_list:
                convert_list = False
                member_list = [ member_list ]

            member_list.append(space[space_name]["members"])

    writer.write_list(members_list, args=space_args)

def members_action(space_args):
    space = config.dwc.get_space(space_args.spaceName)
    users = config.dwc.get_user(space_args.user, wildcard=space_args.wildcard)

    if users is None or len(users) == 0:
        logger.warn("members_action: no valid users specified")
        return
    
    if space is None or len(space) == 0:
        logger.warn("member_action: no valid space specified")
        return

    for user in users:
        if space_args.member_subcommand == "add":
            config.dwc.add_member(space_args.spaceName, user)
        elif space_args.member_subcommand == "remove":
            config.dwc.remove_member(space_args.spaceName, user)
        else:
            logger.error("members_action: invalid action.")