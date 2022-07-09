import logging

import session_config as config
import utility as utility

logger = logging.getLogger("shares")

def process(share_args):
    """ Sub-processor for the "shares" command. """

    utility.start_timer("shares")

    if share_args.subcommand == "create":
        shares_create(share_args)

def shares_create(share_args):
    # NOTE: We DO NOT validate the object to share - the
    # share operation will report any error.

    # Verify the source space exists.
    source_space = config.dwc.get_space(share_args.sourceSpace)

    if source_space is None or len(source_space) ==  0:
        logger.error("shares_create: source space {} not found".format(share_args.sourceSpace))
        return

    target_spaces = config.dwc.get_space_list(share_args.targetSpace)

    if len(target_spaces) == 0:
        logger.error("shares_create: target space(s) not found")
        return

    config.dwc.add_share(share_args.sourceSpace, share_args.sourceObject, target_spaces)
