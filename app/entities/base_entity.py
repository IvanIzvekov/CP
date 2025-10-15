from datetime import datetime
from typing import Any, Dict, List, Optional, get_args, get_origin

from app.models.base_model import Base


class BaseEntity:
    def to_dict(self) -> dict:
        def convert(value: Any):
            if isinstance(value, BaseEntity):
                return value.to_dict()
            elif isinstance(value, list):
                return [convert(v) for v in value]
            elif isinstance(value, dict):
                return {k: convert(v) for k, v in value.items()}
            elif isinstance(value, datetime):
                return value.isoformat()
            else:
                return value

        result = {}
        for k, v in self.__dict__.items():
            if k.startswith("_") or v is None:
                continue
            result[k] = convert(v)
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        allowed_fields = cls.__annotations__.keys()
        filtered = {k: v for k, v in data.items() if k in allowed_fields}
        return cls(**filtered)

    @classmethod
    def from_schema(cls, schema: Any):
        if hasattr(schema, "model_dump"):
            data = schema.model_dump(exclude_unset=True)
        elif hasattr(schema, "dict"):
            data = schema.dict(exclude_unset=True)
        else:
            raise TypeError("Schema must be a Pydantic model or dataclass")
        return cls.from_dict(data)

    @classmethod
    def from_model(cls, model, load_relations: bool = False):
        """
        Преобразует SQLAlchemy модель в Entity.
        Если load_relations=False, не обращается к связанным объектам,
        чтобы избежать ленивых запросов и падений в async.
        """
        allowed_fields = cls.__annotations__.keys()
        data = {}

        for field in allowed_fields:
            if not hasattr(model, field):
                continue
            value = getattr(model, field)

            if value is None:
                data[field] = None
                continue

            entity_type = cls.__annotations__.get(field)
            origin_type = get_origin(entity_type)
            args = get_args(entity_type)

            # Списки
            if origin_type in (list, List) and args:
                inner_type = args[0]
                if isinstance(value, list):
                    if load_relations and hasattr(inner_type, "from_model"):
                        data[field] = [
                            (
                                inner_type.from_model(v, load_relations=True)
                                if isinstance(v, Base)
                                else v
                            )
                            for v in value
                        ]
                    else:
                        data[field] = value
                else:
                    data[field] = value
                continue

            # Optional
            if origin_type is Optional and args:
                inner_type = args[0]
                if (
                    load_relations
                    and hasattr(inner_type, "from_model")
                    and isinstance(value, Base)
                ):
                    data[field] = inner_type.from_model(
                        value, load_relations=True
                    )
                else:
                    data[field] = value
                continue

            # Entity
            if (
                load_relations
                and hasattr(entity_type, "from_model")
                and isinstance(value, Base)
            ):
                data[field] = entity_type.from_model(
                    value, load_relations=True
                )
                continue

            # Простые поля
            data[field] = value

        return cls(**data)
