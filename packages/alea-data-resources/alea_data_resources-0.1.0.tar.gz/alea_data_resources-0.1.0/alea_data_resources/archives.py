"""
Archive utilities for the ALEA data resources package.
"""

# imports
import logging
import tarfile
import zipfile
from pathlib import Path
from typing import Union

# packages
import tqdm

# project
from alea_data_resources.caching import get_resource_path

# set up logger
logger = logging.getLogger(__name__)

# chunk sizes for reading/writing to avoid memory issues
CHUNK_SIZE = 1024 * 1024  # 1 MB


def extract_archive_to_resource(
    resource_id: str,
    version_id: str,
    archive_file: Union[zipfile.ZipFile, tarfile.TarFile],
    drop_components: int = 0,
) -> bool:
    """
    Extract a ZIP or TAR archive to the resource path, optionally dropping the first N path
    components from the archive.

    Args:
        resource_id (str): The resource identifier.
        version_id (str): The version identifier.
        archive_file (Union[zipfile.ZipFile, tarfile.TarFile]): The archive file object.
        drop_components (int): The number of path components to drop.

    Returns:
        bool: True if successful, False otherwise.
    """
    if isinstance(archive_file, zipfile.ZipFile):
        return extract_zip_to_resource(
            resource_id, version_id, archive_file, drop_components
        )

    if isinstance(archive_file, tarfile.TarFile):
        return extract_tar_to_resource(
            resource_id, version_id, archive_file, drop_components
        )

    logger.error(
        "Unsupported archive type: %s for resource %s:%s",
        type(archive_file),
        resource_id,
        version_id,
    )
    return False


def extract_zip_to_resource(
    resource_id: str,
    version_id: str,
    zip_file: zipfile.ZipFile,
    drop_components: int = 0,
) -> bool:
    """
    Extract a ZIP archive to the resource path, optionally dropping the first N path
    components from the archive.

    Args:
        resource_id (str): The resource identifier.
        version_id (str): The version identifier.
        zip_file (zipfile.ZipFile): The ZIP file object.
        drop_components (int): The number of path components to drop.

    Returns:
        bool: True if successful, False otherwise.
    """

    # get the resource path
    resource_path = get_resource_path(resource_id, version_id)

    # iterate through all ZIP members and extract them to the resource path
    for zip_member in tqdm.tqdm(zip_file.infolist(), desc="Extracting ZIP archive"):
        try:
            # drop components if requested
            member_output_path = Path(zip_member.filename)
            if drop_components > 0:
                member_output_path = Path(*member_output_path.parts[drop_components:])
            member_output_path = resource_path / member_output_path

            # check if the member is a directory or file
            if zip_member.is_dir():
                member_output_path.mkdir(parents=True, exist_ok=True)
                continue

            # extract the member
            with zip_file.open(zip_member) as zip_source:
                with member_output_path.open("wb") as output_file:
                    while data := zip_source.read(CHUNK_SIZE):
                        output_file.write(data)
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Failed to extract ZIP member %s: %s", zip_member.filename, e)
            return False

    return True


def extract_tar_to_resource(
    resource_id: str,
    version_id: str,
    tar_file: tarfile.TarFile,
    drop_components: int = 0,
) -> bool:
    """
    Extract a TAR archive to the resource path, optionally dropping the first N path
    components from the archive.

    Args:
        resource_id (str): The resource identifier.
        version_id (str): The version identifier.
        tar_file (tarfile.TarFile): The TAR file object.
        drop_components (int): The number of path components to drop.

    Returns:
        bool: True if successful, False otherwise.
    """

    # get the resource path
    resource_path = get_resource_path(resource_id, version_id)

    # iterate through all TAR members and extract them to the resource path
    for tar_member in tqdm.tqdm(tar_file.getmembers(), desc="Extracting TAR archive"):
        try:
            # drop components if requested
            member_output_path = Path(tar_member.name)
            if drop_components > 0:
                member_output_path = Path(*member_output_path.parts[drop_components:])
            member_output_path = resource_path / member_output_path

            # check if the member is a directory or file
            if tar_member.isdir():
                member_output_path.mkdir(parents=True, exist_ok=True)
                continue

            # extract the member
            with tar_file.extractfile(tar_member) as tar_source:  # type: ignore
                with member_output_path.open("wb") as output_file:
                    while data := tar_source.read(CHUNK_SIZE):
                        output_file.write(data)
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Failed to extract TAR member  %s: %s", tar_member.name, e)
            return False

    return True
