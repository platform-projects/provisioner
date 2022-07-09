import logging
import os
import copy

import cmdparse as cmdparse
import constants as constants
import session_config as config
import utility as utility
import writer as writer

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

    assigned_storage = constants.CONST_DEFAULT_SPACE_STORAGE
    assigned_ram = constants.CONST_DEFAULT_SPACE_MEMORY

    # If the user specified the "--force" command line option, this may be overridden
    delete_flag = False

    # Check to see if the space already exists.
    space_def = config.dwc.get_space(space_name)

    # Check to see if the space objects (or empty object) has the
    # space_name as a dictionary object - this only valid when
    # a real space is returned.

    if space_def is not None and space_name in space_def:
        if space_args.force == False:
            logger.warning(f'spaces_create: space {space_args.spaceName} already exists - specify force.')
            return
        else:
            delete_flag = True

    # If a template was specified, make sure it exists.  If there is no template name,
    # compose a minimal space defintion.

    if space_args.template is None:
        new_space_def = {}
        new_space_def[space_name] = copy.deepcopy(constants.default_space_definition)
        
        new_space_def[space_name]["spaceDefinition"]["label"] = space_label
        new_space_def[space_name]["spaceDefinition"]["assignedStorage"] = assigned_storage
        new_space_def[space_name]["spaceDefinition"]["assignedRam"] = assigned_ram

        new_space_def[space_name]["spaceDefinition"]["members"] = []   # We will add members shortly.
    else:
        # Make sure the template space is in the tenant.
        template_spaces = config.dwc.get_space_list(space_args.template, wildcard=False)

        if template_spaces is None or len(template_spaces) != 1:
            logger.error("spaces_create: create space {} - template space {} - invalid.".format(space_args.spaceName, space_args.template))
            return

        template = config.dwc.get_space(template_spaces[0]["name"])
        
        new_space_def = {}
        new_space_def[space_name] = {}

        # Copy the space definition from the template
        new_space_def[space_name]["spaceDefinition"] = template[space_args.template]["spaceDefinition"]
        new_space_def[space_name]["spaceDefinition"]["label"] = space_label
        new_space_def[space_name]["spaceDefinition"]["members"] = []   # We will add members shortly

    # Set values if there are command line arguments for disk and memory. Command line 
    # arguments for disk/memory override default or template values.
    if space_args.disk is not None:
        assigned_storage = int(float(space_args.disk) * constants.CONST_GIGABYTE)
        new_space_def[space_name]["spaceDefinition"]["assignedStorage"] = assigned_storage

    if space_args.memory is not None:
        assigned_ram = int(float(space_args.memory) * constants.CONST_GIGABYTE)
        new_space_def[space_name]["spaceDefinition"]["assignedRam"] = assigned_ram

    # Add members to the space definition.

    users = config.dwc.get_users(space_args.users)

    # Let the user know they didn't specify valid users for the space.
    if len(users) == 0:    
        logger.warning("spaces_create: create space {} found no matching DWC users.".format(space_name))
        
    for user in users:
        new_space_def[space_name]["spaceDefinition"]["members"].append(
                    { "name" : user["userName"], "type" : "user" }
                )

    # If we need to force the creation of the space, delete the existing space first.

    if delete_flag:
        logger.info(f"spaces_create: {space_name} forced create - deleting existing space.")

        config.dwc.spaces_delete_cli(space_name)

    # The space is ready to be created, call the CLI to do the operation.

    config.dwc.spaces_create_cli('create', new_space_def)

    logger.info(utility.log_timer("spaces_create", f"spaces_create: {space_name} creation complete."))

def spaces_delete(space_args):
    utility.start_timer("spaces_delete")

    space_list = config.dwc.get_space_names(space_args.spaceName)
    
    if len(space_list) == 0:
        logger.warning("spaces_delete: no spaces found to delete")
    else:
        for space_name in space_list:
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

    # Remove the header line by clipping starting at the skip value (default=1).
    bulk_text = bulk_text[int(space_args.skip):]
    
    for text in bulk_text:
        text = text.strip()

        # Skip comment lines - I WANTED THE ABILITY TO COMMENT - so shoot me.
        if text[0] == '#':
            continue

        if space_args.bulk_subcommand == "create":
            spaces_bulk_create(space_args, text)
        elif space_args.bulk_subcommand == "delete":
            spaces_bulk_delete(text)

