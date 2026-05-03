from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import Optional
from bitstring import ConstBitStream

NULL_CHAR = '\0'


@dataclass
class CompressionResult:
    input_string: str
    output_value: ConstBitStream
    tree: 'HuffmanNode'
    codes: dict[str, str]
    frequency_table: dict[str, int]

    # TODO :: Impl display method


@dataclass
class HuffmanNode:
    left: Optional['HuffmanNode'] = field(default=None)
    right: Optional['HuffmanNode'] = field(default=None)
    character: str = field(default=NULL_CHAR)
    frequency: int = field(default=0)

    def __lt__(self, other: 'HuffmanNode'):
        return self.frequency < other.frequency

    def is_leaf(self) -> bool:
        return all(n is None for n in (self.left, self.right))

    def is_intermediate(self) -> bool:
        return not self.is_leaf()

    @classmethod
    def create_internal(
        cls,
        left: Optional['HuffmanNode'],
        right: Optional['HuffmanNode'],
    ) -> 'HuffmanNode':
        internal_node = cls(left, right)
        for side in (left, right):
            if side:
                internal_node.frequency += side.frequency
        return internal_node

    @classmethod
    def create_leaf(cls, character: str, frequency: int) -> 'HuffmanNode':
        if not character:
            raise ValueError()

        if frequency == 0:
            raise ValueError()

        return cls(character=character, frequency=frequency)


def build_frequency_table(input_string: str) -> dict[str, int]:
    map_ct = dict()
    for letter in input_string:
        value = map_ct.setdefault(letter, 0)
        map_ct[letter] = value + 1

    # This isn't really needed since we're relying on ``HuffmanNode``
    # having a less than impl
    #sorted_items = sorted(map_ct.items(), key=lambda v: v[1], reverse=True)
    #return dict(sorted_items)
    return map_ct


def get_huffman_codes(node, prefix, output):
    if left := node.left:
        get_huffman_codes(left, prefix + "0", output)
        if right := node.right:
            get_huffman_codes(right, prefix + "1", output)
    else:
        output[node.character] = prefix


def build_huffman_tree(
    input_string: str,
) -> tuple['HuffmanNode', dict[str, int]]:
    """Returns the root node and the frequency table used to build the tree."""
    table = build_frequency_table(input_string)
    nodes = PriorityQueue()

    for character in table:
        leaf = HuffmanNode.create_leaf(
            character=character, frequency=table[character]
        )
        nodes.put(leaf)

    # Build intermediate nodes.
    while nodes.qsize() > 1:
        left = nodes.get()
        right = nodes.get()
        intermediate_node = HuffmanNode.create_internal(left, right)
        nodes.put(intermediate_node)

    return nodes.get(), table


def compress_string(input_string: str, verbose: bool = False) -> CompressionResult:
    """
    Compress ``input_string`` into a binary bit-string (a sequence of ones and zeroes,)
    and return that new string alongside a mapping of binary 'characters' to their
    original value. Note that the string will be in hex, but the underlying data is there!

    Each characters' binary string is formed by traversing a binary tree from the root
    node. A left move yields a 0, a right move a 1.

    For example:
        > compress_string('Sponge Bob')
        > string => 0x5f8873b5
        > map    =>
            {
              "000": "g",
              "001": "n",
              "010": "S",
              "011": "e",
              "100": " ",
              "101": "b",
              "110": "o",
              "1110": "B",
              "1111": "p"
            }
    """
    if not input_string:
        raise ValueError(f'Cannot compress an empty string')

    root, table = build_huffman_tree(input_string)
    codes = dict()
    get_huffman_codes(root, '', codes)

    # On the way out, revert the map, so we  can scan chars left to right,
    # and map them to letters.
    compressed_value = [int(v) for v in ''.join(map(lambda c: codes[c], input_string))]
    bitstream = ConstBitStream(compressed_value)
    return CompressionResult(
        input_string=input_string,
        output_value=bitstream,
        tree=root,
        codes=codes,
        frequency_table=table
    )


def decompress_string(input_stream: ConstBitStream, codes: dict[str, str]) -> str:
    k = ''
    decompressed_string = ''

    for c in input_stream:
        k += '1' if c else '0'
        if k in codes:
            decompressed_string += codes[k]
            k = ''

    return decompressed_string
