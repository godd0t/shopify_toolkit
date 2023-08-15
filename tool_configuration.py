from .tool_config_key_type import ToolConfigKeyType


class ToolConfiguration:

    def __init__(self, key: str, key_type: str = None, is_required: bool = False, is_secret: bool = False):
        self.key = key
        self.is_secret = self._validate_boolean(is_secret, "is_secret")
        self.is_required = self._validate_boolean(is_required, "is_required")
        self.key_type = self._validate_key_type(key_type)

    def _validate_boolean(self, value: bool, attribute_name: str) -> bool:
        if value is None:
            return False
        elif isinstance(value, bool):
            return value
        else:
            raise ValueError(f"{attribute_name} should be a boolean value")

    def _validate_key_type(self, key_type: str) -> str:
        if key_type is None:
            return ToolConfigKeyType.STRING.value
        elif key_type in ToolConfigKeyType._value2member_map_:
            return key_type
        else:
            raise ValueError(f"{key_type} is not a valid key type.")
