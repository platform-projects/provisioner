import argparse

dwc_parser = None

def config_parser():
    """Define the parsers for ALL possible command lines"""

    global dwc_parser

    dwc_parser = argparse.ArgumentParser(
        description=__doc__,
        prog='dwc.py',
        formatter_class=argparse.RawDescriptionHelpFormatter)

    dwc_parser.add_argument("-l", "--logging",  help="set the logging level, default=none", choices=['info', 'debug'])

    dwc_parser.add_argument("-c", "--config",   help="provisioning tool config file (default=config.json")


    global_subparsers = dwc_parser.add_subparsers(help='dwc provisioning tool commands', dest="command")

    # The following are "optional" parameters that have meaning
    # for different commands.

    config_parser = global_subparsers.add_parser('config', help="Set URLs and credentials for the tool")
    config_parser.add_argument("--dwc-cli",      help="installation location of the DWC Command Line")
    config_parser.add_argument("--dwc-url",      help="DWC tenant URL")
    config_parser.add_argument("--dwc-user",     help="DWC user name or email")
    config_parser.add_argument("--dwc-password", help="DWC password")
    config_parser.add_argument("--dwc-tenant",   help="DWC tenant URL")

    config_parser.add_argument("--hana-host",     help="HANA host name")
    config_parser.add_argument("--hana-port",     help="HANA port")
    config_parser.add_argument("--hana-user",     help="HANA username")
    config_parser.add_argument("--hana-password", help="HANA password")
    config_parser.add_argument("--hana-encrypt",  help="Encrypt HANA communication (default=False)", action="store_true")
    config_parser.add_argument("--hana-validate", help="Validate the HANA certificate (default=False)", action="store_true")
        
    # Users commands: list (only right now)
    user_parser = global_subparsers.add_parser('users', help='Create, delete and list DWC users')
    user_subparsers = user_parser.add_subparsers(help="users command", dest="subcommand")

    user_list_parser = user_subparsers.add_parser('list', help='Space member list command')
    user_list_parser.add_argument("-o", "--output",   help="filename for output")
    user_list_parser.add_argument("-f", "--format",   help="output style", default="text", choices=['hana', 'csv', 'json', 'text'])
    user_list_parser.add_argument("-p", "--prefix",   help="output prefix for writing", default="DWC_USERS")
    user_list_parser.add_argument('users', help='list of user patterns', nargs=argparse.REMAINDER)

    # Script command - only takes a file name
    script_parser = global_subparsers.add_parser('script', help='Execute a series of commands from a script file')
    script_parser.add_argument('filename', help='script file name')

    # Spaces: list, create, delete, members
    space_parser = global_subparsers.add_parser('spaces', help="Create, delete, list and manage members for DWC spaces")
    space_subparsers = space_parser.add_subparsers(help="space command", dest="subcommand")

    # Spaces LIST options
    space_list_parser = space_subparsers.add_parser('list', help='spaces list command')
    space_list_parser.add_argument("spaceName", help="space name(s) to list", nargs=argparse.REMAINDER)
    space_list_parser.add_argument("-f", "--format", help="output style", default="text", choices=['hana', 'csv', 'json', 'text'])
    space_list_parser.add_argument("-p", "--prefix", help="prefix for output", default="DWC_SPACES")
    space_list_parser.add_argument("-w", "--wildcard", help="seach expansion of space names", action="store_true")
    space_list_parser.add_argument("-o", "--output", help="filename for output")

    # Spaces CREATE options
    space_create_parser = space_subparsers.add_parser('create', help='Space create command')
    space_create_parser.add_argument("--label", help="optional label to assign - defaults to spaceId")
    space_create_parser.add_argument("-t", "--template", help="Space name to use as a template")
    space_create_parser.add_argument("-d", "--disk", help="Disk allocated to space")
    space_create_parser.add_argument("-m", "--memory", help="Memory allocated to space")
    space_create_parser.add_argument("-f", "--force", help="force the re-creation if space exists", action="store_true")
    space_create_parser.add_argument("spaceName", help="space name to create")
    space_create_parser.add_argument("users", help="users to add to the space", nargs=argparse.REMAINDER)

    # Spaces DELETE options
    space_delete_parser = space_subparsers.add_parser('delete', help='Delete one or more spaces.')
    space_delete_parser.add_argument("spaceName", help="space name(s) to create", nargs=argparse.REMAINDER)

    # Spaces BULK options
    space_bulk_parser = space_subparsers.add_parser('bulk', help='Bulk operation on one or more spaces.')
    space_bulk_subparsers = space_bulk_parser.add_subparsers(help="space bulk command", dest="bulk_subcommand")

    space_bulk_create_parser = space_bulk_subparsers.add_parser('create', help='Space bulk create command')
    space_bulk_create_parser.add_argument("-s", "--skip", help="header lines to skip in the CSV file", default="1")
    space_bulk_create_parser.add_argument("-f", "--force", help="force the re-creation if space exists", action="store_true")
    space_bulk_create_parser.add_argument("-t", "--template", help="Space name to use as a template")
    space_bulk_create_parser.add_argument("filename", help="CSV file containing spaces to create")

    space_bulk_delete_parser = space_bulk_subparsers.add_parser('delete', help='Space bulk delete command')
    space_bulk_delete_parser.add_argument("-s", "--skip", help="header lines to skip in the CSV file", default="1")
    space_bulk_delete_parser.add_argument("filename", help="CSV file containing space names to delete")

    # Space MEMBER options
    space_member_parser = space_subparsers.add_parser('member', help='Bulk operation on one or more spaces.')
    space_member_subparsers = space_member_parser.add_subparsers(help="space member command", dest="member_subcommand")

    space_member_list_parser = space_member_subparsers.add_parser('list', help='Space member list command')
    space_member_list_parser.add_argument("-n", "--no-wildcard", help="Use wildcard lookup for space name and users", action="store_true")
    space_member_list_parser.add_argument("-f", "--format",      help="output style", default="text", choices=['hana', 'csv', 'json', 'text'])
    space_member_list_parser.add_argument("-p", "--prefix",      help="output style", default="DWC_MEMBERS")
    space_member_list_parser.add_argument("-o", "--output",      help="filename for output")
    space_member_list_parser.add_argument("spaceName",           help="Search pattern for spaces to add user")

    space_member_add_parser = space_member_subparsers.add_parser('add', help='Space member add command')
    space_member_add_parser.add_argument("-w", "--wildcard", default="false", help="Use wildcard lookup for space name and users", choices=["true", "false"])
    space_member_add_parser.add_argument("user", help="A user name or email to add to one or more spaces")
    space_member_add_parser.add_argument("spaceName", help="Search pattern for spaces to add user", nargs=argparse.REMAINDER)

    space_member_remove_parser = space_member_subparsers.add_parser('remove', help='Space member remove command')
    space_member_remove_parser.add_argument("-w", "--wildcard", default="true", help="Use wildcard lookup for space name and users", choices=["true", "false"])
    space_member_remove_parser.add_argument("spaceName", help="Search pattern for spaces to remove user")
    space_member_remove_parser.add_argument("users", help="User list (patterns) to remove", nargs=argparse.REMAINDER)

    # Start the CONNECTIONS command
    conn_parser = global_subparsers.add_parser('connections', help='Create, delete and list connections in space(s)')
    conn_subparsers = conn_parser.add_subparsers(help="connections command", dest="subcommand")

    conn_create_parser = conn_subparsers.add_parser('create', help='Connection create command')
    conn_create_parser.add_argument("-w", "--wildcard", help="Use wildcard lookup for space name (default=false)", action="store_true")
    conn_create_parser.add_argument("-f", "--force", help="force the re-creation if connection exists", action="store_true")
    conn_create_parser.add_argument("targetSpace", help="spaces to receive the connection", nargs='+')
    conn_create_parser.add_argument("filename", help="connection definition JSON file")

    conn_delete_parser = conn_subparsers.add_parser('delete', help='Connection delete command')
    conn_delete_parser.add_argument("-w", "--wildcard", help="Use wildcard lookup for space name (default=false)", action="store_true")
    conn_delete_parser.add_argument("targetSpace", help="spaces to receive the connection", nargs='+')
    conn_delete_parser.add_argument("connectionName", help="connection name to delete")

    conn_list_parser = conn_subparsers.add_parser('list', help='Connection list command')
    conn_list_parser.add_argument("-w", "--wildcard",     help="Use wildcard lookup for space name (default=true)", action="store_true")
    conn_list_parser.add_argument("-c", "--connection",   help="connection name to list from space")
    conn_list_parser.add_argument("-f", "--format",       help="output style", default="text", choices=['hana', 'csv', 'json', 'text'])
    conn_list_parser.add_argument("-p", "--prefix",       help="output prefix", default="DWC_CONNECTIONS")
    conn_list_parser.add_argument("-o", "--output",       help="filename for output")
    conn_list_parser.add_argument("sourceSpace",          help="space(s) to list connections", nargs='+')

    # Start the SHARES command
    share_parser = global_subparsers.add_parser('shares', help='Create, delete and list shares in space(s)')
    share_subparsers = share_parser.add_subparsers(help="share command", dest="subcommand")

    share_create_parser = share_subparsers.add_parser('create', help='shares create command help')
    share_create_parser.add_argument("sourceSpace", help="source space with object to share")
    share_create_parser.add_argument("sourceObject", help="source object technical name to share")
    share_create_parser.add_argument("targetSpace", help="target space(s) getting the share")

    # share_list_parser = share_subparsers.add_parser('list', help='shares list command help')
    # share_unshare_parser = share_subparsers.add_parser('unshare', help='shares unshare command help')

def parse(args):
    if dwc_parser is None:
        config_parser()

    parsed_args = dwc_parser.parse_known_args(args)
    return parsed_args[0]