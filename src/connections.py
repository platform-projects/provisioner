import logging

import session_config, utility, writer

logger = logging.getLogger("connections")

def process(connection_args):
    """ Sub-processor for handling "spaces create/delete/list" commands."""

    logger.setLevel(session_config.log_level)

    if connection_args.subcommand == "create":
        connections_create(connection_args)
    elif connection_args.subcommand == "delete":
        connections_delete(connection_args)
    elif connection_args.subcommand == "list":
        connections_list(connection_args)

def connections_create(connection_args):
    utility.start_timer("connections_create")

    # See if the space exists.
    space_list = session_config.dwc.get_space_list(connection_args.targetSpace)

    if len(space_list) == 0:
        logger.warn("connections_create: no spaces found to create connection")
    else:
        for space in space_list:
            session_config.dwc.add_connection(space["name"], connection_args.filename, connection_args.force)

    logger.debug(utility.log_timer("connections_create", "completed."))

def connections_delete(connection_args):
    utility.start_timer("connections_delete")

    space_list = session_config.dwc.get_space_list(connection_args.targetSpace, False)

    if len(space_list) == 0:
        logger.warn("connections_delete: no spaces found")
    else:
        for space in session_config.dwc.get_space_list(space_list):
            session_config.dwc.delete_connection(space["name"], connection_args.connectionName)

    logger.debug(utility.log_timer("connections_delete", "completed."))

def connections_list(connection_args):
    utility.start_timer("connections_list")

    # Expand the list with any wild cards before processing.
    space_list = session_config.dwc.get_space_list(connection_args.sourceSpace, connection_args.wildcard)

    if len(space_list) == 0:
        logger.warn("connections_list: no spaces found to list")
    else:
        list_of_connections = []

        for space in space_list:
            connections = session_config.dwc.get_connections(space["name"], connection_args.connection)

            if connections is not None and len(connections) > 0:
                for connection in connections:
                    list_of_connections.append(connection)

        writer.write_list(list_of_connections, args=connection_args)

    logger.debug(utility.log_timer("connections_list", "completed."))
    