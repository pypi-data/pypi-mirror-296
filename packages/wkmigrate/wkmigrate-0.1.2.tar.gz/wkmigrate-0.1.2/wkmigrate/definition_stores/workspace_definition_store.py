""" This module defines the ``DatabricksWorkspaceDefinitionStore`` class."""
from dataclasses import dataclass, field
from typing import Optional
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import BaseJob, CronSchedule, Job, Task
from wkmigrate.definition_stores.definition_store import DefinitionStore


@dataclass
class WorkspaceDefinitionStore(DefinitionStore):
    """This class is used to list, describe, and update objects in a Databricks workspace."""
    authentication_type: str
    host_name: str
    pat: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    resource_id: Optional[str] = None
    tenant_id: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    workspace_client: Optional[WorkspaceClient] = field(init=False)

    def __post_init__(self) -> None:
        """ Sets up the workspace client for the provided authentication credentials.
            :return: ``None``
        """
        if self.authentication_type == 'pat':
            self.workspace_client = self._login_with_pat()
            return
        if self.authentication_type == 'basic':
            self.workspace_client = self._login_with_basic_auth()
            return
        if self.authentication_type == 'azure-client-secret':
            self.workspace_client = self._login_with_azure_client_secret()
            return
        raise ValueError(
            'Got an invalid value for "self.authentication_type", must be "pat", "basic", or "azure-client-secret"')

    def load(self, job_id: Optional[int] = None, job_name: Optional[str] = None) -> dict:
        """ Gets a dictionary representation of a Databricks workflow from the Databricks workspace.
            :parameter job_id: Job ID for the specified workflow
            :parameter job_name: Job name for the specified workflow
            :return: Workflow definition as a ``dict``
        """
        workflow = self._get_workflow(job_id=job_id, job_name=job_name)
        return workflow.as_dict()

    def dump(self, job_settings: dict) -> None:
        """ Creates workflow in the Databricks workspace with the specified definition.
            :parameter job_settings: Workflow definition as a ``dict``
            :return: ``None``
        """
        job_definition = {'settings': job_settings}
        self._create_workflow(job_definition=job_definition)

    def _login_with_pat(self) -> WorkspaceClient:
        """ Creates a ``WorkspaceClient`` with PAT authentication.
            :return: A ``WorkspaceClient`` from the Databricks SDK
        """
        if self.pat is None:
            raise ValueError('No value provided for "pat" with access token authentication')
        return WorkspaceClient(
            auth_type=self.authentication_type,
            host=self.host_name,
            token=self.pat
        )

    def _login_with_basic_auth(self) -> WorkspaceClient:
        """ Creates a ``WorkspaceClient`` with basic authentication.
            :return: A ``WorkspaceClient`` from the Databricks SDK
        """
        if self.username is None:
            raise ValueError('No value provided for "username" with basic authentication')
        if self.password is None:
            raise ValueError('No value provided for "password" with basic authentication')
        return WorkspaceClient(
            auth_type=self.authentication_type,
            host=self.host_name,
            username=self.username,
            password=self.password
        )

    def _login_with_azure_client_secret(self) -> WorkspaceClient:
        """ Creates a ``WorkspaceClient`` with Azure client secret authentication.
            :return: A ``WorkspaceClient`` from the Databricks SDK
        """
        if self.resource_id is None:
            raise ValueError('No value provided for "resource_id" with Azure client secret authentication')
        if self.tenant_id is None:
            raise ValueError('No value provided for "tenant_id" with Azure client secret authentication')
        if self.client_id is None:
            raise ValueError('No value provided for "client_id" with Azure client secret authentication')
        if self.client_secret is None:
            raise ValueError('No value provided for "client_secret" with Azure client secret authentication')
        return WorkspaceClient(
            auth_type=self.authentication_type,
            host=self.host_name,
            azure_workspace_resource_id=self.resource_id,
            azure_tenant_id=self.tenant_id,
            client_id=self.client_id,
            client_secret=self.client_secret
        )

    def _list_workflows(self) -> list[BaseJob]:
        """ Lists workflows in the workspace as ``BaseJob`` objects.
            :return: Workflow definitions as a ``list[BaseJob]``
        """
        workflows = list(self.workspace_client.jobs.list())
        if workflows is None or len(workflows) == 0:
            raise ValueError(f'No workflows found in the target workspace')
        return workflows

    def _get_workflows(self, job_name: str) -> list[BaseJob]:
        """ Gets workflows with the specified name as ``BaseJob`` objects.
            :return: Workflow definitions as a ``list[BaseJob]``
        """
        workflows = list(self.workspace_client.jobs.list(name=job_name))
        if workflows is None or len(workflows) == 0:
            raise ValueError(f'No workflows found in the target workspace with name "{job_name}"')
        return workflows

    def _get_workflow(self, job_id: Optional[int] = None, job_name: Optional[str] = None) -> Job:
        """ Gets a workflow with the specified ID or name as a ``Job`` object.
            :parameter job_id: Job ID for the specified workflow
            :parameter job_name: Job name for the specified workflow
            :return: Workflow definition as a ``Job``
        """
        if job_id is None and job_name is None:
            raise ValueError('Must provide a value for "job_id" or "job_name".')
        if job_id is not None:
            return self.workspace_client.jobs.get(job_id=job_id)
        workflows = self._get_workflows(job_name=job_name)
        if len(workflows) > 1:
            raise ValueError(f'Duplicate workflows found in the target workspace with name "{job_name}"')
        return self.workspace_client.jobs.get(job_id=workflows[0].job_id)

    def _create_workflow(self, job_definition: dict) -> int:
        """ Creates a workflow with the specified definition as a ``dict``.
            :parameter job_definition: Workflow definition settings
            :return: Created Job ID as an ``int``
        """
        job_settings = job_definition.get('settings')
        if job_settings is None:
            raise ValueError('Invalid "job_definition" object.')
        job_name = job_settings.get('name', None)
        if job_name is None:
            raise ValueError('No value provided for "name"')
        else:
            access_control_list = job_settings.get('access_control_list', None)
            is_continuous = job_settings.get('is_continuous', None)
            deployment = job_settings.get('deployment', None)
            description = job_settings.get('description', None)
            edit_mode = job_settings.get('edit_mode', None)
            email_notifications = job_settings.get('email_notifications', None)
            git_source = job_settings.get('git_source', None)
            health_rules = job_settings.get('health_rules', None)
            max_concurrent_runs = job_settings.get('max_concurrent_runs', None)
            notification_settings = job_settings.get('notification_settings', None)
            parameter_definitions = job_settings.get('parameter_definitions', None)
            queue = job_settings.get('queue', None)
            run_as_principal = job_settings.get('run_as_principal', None)
            timeout_seconds = job_settings.get('timeout_seconds', None)
            webhook_notifications = job_settings.get('webhook_notifications', None)
            response = (
                self.workspace_client.jobs.create(
                    name=job_settings.get('name'),
                    schedule=CronSchedule.from_dict(job_settings.get('schedule')),
                    tags=job_settings.get('tags'),
                    tasks=[Task.from_dict(task) for task in job_settings.get('tasks')]
                )
            )
            return response.job_id
