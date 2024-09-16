"""
CMU Pronouncing Dictionary data source.
"""
# pylint: disable=duplicate-code

# project imports
from alea_data_resources.caching import save_resource_metadata
from alea_data_resources.sources.base.http_source import download_http_resource_archive

SOURCE_METADATA = {
    "id": "cmudict",
    "title": "CMU Pronouncing Dictionary",
    "creator": "Carnegie Mellon University",
    "subject": "Pronouncing Dictionary",
    "description": """CMUdict (the Carnegie Mellon Pronouncing Dictionary) is a free
pronouncing dictionary of English, suitable for uses in speech
technology and is maintained by the Speech Group in the School of
Computer Science at Carnegie Mellon University.""",
    "publisher": "Carnegie Mellon University",
    "contributor": "Carnegie Mellon University",
    "url": "https://github.com/cmusphinx/cmudict",
    "license": """Use of this dictionary for any research or commercial
purpose is completely unrestricted.  If you make use of or
redistribute this material we request that you acknowledge its
origin in your descriptions.""",
}


def download(version_id: str = "default") -> bool:
    """
    Download the CMU Pronouncing Dictionary data source.

    Args:
        version_id (str): The branch or commit ID to download.

    Returns:
        bool: True if successful, False otherwise.
    """
    # add to local metadata copy
    download_metadata = SOURCE_METADATA.copy()

    if version_id == "default":
        download_metadata["download_url"] = (
            "https://github.com/cmusphinx/cmudict/archive/refs/heads/master.zip"
        )
    else:
        download_metadata["download_url"] = (
            f"https://github.com/cmusphinx/cmudict/archive/refs/heads/{version_id}.zip"
        )

    # download and extract to cache
    download_status = download_http_resource_archive(
        resource_id="cmudict",
        version_id=version_id,
        url=download_metadata["download_url"],
        archive_type="zip",
        drop_components=1,
    )

    if not download_status:
        return False

    # otherwise, save metadata to cache folder for reference
    save_resource_metadata("cmudict", download_metadata, version_id)

    return True
