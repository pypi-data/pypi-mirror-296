"""
Command line interface for ALEA Data Resources
"""

# imports
import argparse
import importlib
import json
import logging
from typing import Dict, Literal, Optional

# project imports
from alea_data_resources.caching import delete_resource, list_resources, resource_exists

# set up the logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def list_command(output_format: Literal["text", "json", "table"] = "json"):
    """
    List all resources in the cache.

    Args:
        output_format (Literal["text", "json", "table"]): The output format.

    Returns:
        None
    """
    resources = list_resources()
    if not resources:
        if output_format == "json":
            print("[]")
        else:
            print("No resources found.")
    else:
        if output_format == "json":
            print(json.dumps(resources, indent=2))
        elif output_format == "text":
            for resource in resources:
                print(f"Resource ID: {resource['resource_id']}")
                print(f"Version ID: {resource['version_id']}")
                print(f"Path: {resource['resource_path']}")
                print(f"Metadata: {resource['resource_metadata']}")
                print("---")
        else:
            # get all values and print them, truncated up to 80 chars per field
            values = [
                {
                    "resource_id": resource["resource_id"],
                    "version_id": resource["version_id"],
                    "resource_path": str(resource["resource_path"]),
                    "resource_title": resource["resource_metadata"].get("title", "")[
                        0:40
                    ],
                    "resource_creator": resource["resource_metadata"].get(
                        "creator", ""
                    )[0:40],
                    "resource_description": resource["resource_metadata"].get(
                        "description", ""
                    )[0:40],
                }
                for resource in resources
            ]

            # get column widths
            max_field_length: Dict[str, int] = {}
            for key in values[0].keys():
                # set key as longest value
                max_field_length[key] = len(key)
                for value in values:
                    max_field_length[key] = max(
                        max_field_length[key], len(value[key][0:40])
                    )

            print(
                " | ".join(
                    [f"{key:<{max_field_length[key]}}" for key in values[0].keys()]
                )
            )
            print("-" * sum(max_field_length.values()))

            for value in values:
                print(
                    " | ".join(
                        [
                            f"{value[key][0:40]:<{max_field_length[key]}}"
                            for key in value.keys()
                        ]
                    )
                )


def download_command(resource_id: str, version_id: Optional[str] = None):
    """
    Download a resource.

    Args:
        resource_id (str): The resource identifier.
        version_id (Optional[str]): The version identifier.

    Returns:
        None
    """
    try:
        module = importlib.import_module(f"alea_data_resources.sources.{resource_id}")
        download_func = getattr(module, "download")
        success = download_func(version_id=version_id or "default")
        if success:
            print(
                f"Successfully downloaded {resource_id} (version: {version_id or 'default'})"
            )
        else:
            print(
                f"Failed to download {resource_id} (version: {version_id or 'default'})"
            )
    except ImportError:
        print(f"Resource {resource_id} not found or does not have a download function.")
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error downloading {resource_id}: {str(e)}")


def delete_command(resource_id: str, version_id: Optional[str] = None):
    """
    Delete a resource from the cache

    Args:
        resource_id (str): The resource identifier.
        version_id (Optional[str]): The version identifier.

    Returns:

    """
    if resource_exists(resource_id, version_id):
        delete_resource(resource_id, version_id)
        print(f"Deleted resource: {resource_id} (version: {version_id or 'default'})")
    else:
        print(f"Resource not found: {resource_id} (version: {version_id or 'default'})")


def main():
    """
    Main CLI entry point.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="ALEA Data Resources CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # List command
    list_parser = subparsers.add_parser("list", help="List all resources")
    list_parser.add_argument(
        "--format",
        choices=["text", "json", "table"],
        default="table",
        help="Output format",
    )

    # Download command
    download_parser = subparsers.add_parser("download", help="Download a resource")
    download_parser.add_argument("resource_id", help="Resource identifier")
    download_parser.add_argument("--version", help="Version identifier")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a resource")
    delete_parser.add_argument("resource_id", help="Resource identifier")
    delete_parser.add_argument("--version", help="Version identifier")

    args = parser.parse_args()

    if args.command == "list":
        list_command(args.format)
    elif args.command == "download":
        download_command(args.resource_id, args.version)
    elif args.command == "delete":
        delete_command(args.resource_id, args.version)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
