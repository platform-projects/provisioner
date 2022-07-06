import logging

import dwc_config as config
import dwc_utility as utility

logger = logging.getLogger("shares")

def process(share_args):
    """ Sub-processor for the "shares" command. """

    utility.start_timer("shares")

    if share_args.subcommand == "create":
        shares_create(share_args)

def shares_create(share_args):
    # NOTE: We DO NOT validate the object to share - the
    # share operation will report the error.

    # Verify the source space exists.
    source_space = config.dwc.get_space(share_args.sourceSpace)

    if source_space is None or len(source_space) ==  0:
        logger.error("create share: source space {} not found".format(share_args.sourceSpace))
        return

    target_spaces = config.dwc.get_space_list(share_args.targetSpace)

    if len(target_spaces) == 0:
        logger.error("create share: target space(s) not found")
        return

    config.dwc.add_share(share_args.sourceSpace, share_args.sourceObject, target_spaces)
