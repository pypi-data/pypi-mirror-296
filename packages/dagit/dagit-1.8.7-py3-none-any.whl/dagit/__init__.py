from dagster._core.libraries import DagsterLibraryRegistry

from dagit.version import __version__

DagsterLibraryRegistry.register("dagit", __version__)
