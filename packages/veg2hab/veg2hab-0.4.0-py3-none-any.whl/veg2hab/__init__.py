import warnings

__version__ = "0.4.0"

# Filter out the following warning message
warnings.filterwarnings(
    "ignore",
    message="The Shapely GEOS version .* is incompatible with the GEOS version PyGEOS was compiled with .*",
)

from .main import bronbestanden, installatie_instructies, run
