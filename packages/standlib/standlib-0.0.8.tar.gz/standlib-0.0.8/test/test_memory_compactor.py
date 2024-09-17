import unittest
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
UTILS_DIR = os.path.join(ROOT_DIR, 'standlib', 'utils')

sys.path.append(UTILS_DIR)

from standlib.utils.alloc import MemoryAllocator, MemoryBlock
from standlib.utils.memory_compactor import MemoryCompactor

class TestMemoryCompactor(unittest.TestCase):

    def setUp(self) -> None:
        self.allocator = MemoryAllocator()

    def test_compact_with_non_empty_blocks(self):
        block1 = self.allocator.alloc(size=50)
        block1.write(offset=0, data=b"block1 data")
        block2 = self.allocator.alloc(size=50)
        block2.write(offset=0, data=b"block2 data")

        MemoryCompactor.compact(allocator=self.allocator)

        self.assertEqual(len(self.allocator.allocated_blocks), 1)
        compacted_block = self.allocator.allocated_blocks[0]

        self.assertEqual(compacted_block.size, 50)
        compacted_data = compacted_block.read(0, len(b"block1 data" + b"block2 data"))
        self.assertEqual(compacted_data, b"block1 data" + b"block2 data")

    def test_compact_with_empty_blocks(self):
        block1 = self.allocator.alloc(size=50)
        block1.write(offset=0, data=b"block1 data")
        block2 = self.allocator.alloc(size=50)  # Empty block

        MemoryCompactor.compact(allocator=self.allocator)

        self.assertEqual(len(self.allocator.allocated_blocks), 1)
        compacted_block = self.allocator.allocated_blocks[0]

        self.assertEqual(compacted_block.size, 50)
        compacted_data = compacted_block.read(0, len(b"block1 data"))
        self.assertEqual(compacted_data, b"block1 data")

    def test_compact_with_all_empty_blocks(self):
        block1 = self.allocator.alloc(size=10)
        block1.write(offset=0, data=b'\x00' * 10)  # Empty data
        block2 = self.allocator.alloc(size=20)
        block2.write(offset=0, data=b'\x00' * 20)  # Empty data

        MemoryCompactor.compact(allocator=self.allocator)

        self.assertEqual(len(self.allocator.allocated_blocks), 0)

    def test_compact_with_partial_data(self):
        block1 = self.allocator.alloc(size=50)
        block1.write(offset=0, data=b"data1")
        block2 = self.allocator.alloc(size=50)
        block2.write(offset=0, data=b"data2")
        block3 = self.allocator.alloc(size=50)  # Empty block

        MemoryCompactor.compact(allocator=self.allocator)

        self.assertEqual(len(self.allocator.allocated_blocks), 1)
        compacted_block = self.allocator.allocated_blocks[0]

        expected_size = len(b"data1" + b"data2")
        self.assertEqual(compacted_block.size, expected_size)
        compacted_data = compacted_block.read(0, expected_size)
        self.assertEqual(compacted_data, b"data1" + b"data2")

if __name__ == '__main__':
    unittest.main()
