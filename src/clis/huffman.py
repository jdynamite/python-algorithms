import json
from pathlib import Path

from bitstring import ConstBitStream
import click
import rich
from rich import tree, text

from lib.huffman_tree import (
    HuffmanNode,
    build_frequency_table,
    build_huffman_tree,
    compress_string,
    decompress_string,
    get_huffman_codes,
)


@click.group
def main():
    pass

@main.command('hello')
def hello():
    print("Hello from python-algorithms!")


@main.command('count')
@click.argument('string', type=click.STRING)
def count(string: str):
    from pprint import pprint
    pprint(build_frequency_table(string))


@main.command('huffman-tree')
@click.argument('string', type=click.STRING)
def huffman_tree(string: str):
    root = build_huffman_tree(string)
    codes = dict()
    get_huffman_codes(root, "", codes)
    rich_tree = tree.Tree(text.Text(f'({root.frequency})'))

    def _add_children_to_tree(n: HuffmanNode, tree: tree.Tree, include_self: bool = True):
        # only traverse children if we're an intermediate node
        if n.is_intermediate():
            if include_self:
                tree = tree.add(text.Text(f'({n.frequency})'))
            for child in (n.left, n.right):
                if child is None:
                    continue
                else:
                    _add_children_to_tree(child, tree, include_self=True)
        else:
            tree.add(text.Text(f'[{n.character}][{n.frequency}][{codes[n.character]}]', style='bold bright_blue'))

    # traverse the tree
    _add_children_to_tree(root, rich_tree, include_self=False)

    # and print the result
    rich.print(rich_tree)


@main.command('huffman-compress')
@click.argument('string', type=click.STRING)
@click.argument('output', type=click.Path(path_type=Path))
def huffman_compress(string: str, output: Path):
    new_string, codes = compress_string(string)
    output.write_text(json.dumps(codes, indent=4))
    print(f'compressed into: {new_string}')
    print(f'codes output to: {output}')


@main.command('huffman-decompress')
@click.argument('string', type=click.STRING)
@click.argument('codes', type=click.Path(path_type=Path))
def huffman_decompress(string: str, codes):
    stream = ConstBitStream(string)
    print(f'original string is: {decompress_string(stream, json.loads(codes.read_text()))}')


if __name__ == "__main__":
    main()
