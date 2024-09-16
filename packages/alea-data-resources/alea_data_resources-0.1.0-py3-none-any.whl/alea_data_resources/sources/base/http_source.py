"""
HTTP Source implementation for ALEA data resources.
"""

# imports
import io
import tarfile
import tempfile
import zipfile
from typing import Literal

# packages
import httpx
import tqdm

# project
from alea_data_resources.archives import extract_archive_to_resource
from alea_data_resources.caching import get_resource_path

# constants
HTTP_CHUNK_SIZE = 1024 * 1024  # 1 MB


def download_http_resource_file(
    resource_id: str, version_id: str, url: str, filename: str
) -> bool:
    """
    Download an HTTP resource file to the resource path.

    Args:
        resource_id (str): The resource identifier.
        version_id (str): The version identifier.
        url (str): The URL of the file to download.
        filename (str): The filename to save the file as.

    Returns:
        bool: True if successful, False otherwise.
    """

    # get the resource path
    resource_path = get_resource_path(resource_id, version_id)
    output_file_path = resource_path / filename

    # download the file with tqdm progress bar
    file_prog_bar = tqdm.tqdm(
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
        desc=f"Downloading {filename}",
    )
    with httpx.Client(http2=True, http1=True, follow_redirects=True) as client:
        with client.stream("GET", url, follow_redirects=True) as response:
            try:
                with output_file_path.open("wb") as output_file:
                    for chunk in response.iter_bytes(HTTP_CHUNK_SIZE):
                        output_file.write(chunk)
                        file_prog_bar.update(len(chunk))
            except Exception:  # pylint: disable=broad-except
                return False
            finally:
                file_prog_bar.close()

    return True


# pylint: disable=too-many-return-statements
def download_http_resource_archive(
    resource_id: str,
    version_id: str,
    url: str,
    archive_type: Literal["zip", "tar.gz"],
    drop_components: int = 0,
    use_disk: bool = False,
) -> bool:
    """
    Download an HTTP resource archive to the resource path.

    Args:
        resource_id (str): The resource identifier.
        version_id (str): The version identifier.
        url (str): The URL of the file to download.
        archive_type (Literal["zip", "tar.gz"]): The type of archive.
        drop_components (int): The number of path components to drop.
        use_disk (bool): Whether to use disk for the download

    Returns:
        bool: True if successful, False otherwise.
    """
    # download the file with tqdm progress bar
    file_prog_bar = tqdm.tqdm(
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
        desc=f"Downloading {resource_id}:{version_id} archive",
    )

    # stream into the buffer
    with httpx.Client(http2=True, http1=True, follow_redirects=True) as client:
        with client.stream("GET", url, follow_redirects=True) as response:
            if not use_disk:
                # archive buffer
                archive_buffer = io.BytesIO()

                try:
                    for chunk in response.iter_bytes(HTTP_CHUNK_SIZE):
                        archive_buffer.write(chunk)
                        file_prog_bar.update(len(chunk))
                except Exception:  # pylint: disable=broad-except
                    return False
                finally:
                    file_prog_bar.close()

                # get the archive
                archive_buffer.seek(0)
                if archive_type == "zip":
                    with zipfile.ZipFile(archive_buffer) as archive_file:
                        return extract_archive_to_resource(
                            resource_id, version_id, archive_file, drop_components
                        )
                elif archive_type == "tar.gz":
                    with tarfile.open(
                        fileobj=archive_buffer, mode="r:gz"
                    ) as archive_file:
                        return extract_archive_to_resource(
                            resource_id, version_id, archive_file, drop_components
                        )
                else:
                    return False

            # disk-based case for large files/low mem
            with tempfile.TemporaryFile() as temp_file:
                for chunk in response.iter_bytes(HTTP_CHUNK_SIZE):
                    temp_file.write(chunk)
                    file_prog_bar.update(len(chunk))
                temp_file.seek(0)
                file_prog_bar.close()

                # get the archive
                if archive_type == "zip":
                    with zipfile.ZipFile(temp_file) as archive_file:
                        return extract_archive_to_resource(
                            resource_id, version_id, archive_file, drop_components
                        )
                elif archive_type == "tar.gz":
                    with tarfile.open(fileobj=temp_file, mode="r:gz") as archive_file:
                        return extract_archive_to_resource(
                            resource_id, version_id, archive_file, drop_components
                        )
                else:
                    return False
