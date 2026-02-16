# PyProg2025_5

Глушков Матвей группа P3120
Lab5: Бинарное дерево (нерекурсивная реализация)
Вывод покажет дерево в четырёх форматах: dict, list, namedtuple, OrderedDict, а также пример с кастомными формулами.

Запуск тестов
python -m unittest test_binary_tree -v
Использование в коде
from binary_tree import gen_bin_tree

# С параметрами по умолчанию (root=13, height=3, left=root+1, right=root-1)
tree = gen_bin_tree()

# С произвольными параметрами
tree = gen_bin_tree(height=4, root=100)

# С кастомными формулами ветвления
tree = gen_bin_tree(
    height=2,
    root=5,
    left_branch=lambda r: r + 1,
    right_branch=lambda r: r**2,
)

# Выбор формата представления
tree_dict = gen_bin_tree(structure="dict")         # базовый
tree_list = gen_bin_tree(structure="list")
tree_nt = gen_bin_tree(structure="namedtuple")
tree_od = gen_bin_tree(structure="ordered_dict")
Описание программы
Алгоритм (нерекурсивный)
Функция gen_bin_tree строит бинарное дерево в два прохода без рекурсии:

Шаг 1 — вычисление значений узлов по уровням:

Уровень 0: [root]
Уровень 1: [left_branch(root), right_branch(root)]
Уровень h: для каждого узла на уровне h-1 вычисляются left_branch(val) и right_branch(val)
Шаг 2 — сборка дерева снизу вверх:

Уровень height: все узлы — листья, {str(val): []}
Уровни h < height: {str(val): [left_tree, right_tree]} — поддеревья берутся из буфера
Параметры
Параметр	По умолчанию	Описание
height	3	Высота дерева
root	13	Значение в корне (вариант задания)
left_branch	lambda r: r + 1	Функция для левого потомка
right_branch	lambda r: r - 1	Функция для правого потомка
structure	"dict"	Формат: dict, list, namedtuple, ordered_dict
Форматы представления
Dict (базовый, формат ТЗ):

{"13": []}                                    # height=0
{"13": [{"14": []}, {"12": []}]}              # height=1
{"13": [{"14": [{"15": []}, {"13": []}]}, {"12": [{"13": []}, {"11": []}]}]}  # height=2
List — [root, left_subtree, right_subtree]:

[13, [14, [], []], [12, [], []]]
NamedTuple (collections):

Node(root=13, left=Node(14, ...), right=Node(12, ...))
OrderedDict (collections):

OrderedDict([("13", [left_tree, right_tree])])
Пример дерева (root=13, height=3)
        13
       /  \
     14    12
    / \   / \
  15  13 13  11
