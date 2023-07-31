from configparser import ConfigParser


def create_property(name, name_type):
    match name_type():
        case bool():
            @property
            def prop(self):
                return self._config.getboolean(self._section_name, name)
        case int():
            @property
            def prop(self):
                return self._config.getint(self._section_name, name)
        case float():
            @property
            def prop(self):
                return self._config.getfloat(self._section_name, name)
        case str():
            @property
            def prop(self):
                return self._config.get(self._section_name, name)
        case _:
            raise Exception("Non-supported type: " + str(name_type))

    @prop.setter
    def prop(self, value):
        self._config.set(self._section_name, name, str(value))
        self.save()

    return prop


def section(config_path: str, section_name: str):
    def decorator(cls):
        def __init__(self):
            self._config = ConfigParser()
            self._config.read(self._config_path)

        def save(self):
            with open(self._config_path, "w") as fileconfig:
                self._config.write(fileconfig)

        # Для каждого поля типа a: int создаёт сеттер и геттер
        for name, name_type in cls.__annotations__.items():
            setattr(cls, name, create_property(name, name_type))

        setattr(cls, "_config_path", config_path)
        setattr(cls, "_section_name", section_name)
        setattr(cls, "__init__", __init__)
        setattr(cls, "save", save)

        return cls

    return decorator
