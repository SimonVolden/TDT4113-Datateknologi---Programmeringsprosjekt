"""Contains Stack and Queue classes"""

class Container:
    """Container superclass"""
    def __init__(self):
        self.items = []

    def size(self):
        """Return number of elements in items"""
        return len(self.items)

    def is_empty(self):
        """Check if self.items is empty"""
        return len(self.items) == 0

    def push(self, item):
        """Adds item to self.items"""
        # Add item to end of self.items
        self.items.append(item)

    def pop(self):
        """Pop off the correct element in self.items and return it
        This method differs between the subclasses, hence its not
        implemented in the superclass"""

        raise NotImplementedError

    def peek(self):
        """Return the top element without removing it
        This method differs between subclasses, hence is not
        implemented in the superclass"""

        raise NotImplementedError

class Queue(Container):
    """Queue datastructure"""

    def peek(self):
        """Checks element at the start of the queue"""
        if not self.is_empty():
            return self.items[0]
        return None

    def pop(self):
        """Removes the first element of the queue"""
        if not self.is_empty():
            return self.items.pop(0)
        return None

class Stack(Container):
    """Stack datastructure"""

    def peek(self):
        """Checks the last element of the stack"""
        if not self.is_empty():
            return self.items[-1]
        return None

    def pop(self):
        """Removes the last element of the stack"""
        if not self.is_empty():
            return self.items.pop()
        return None

if __name__ == "__main__":
    s = Stack()
    s.push(1)
    print(s.pop())
