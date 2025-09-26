""""
Conjugator Utilites

Provides functions to ease setting up the conjugator proper
"""

import re
import verbs as v
from enum import IntEnum
import os


class IrregularIdx(IntEnum):
    CATEGORY = 0
    INFINITIVE = 1
    PAST_STEM = 2
    PARTICIPLE= 3
    CONJUGATION = 4 # present tense only, for Irregular and preterite-present verbs

def get_irregular_verbs() -> list:
	"""
	Retrieve the irregular verb constructions from the file and store them as a list of tuples.
	
	Each line becomes its own tuple, with each element within each tuple being the following:
	0 (IrregularIdx.CATEGORY): The verb's category
        - Numbered categories refer to its classification as a strong verb
		- M is for mixed
		- I is for irregular
        - PP is for preterite-present
	1 (IrregularIdx.INFINITIVE)
	2 (IrregularIdx.PAST_STEM)
	3 (IrregularIdx.PARTICIPLE)
	4 (IrregularIdx.CONJUGATION): present tense conjugation (indicative) for irregular and preterite-present verbs

	Return:
		list[tuple[str, str, str, str, str, str]]
	"""
	# file = open(os.environ["VERB_DATA_DIR"] + "/" + "verbs.txt", "r")
	file = open("data" + "/" + "verbs.txt", "r")
	lines = file.readlines()
	file.close()

	verbs = []
	for line in lines:
		verb = (line.rstrip("\n")).split(",")[:-1] # remove the newline as well
		verb = tuple(verb)
		verbs.append(verb)
	return verbs

def find_verb_matches(word : str, verbs : list) -> list:
	"""
	Return all verb-tuples that end with <word>.
	
		Construct a list of matches by comparing <word> with the infinitive in <verbs> and if they
		end identically. If so, it is added to the list.

		Parameters:
			word: str --> string to compare the irregular verbs to.
			verbs: list[tuple[str, str, str, str, str]] --> list holding the irregular verb information.
		Return:
			list[tuple[str, str, str, str, str]] --> list of irregular verb-tuples that match the word-ending regex pattern.
	"""
	matches = [verb for verb in verbs if re.findall("(" + verb[IrregularIdx.INFINITIVE] + ")" + "$", word) != []]
	return matches[0] if len(matches) > 0 else []


def construct_verb(word : str, match : tuple) -> v.Verb:
	"""Construct a Verb object manually by overwriting stem values from __init__()."""
	remainder = word[:-len(match[IrregularIdx.INFINITIVE])]
	verb = v.Verb()
	verb.past_stem = remainder + match[IrregularIdx.PAST_STEM]
	# TODO: fill with the other values
	return verb

def get_prefixes() -> str:
	"""Retrieve the prefixes from the file as a single regex expression."""
	file = open(os.environ["VERB_DATA_DIR"] + "/" + "prefix.txt", "r")
	lines = file.readlines()
	file.close()

	# append each line (excluding the new line) within an OR capture
	prefixes = "^("
	for line in lines:
		prefixes += "(" + line[:-1] + ")|"
	prefixes =  prefixes[:-1] + ")" # remove last/redundant "|"
	return prefixes


def get_last_prefix(matches : tuple):
	"""Return the last non-empty element in tuple <matches>."""
	prefix_match = ""
	for match in matches:
		if match:
			prefix_match = match # the previous match is overwritten.
	return prefix_match


def get_prefix(word : str, prefixes_expr: str) -> tuple:

	"""
	Extract the prefixes from provided <word>.
	
	Continuously appends consecutive prefixes to string <prefixes> in order to obtain
	a string containing all of the contained prefixes within <word> that
	adhere to the <prefixes> regex pattern. As a result, as <prefixes> expands,
	the remaining length of <word> decreases, eventually reducing it to its
	unprefixed root.

	Parameters:
		word : str --> word to extract the prefixes from.
		prefixes_expr : str -->  regex expression containing all valid verbal prefixes.
	Return:
		tuple[str, str] --> [0]: The resulting string from appending all of the consecutively found prefixes in <word>.
							[1]: The resulting string from removing the found prefixes from <word> within <word> (the root).
	"""
	prefixes = ""
	prefix = ""
	root = ""
	while(1):
		# keep extracting last prefix matched until all have been found.
		word = word[len(prefix):]
		found_prefixes = re.findall(prefixes_expr, word)
		if found_prefixes == []:
			break
		found_prefixes = found_prefixes[0] # list is a singleton
		prefix = get_last_prefix(found_prefixes)
		prefixes += prefix
	root = word
	return (prefixes, root)

def determine_verb_class(word : str, matches : list[tuple[str, str, str, str, str]]) -> v.Verb:
	'''Determines verb class based on presence within irregular matches and found properties'''
	verb = None
	found = False
	parts = {}
	found = len(matches) > 0
	if found:
		# update parts dictionary
		parts = {"present" : matches[IrregularIdx.INFINITIVE],
				 "past" : matches[IrregularIdx.PAST_STEM],
				 "participle" : matches[IrregularIdx.PARTICIPLE],
				 "conjugation" : ()
				 }
		if len(matches) > IrregularIdx.CONJUGATION:
			parts["conjugation"] = matches[IrregularIdx.CONJUGATION]

	
		# strong or mixed?
		if (matches[IrregularIdx.CATEGORY] == "M") or \
		(matches[IrregularIdx.CATEGORY] == "PP"):
			verb = v.Mixed(infinitive = word, use_haben = True, parts = parts)
		else:
			verb = v.Strong(infinitive = word, use_haben = True, parts = parts)
	else:
		# weak
		verb = v.Weak(infinitive = word, use_haben = True, parts = parts)
	return verb