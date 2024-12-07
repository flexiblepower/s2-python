import inspect
import s2python.generated.gen_s2

all_members = inspect.getmembers(s2python.generated.gen_s2)
all_members.sort(key=lambda t: t[0])


print(
    """
from s2python.common import *
from s2python.frbc import *

TYPE_TO_MESSAGE_CLASS = {"""
)

for name, member in all_members:
    if (
        inspect.isclass(member)
        and hasattr(member, "__fields__")
        and ("message_type" in member.__fields__)
    ):
        print(f"    '{member.__fields__['message_type'].default}': {name},")

print("}")
