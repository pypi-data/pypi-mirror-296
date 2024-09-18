"""Init and utils."""
from zope.i18nmessageid import MessageFactory

import logging


PACKAGE_NAME = "rss_provider"

_ = MessageFactory("rss_provider")

logger = logging.getLogger("rss_provider")
