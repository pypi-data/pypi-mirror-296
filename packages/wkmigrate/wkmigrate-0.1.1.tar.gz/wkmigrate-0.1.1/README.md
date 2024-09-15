# Databricks Workflows Migrator (`wkmigrate`)

<!-- Top bar will be removed from PyPi packaged versions -->
<!-- Dont remove: exclude package -->
[Examples](examples)
<!-- Dont remove: end exclude package -->

[![PyPi package](https://img.shields.io/pypi/v/dbldatagen?color=green)](https://pypi.org/project/wkmigrate)
[![PyPi downloads](https://img.shields.io/pypi/dm/dbldatagen?label=PyPi%20Downloads)](https://pypistats.org/packages/wkmigrate)

## Project Description
`wkmigrate` is a Python library for migrating data pipelines to Databricks workflows from various
frameworks. Users can programmatically create or migrate workflows with a simple set of commands.

Pipeline definitions are read from a user-specified source system, translated for compatibility
with Databricks workflows, and either directly created or stored in `json` or `yml` files.

## Installation

Use `pip install wkmigrate` to install the PyPi package.

## Compatibility 
`wkmigrate` is a standalone project. Using some features (e.g. serverless jobs compute options) may
require a premium-tier Databricks workspace.

## Using the Data Generator
To use the `wkmigrate`, install the library using the `%pip install wkmigrate` method or install the 
Python wheel directly in your environment.

Once the library has been installed, create source and target **definition stores** for the migration.

```buildoutcfg
from azure.identity import ClientSecretCredential
from wkmigrate.definition_store_builder import DefinitionStoreBuilder

# Create the definition store builder:
builder = DefinitionStoreBuilder()

# Create the source definition store (an Azure Data Factory):
factory_credential = ClientSecretCredential(
    tenant_id="<TENANT_ID>",
    client_id="<CLIENT_ID>",
    client_secret="<CLIENT_SECRET>"
)
factory_options = {
    "credential": factory_credential,
    "subscription_id": "<SUBSCRIPTION_ID>",
    "resource_group_name": "<RESOURCE_GROUP_NAME>",
    "factory_name": "<FACTORY_NAME>"
}
factory_store = builder('factory_definition_store', factory_options)

# Create the target definition store (a Databricks workspace):
workspace_options = {
    "authentication_type": "pat",
    "host_name": "DATABRICKS_HOST_URL",
    "pat": "DATABRICKS_PERSONAL_ACCESS_TOKEN",
}
workspace_store = builder('workspace_definition_store', workspace_options)                        
```

Use the `load` method to get definitions from a source.

```buildoutcfg
pipeline = factory_store.load(pipeline_name='PIPELINE_NAME')                      
```

Use `pipeline_translator.translate()` to make pipeline definitions compatible
with Databricks workflows.

```buildoutcfg
from wkmigrate import pipeline_translator
translated_pipeline = pipeline_translator.translate(pipeline)
```

Use the ``dump`` method to sync workflows into a target.

```buildoutcfg
workspace_store.dump(translated_pipeline)
```

The GitHub repository contains more examples in the **examples** directory.
