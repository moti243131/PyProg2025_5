"""
Модуль для построения бинарного дерева нерекурсивным способом.

Поддерживает несколько форматов представления: dict, list,
namedtuple и OrderedDict из модуля collections.
"""

from collections import OrderedDict, namedtuple
from typing import Any, Callable

Node = namedtuple("Node", ["root", "left", "right"])


def gen_bin_tree(
    height: int = 3,
    root: int = 13,
    left_branch: Callable[[int], int] = lambda r: r + 1,
    right_branch: Callable[[int], int] = lambda r: r - 1,
    structure: str = "dict",
) -> dict[str, Any] | list[Any] | Node | OrderedDict[str, Any]:
    """
    Строит бинарное дерево нерекурсивно с заданной высотой и корнем.

    Левый потомок вычисляется через left_branch(root), правый — через
    right_branch(root). По умолчанию: left=root+1, right=root-1.
    При height=0 возвращается только корень без потомков.

    Args:
        height: Высота дерева. По умолчанию 3 (вариант).
        root: Значение в корне дерева. По умолчанию 13 (вариант).
        left_branch: Функция для вычисления левого потомка. По умолчанию r+1.
        right_branch: Функция для вычисления правого потомка. По умолчанию r-1.
        structure: Формат представления: "dict", "list", "namedtuple",
            "ordered_dict". По умолчанию "dict".

    Returns:
        Бинарное дерево в выбранном формате.

    Raises:
        ValueError: Если structure не поддерживается.
    """
    if structure == "dict":
        return _build_tree_dict(height, root, left_branch, right_branch)
    if structure == "list":
        return _build_tree_list(height, root, left_branch, right_branch)
    if structure == "namedtuple":
        return _build_tree_namedtuple(height, root, left_branch, right_branch)
    if structure == "ordered_dict":
        return _build_tree_ordered_dict(height, root, left_branch, right_branch)
    raise ValueError(
        f"Неизвестный формат: {structure}. "
        "Допустимые: dict, list, namedtuple, ordered_dict"
    )


def _compute_levels(
    height: int,
    root: int,
    left_branch: Callable[[int], int],
    right_branch: Callable[[int], int],
) -> list[list[int]]:
    """
    Вычисляет значения всех узлов по уровням (итеративно).

    Returns:
        Список уровней, где levels[h] — список значений узлов на уровне h.
    """
    levels: list[list[int]] = []
    if height < 0:
        return levels
    levels.append([root])
    for h in range(1, height + 1):
        prev_level = levels[h - 1]
        curr_level: list[int] = []
        for val in prev_level:
            curr_level.append(left_branch(val))
            curr_level.append(right_branch(val))
        levels.append(curr_level)
    return levels


def _build_tree_dict(
    height: int,
    root: int,
    left_branch: Callable[[int], int],
    right_branch: Callable[[int], int],
) -> dict[str, Any]:
    """Строит дерево в формате словаря (базовый формат ТЗ)."""
    levels = _compute_levels(height, root, left_branch, right_branch)
    if not levels:
        return {}
    # Буфер поддеревьев: trees[h][i] — дерево узла (h, i)
    trees: list[list[dict[str, Any]]] = []
    for h in range(height, -1, -1):
        level_vals = levels[h]
        level_trees: list[dict[str, Any]] = []
        for i, val in enumerate(level_vals):
            if h == height:
                level_trees.append({str(val): []})
            else:
                left_tree = trees[height - h - 1][2 * i]
                right_tree = trees[height - h - 1][2 * i + 1]
                level_trees.append({str(val): [left_tree, right_tree]})
        trees.append(level_trees)
    return trees[-1][0]


def _build_tree_list(
    height: int,
    root: int,
    left_branch: Callable[[int], int],
    right_branch: Callable[[int], int],
) -> list[Any]:
    """Строит дерево в формате списка [root, left_subtree, right_subtree]."""
    levels = _compute_levels(height, root, left_branch, right_branch)
    if not levels:
        return []
    trees: list[list[list[Any]]] = []
    for h in range(height, -1, -1):
        level_vals = levels[h]
        level_trees: list[list[Any]] = []
        for i, val in enumerate(level_vals):
            if h == height:
                level_trees.append([val, [], []])
            else:
                left_tree = trees[height - h - 1][2 * i]
                right_tree = trees[height - h - 1][2 * i + 1]
                level_trees.append([val, left_tree, right_tree])
        trees.append(level_trees)
    return trees[-1][0]


def _build_tree_namedtuple(
    height: int,
    root: int,
    left_branch: Callable[[int], int],
    right_branch: Callable[[int], int],
) -> Node:
    """Строит дерево в формате namedtuple из collections."""
    levels = _compute_levels(height, root, left_branch, right_branch)
    if not levels:
        return Node(root=0, left=None, right=None)
    trees: list[list[Node | None]] = []
    for h in range(height, -1, -1):
        level_vals = levels[h]
        level_trees: list[Node | None] = []
        for i, val in enumerate(level_vals):
            if h == height:
                level_trees.append(Node(root=val, left=None, right=None))
            else:
                left_node = trees[height - h - 1][2 * i]
                right_node = trees[height - h - 1][2 * i + 1]
                level_trees.append(Node(root=val, left=left_node, right=right_node))
        trees.append(level_trees)
    result = trees[-1][0]
    return result if result is not None else Node(root=root, left=None, right=None)


def _build_tree_ordered_dict(
    height: int,
    root: int,
    left_branch: Callable[[int], int],
    right_branch: Callable[[int], int],
) -> OrderedDict[str, Any]:
    """Строит дерево в формате OrderedDict из collections."""
    levels = _compute_levels(height, root, left_branch, right_branch)
    if not levels:
        return OrderedDict()
    trees: list[list[OrderedDict[str, Any]]] = []
    for h in range(height, -1, -1):
        level_vals = levels[h]
        level_trees: list[OrderedDict[str, Any]] = []
        for i, val in enumerate(level_vals):
            if h == height:
                level_trees.append(OrderedDict([(str(val), [])]))
            else:
                left_tree = trees[height - h - 1][2 * i]
                right_tree = trees[height - h - 1][2 * i + 1]
                level_trees.append(
                    OrderedDict([(str(val), [left_tree, right_tree])])
                )
        trees.append(level_trees)
    return trees[-1][0]


def main() -> None:
    """Демонстрация работы gen_bin_tree для всех форматов."""

    print("Dict (базовый формат)")
    tree_dict = gen_bin_tree(height=3, root=13, structure="dict")
    print(tree_dict)

    print("\nList")
    tree_list = gen_bin_tree(height=3, root=13, structure="list")
    print(tree_list)

    print("\nNamedTuple (collections)")
    tree_nt = gen_bin_tree(height=3, root=13, structure="namedtuple")
    print(tree_nt)

    print("\nOrderedDict (collections)")
    tree_od = gen_bin_tree(height=3, root=13, structure="ordered_dict")
    print(tree_od)

    print("\nС кастомными формулами (left=root+1, right=root**2)")
    tree_custom = gen_bin_tree(
        height=2,
        root=5,
        left_branch=lambda r: r + 1,
        right_branch=lambda r: r**2,
        structure="dict",
    )
    print(tree_custom)


if __name__ == "__main__":
    main()
