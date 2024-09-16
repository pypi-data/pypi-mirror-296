"""
CMU Pronouncing Dictionary data source.
"""
# pylint: disable=duplicate-code

# project imports
from alea_data_resources.caching import save_resource_metadata
from alea_data_resources.sources.base.http_source import download_http_resource_archive

SOURCE_METADATA = {
    "id": "wordnet",
    "title": "WordNet",
    "creator": "Carnegie Mellon University",
    "subject": "A Lexical Database for English",
    "description": """WordNet® is a large lexical database of English. Nouns, verbs, adjectives and adverbs are
grouped into sets of cognitive synonyms (synsets), each expressing a distinct concept. Synsets are interlinked
by means of conceptual-semantic and lexical relations. The resulting network of meaningfully related words and
concepts can be navigated with the browser.""",
    "publisher": "Princeton University",
    "contributor": "Princeton University",
    "url": "https://wordnet.princeton.edu/",
    "license": "https://wordnet.princeton.edu/license-and-commercial-use",
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
            "https://wordnetcode.princeton.edu/wn3.1.dict.tar.gz"
        )
    else:
        download_metadata["download_url"] = (
            f"https://wordnetcode.princeton.edu/wn{version_id}.dict.tar.gz"
        )

    # download and extract to cache
    download_status = download_http_resource_archive(
        resource_id="wordnet",
        version_id=version_id,
        url=download_metadata["download_url"],
        archive_type="tar.gz",
        drop_components=1,
    )

    if not download_status:
        return False

    # otherwise, save metadata to cache folder for reference
    save_resource_metadata("cmudict", download_metadata, version_id)

    return True
