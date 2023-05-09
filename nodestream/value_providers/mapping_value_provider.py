from typing import Any, Iterable, Type

from yaml import SafeLoader

from ..model import InterpreterContext
from .value_provider import StaticValueOrValueProvider, ValueProvider


class MappingValueProvider(ValueProvider):
    @classmethod
    def install_yaml_tag(cls, loader: Type[SafeLoader]):
        loader.add_constructor(
            "!mapping",
            lambda loader, node: MappingValueProvider(**loader.construct_mapping(node)),
        )

    def __init__(self, mapping_name: str, key: StaticValueOrValueProvider) -> None:
        self.mapping_name = mapping_name
        self.key = ValueProvider.garuntee_value_provider(key)

    def single_value(self, context: InterpreterContext) -> Any:
        mapping = context.mappings.get(self.mapping_name)
        if not mapping:
            return

        key = self.key.single_value(context)
        if not key:
            return

        value = ValueProvider.garuntee_value_provider(mapping.get(key))
        return value.single_value(context)

    def many_values(self, context: InterpreterContext) -> Iterable[Any]:
        value = self.single_value(context)
        return [value] if value else []