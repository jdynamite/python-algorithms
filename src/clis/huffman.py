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

def print_huffman_tree(root: 'HuffmanNode', codes: dict[str, str]):
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
    root, _ = build_huffman_tree(string)
    codes = dict()
    get_huffman_codes(root, "", codes)
    print_huffman_tree(root, codes)


@main.command('huffman-compress')
@click.argument('string', type=click.STRING)
@click.argument('output', type=click.Path(path_type=Path))
def huffman_compress(string: str, output: Path):
    result = compress_string(string)
    reversed_codes = {v: k for k,v in result.codes.items()}
    output.write_text(json.dumps(reversed_codes, indent=4))

    click.secho(f'Frequency table:', fg='cyan')
    rich.print(result.frequency_table)

    click.secho(f'Compressed string into: {result.output_value}', fg='cyan')
    click.secho(f'Codes output to: {output}', fg='cyan')

    click.secho(f'Tree:', fg='cyan')
    print_huffman_tree(result.tree, result.codes)


@main.command('huffman-decompress')
@click.argument('string', type=click.STRING)
@click.argument('codes', type=click.Path(path_type=Path))
def huffman_decompress(string: str, codes: Path):
    stream = ConstBitStream(string)
    print(f'original string is: {decompress_string(stream, json.loads(codes.read_text()))}')


if __name__ == "__main__":
    main()
