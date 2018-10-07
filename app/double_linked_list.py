"""DoubleLinkedList, Methods don't return Item because it's unsecure"""

class DoubleLinkedList:
    """DoubleLinkedList"""
    class Item:
        """Item is segment of DoubleLinkedList"""
        def __init__(self, elem):
            self.elem = elem
            self.next_item = None
            self.prev_item = None

    def __init__(self):
        self.head = self.Item(None)
        self.tail = self.Item(None)
        self.head.next_item = self.tail
        self.tail.prev_item = self.head
        self.size = 0

    def __str__(self):
        self_str = ""
        curr = self.head.next_item
        for _ in range(0, self.size):
            self_str += str(curr.elem) + " "
            curr = curr.next_item
        return self_str

    def __get_item_by_index(self, index):
        if index > self.size:
            return None
        if index < 0:
            index += self.size
        if index < 0:
            return None
        if index <= self.size / 2:
            curr = self.head
            for _ in range(0, index + 1):
                curr = curr.next_item
            return curr
        curr = self.tail
        for _ in range(0, self.size - index):
            if curr is None:
                return None
            curr = curr.prev_item
        return curr

    def __add_item_by_index(self, item, index):
        curr = self.__get_item_by_index(index)
        if curr is None:
            return None
        curr.prev_item.next_item = item
        item.prev_item = curr.prev_item
        item.next_item = curr
        curr.prev_item = item
        self.size += 1
        return None

    def __remove_item_by_index(self, index):
        curr = self.__get_item_by_index(index)
        if curr is None or curr == self.tail:
            return None
        curr.prev_item.next_item = curr.next_item
        curr.next_item.prev_item = curr.prev_item
        self.size -= 1
        return curr

    def push(self, elem):
        """Add not None elem at the end of list"""
        assert elem is not None, "# Elem is None"
        self.__add_item_by_index(self.Item(elem), self.size)

    def pop(self):
        """Pop elem from the end of list and return elem or None if list is empty"""
        ret = self.__remove_item_by_index(self.size - 1)
        if ret is None:
            return None
        return ret.elem

    def unshift(self, elem):
        """Add not None elem at the begining of list"""
        assert elem is not None, "# Elem is None"
        self.__add_item_by_index(self.Item(elem), 0);

    def shift(self):
        """Pop elem from the begining of list and return elem or None if list is empty"""
        ret = self.__remove_item_by_index(0)
        if ret is None:
            return None
        return ret.elem

    def len(self):
        """Returns len of list"""
        return self.size

    def delete(self, elem):
        """Delete all occurrences of not None elem in list (using 'is') and return count of deleted"""
        assert elem is not None, "# Elem is None"
        curr = self.head.next_item;
        count = 0
        while curr != self.tail:
            if curr.elem is elem:
                curr.prev_item.next_item = curr.next_item
                curr.next_item.prev_item = curr.prev_item
                self.size -= 1
                count += 1
            curr = curr.next_item
        return count

    def contains(self, elem):
        """Returns count if elem's occurrence (using 'is')"""
        assert elem is not None, "# Elem is None"
        curr = self.head.next_item;
        count = 0
        while curr != self.tail:
            if curr.elem is elem:
                count += 1
            curr = curr.next_item
        return count

    def first(self):
        """Return begining elem from the list or None if list is empty"""
        ret = self.__get_item_by_index(0)
        if ret is None:
            return None
        return ret.elem

    def last(self):
        """Return ending elem from the list or None if list is empty"""
        ret = self.__get_item_by_index(self.size - 1)
        if ret is None:
            return None
        return ret.elem
