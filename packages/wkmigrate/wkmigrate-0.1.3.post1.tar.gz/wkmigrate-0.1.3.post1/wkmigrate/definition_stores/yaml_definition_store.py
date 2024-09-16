""" This module defines the ``YAMLDefinitionStore`` class."""
import yaml
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from wkmigrate.definition_stores.definition_store import DefinitionStore


@dataclass
class YAMLDefinitionStore(DefinitionStore):
    """ This class is used to create a target YAML file."""
    yaml_file_path: Optional[str]

    def load(self) -> dict:
        """ Gets a dictionary representation of a Databricks workflow from the YAML file.
            :return: ``dict`` representation of the Databricks workflow
        """
        if self.yaml_file_path is None:
            raise ValueError('Must provide a value for "yaml_file_path".')
        return yaml.safe_load(Path(self.yaml_file_path))

    def dump(self, job_definition: dict) -> None:
        """ Writes a workflow definition to the YAML file following Databricks Asset Bundles' YAML specification.
            :parameter job_definition: Databricks workflow as a ``dict``
            :return: ``None``
        """
        yaml.dump(job_definition, Path(self.yaml_file_path), sort_keys=False)
