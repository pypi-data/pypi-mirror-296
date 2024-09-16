""" This module defines the ``JSONDefinitionStore`` class."""
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from wkmigrate.definition_stores.definition_store import DefinitionStore
from wkmigrate.enums.json_source_type import JSONSourceType


@dataclass
class JSONDefinitionStore(DefinitionStore):
    """This class is used to create a target JSON file."""
    json_file_path: Optional[str]

    def load(self, json_source_type: JSONSourceType = JSONSourceType.DATA_FACTORY_PIPELINE) -> dict:
        """ Gets a dictionary representation of a Databricks workflow from the JSON file.
            :return: ``dict`` representation of the Databricks workflow
        """
        if self.json_file_path is None:
            raise ValueError('Must provide a value for "json_file_path".')
        if json_source_type == JSONSourceType.DATA_FACTORY_PIPELINE:
            # TODO: Translate the JSON to the Databricks object model
            pass
        return json.safe_load(Path(self.json_file_path))

    def dump(self, job_definition: dict) -> None:
        """ Writes a workflow definition to the JSON file following the Databricks SDK ``Job`` object definition.
            :parameter job_definition: Databricks workflow definition as a ``dict``
            :return: ``None``
        """
        json.dump(job_definition, Path(self.json_file_path), sort_keys=False)
