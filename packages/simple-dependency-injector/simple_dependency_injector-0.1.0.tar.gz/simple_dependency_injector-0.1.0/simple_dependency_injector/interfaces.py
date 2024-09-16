from typing import Dict, List, Optional


class IService:
    def __init__(
        self,
        class_name: Optional[str] = None,
        arguments: Optional[List[str]] = None,
        scope: Optional[str] = "singleton",
        factory: Optional[dict] = None,
        tags: Optional[List[str]] = None,
        instance: Optional[str] = None,
    ) -> None:
        self.class_name = class_name
        self.arguments = arguments or []
        self.scope = scope
        self.factory = factory
        self.tags = tags or []
        self.instance = instance


class IApplicationFile:
    def __init__(
        self,
        services: Dict[str, IService],
        imports: Optional[List[Dict[str, str]]] = None,
    ) -> None:
        self.services = services
        self.imports = imports or []
