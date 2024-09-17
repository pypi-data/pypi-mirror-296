import unittest
import os
import sys

SCRIPT_DIR: str = os.path.dirname(p=os.path.abspath(path=__file__))
sys.path.append(os.path.dirname(p=SCRIPT_DIR))
from src.utils.alloc import MemoryAllocator, MemoryBlock
from src.utils.memory_compactor import MemoryCompactor


class TestMemoryCompactor(unittest.TestCase):

    def setUp(self) -> None:
        self.allocator = MemoryAllocator()

    def test_compact_with_non_empty_blocks(self):

        block1: MemoryBlock = self.allocator.alloc(size=50)
        block1.write(offset=0, data=b"block1 data")
        block2: MemoryBlock = self.allocator.alloc(size=50)
        block2.write(offset=0, data=b"block2 data")

        
        MemoryCompactor.compact(allocator=self.allocator)

        
        self.assertEqual(first=len(self.allocator.allocated_blocks), second=1)
        compacted_block = self.allocator.allocated_blocks[0]
        
        
        self.assertEqual(first=compacted_block.size, second=100)  

    
        compacted_data = compacted_block.read(0, len(b"block1 datablock2 data"))
        self.assertEqual(first=compacted_data, second=b"block1 datablock2 data")

    def test_compact_with_empty_blocks(self):
        block1: MemoryBlock = self.allocator.alloc(size=50)
        block1.write(offset=0, data=b"block1 data")
        block2: MemoryBlock = self.allocator.alloc(size=50)  

        
        MemoryCompactor.compact(allocator=self.allocator)

        self.assertEqual(len(self.allocator.allocated_blocks), 1)
        compacted_block = self.allocator.allocated_blocks[0]

        self.assertEqual(compacted_block.size, 50)

    
        compacted_data = compacted_block.read(0, len(b"block1 data"))
        self.assertEqual(first=compacted_data, second=b"block1 data")

    def test_compact_with_all_empty_blocks(self):

        self.allocator.alloc(size=50)
        self.allocator.alloc(size=50)

        
        MemoryCompactor.compact(allocator=self.allocator)

        
        self.assertEqual(first=len(self.allocator.allocated_blocks), second=0)

    def test_compact_with_partial_data(self):

        block1: MemoryBlock = self.allocator.alloc(size=50)
        block1.write(offset=0, data=b"data1")
        block2: MemoryBlock = self.allocator.alloc(size=50)
        block2.write(offset=0, data=b"data2")
        block3: MemoryBlock = self.allocator.alloc(size=50)  


        MemoryCompactor.compact(allocator=self.allocator)


        self.assertEqual(len(self.allocator.allocated_blocks), 1)
        compacted_block = self.allocator.allocated_blocks[0]

        expected_size = len(b"data1data2")  
        self.assertEqual(compacted_block.size, 100)  


        compacted_data = compacted_block.read(0, expected_size)
        self.assertEqual(compacted_data, b"data1data2")


if __name__ == '__main__':
    unittest.main()
