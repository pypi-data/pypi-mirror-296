import warnings

warnings.warn(
    "Import `.corva_streamx_semattrs` instead",
    DeprecationWarning,
    stacklevel=2
)

from .corva_streamx_semattrs import *  # noqa: F401 F403
