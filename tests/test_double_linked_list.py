"""DoubleLinkedList Tests"""

import unittest
from app.double_linked_list import DoubleLinkedList

class TestAdd(unittest.TestCase):
    """Unittest class"""
    def test_push_pop(self):
        """test_push_pop"""
        test_list = DoubleLinkedList()
        with self.subTest():
            test_list.push(1)
            self.assertEqual(str(test_list), "1 ")
        with self.subTest():
            test_list.push(2)
            self.assertEqual(str(test_list), "1 2 ")
        with self.subTest():
            test_list.push(3)
            self.assertEqual(str(test_list), "1 2 3 ")
        with self.subTest():
            poped = test_list.pop()
            self.assertEqual((str(test_list), poped), ("1 2 ", 3))
        with self.subTest():
            poped = test_list.pop()
            self.assertEqual((str(test_list), poped), ("1 ", 2))
        with self.subTest():
            poped = test_list.pop()
            self.assertEqual((str(test_list), poped), ("", 1))
        with self.subTest():
            poped = test_list.pop()
            self.assertEqual((str(test_list), poped), ("", None))

    def test_unshift_shift(self):
        """test_inshift_shift"""
        test_list = DoubleLinkedList()
        with self.subTest():
            test_list.unshift(1)
            self.assertEqual(str(test_list), "1 ")
        with self.subTest():
            test_list.unshift(2)
            self.assertEqual(str(test_list), "2 1 ")
        with self.subTest():
            test_list.unshift(3)
            self.assertEqual(str(test_list), "3 2 1 ")
        with self.subTest():
            shifted = test_list.shift()
            self.assertEqual((str(test_list), shifted), ("2 1 ", 3))
        with self.subTest():
            shifted = test_list.shift()
            self.assertEqual((str(test_list), shifted), ("1 ", 2))
        with self.subTest():
            shifted = test_list.shift()
            self.assertEqual((str(test_list), shifted), ("", 1))
        with self.subTest():
            shifted = test_list.shift()
            self.assertEqual((str(test_list), shifted), ("", None))

    def test_len(self):
        """test_len"""
        test_list = DoubleLinkedList()
        with self.subTest():
            self.assertEqual(test_list.len(), 0)
        with self.subTest():
            test_list.push(1)
            self.assertEqual(test_list.len(), 1)
        with self.subTest():
            test_list.push(2)
            self.assertEqual(test_list.len(), 2)
        with self.subTest():
            test_list.push(3)
            self.assertEqual(test_list.len(), 3)
        with self.subTest():
            test_list.pop()
            self.assertEqual(test_list.len(), 2)
        with self.subTest():
            test_list.pop()
            self.assertEqual(test_list.len(), 1)
        with self.subTest():
            test_list.pop()
            self.assertEqual(test_list.len(), 0)
        with self.subTest():
            test_list.pop()
            self.assertEqual(test_list.len(), 0)

    def test_delete(self):
        """test_delete"""
        with self.subTest():
            test_list = DoubleLinkedList()
            test_list.push(1)
            test_list.push(2)
            test_list.push(3)
            count = test_list.delete(1)
            self.assertEqual((str(test_list), count), ("2 3 ", 1))
        with self.subTest():
            test_list = DoubleLinkedList()
            test_list.push(1)
            test_list.push(1)
            test_list.push(2)
            count = test_list.delete(1)
            self.assertEqual((str(test_list), count), ("2 ", 2))
        with self.subTest():
            test_list = DoubleLinkedList()
            test_list.push(1)
            test_list.push(1)
            test_list.push(1)
            count = test_list.delete(1)
            self.assertEqual((str(test_list), count), ("", 3))
        with self.subTest():
            test_list = DoubleLinkedList()
            count = test_list.delete(1)
            self.assertEqual((str(test_list), count), ("", 0))
        with self.subTest():
            test_list = DoubleLinkedList()
            test_list.push(1)
            test_list.push(1)
            test_list.push(1)
            count = test_list.delete(2)
            self.assertEqual((str(test_list), count), ("1 1 1 ", 0))

    def test_contains(self):
        """test_contains"""
        with self.subTest():
            test_list = DoubleLinkedList()
            test_list.push(1)
            test_list.push(2)
            test_list.push(3)
            count = test_list.contains(1)
            self.assertEqual((str(test_list), count), ("1 2 3 ", 1))
        with self.subTest():
            test_list = DoubleLinkedList()
            test_list.push(1)
            test_list.push(1)
            test_list.push(2)
            count = test_list.contains(1)
            self.assertEqual((str(test_list), count), ("1 1 2 ", 2))
        with self.subTest():
            test_list = DoubleLinkedList()
            test_list.push(1)
            test_list.push(1)
            test_list.push(1)
            count = test_list.contains(1)
            self.assertEqual((str(test_list), count), ("1 1 1 ", 3))
        with self.subTest():
            test_list = DoubleLinkedList()
            count = test_list.contains(1)
            self.assertEqual((str(test_list), count), ("", 0))
        with self.subTest():
            test_list = DoubleLinkedList()
            test_list.push(1)
            test_list.push(1)
            test_list.push(1)
            count = test_list.contains(2)
            self.assertEqual((str(test_list), count), ("1 1 1 ", 0))

    def test_first(self):
        """test_first"""
        test_list = DoubleLinkedList()
        first = test_list.first()
        self.assertEqual(first, None)
        with self.subTest():
            test_list.unshift(1)
            first = test_list.first()
            self.assertEqual(first, 1)
        with self.subTest():
            test_list.unshift(2)
            first = test_list.first()
            self.assertEqual(first, 2)
        with self.subTest():
            test_list.unshift(3)
            first = test_list.first()
            self.assertEqual(first, 3)

    def test_last(self):
        """test_last"""
        test_list = DoubleLinkedList()
        last = test_list.last()
        self.assertEqual(last, None)
        with self.subTest():
            test_list.push(1)
            last = test_list.last()
            self.assertEqual(last, 1)
        with self.subTest():
            test_list.push(2)
            last = test_list.last()
            self.assertEqual(last, 2)
        with self.subTest():
            test_list.push(3)
            last = test_list.last()
            self.assertEqual(last, 3)

if __name__ == '__main__':
    unittest.main()
