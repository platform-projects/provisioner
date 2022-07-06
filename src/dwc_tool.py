"""
This is a general purpose script to retrieve information from the DWC instance.  The
major elements of the GUI are available for download:

    users     - retrieve all the users from DWC
    spaces    - retrieve space details from DWC - including data/business builder and data access objects 

There are various options that can be set to control the operation of this script.
"""

import os
import sys
import logging

import dwc_config as config
import dwc_cmdparse as cmdparse
import dwc_connections as connections
import dwc_spaces as spaces
import dwc_shares as shares
import dwc_users as users
import dwc_utility as utility

from dwc_session import DWCSession

logger = logging.getLogger("dwc_tool")

if __name__ == '__main__':
    if sys.version_info<(3,8,0):
        sys.stderr.write("You need python 3.8 or later to run this script\n")
        sys.exit(1)

    # Track how long this process runs across any/all commands.
    utility.start_timer("dwc_tool")
            
    # Capture the command line arguments.
    # Note: Remove this script file name before parsing.
    args = cmdparse.parse(sys.argv[1:])  

    # Make sure the configuration is present and valid.    
    config.ensure_config(args)

    # For the configuration operation, there's nothing else to do.
    if args.command == "config":
        sys.exit(0)
        
    # Build the full list of commands, including commands
    # coming from a script.
    
    commands = []  # We love lists to loop over.
    commands.append(args)

    # Check if a script was provided on the command line.  If so, the
    # commands in the script file will be added to the commands to
    # run - in addition to the global parameters.

    if args.command == 'script':
        if not os.path.exists(args.filename):
            logger.fatal("Script {} not found.".format(args.filename))
            sys.exit(1)

        # Read all the commands from the script - stop when if we
        # encounter the "exit" command.  Also, skip any "config"
        # commands.

        with open(args.filename, "r") as script:
            commandScript = script.readlines()
    
        # Append them to the list of commands after parsing their arguments
        for command in commandScript:
            script_args = command.strip()

            # Only process non-blank and non-comment lines in the file.
            if len(script_args) == 0 or script_args[0] == "#":   
                continue
            
            # If we see "exit" we are done with this script.
            if script_args == "exit":
                break
            
            # Invalid script commands - skip.    
            if script_args.startswith("config"):
                logger.warning("config commands are not permitted in script files")
                continue
            
            logger.debug("..script cmd: {}".format(script_args))

            # Add this command to the list we will process later.  Go ahead
            # and parse the commands to get/verify the arguments.
            script_args = script_args.split(" ")
            commands.append(cmdparse.parse(script_args))

    # We are good to go, login to the DWC tenant
    
    config.dwc = DWCSession(
        url=config.get_config_param("dwc", "dwc_url"), 
        user=config.get_config_param("dwc", "dwc_user"), 
        password=config.get_config_param("dwc", "dwc_password"))
    
    config.dwc.setLevel(logger.getEffectiveLevel())

    # Start the interaction with DWC by logging in.

    if config.dwc.login() == False:
        sys.exit(1)
        
    # Loop over the commands processing each with their own arguments.
    
    for command_args in commands:
        if command_args.command == "spaces":
            spaces.process(command_args)
        elif command_args.command == "connections":
            connections.process(command_args)
        elif command_args.command == "users":
            users.process(command_args)
        elif command_args.command == "shares":
            shares.process(command_args)
        elif command_args.command == "exit":
            break
        
    logger.info(utility.log_timer("dwc_tool", "DWC Operation"))
