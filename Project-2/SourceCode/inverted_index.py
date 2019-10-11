"""
Created on 10/10/19 @ 01:04:10

@author: ajithkumar-natarajan

Syntax to run: python3 inverted_index.py input_corpus.txt output.txt query.txt
"""

import sys


class PostingsAttribute:
	def __init__(self, docID = None, freq = None):
		self.docID = docID
		self.freq = freq


class Postings:

	def __init__(self,docID, freq, next_node=None, head=None):
		self.data = PostingsAttribute(docID, freq)
		self.next_node = next_node
		self.head = head

	def get_docID(self):
		return self.data.docID

	def get_freq(self):
		return self.data.freq

	def get_next(self):
		return self.next_node

	def set_next(self, new_next):
		self.next_node = new_next

	def insert(self, docID, freq):
		new_node = Postings(docID, freq)
		new_node.set_next(self.head)
		self.head = new_node
		return self


input_file_loc = str(sys.argv[1])
output_file_loc = str(sys.argv[2])
queries_file_loc = str(sys.argv[3])
corpus = open(input_file_loc, 'r')
queries = open(queries_file_loc, 'r')
inv_index = dict()

for line in corpus:
	docID_terms = line.split("\t")
	docID = docID_terms[0]
	doc_text = docID_terms[1]
	term_list = []
	for each_term in doc_text.split():
		term_list.append(each_term)
	for each_term in term_list:
		if each_term in inv_index:
			posting_list = inv_index[each_term]
			if term_list.count(each_term) > 0:
				while posting_list.next_node is not None:
					posting_list = posting_list.get_next()
				posting_list_new = Postings(docID, term_list.count(each_term))
				posting_list.set_next(posting_list_new.insert(docID, term_list.count(each_term)))
			term_list = list(filter(lambda a: a != each_term, term_list))
		else:
			posting_list = Postings(docID, term_list.count(each_term))
			inv_index[each_term] = posting_list.insert(docID, term_list.count(each_term))
			term_list = list(filter(lambda a: a != each_term, term_list))


for line in queries:
	for query in line.split():
		output_file = open(output_file_loc, "a+")
		output_file.write("GetPostings\n")
		output_file.write(query+"\n")
		output_file.write("Postings list:")
		posting_list = inv_index[query]
		output_file.write(" %s" % (posting_list.get_docID()))
		while posting_list.next_node is not None:
			posting_list = posting_list.get_next()
			output_file.write(" %s" % (posting_list.get_docID()))
		output_file.write("\n")
	output_file.write("\n")
