import logging

from gin.paths import log_path

LOG = logging.getLogger('logger')
LOG.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(message)s")

fh = logging.FileHandler(log_path())
LOG.addHandler(fh)
