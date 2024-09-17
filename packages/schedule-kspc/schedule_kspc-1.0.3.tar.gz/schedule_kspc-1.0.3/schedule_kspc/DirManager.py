from os import makedirs, listdir
from dataclasses import dataclass, field
from datetime import datetime, timedelta


from .Store import DATETIME_PATTERN


def _create_folder(path: str):
    makedirs(name=path, exist_ok=True)


@dataclass
class _Node:
    name: str = field(default='')
    path: str = field(default='')


@dataclass
class Node(_Node):
    root: None = field(default=None)
    children: list = field(default_factory=list)

    def add_child(self, name: str):
        self.children.append(Node(name=name, path=f'{self.path}\\{name}'))
        return self.children[-1]


@dataclass
class Tree:
    root_node: Node

    def __post_init__(self):
        if self.root_node.name:
            self.root_node.path += f'\\{self.root_node.name}'

    @staticmethod
    def add_node(root, name: str):
        return root.add_child(name)

    @staticmethod
    def get_files(node: Node) -> list:
        return listdir(path=node.path)

    def make_folders(self, node: Node, level: int = 0):
        _create_folder(path=node.path)

        for child in node.children:
            self.make_folders(child, level + 1)


def get_relevant_files(dir_tree: Tree, dir_node: Node) -> dict:
    """
    Sorted filename by current datetime
    :param dir_node:
    :param dir_tree:
    :return:
    """

    # Get nodes (children)
    nodes: list = dir_node.children

    # Get nodes (root_node)
    if not len(nodes):
        nodes: list = [dir_node]

    # Output { node.name: [file1, file2, ...] }
    output: dict = dict({node.name: None for node in nodes})

    # Current datetime
    current_datetime: str = datetime.now().strftime(DATETIME_PATTERN)

    # Cycle for nodes
    for node in nodes:

        # Splitext, remove extension
        files = dir_tree.get_files(node)

        # Not files in directory
        if not len(files):
            continue

        # Find 1 file in directory
        if len(files) == 1:
            output[node.name] = files
            continue

        # Filename convert to datetime
        datetime_files = tuple(_compare_datetime(current_datetime, '_'.join(file.split('_')[0:2])) for file in files)

        # Get sorted indices
        sorted_indices: list[int] = sorted(range(len(datetime_files)), key=lambda i: datetime_files[i])

        # Output { node.name: [ append sorted by datetime file ] }
        output[node.name] = [files[i] for i in sorted_indices]

    return output


def get_first_relevant_file(dir_tree: Tree, dir_node: Node) -> dict[str: str, str: str] | None:
    department_name, files = tuple(get_relevant_files(dir_tree=dir_tree, dir_node=dir_node).items())[0]
    return None if files is None else {'path': f'{dir_node.path}\\{files[0]}', 'name': files[0]}


def _compare_datetime(str_datetime1: str, str_datetime2: str) -> timedelta:
    """
    Compare two datetime
    :param str_datetime1:
    :param str_datetime2:
    :return:
    """
    datetime1: datetime = datetime.strptime(str_datetime1, DATETIME_PATTERN)
    datetime2: datetime = datetime.strptime(str_datetime2, DATETIME_PATTERN)
    date: timedelta = datetime1 - datetime2
    return date
