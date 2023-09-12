def pairwise(arr: list):
    for i in range(max(len(arr) - 1, 0)):
        yield (arr[i], arr[i + 1])
