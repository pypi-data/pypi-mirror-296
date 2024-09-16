import os
from typing import Any, Dict, List, Optional, Union
from .file_handlers import load_file, import_module
from .interfaces import IService, IApplicationFile


class ContextDependencyInjector:
    def __init__(self, parent: "DependencyInjector") -> None:
        self.parent = parent
        self.context_instances: Dict[str, Any] = {}

    def set(self, service_name: str, instance: Any) -> None:
        self.context_instances[service_name] = instance

    def get_instance(self, service_name: str) -> Optional[Any]:
        return self.context_instances.get(service_name)

    def get(self, service_name: str) -> Any:
        if service_name in self.context_instances:
            return self.context_instances[service_name]
        return self.parent.get(service_name, self)


class DependencyInjector:
    def __init__(self, base_path: str = os.path.dirname(__file__)) -> None:
        self.base_path = base_path
        self.definitions: Dict[str, IService] = {}
        self.instances: Dict[str, Any] = {}
        self.modules: Dict[str, Any] = {}
        self.compiled = False

    def load(self, file_path: str, base_path: Optional[str] = None) -> None:
        full_path = os.path.join(base_path or self.base_path, file_path)
        app_file: IApplicationFile = load_file(full_path)

        if app_file.imports:
            current_base_path = os.path.dirname(full_path)
            for import_item in app_file.imports:
                self.load(import_item["resource"], current_base_path)

        self.definitions.update(app_file.services)

    def compile(self) -> None:
        if self.compiled:
            return

        for key, definition in self.definitions.items():
            class_path = self.resolve_class_path(definition)
            if class_path:
                _class_path, class_attribute = class_path.split("#")

                self.modules[key] = getattr(
                    import_module(_class_path), class_attribute or "default"
                )

        self.compiled = True

    def resolve_class_path(self, definition: IService) -> Optional[str]:
        if definition.class_name:
            return os.path.join(self.base_path, definition.class_name)
        if definition.factory and "class" in definition.factory:
            return os.path.join(self.base_path, definition.factory["class"])
        if definition.instance:
            return os.path.join(self.base_path, definition.instance)
        return None

    def get_definition(self, service_name: str) -> Optional[IService]:
        return self.definitions.get(service_name)

    def get_module(self, service_name: str) -> Optional[Any]:
        return self.modules.get(service_name)

    def resolve_argument(
        self,
        arg: Union[str, int, bool],
        context: Optional[ContextDependencyInjector] = None,
    ) -> Any:
        if isinstance(arg, str):
            if arg.startswith("@"):
                return self.get(arg[1:], context)
            if arg.startswith("!tagged"):
                return [
                    self.get(key, context)
                    for key, value in self.definitions.items()
                    if "tags" in value and arg[8:] in value.tags
                ]
            if arg == "!context":
                return context or self
        return arg

    def instantiate_class(self, service_name: str, args: List[Any] = None) -> Any:
        if args is None:
            args = []
        class_ = self.get_module(service_name)
        if not class_:
            raise ValueError(f"Class not found for {service_name}")
        return class_(*args)

    def call_factory(self, service_name: str, method: str, args: List[Any] = None) -> Any:
        if args is None:
            args = []
        factory_class = self.get_module(service_name)
        if not factory_class:
            raise ValueError(f"Factory class not found for {service_name}")
        return getattr(factory_class, method)(*args)

    def create_context(self) -> ContextDependencyInjector:
        return ContextDependencyInjector(self)

    def get(self, service_name: str, context: Optional[ContextDependencyInjector] = None) -> Any:
        definition = self.get_definition(service_name)
        if not definition:
            raise ValueError(f"Service {service_name} is not defined.")

        scope = definition.scope or "ambivalent"
        if scope != "singleton":
            if scope == "request" or context:
                if not context:
                    context = self.create_context()
                instance = context.get_instance(service_name)
                if not instance:
                    instance = self.instantiate_service(service_name, definition, context)
                    context.set(service_name, instance)
                return instance

        if service_name in self.instances:
            return self.instances[service_name]

        instance = self.instantiate_service(service_name, definition)
        if scope != "transient":
            self.instances[service_name] = instance
        return instance

    def instantiate_service(
        self,
        service_name: str,
        definition: IService,
        context: Optional[ContextDependencyInjector] = None,
    ) -> Any:
        args = [self.resolve_argument(arg, context) for arg in definition.arguments]
        if definition.class_name:
            return self.instantiate_class(service_name, args)
        if definition.factory:
            return self.call_factory(service_name, definition.factory["method"], args)
        if definition.instance:
            return self.get_module(service_name)
        raise ValueError(f"Invalid service definition for {service_name}")

    def set(
        self,
        service_name: str,
        instance: Any,
        context: Optional[ContextDependencyInjector] = None,
    ) -> None:
        if context:
            context.set(service_name, instance)
        else:
            self.instances[service_name] = instance

    def get_list_with_tag(
        self, tag_name: str, context: Optional[ContextDependencyInjector] = None
    ) -> List[Any]:
        return [
            self.get(service_name, context)
            for service_name, definition in self.definitions.items()
            if "tags" in definition.tags and tag_name in definition.tags
        ]

    def get_dict_with_tag(
        self, tag_name: str, context: Optional[ContextDependencyInjector] = None
    ) -> Dict[str, Any]:
        return {
            service_name: self.get(service_name, context)
            for service_name, definition in self.definitions.items()
            if "tags" in definition.tags and tag_name in definition.tags
        }

    def link(
        self,
        source_service_name: str,
        target_service_name: str,
        context: Optional[ContextDependencyInjector] = None,
    ) -> None:
        service_instance = self.get(source_service_name, context)

        if service_instance:
            self.set(target_service_name, service_instance, context)
