""" This module defines the ``DefinitionStoreFactory`` class."""
from dataclasses import dataclass
from typing import Callable, Optional
from wkmigrate.definition_stores.definition_store import DefinitionStore
from wkmigrate.definition_stores import types


@dataclass
class DefinitionStoreBuilder:
    """ Builder class for creating ``DefinitionStore`` objects."""
    getters: dict[str, Callable[..., DefinitionStore]] = None

    def __post_init__(self) -> None:
        """ Registers any definition stores to the factory.
            :return: ``None``
        """
        self._register_definition_stores(types)

    def __call__(self, definition_store_type: str, options: Optional[dict] = None) -> DefinitionStore:
        """ Gets a ``DefinitionStore`` object with the given options.
            :parameter definition_store_type: Definition store type
            :parameter options: A set of options for the specified definition store type
            :return: ``DefinitionStore``: A ``DefinitionStore`` of the specified type
        """
        return self.build(definition_store_type=definition_store_type, options=options)

    def build(self, definition_store_type: str, options: Optional[dict] = None) -> DefinitionStore:
        """ Gets a ``DefinitionStore`` object with the given options.
            :parameter definition_store_type: Definition store type
            :parameter options: A set of options for the specified definition store type
            :return: ``DefinitionStore``: A ``DefinitionStore`` of the specified type
        """
        getter = self.getters.get(definition_store_type, None)
        if getter is None:
            raise ValueError(f'No definition store registered with type {definition_store_type}')
        return getter(**options)

    def _register_definition_store(self, definition_store_type: str, getter: Callable[..., DefinitionStore]) -> None:
        """ Registers the ``DefinitionStoreType`` in the factory.
            :parameter definition_store_type: Definition store type
            :parameter getter: A method to instantiate the specified definition store type
            :return: ``None``
        """
        self.getters[definition_store_type] = getter

    def _register_definition_stores(self, definition_stores: dict[str, Callable[..., DefinitionStore]]) -> None:
        """ Registers multiple ``DefinitionStoreTypes`` in the factory.
            :parameter definition_stores: Dictionary of definition store types and instantiators
            :return: ``None``
        """
        self.getters = definition_stores

    def _unregister_definition_store(self, definition_store_type: str) -> None:
        """ Unregisters the specified ``DefinitionStoreType`` in the factory.
            :parameter definition_store_type: Definition store type
            :return: ``None``
        """
        result = self.getters.pop(definition_store_type, None)
        if result is None:
            raise UserWarning(f'No definition store registered with type {definition_store_type}')
