"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from linkedstack import LinkedStack
from bstnode import BSTNode
from math import log
import random
import time
from tkinter import *


class LinkedBST(AbstractCollection):
    """
    An link-based binary search tree implementation
    """

    def __init__(self, sourceCollection=None):
        """
        Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present
        """
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """
        Returns a string representation with the tree rotated
        90 degrees counterclockwise
        """

        def recurse(node, level):
            string = ""
            if node is not None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """
        Supports a preorder traversal on a view of self
        """

        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """
        Supports an inorder traversal on a view of self
        """

        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """
        If item matches an item in self, returns the
        matched item, or None otherwise
        """

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """
        Adds item to the tree
        """

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """
        Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self
        """
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        preroot = BSTNode(None)
        preroot.left = self._root
        parent = preroot
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preroot.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self, top=None):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top.is_leaf():
                return 0

            return 1 + max([
                height1(top.left) if top.left else 0,
                height1(top.right) if top.right else 0
            ])

        return height1(top or self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        num_vertex = len([leaf for leaf in self])
        if self.height() < 2 * log(num_vertex + 1, 2) - 1:
            return True
        return False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''

        def recurse(node):
            tree_eles = []
            if node is not None:
                tree_eles.append(node.data)
                if node.left is not None:
                    tree_eles += recurse(node.left)
                if node.right is not None:
                    tree_eles += recurse(node.right)
            tree_eles = sorted(tree_eles)
            return tree_eles

        tree_eles = recurse(self._root)
        subtree = []
        for leaf in tree_eles:
            if leaf >= low and leaf <= high:
                subtree.append(leaf)
        return subtree

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''

        def recurse(node):
            tree_eles = []
            if node is not None:
                tree_eles += [node.data]
                if node.left is not None:
                    tree_eles += recurse(node.left)
                if node.right is not None:
                    tree_eles += recurse(node.right)
            tree_eles = sorted(tree_eles)
            return tree_eles

        def rebalance_1(bal_tree, eles):
            half_length_lst = len(eles) // 2
            bal_tree.add(eles[half_length_lst])
            if len(eles[:half_length_lst]) > 0:
                rebalance_1(bal_tree, eles[:half_length_lst])
            if len(eles[half_length_lst + 1:]) > 0:
                rebalance_1(bal_tree, eles[half_length_lst + 1:])
            return bal_tree

        tree_eles = recurse(self._root)
        rez_tree = LinkedBST()
        self._root = rebalance_1(rez_tree, tree_eles)._root

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """

        def recurse(node):
            tree_eles = []
            if node is not None:
                tree_eles.append(node.data)
                if node.left is not None:
                    tree_eles += recurse(node.left)
                if node.right is not None:
                    tree_eles += recurse(node.right)
            tree_eles = sorted(tree_eles)
            return tree_eles

        tree_eles = recurse(self._root)
        for leaf in tree_eles:
            if leaf > item:
                return leaf
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """

        def recurse(node):
            tree_eles = []
            if node is not None:
                tree_eles.append(node.data)
                if node.left is not None:
                    tree_eles += recurse(node.left)
                if node.right is not None:
                    tree_eles += recurse(node.right)
            tree_eles = sorted(tree_eles)
            return tree_eles

        tree_eles = recurse(self._root)
        res_small = []
        for leaf in tree_eles:

            if leaf < item:
                res_small.append(leaf)
        if res_small:
            return res_small[-1]
        return None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """

        def dictionary_reader(file):
            """
            Returns the list
            of words from given
            dictionary file
            """
            words = []
            with open(file, 'r') as fdata:
                for word in fdata.readlines():
                    words.append(word.strip())
            return words

        def bin_tree_ordered():
            """
            Search words in
            binary tree.
            Alphabetically implemented
            """
            words = random.sample(dictionary_reader(path), 10000)
            alphabet_tree = LinkedBST()
            alphabet_tree.add(words[0])
            top = alphabet_tree._root
            for word in words[1:10000]:
                top.right = BSTNode(word)
                top = top.right
                tree._size += 1
            return alphabet_tree

        def bin_tree_random():
            """
            Search words in
            binary tree.
            Random order implemented
            """
            all_words = dictionary_reader(path)
            words = random.sample(all_words, 10000)
            random_words_tree = LinkedBST()
            for word in words:
                random_words_tree.add(word)
            return random_words_tree

        def bin_balanced_tree():
            """
            Search words in
            balanced binary tree.
            """
            all_words = dictionary_reader(path)
            words = random.sample(all_words, 1000)
            balanced_tree = LinkedBST()
            for word in words:
                balanced_tree.add(word)
            balanced_tree.rebalance()
            return balanced_tree

        root = Tk()
        root.title("dictionary words")

        start_implementation1_list = time.time()
        random.sample(dictionary_reader(path), 10000)
        end_implementation1_list = time.time()
        text_implementation1 = f"Time of searching 10000 random words in alphabetically ordered dictionary\n"\
              f"(searching in an array of words with the help of built-in method list).\n"\
              f"First implementation took {end_implementation1_list-start_implementation1_list} seconds.\n"

        text_implementation1_show = Label(root, text=text_implementation1, font="Candara 14", justify=CENTER, padx=3, pady=3)
        text_implementation1_show.pack()

        start_implementation2_alpha_bin_tree = time.time()
        bin_tree_ordered()
        end_implementation2_alpha_bin_tree = time.time()
        text_implementation2 = f"Time of searching 10000 random words in alphabetically ordered dictionary, which is represented in form of binary tree.\n"\
              f"Binary tree is build based on sequentially adding words from dictionary, which ordered alphabetically, to tree.\n"\
              f"Second implementation took {end_implementation2_alpha_bin_tree-start_implementation2_alpha_bin_tree} seconds.\n"

        text_implementation2_show = Label(root, text=text_implementation2, font="Candara 14", justify=CENTER, padx=3,
                                          pady=3)
        text_implementation2_show.pack()

        start_implementation3_random_bin_tree = time.time()
        bin_tree_random()
        end_implementation3_random_bin_tree = time.time()
        text_implementation3 = f"Time of searching 10000 random words in alphabetically ordered dictionary, which is represented in form of binary tree.\n"\
              f"Binary tree is build based on randomly adding words from dictionary.\n"\
              f"Third implementation took {end_implementation3_random_bin_tree-start_implementation3_random_bin_tree} seconds.\n"

        text_implementation3_show = Label(root, text=text_implementation3, font="Candara 14", justify=CENTER, padx=3,
                                          pady=3)
        text_implementation3_show.pack()

        start_implementation4_balanced_bin_tree = time.time()
        bin_balanced_tree()
        end_implementation4_balanced_bin_tree = time.time()
        text_implementation4 = f"Time of searching 10000 random words in alphabetically ordered dictionary, which is represented in form of binary tree.\n"\
              f"Searching is started after rebalancing the tree.\n"\
              f"Fourth implementation took {end_implementation4_balanced_bin_tree - start_implementation4_balanced_bin_tree} seconds."

        text_implementation4_show = Label(root, text=text_implementation4, font="Candara 14", justify=CENTER, padx=3,
                                          pady=3)
        text_implementation4_show.pack()

        print(text_implementation1)
        print(text_implementation2)
        print(text_implementation3)
        print(text_implementation4)
        root.mainloop()

if __name__ == "__main__":
    tree = LinkedBST()

    tree.demo_bst('words.txt')

