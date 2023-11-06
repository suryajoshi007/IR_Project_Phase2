from collections import OrderedDict
from preprocessor import Preprocessor
from postinglist import PostingList
from indexer import Indexer
import json

class QueryProcessor:

    def __init__(self, input_corpus):
        self.tk = Preprocessor()
        self.indexer = Indexer(index_file=input_corpus)
        self.indexer.build_index()
        self.index = self.indexer.get_index()

    def get__daatAnd_struct(self):
        daatAnd_struct = {
            "num_comparisons": 0,
            "num_docs": 0,
            "results": []
        }

        return daatAnd_struct.copy()
    
    def merge(self, list1, list2):
        """
        returns intersection of 2 posting lists
        """

        first = list1.start_node
        second = list2.start_node

        res = PostingList()

        comparison_count = 0

        while first and second:

            comparison_count += 1
            
            if first.docId == second.docId:
                
                # TODO: what to do of the tf idf cal?
                # both first and second have same docid but for different terms
                # how to calculate tf-idf for resultant node?

                res.insert_end(first.docId, tf_idf=(first.tf_idf + second.tf_idf))

                first = first.next
                second = second.next

            elif first.docId < second.docId:
                first = first.next

            else:
                second = second.next

        return res, comparison_count
    
    def mergeSkip(self, list1, list2):
        """
        returns intersection of 2 posting lists
        """

        print("Invoking mergeSkip")

        first = list1.start_node
        second = list2.start_node

        res = PostingList()

        comparison_count = 0

        while first and second:

            print(first.docId, second.docId)

            comparison_count += 1
            
            if first.docId == second.docId:
                
                # insert_end to insert tf_idf score
                res.insert_end(first.docId, tf_idf=(first.tf_idf + second.tf_idf))

                first = first.next
                second = second.next

            elif first.docId < second.docId:
                if first.skip_pointer and first.skip_pointer.docId <= second.docId:
                    # while first and first.skip_pointer and first.skip_pointer.docId <= second.docId:
                        # comparison_count += 1
                    first = first.skip_pointer
                else:
                    first = first.next
            else:
                if second.skip_pointer and second.skip_pointer.docId <= first.docId:
                    # while second and second.skip_pointer and second.skip_pointer.docId <= first.docId:
                        # comparison_count += 1
                    second = second.skip_pointer
                else:
                    second = second.next

        return res, comparison_count
    

    def daatAnd(self, query, skip=False, sort=False):

        _, tokens = self.tk.tokenizer(f"0\t{query}")

        res_struct = self.get__daatAnd_struct()

        plist = []

        for token in tokens:

            if not token in self.index:
                return { query: res_struct }
            
            plist.append(self.index[token])

        # if query is only made of 1 token, return result
        if len(tokens) < 2:
            res_struct["num_docs"] = self.index[tokens[0]]
            res_struct["results"] = self.index[tokens[0]].get_sorted_docId()


        plist.sort(key = lambda x: x.length)


        res, comparison_count = None, 0

        for postinglist in plist:

            if not res:
                res = postinglist
                continue
            
            if not skip:
                res, count = self.merge(res, postinglist)
            else:
                res, count = self.mergeSkip(res, postinglist)

            comparison_count += count

        final_res = {}
        final_res[query] = res_struct
        final_res[query]["num_comparisons"] = comparison_count
        final_res[query]["num_docs"] = res.length
        final_res[query]["results"] = res.get_docId(sort=sort)

        return final_res
    
    def get_final_struct(self, queries):

        queries.sort()

        res_struct = OrderedDict()

        res_struct["Response"] = {}

        # get posting lists
        postingslist = self.indexer.get_postinglists(queries=queries)
        res_struct["Response"]["postingsList"] = postingslist["postingsList"]
        # print(json.dumps(postingslist, indent=4))


        res_struct["Response"]["daatAnd"] = {}

        # daatAnd op
        for query in queries:
            res = self.daatAnd(query)
            res_struct["Response"]["daatAnd"][query] = res[query].copy()
            # print(json.dumps(res, indent = 4))

        

        # get postinglists with skip pointers
        postingslistskip = self.indexer.get_postinglistsskip(queries=queries)
        res_struct["Response"]["postingsListSkip"] = postingslistskip["postingsListSkip"]
        # print(json.dumps(postingslistskip, indent=4))


        res_struct["Response"]["daatAndSkip"] = {}
        # daatAndSkip op
        for query in queries:
            res = self.daatAnd(query, skip=True)
            res_struct["Response"]["daatAndSkip"][query] = res[query].copy()
            # print(json.dumps(res, indent = 4))


        res_struct["Response"]["daatAndTfIdf"] = {}

        # daatAndTfIdf op
        for query in queries:
            res = self.daatAnd(query, sort=True)
            res_struct["Response"]["daatAndTfIdf"][query] = res[query].copy()
            # print(json.dumps(res, indent = 4))

        res_struct["Response"]["daatAndSkipTfIdf"] = {}

        # daatAndSkipTfIdf op
        for query in queries:
            res = self.daatAnd(query, skip=True, sort=True)
            res_struct["Response"]["daatAndSkipTfIdf"][query] = res[query].copy()
            # print(json.dumps(res, indent = 4))

        return res_struct





if __name__ == "__main__":

    queryprocessor = QueryProcessor(input_corpus="./data/input_corpus.txt")

    queries = []

    with open("./data/queries.txt", 'r') as file:
        for query in file:
            queries.append(query.strip())

    ans = queryprocessor.get_final_struct(queries=queries)

    print(json.dumps(ans, indent=4))

    with open("./data/new_output.json", 'w') as json_file:
        json.dump(ans, json_file, indent=4)

    

