"""
Тесты для модуля binary_tree (Lab5).

Запуск: python -m unittest test_binary_tree -v
"""

import unittest
from collections import OrderedDict

from binary_tree import gen_bin_tree


class TestGenBinTree(unittest.TestCase):
    """Тесты функции gen_bin_tree (нерекурсивная реализация)."""

    def test_default_params(self) -> None:
        """Проверка работы с параметрами по умолчанию (root=13, height=3)."""
        tree = gen_bin_tree()
        self.assertIn("13", tree)
        children = tree["13"]
        self.assertEqual(len(children), 2)
        self.assertIn("14", children[0])
        self.assertIn("12", children[1])

    def test_height_zero(self) -> None:
        """При height=0 возвращается только корень без потомков."""
        tree = gen_bin_tree(height=0, root=13)
        self.assertEqual(tree, {"13": []})

    def test_height_one(self) -> None:
        """При height=1 — корень с двумя листьями."""
        tree = gen_bin_tree(height=1, root=13)
        self.assertEqual(tree, {"13": [{"14": []}, {"12": []}]})

    def test_custom_params(self) -> None:
        """Проверка с произвольными параметрами height и root."""
        tree = gen_bin_tree(height=2, root=100)
        self.assertIn("100", tree)
        children = tree["100"]
        self.assertEqual(children[0], {"101": [{"102": []}, {"100": []}]})
        self.assertEqual(children[1], {"99": [{"100": []}, {"98": []}]})

    def test_left_right_formula(self) -> None:
        """Проверка формул по умолчанию: left=root+1, right=root-1."""
        tree = gen_bin_tree(height=1, root=50)
        self.assertEqual(tree, {"50": [{"51": []}, {"49": []}]})

    def test_custom_branches(self) -> None:
        """Проверка передачи своих left_branch и right_branch."""
        tree = gen_bin_tree(
            height=2,
            root=5,
            left_branch=lambda r: r + 1,
            right_branch=lambda r: r**2,
        )
        expected = {
            "5": [
                {"6": [{"7": []}, {"36": []}]},
                {"25": [{"26": []}, {"625": []}]},
            ]
        }
        self.assertEqual(tree, expected)

    def test_dict_structure(self) -> None:
        """Проверка корректности структуры dict."""
        tree = gen_bin_tree(height=2, root=10, structure="dict")
        self.assertIn("10", tree)
        self.assertIsInstance(tree["10"], list)
        self.assertEqual(len(tree["10"]), 2)
        self.assertIsInstance(tree["10"][0], dict)
        self.assertIsInstance(tree["10"][1], dict)

    def test_list_structure(self) -> None:
        """Проверка корректности структуры list."""
        tree = gen_bin_tree(height=2, root=10, structure="list")
        self.assertIsInstance(tree, list)
        self.assertEqual(len(tree), 3)
        self.assertEqual(tree[0], 10)
        self.assertIsInstance(tree[1], list)
        self.assertIsInstance(tree[2], list)

    def test_namedtuple_structure(self) -> None:
        """Проверка структуры namedtuple."""
        tree = gen_bin_tree(height=2, root=10, structure="namedtuple")
        self.assertEqual(tree.root, 10)
        self.assertIsNotNone(tree.left)
        self.assertIsNotNone(tree.right)
        self.assertEqual(tree.left.root, 11)
        self.assertEqual(tree.right.root, 9)

    def test_ordered_dict_structure(self) -> None:
        """Проверка OrderedDict из collections."""
        tree = gen_bin_tree(height=2, root=10, structure="ordered_dict")
        self.assertIsInstance(tree, OrderedDict)
        self.assertIn("10", tree)
        children = tree["10"]
        self.assertEqual(len(children), 2)
        self.assertIn("11", children[0])
        self.assertIn("9", children[1])

    def test_invalid_structure_raises(self) -> None:
        """Неизвестный format вызывает ValueError."""
        with self.assertRaises(ValueError):
            gen_bin_tree(structure="invalid")


if __name__ == "__main__":
    unittest.main()
