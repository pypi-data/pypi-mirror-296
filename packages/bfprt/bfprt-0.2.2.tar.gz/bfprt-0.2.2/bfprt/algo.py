from bfprt.types import Comparable


def select[T: Comparable](items: list[T], left: int, right: int, k: int) -> T:
    """Quickselect using left item as pivot.

    - Returns the k-th smallest element of items within left..right inclusive.
    - Also known as the "k-th order statistic".
    - This runs in O(n^2) time, but average case linear.

    Args:
        items (list[T]): A list of items.
        left (int): Start index of the range of items to select from.
        right (int): End index of the range of items to select from.
        k (int): Index of the item to select.

    Returns:
        T: The k-th smallest element of the list of items.
    """
    while True:
        # If the list contains only one element return that element
        if left == right:
            return items[left]

        # Select a pivot_index between left and right
        pivot_index = left

        # Place pivot element in sorted position
        pivot_index = partition(items, left, right, pivot_index)

        # Return selected element or recursively search to the correct side
        if k == pivot_index:
            return items[k]
        if k < pivot_index:
            right = pivot_index - 1
        else:
            left = pivot_index + 1


def partition[T: Comparable](items: list[T], left: int, right: int, pivot_index: int) -> int:
    """Partition items into those less than a pivot and those greater.

    This partition runs in O(n) time.

    Args:
        items (list[T]): A list of items.
        left (int): Start index of the range of items to partition.
        right (int): End index of the range of items to partition.
        pivot_index (int): Index of the element to partition around.

    Returns:
        int: Final index of the pivot element.
    """
    # Determine pivot value
    pivot_value = items[pivot_index]

    # Move pivot to end
    swap(items, pivot_index, right)

    # Swap items until they are partitioned by the pivot element
    store_index = left
    for i in range(left, right):
        if items[i] < pivot_value:
            swap(items, store_index, i)
            store_index += 1

    # Move pivot to its final place
    swap(items, right, store_index)
    return store_index


def select_fast[T: Comparable](items: list[T], left: int, right: int, k: int) -> int:
    """Quickselect using median of medians.

    This runs in O(n) time.

    Args:
        items (list[T]): A list of items.
        left (int): Start index of the range of items to select from.
        right (int): End index of the range of items to select from.
        k (int): Index of the item to select.

    Returns:
        int: Final index of the median element.
    """
    while True:
        if left == right:
            return left
        pivot_index = pick_pivot(items, left, right)
        pivot_index = three_partition(items, left, right, pivot_index, k)

        if k == pivot_index:
            return k
        if k < pivot_index:
            right = pivot_index - 1
        else:
            left = pivot_index + 1


def pick_pivot[T: Comparable](items: list[T], left: int, right: int) -> int:
    """Median of medians pivot selection.

    1. Divide items into groups of at most 5 elements.
    2. Compute the median of each group of 5.
    3. Recursively compute the median of the `n / 5` medians.

    We are guaranteed that this pivot is between the 30th and 70th percentiles.

    Args:
        items (list[T]): A list of items.
        left (int): Start index of the range of items to select a pivot.
        right (int): End index of the range of items to select a pivot.

    Returns:
        int: Index of the pivot element.
    """
    # For 5 or fewer elements get median with insertion sort
    constant_sort_threshold = 5
    if right - left < constant_sort_threshold:
        insertion_sort(items, left, right)
        return (left + right) // 2

    # Chunk n items into n / 5 groups of 5 elements
    for i in range(left, right, 5):
        group_right = i + 4

        # Handle special case of n not a multiple of 5
        if group_right > right:
            group_right = right

        # Compute the median of the group
        insertion_sort(items, i, group_right)

        # Move group median to one of the first n / 5 positions
        group_median = (i + group_right) // 2
        swap(items, group_median, left + (i - left) // 5)

    # Compute the median of all group medians
    mid = int((right - left) / 10 + left + 1)
    return select_fast(items, left, left + (right - left) // 5, mid)


def three_partition[T: Comparable](items: list[T], left: int, right: int, pivot_index: int, k: int) -> int:
    """Partition a list into three partitions, elements less than the pivot, those equal, and those greater.

    This runs in O(n) time.

    Args:
        items (list[T]): A list of items.
        left (int): Start index of the range of items to partition.
        right (int): End index of the range of items to partition.
        pivot_index (int): Index of the element to partition around.
        k (int): Index of the item to select.

    Returns:
        int: Index of the pivot element.
    """
    pivot_value = items[pivot_index]

    # Move pivot to end
    swap(items, pivot_index, right)

    # Move all elements smaller than the pivot to the left of the pivot
    store_index = left
    for i in range(left, right):
        if items[i] < pivot_value:
            swap(items, store_index, i)
            store_index += 1

    # Move all elements equal to the pivot right after the smaller elements
    store_index_eq = store_index
    for i in range(store_index, right):
        if items[i] == pivot_value:
            swap(items, store_index_eq, i)
            store_index_eq += 1

    # Move pivot to its final place
    swap(items, right, store_index_eq)

    # Return location of pivot considering the desired location n
    if k < store_index:
        return store_index  # k is in the group of smaller elements
    if k <= store_index_eq:
        return k  # k is in the group equal to pivot

    return store_index_eq  # k is in the group of larger elements


def swap[T: Comparable](items: list[T], a: int, b: int) -> None:
    """Swap two items in a list given their indices.

    Args:
        items (list[T]): A list of items.
        a (int): Index of the first item to swap.
        b (int): Index of the second item to swap.
    """
    vt = items[a]
    items[a] = items[b]
    items[b] = vt


def insertion_sort[T: Comparable](items: list[T], left: int, right: int) -> None:
    """Insertion sort.

    This runs in O(n^2) time.

    Args:
        items (list[T]): A list of items.
        left (int): Start index of the range of items to sort.
        right (int): End index of the range of items to sort.
    """
    i = left + 1
    while i <= right:
        j = i
        while j > left and items[j - 1] > items[j]:
            swap(items, j - 1, j)
            j -= 1
        i += 1
