import os
import json
import warnings

from typing import Union
from urllib.request import urlopen
from pathlib import Path
from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.loaders import yaml_loader


def is_web_url(path):
    """
    Checks if the given path is a web URL.
    :param path: path reference to check
    :return: True if a web URL, False otherwise
    """
    return str(path).startswith("http://") or str(path).startswith("https://")


def get_json_from_url(url):
    """Loads JSOn from web URL."""
    return json.loads(urlopen(url).read())


def get_json_from_file(filename):
    """Loads JSON from a file."""
    try:
        with open(filename, "r") as f:
            fc = f.read()
        return json.loads(fc)
    except FileNotFoundError:
        warnings.warn("File not found: " + filename)
    except IOError as exc:
        warnings.warn("I/O error while opening " + filename + ": " + str(exc))
    except json.JSONDecodeError as exc:
        warnings.warn("Failed to parse JSON in " + filename + ": " + str(exc))


def read_schema(schema: Union[str, dict]) -> SchemaDefinition:
    """
    Reads the given LinkML schema.
    Parameters:
        schema: The schema to read. When provided with a string, the input will first attempt to resolve to a predefined
         schema name (e.g., `base`, `cap`, `bican`). If it does not match any predefined schema name, it will be
         interpreted as a path, URL, or other loadable location. If the input is a dictionary, it should be compatible
         with `SchemaDefinition`. Otherwise, it should be an instance of `SchemaDefinition`.
    Returns: The SchemaDefinition object.
    """
    try:
        if isinstance(schema, str) and str(schema).lower() in get_cas_schema_names().keys():
            schema_dir = os.path.join(os.path.dirname(__file__), "../../build")
            schema = os.path.join(schema_dir, get_cas_schema_names()[str(schema).lower()])
        if isinstance(schema, Path):
            schema = str(schema)
        if isinstance(schema, dict):
            schema = SchemaDefinition(**schema)
        elif isinstance(schema, str):
            schema = yaml_loader.load(schema, target_class=SchemaDefinition)

        if not isinstance(schema, SchemaDefinition):
            raise ValueError(f"Schema could not be loaded from {schema}")
    except ValueError as e:
        raise ValueError(f"Invalid schema: {schema}") from e
    return schema


def get_cas_schema_names() -> dict:
    """
    Returns the list of available CAS schema names.

    Returns:
        dict: The available CAS schema names.
    """
    return {
        "base": "general_schema.yaml",
        "cap": "CAP_schema.yaml",
        "bican": "BICAN_schema.yaml",
    }
