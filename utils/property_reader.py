import os


class PropertyReader:
    _props = None

    @classmethod
    def _load_properties(cls):
        if cls._props is None:
            props = {}
            root_dir = os.path.dirname(os.path.dirname(__file__))
            filepath = os.path.join(root_dir, "config.properties")
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            if "=" in line:
                                key, value = line.split("=", 1)
                                props[key.strip()] = value.strip()
            cls._props = props
        return cls._props

    @classmethod
    def get_prop(cls, prop_name, default=None):
        props = cls._load_properties()
        return props.get(prop_name, default)
