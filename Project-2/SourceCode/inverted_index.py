"""
Created on 10/10/19 @ 01:04:10

@author: ajithkumar-natarajan

Syntax to run: python3 inverted_index.py input_corpus.txt output.txt query.txt
"""

import sys
import copy

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


# def DAATAnd(postings):
	# number_of_query_terms = len(postings)
	# # print("new call", postings)
	# length = list()
	# for i in range(number_of_query_terms):
	# 	pointer = [0] * number_of_query_terms
	# 	length.append(len(postings[i]))
	# 	# print(length)
	#
	# # for i in range(number_of_query_terms):
	# # 	go = True
	# # 	if not (pointer[i]<length[i]):
	# # 		go = False
	# print(postings)
	# daat_and_output = list()
	# # while True:
	# comparisons = 0
	# for i in range(number_of_query_terms-1):
	# 	if int(postings[i][pointer[i]]) == int(postings[i+1][pointer[i + 1]]):
	# 		# print(i, postings[i][pointer[i]])
	# 		# print(i+1, postings[i+1][pointer[i+1]])
	# 		match = True
	# 		comparisons += 1
	# 		i += 1
	# 		if (i == number_of_query_terms-1):
	# 			daat_and_output.append(postings[pointer[i]])
	# 		if pointer[i] < length[i]:
	# 			pointer[i] = pointer[i]+1
	# 			# print('5', postings[i][pointer[i]])
	# 		else:
	# 			break
	# 	else:
	# 		if int(postings[i][pointer[i]]) < int(postings[i+1][pointer[i + 1]]):
	# 			print('1', postings[i][pointer[i]])
	# 			print('2', postings[i+1][pointer[i+1]])
	# 			while int(postings[i][pointer[i]]) < int(postings[i][pointer[i + 1]]):
	# 				if pointer[i] < length[i]:
	# 					pointer[i] = pointer[i]+1
	# 					comparisons += 1
	# 				else:
	# 					break
	# 		elif int(postings[i][pointer[i]]) > int(postings[i+1][pointer[i + 1]]):
	# 			print('3', postings[i][pointer[i]])
	# 			print('4', postings[i+1][pointer[i+1]])
	# 			while int(postings[i][pointer[i]]) > int(postings[i][pointer[i + 1]]):
	# 				if pointer[i+1] < length[i+1]:
	# 					pointer[i+1] = pointer[i]+1
	# 					comparisons += 1
	# 				else:
	# 					break
	# 	print(number_of_query_terms-2)
	# 	print(i)
	# 	if i == number_of_query_terms-2:
	# 		print("hi")
	# 		i = 0
	# print(daat_and_output)
	# print(comparisons)


def DAATOr(postings):
	daat_or_output = []
	flag = 0
	comparisons = 0
	while flag != 1:
		if len(postings) == 0:
			flag = 1
			break
		j=0
		while j < len(postings):
			if not postings[j]:
				del postings[j]
				j = 0
			else:
				j = j+1

		if flag != 1:
			if len(postings) == 0:
				flag = 1
				break
			min_val, min_index = find_min(postings)

			for i in range(len(postings)):
				if min_val != postings[i][0] and i != min_index:
					comparisons += 1
				elif  i != min_index:
					comparisons += 1

			daat_or_output.append(min_val)
			for to_del in range(len(postings)):
				if postings[to_del][0] == min_val:
					del postings[to_del][0]

	return daat_or_output, comparisons


def DAATAnd(postings):
	daat_and_output = []
	flag = 0
	comparisons = 0
	while flag != 1:
		for i in postings:
			if not i:
				flag = 1
				break

		if flag != 1:
			min_val, min_index = find_min(postings)
			match_count = 0
			for i in range(len(postings)):
				if min_val != postings[i][0] and i != min_index:
					comparisons = comparisons+1
				elif i != min_index:
					comparisons = comparisons+1

				if min_val == postings[i][0]:
					match_count = match_count + 1
			if match_count == len(postings):
				daat_and_output.append(min_val)

			for to_del in range(len(postings)):
				if postings[to_del][0] == min_val:
					del postings[to_del][0]

	return daat_and_output, comparisons


