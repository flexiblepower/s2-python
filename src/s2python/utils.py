from typing import Generator, Tuple, List, TypeVar

P = TypeVar("P")


def pairwise(arr: List[P]) -> Generator[Tuple[P, P], None, None]:
    for i in range(max(len(arr) - 1, 0)):
        yield arr[i], arr[i + 1]
