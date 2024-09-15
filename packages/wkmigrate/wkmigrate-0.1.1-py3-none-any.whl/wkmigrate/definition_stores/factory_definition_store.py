""" This module defines the ``FactoryDefinitionStore`` class."""
from dataclasses import dataclass, field
from typing import Optional
from azure.identity import DefaultAzureCredential
from azure.mgmt.datafactory import DataFactoryManagementClient
from .definition_store import DefinitionStore


@dataclass
class FactoryDefinitionStore(DefinitionStore):
    """This class is used to list and describe objects in an Azure Data Factory instance."""
    credential: DefaultAzureCredential
    subscription_id: str
    resource_group_name: str
    factory_name: str
    management_client: Optional[DataFactoryManagementClient] = field(init=False)

    def load(self, pipeline_name: str) -> dict:
        """ Gets a dictionary representation of a Data Factory pipeline.
            :parameter pipeline_name: Name of the Data Factory pipeline as an ``str``
            :return: Data Factory pipeline as a ``dict``
        """
        pipeline = self._get_pipeline(pipeline_name=pipeline_name)
        pipeline['trigger'] = self._get_trigger(pipeline_name=pipeline_name)
        pipeline['activities'] = [
            self._append_linked_service(activity=activity)
            for activity in pipeline.get('activities')
        ]
        return pipeline

    def dump(self, pipeline_definition: dict) -> None:
        raise UserWarning('Dump to FactoryDefinitionStore not supported.')

    def __post_init__(self) -> None:
        """ Sets up the Data Factory management client for the provided credentials."""
        self.management_client = DataFactoryManagementClient(self.credential, self.subscription_id)

    def _get_pipeline(self, pipeline_name: str) -> dict:
        """ Gets a pipeline definition with the specified name.
            :parameter pipeline_name: Name of the Data Factory pipeline as an ``str``
            :return: Data Factory pipeline definition as a ``dict``
        """
        pipeline = self.management_client.pipelines.get(self.resource_group_name, self.factory_name, pipeline_name)
        if pipeline is None:
            raise ValueError(f'No pipeline found with name "{pipeline_name}"')
        return pipeline.as_dict()

    def _append_linked_service(self, activity: dict) -> Optional[dict]:
        """ Gets the Databricks linked service for the specified pipeline activity
            :parameter activity: Data Factory activity definition as a ``dict``
            :return: Data Factory activity definition with parsed linked service as a ``dict``
        """
        if 'linked_service_name' in activity:
            # Get the linked service reference name:
            linked_service_reference = activity.get('linked_service_name')
            linked_service_name = linked_service_reference.get('reference_name')
            # Get the linked service details from data factory:
            activity['linked_service_definition'] = self._get_linked_service(linked_service_name=linked_service_name)
        # Check the nested activities:
        if 'if_false_activities' in activity:
            activity['if_false_activities'] = [
                self._append_linked_service(activity=if_false_activity)
                for if_false_activity in activity.get('if_false_activities')
            ]
        if 'if_true_activities' in activity:
            activity['if_true_activities'] = [
                self._append_linked_service(activity=if_true_activity)
                for if_true_activity in activity.get('if_true_activities')
            ]
        return activity

    def _get_linked_service(self, linked_service_name: str) -> dict:
        """ Gets a linked service with the specified name from a Data Factory.
            :parameter linked_service_name: Name of the linked service in Data Factory as an ``str``
            :return: Linked service definition as a ``dict``
        """
        linked_service = self.management_client.linked_services.get(
            resource_group_name=self.resource_group_name,
            factory_name=self.factory_name,
            linked_service_name=linked_service_name
        )
        return linked_service.as_dict()

    def _get_trigger(self, pipeline_name: str) -> dict:
        """ Gets a single trigger for a Data Factory pipeline.
            :parameter pipeline_name: Name of the Data Factory pipeline as an ``str``
            :return: Triggers in the source Data Factory as a ``list[dict]``
        """
        triggers = self._get_triggers()
        for trigger in triggers:
            properties = trigger.get('properties')
            if properties is None:
                continue
            pipelines = properties.get('pipelines')
            if pipelines is None:
                continue
            pipeline_references = [
                pipeline.get('pipeline_reference') for pipeline in pipelines
                if pipeline.get('pipeline_reference') is not None
            ]
            pipeline_names = [
                pipeline_reference.get('reference_name') for pipeline_reference in pipeline_references
                if pipeline_reference.get('reference_name') is not None
                and pipeline_reference.get('type') == 'PipelineReference'
            ]
            if pipeline_name in pipeline_names:
                return trigger

    def _get_triggers(self) -> list[dict]:
        """ Lists triggers in the source Data Factory.
            :return: Triggers in the source Data Factory as a ``list[dict]``
        """
        triggers = self.management_client.triggers.list_by_factory(
            resource_group_name=self.resource_group_name,
            factory_name=self.factory_name
        )
        if triggers is None:
            raise ValueError(f'No triggers found for factory "{self.factory_name}"')
        return [trigger.as_dict() for trigger in triggers]
