import inspect
import s2python.frbc as frbc
import s2python.common as common

from pydantic import BaseModel

all_members = inspect.getmembers(frbc) + inspect.getmembers(common)
all_members.sort(key=lambda t: t[0])

for name, member in all_members:
    if (
        inspect.isclass(member)
        and issubclass(member, BaseModel)
        and "message_type" in member.__fields__
    ):
        print(f"{name},")
