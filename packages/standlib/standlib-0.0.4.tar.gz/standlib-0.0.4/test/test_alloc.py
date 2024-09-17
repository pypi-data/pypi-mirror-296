import unittest
import gc
from io import StringIO
import sys
import os

SCRIPT_DIR: str = os.path.dirname(p=os.path.abspath(path=__file__))
sys.path.append(os.path.dirname(p=SCRIPT_DIR))

from src.utils.alloc import *

class TestMemoryBlock(unittest.TestCase):

    def setUp(self):
        self.memory_block = MemoryBlock(100)  

    def test_initialization(self):
        
        self.assertEqual(self.memory_block.size, 100)
        self.assertEqual(len(self.memory_block.data), 100)

    def test_invalid_size(self):
        
        with self.assertRaises(ValueError):
            MemoryBlock(-10)

    def test_write_and_read(self):
        
        data_to_write = b"hello"
        self.memory_block.write(10, data_to_write)
        read_data = self.memory_block.read(10, 5)
        self.assertEqual(read_data, data_to_write)

    def test_write_out_of_bounds(self):
        
        with self.assertRaises(ValueError):
            self.memory_block.write(95, b"overflow")  

    def test_read_out_of_bounds(self):
       
        with self.assertRaises(ValueError):
            self.memory_block.read(95, 10)  

    def test_memory_deallocation(self):
        
        temp_out = StringIO()  
        sys.stdout = temp_out
        del self.memory_block
        gc.collect()  

        output = temp_out.getvalue().strip()
        self.assertIn("Releasing 100 bytes of memory", output)
        sys.stdout = sys.__stdout__  


class TestMemoryAllocator(unittest.TestCase):

    def setUp(self):
        self.allocator = MemoryAllocator()

    def test_alloc_memory_block(self):
    
        block = self.allocator.alloc(50)
        self.assertEqual(block.size, 50)
        self.assertIn(block, self.allocator.allocated_blocks)

    def test_free_memory_block(self):
        
        block = self.allocator.alloc(50)
        self.allocator.free(block)
        self.assertNotIn(block, self.allocator.allocated_blocks)

    def test_free_all_memory(self):
        
        self.allocator.alloc(50)
        self.allocator.alloc(100)
        self.allocator.free_all()
        self.assertEqual(len(self.allocator.allocated_blocks), 0)


if __name__ == '__main__':
    unittest.main()
 