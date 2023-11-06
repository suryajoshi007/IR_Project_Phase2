import math
from typing import List

class Node:

    def __init__(self, docId):

        self.docId = docId
        self.next = None
        self.skip_pointer = None
        self.tf = 0.0
        self.tf_idf = 0.0

class PostingList:

    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.length = 0
        self.n_skips = 0
        self.idf = 0.0

    def insert_end(self, docId, tf=0.0, tf_idf=0.0):

        node = Node(docId)
        node.tf = tf
        node.tf_idf = tf_idf

        if not self.start_node:
            self.start_node = node
            self.end_node = node
        else:
            self.end_node.next = node
            self.end_node = node
        
        self.length += 1

    def insert_skip_pointers(self):

        print(f"Inserting skip pointers")

        if self.length < 3:
            print("Length less than 3. Not Inserting skip pointers")
            return

        self.n_skips = math.floor(math.sqrt(self.length))

        if self.n_skips ** 2 == self.length:
            self.n_skips -= 1
        
        self.skip_gap = round(math.sqrt(self.length), 0)

        pointer_count = 0

        if self.start_node:

            gap = self.skip_gap
            head = prev = self.start_node

            while head:

                if gap == 0:

                    prev.skip_pointer = head
                    prev = head
                    gap = self.skip_gap
                    pointer_count += 1
                
                head = head.next
                gap -= 1
        
        print(f"Inserted no of skip pointers: {pointer_count}, Expected: {self.n_skips}")

    def calculate_tf_idf(self):

        if self.start_node:
            
            head = self.start_node

            while head:
                head.tf_idf = head.tf * self.idf
                head = head.next

    def get_docId(self, sort=False) -> List:

        """
        get a list of docIds from a posting list
        """
        
        ans = []

        if self.length == 0:
            return ans

        head = self.start_node
        while head:
            ans.append((head.docId, head.tf_idf))
            head = head.next

        if sort:
            ans.sort(key = lambda x: x[1], reverse=True)

        ans = [entry[0] for entry in ans]
        
        return ans
    
    def get_docId_skip(self) -> List:

        """
        get a list of docIds from a posting list with only using skip pointers
        """
        
        ans = []

        if self.length == 0:
            return ans

        head = self.start_node
        print(f"nskip: {self.n_skips}")
        while head:
            ans.append((head.docId, head.tf_idf))
            head = head.skip_pointer

        if len(ans) < 2:
            return []
        
        ans = [entry[0] for entry in ans]
        
        return ans

        

        
        





