"""
Caching implementation for ALEA data resources.
"""

# imports
import json
import logging
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

# packages

# set up logging
logger = logging.getLogger(__name__)

# set the default cache path and ensure it exists
DEFAULT_CACHE_PATH = Path.home() / ".alea" / "data"
try:
    DEFAULT_CACHE_PATH.mkdir(parents=True, exist_ok=True)
except Exception as e:
    raise RuntimeError(f"Failed to create cache directory: {DEFAULT_CACHE_PATH}") from e


def resource_exists(resource_id: str, version_id: Optional[str] = None) -> bool:
    """
    Check if a resource exists in the cache.

    Args:
        resource_id (str): The resource identifier.
        version_id (str): The version identifier.

    Returns:
        bool: True if the resource exists, False otherwise.
    """
    # get the resource path
    resource_path = get_resource_path(resource_id, version_id)

    # check if the path exists
    return resource_path.exists()


def delete_resource(resource_id: str, version_id: Optional[str] = None):
    """
    Delete a resource from the cache.

    Args:
        resource_id (str): The resource identifier.
        version_id (str): The version identifier.
    """
    # log it
    logger.info("Deleting resource: %s:%s", resource_id, version_id)

    # get the resource path
    resource_path = get_resource_path(resource_id, version_id)

    # delete the path if it exists
    if resource_path.exists():
        # delete all objects via rglob
        shutil.rmtree(resource_path)

        # log it
        logger.info("Completed resource deletion: %s:%s", resource_id, version_id)


def get_resource_path(resource_id: str, version_id: Optional[str] = None) -> Path:
    """
    Get the cache path for a resource.

    Args:
        resource_id (str): The resource identifier.
        version_id (str): The version identifier.

    Returns:
        Path object: The cache path.
    """
    # full resource id
    full_name = resource_id
    if version_id:
        full_name += f"-{version_id}"
    else:
        full_name += "-default"

    # return the full path after creating
    full_path = DEFAULT_CACHE_PATH / full_name
    try:
        full_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise RuntimeError(f"Failed to create cache directory: {full_path}") from e

    return full_path


def get_resource_metadata_path(
    resource_id: str, version_id: Optional[str] = None
) -> Path:
    """
    Get the metadata path for a resource.

    Args:
        resource_id (str): The resource identifier.
        version_id (str): The version identifier.

    Returns:
        Path object: The metadata path.
    """
    # get the resource path
    resource_path = get_resource_path(resource_id, version_id)
    return resource_path / ".alea.metadata.json"


def load_resource_metadata(resource_id: str, version_id: Optional[str] = None) -> dict:
    """
    Load the metadata for a resource.

    Args:
        resource_id (str): The resource identifier.
        version_id (str): The version identifier.

    Returns:
        dict: The metadata dictionary.
    """
    # get the resource path
    metadata_path = get_resource_metadata_path(resource_id, version_id)

    # load the metadata if it exists
    if metadata_path.exists():
        with open(metadata_path, "rt", encoding="utf-8") as metadata_file:
            return json.load(metadata_file)

    return {}


def save_resource_metadata(
    resource_id: str, metadata: dict, version_id: Optional[str] = None
):
    """
    Save the metadata for a resource.

    Args:
        resource_id (str): The resource identifier.
        metadata (dict): The metadata dictionary.
        version_id (str): The version identifier.
    """
    # get the resource path
    metadata_path = get_resource_metadata_path(resource_id, version_id)

    # save the metadata
    with open(metadata_path, "wt", encoding="utf-8") as metadata_file:
        json.dump(metadata, metadata_file, default=str, indent=2)


def get_resource_file_path(
    resource_id: str, file_name: str, version_id: Optional[str] = None
) -> Path:
    """
    Get the file path for a resource.

    Args:
        resource_id (str): The resource identifier.
        file_name (str): The file name.
        version_id (str): The version identifier.

    Returns:
        Path object: The file path.
    """
    # get the resource path
    resource_path = get_resource_path(resource_id, version_id)
    return resource_path / file_name


def get_resource_file_data(
    resource_id: str, file_name: str, version_id: Optional[str] = None
) -> Optional[bytes]:
    """
    Get the file data for a resource.

    Args:
        resource_id (str): The resource identifier.
        file_name (str): The file name.
        version_id (str): The version identifier.

    Returns:
        bytes: The file data.
    """
    # get the file path
    file_path = get_resource_file_path(resource_id, file_name, version_id)

    # load the data if it exists
    if file_path.exists():
        with open(file_path, "rb") as file:
            return file.read()

    return None


def get_resource_file_json(
    resource_id: str, file_name: str, version_id: Optional[str] = None
) -> Optional[dict]:
    """
    Get the file data for a resource as a JSON object.

    Args:
        resource_id (str): The resource identifier.
        file_name (str): The file name.
        version_id (str): The version identifier.

    Returns:
        dict: The JSON object.
    """
    # get the file data
    file_data = get_resource_file_data(resource_id, file_name, version_id)
    if file_data:
        return json.loads(file_data.decode("utf-8"))

    return None


def list_resources() -> List[Dict[str, Any]]:
    """
    List all resources in the cache.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing resource information.
    """
    # log it
    logger.info("Listing all resources in cache...")
    resources = []
    for resource_path in DEFAULT_CACHE_PATH.iterdir():
        if resource_path.is_dir():
            resource_id, version_id = resource_path.name.rsplit("-", 1)
            try:
                metadata = load_resource_metadata(resource_id, version_id)
            except Exception:  # pylint: disable=broad-except
                metadata = {}

            resources.append(
                {
                    "resource_id": resource_id,
                    "version_id": version_id,
                    "resource_path": str(resource_path),
                    "resource_metadata": metadata,
                }
            )
    return resources
