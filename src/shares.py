import logging

import session_config, utility

logger = logging.getLogger("shares")

def process(share_args):
    """ Sub-processor for the "shares" command. """

    logger.setLevel(session_config.log_level)
    
    if share_args.subcommand == "list":
        shares_list(share_args)
    elif share_args.subcommand == "create":
        shares_create(share_args)
    elif share_args.subcommand == "delete":
        shares_list(share_args)
    else:
        logger.error(f"process: unexpected subcommand: {share_args.subcommand}")

def shares_list(share_args):
    x = 1
    
def shares_create(share_args):
    # NOTE: We DO NOT validate the object to share - the
    # share operation will report any error.

    # Verify the source space exists.
    source_space = session_config.dwc.get_space(share_args.sourceSpace)

    if source_space is None or len(source_space) ==  0:
        logger.error(f"shares_create: source space {share_args.sourceSpace} not found")
        return

    target_spaces = session_config.dwc.get_space_list(share_args.targetSpace)

    if len(target_spaces) == 0:
        logger.error("shares_create: target space(s) not found")
        return

    session_config.dwc.add_share(share_args.sourceSpace, share_args.sourceObject, target_spaces)

def shares_delete(share_args):
    x = 1