def find_min(input_list):
	m = input_list[0][0]
	index = 0
	for i in range(len(input_list)):
		if m > input_list[i][0]:
			m = input_list[i][0]
			index = i
	return m, index


# def calculate_TF(dictOfDict, TotTermsDoc, token, idf, unionList):
# 	tf = 0
# 	rank_dict = dict()
# 	for key, value in dictOfDict[token].items():
# 		if key in unionList:
# 			tf = tf + float(value)/TotTermsDoc[key]
# 			tf_idf = (float(value)/TotTermsDoc[key]) * idf
# 			rank_dict[key] = tf_idf
# 	return rank_dict, tf
#
#
# def calculate_IDF(dictOfDict, tot_numb_Of_doc, findWord):
# 	no_Of_docs_with_T = len(dictOfDict[findWord])
# 	IDF = tot_numb_Of_doc/no_Of_docs_with_T
# 	return IDF


# def calculate_TF_IDF(query_line, daat_output):
# 	tf_idf = 0
# 	for query in query_line:



input_file_loc = str(sys.argv[1])
output_file_loc = str(sys.argv[2])
queries_file_loc = str(sys.argv[3])
corpus = open(input_file_loc, 'r')
queries = open(queries_file_loc, 'r')
total_queries_lines_count = len(open(queries_file_loc, 'r').readlines())
inv_index = dict()
line_count = 1
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
	line_count += 1
	postings_for_daat_and = list()
	postings_for_daat_or = list()
	for query in line.split():
		output_file = open(output_file_loc, "a+")
		output_file.write("GetPostings\n")
		output_file.write(query+"\n")
		output_file.write("Postings list:")
		posting_list = inv_index[query]
		output_file.write(" %s" % (posting_list.get_docID()))
		postings = list()
		postings.append(posting_list.get_docID())
		while posting_list.next_node is not None:
			posting_list = posting_list.get_next()
			output_file.write(" %s" % (posting_list.get_docID()))
			postings.append(posting_list.get_docID())
		output_file.write("\n")
		postings_for_daat_and.append(postings)
	postings_for_daat_or = copy.deepcopy(postings_for_daat_and)
	daat_and_output, comparisons_and = DAATAnd(postings_for_daat_and)
	daat_or_output, comparisons_or = DAATOr(postings_for_daat_or)

	output_file.write("DaatAnd\n")
	output_file.write(line)
	# print(line_count, total_queries_lines_count)
	if line_count-1 == total_queries_lines_count:
		output_file.write("\n")
	output_file.write("Results:")
	if len(daat_and_output) == 0:
		output_file.write(" empty")
	else:
		for doc in daat_and_output:
			output_file.write(" %s" % (doc))
	output_file.write("\n")
	output_file.write("Number of documents in results: %d\n" % len(daat_and_output))
	output_file.write("Number of comparisons: %d\n" % comparisons_and)

	output_file.write("TF-IDF\n")
	if len(daat_and_output) == 0:
		output_file.write("Results: empty\n")

	output_file.write("DaatOr\n")
	output_file.write(line)
	# print(line_count, total_queries_lines_count)
	if line_count-1 == total_queries_lines_count:
		output_file.write("\n")
	output_file.write("Results:")
	if len(daat_or_output) == 0:
		output_file.write(" empty")
	else:
		for doc in daat_or_output:
			output_file.write(" %s" % (doc))
	output_file.write("\n")
	output_file.write("Number of documents in results: %d\n" % len(daat_or_output))
	output_file.write("Number of comparisons: %d\n" % comparisons_or)

	output_file.write("TF-IDF\n")
	if len(daat_or_output) == 0:
		output_file.write("Results: empty\n")
	tf_idf = [0]*len(line.split())
	# print(tf_idf)
	# for i in range(len(line.split())):
	# 	tf_idf[i] += calculate_TF_IDF(line, daat_and_output)


	if not line_count-1 == total_queries_lines_count:
			output_file.write("\n")
