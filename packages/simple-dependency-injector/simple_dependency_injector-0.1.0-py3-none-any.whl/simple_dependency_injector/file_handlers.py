import importlib.util
from typing import Any
import yaml
from .interfaces import IApplicationFile, IService


def load_yaml_file(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def import_module(module_path: str) -> Any:
    spec = importlib.util.spec_from_file_location("module.name", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_services(services_data: dict) -> dict:
    services = {}
    for name, service_data in services_data.items():
        if not isinstance(service_data, dict):
            raise ValueError(f"Service definition for '{name}' must be a dictionary")

        class_name = service_data.get("class")
        arguments = service_data.get("arguments", [])
        scope = service_data.get("scope", "singleton")
        factory = service_data.get("factory", None)
        tags = service_data.get("tags", [])
        instance = service_data.get("instance", None)

        if class_name and not isinstance(class_name, str):
            raise ValueError(f"Service '{name}' has an invalid class name: {class_name}")
        if not isinstance(arguments, list):
            raise ValueError(f"Service '{name}' has invalid arguments, should be a list")
        if scope not in ["singleton", "request", "transient", "ambivalent"]:
            raise ValueError(f"Service '{name}' has an invalid scope: {scope}")
        if factory and not isinstance(factory, dict):
            raise ValueError(f"Service '{name}' has an invalid factory definition")
        if not isinstance(tags, list):
            raise ValueError(f"Service '{name}' has invalid tags, should be a list")
        if instance and not isinstance(instance, str):
            raise ValueError(f"Service '{name}' has an invalid instance: {instance}")

        services[name] = IService(
            class_name=class_name,
            arguments=arguments,
            scope=scope,
            factory=factory,
            tags=tags,
            instance=instance,
        )

    return services


def parse_application_file(data: dict) -> IApplicationFile:
    services = parse_services(data.get("services", {}))
    imports = data.get("imports", [])

    if not isinstance(imports, list):
        raise ValueError("Imports must be a list of dictionaries")

    for imp in imports:
        if not isinstance(imp, dict) or "resource" not in imp:
            raise ValueError(f"Invalid import entry: {imp}")

    return IApplicationFile(services=services, imports=imports)


def load_file(file_path: str) -> IApplicationFile:
    if file_path.endswith(".yaml") or file_path.endswith(".yml"):
        config = load_yaml_file(file_path)
    else:
        module = import_module(file_path)
        config = {
            "services": getattr(module, "services", {}),
            "imports": getattr(module, "imports", []),
        }

    return parse_application_file(config)
