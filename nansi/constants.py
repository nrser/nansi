from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

# The name of the top-level module _this_ _file_ belongs to... which should
# be "nansi"
PKG_LOGGER_NAME = __name__.split(".")[0]

# Before collection were split out into their own repo, they lives under this
# Ansible Galaxy identifier
LEGACY_COLLECTION_LOGGER_NAME = "nrser.nansi"

# I think sometimes file's `__name__` would end up having a
# "ansible_collections." prefix?
LEGACY_ANSIBLE_COLLECTIONS_LOGGER_NAME = (
    f"ansible_collections.{LEGACY_COLLECTION_LOGGER_NAME}"
)

ROOT_LOGGER_NAMES = (
    PKG_LOGGER_NAME,
    LEGACY_COLLECTION_LOGGER_NAME,
    LEGACY_ANSIBLE_COLLECTIONS_LOGGER_NAME,
)