def spaces_bulk_create(space_args, text):
    # Build the arguments to pass to the spaces_create routine - just like
    # it would appear on a command line.
    
    create_args = [ "spaces", "create" ]

    # Split the row into expected columns.
    text_row = text.split(",")

    space_name = text_row[constants.CONST_SPACE_NAME]
    space_label = text_row[constants.CONST_LABEL]
    space_disk = text_row[constants.CONST_DISK]
    space_memory = text_row[constants.CONST_MEMORY]
    space_template = text_row[constants.CONST_TEMPLATE]
    space_force = text_row[constants.CONST_FORCE]

    # Pass along the force option, if present.
    # Note: command line argument overrides individual spaces in the CSV

    if space_args.force:
        create_args.append("--force")
    else:
        if isinstance(space_force, str) and len(space_force) > 0 and space_force.lower() == 'true':
            create_args.append("--force")
            
    # Pass along the template specified on the command line.
    # Note: command line argument overrides individual templates in the CSV
    
    # Note: we do not validate the specified template Space - that occurs
    # during the create operation.

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

    # Add the NON-OPTIONAL space name parameter
    create_args.append(space_name)

    # Add in the NON-OPTIONAL list of users
    for user in text_row[constants.CONST_USERS:]:
        if isinstance(user, str) and len(user) > 0:
            create_args.append(user.strip())

    spaces_create(cmdparse.parse(create_args))

def spaces_bulk_delete(text):
    space_args = text.split(",")
    space_name = space_args[0]

    config.dwc.spaces_delete_cli(space_name)

def spaces_list(space_args):
    utility.start_timer("spaces_list")

    # Get the list of all spaces.  This query returns a list of spaces with 
    # only a few attributes per space.
    
    spaces = config.dwc.get_space_list(space_args.spaceName, space_args.wildcard)

    # Capture this list of spaces to a file so we can visually review if needed.
    utility.write_json("spaces-list", spaces)  
    
    # Now loop over the spaces list and do additional queries to get all the details for each space.

    space_list = []
    
    # Keep track of whether the current (logged in) DWC user is a member of a space.  To
    # capture ALL the details we need to be a space member.  Setting this flag, per space, let's
    # us know when we need to call the DWC CLI to punch our admin user into the space.

    spaces_needing_member = {}
    
    for current_space in spaces:
        space_name = current_space["name"]  # This is the technical name for the space.

        logger.debug(f"spaces_create: starting space list for {space_name}")
        
        # Get the space details (including members/dbusers/connections/etc) from DWC
        space = config.dwc.get_space(space_name)

        # Pull out the space details from the query results.
        space_def = space[space_name]["spaceDefinition"]

        # Compose the space row to be written to the output.  This is a
        # combination of all the short space query attributes 
        # and the detailed query attributes.
        
        new_space = copy.deepcopy(current_space)   # Start with a copy of the simple space defintion
        new_space.update(space_def)                # Add the detailed space attributes

        space_list.append(new_space)       # Add this completed space to the list - we love lists
        
        # Assume the administrative user doing this operation is not a member of this space.  
        spaces_needing_member[space_name] = True 
        
        for member in new_space["members"]:
            # Are we a member of the space?
            if member["name"] == config.dwc.get_user_info()["userName"]:
                spaces_needing_member[space_name] = False
                break

        # Create a list object for this space's dbusers containing the list
        # of schema objects available for building views.

        for object in config.dwc.get_dbuser_objects(space_name, new_space["dbusers"]):
            # Add in the hastag username of the user as a distinct field.
            object["dbuser"] = object["id"][:object["id"].find(".")]  
            
            if "dbuser_objects" not in new_space:
                new_space["dbuser_objects"] = []
                
            new_space["dbuser_objects"].append(object)
 
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
            
                new_space["data_builder"].append(db_object)

        # Pump out the remote tables list
        
        for remote_table in config.dwc.get_remote_tables(space_name):
            if "remote_tables" not in new_space:  # Lazy add to the object
                new_space["remote_tables"] = []
            
            new_space["remote_tables"].append(remote_table)

        # Pump out the business builder objects
        
        business_builder_objects = config.dwc.get_business_builder_objects(space_name)

        for business_builder_object in business_builder_objects:
            business_builder_object["space_name"] = space_name
            
            if "business_builder" not in new_space:
                new_space["business_builder"] = []
                
            new_space["business_builder"].append(business_builder_object)

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