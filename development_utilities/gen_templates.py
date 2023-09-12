import inspect
import gen_s2

all_members = inspect.getmembers(gen_s2)
all_members.sort(key=lambda t: t[0])

for name, member in all_members:
    if inspect.isclass(member):
        print(
            f"""
from s2python.generated.gen_s2 import {name} as Gen{name}
from s2python.validate_values_mixin import catch_and_convert_exceptions, ValidateValuesMixin


@catch_and_convert_exceptions
class {name}(Gen{name}, ValidateValuesMixin['{name}']):
    class Config(Gen{name}.Config):
        validate_assignment = True
        """
        )
