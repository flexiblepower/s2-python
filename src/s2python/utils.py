from typing import Generator, Tuple


def pairwise(arr: list) -> Generator[Tuple[int, int], None, None]:
    for i in range(max(len(arr) - 1, 0)):
        yield arr[i], arr[i + 1]
