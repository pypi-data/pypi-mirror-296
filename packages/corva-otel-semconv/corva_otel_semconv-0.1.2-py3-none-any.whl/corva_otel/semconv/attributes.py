import warnings

warnings.warn(
    "Import `.corva_semattrs` instead",
    DeprecationWarning,
    stacklevel=2
)

from .corva_semattrs import *  # noqa: F401 F403
