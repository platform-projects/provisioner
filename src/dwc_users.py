import argparse
import logging

import dwc_config as config
import dwc_utility as utility
import dwc_writer as writer

logger = logging.getLogger("spaces")

def process(user_args):
    logger.setLevel(config.log_level)

    if user_args.subcommand == "list":
        users_list(user_args)

def users_list(user_args):
    utility.start_timer("users_list")

    user_list = []
    
    for user in config.dwc.get_users(user_args.users):
        # Do some fixup to streamline the user information.
        user["email"] = user["parameters"]["EMAIL"]
        user["display_name"] = user["parameters"]["DISPLAY_NAME"]
        
        if "NUMBER_OF_DAYS_VISITED" in user["parameters"]:
            user["number_of_days_visited"] = user["parameters"]["NUMBER_OF_DAYS_VISITED"]
        else:
            user["number_of_days_visited"] = None

        # It is possible for a user to have no roles.  If roles are present, pivot
        # the string into a list of roles.
        
        if len(user["roles"].strip()) > 0:
            # This is a multi-value string field separated by semi-colons
            
            roles = user["roles"].split(";")
            user["roles_list"] = []  # Add the list as a separate field

            for role in roles:
                # Add referential integrity to the roles based on userName
                user["roles_list"].append({ "userName" : user["userName"], "roleName" : role })

        user_list.append(user)

    # The ETL is complete and we have the users and their roles; push the lists to the database.

    writer.write_list(user_list, args=user_args)
    
    logger.debug(utility.log_timer("users_list", "Command: Users list"))
    
