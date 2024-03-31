""""
Verbs

Module containing verb classes necessary to conjugate a German verb. 

Consists of only a single class: Verb.
    This class handles strong, weak, mixed, irregular, preterite-present verbs (so all verbs pretty much)
The Verb class does most of the work in the conjugations.
A Verb is constructed from its infinitive an 'is_weak' indicator, and an 'is_transitive' indicator.

"""

import re
from enum import IntEnum

# enum classes for easier hash table access.

class Person(IntEnum):
    FIRST = 0
    SECOND = 1
    THIRD = 2

class Number(IntEnum):
    SINGULAR = 0
    PLURAL = 1

class Tense(IntEnum): 
	PRESENT = 0
	IMPERFECT = 1
	FUTURE = 2
	
class Aspect(IntEnum):
	SIMPLE = 0
	PERFECT = 1

class Mood(IntEnum):
	INDICATIVE = 0
	IMPERATIVE = 1 # present only
	SUBJUNCTIVE = 2 # future subjunctive 2 is the conditional
	
n_entries = len(Tense) * len(Mood) * len(Aspect) * len(Person) * len(Number)
	
# lambdas
is_none_value = lambda tense, mood, aspect, person, number: ( False ) # TODO

# hash function
table_hash = lambda tense, mood, aspect, person, number: ( 0 ) # TODO


class Verb:
	"""
	Base class to store a verb's conjugation.

	This base class houses the majority of a verb's necessary conjugation(s), and stems.

	Class members:
		_empty : tuple --> empty/default endings
		_present_endings : tuple --> default present tense endings
		_past_endings : tuple ---> default imperfect tense endings
		_subjunctive_endings : tuple --> default subjunctive mood endings

	Attributes:
		infinitive : str --> a verb's infinitive
		stem : str --> a verb's stem (infinitive sans the ending)
		past_stem : str --> a verb's past tense stem
		participle : str --> a verb's (past) participle
	
	Methods:
		conjugate(self, tense_idx : int = len(Tense), person_idx : int = len(Person))
			conjugate a verb
		get_conjugation_at(self, tense_idx : int, person_idx : int) -> str
			get specified conjugation
		clear_table(self)
			clear conjugation table
		get_table(self)
			get conjugation table
	"""
	# static/protected class members --> constant for ALL verbs pretty much unless aspect stuff appears

	# past participle endings: 1st singular, 2nd singular, 3rd singular, 1st plural, 2nd plural, 3rd plural
	_empty = ("", "", "", "", "", "")
	_present_endings = ("e", "st", "t", "en", "t", "en") # also stong past endings 
	_past_endings = ("te, test, te, ten, tet, ten") # weak endings
	_subjunctive_endings = ("e", "est", "e", "en", "et", "en") # basically weak endings sans initial -t

	# tense to ending mappings

	def __init__(self, infinitive : str = "", ending : str = "",
                 is_weak : bool = True, is_transitive : bool = True,
				 present_endings : tuple = ()):
		"""
		Construct a Verb object.

		Parameters:
			infinitive (default "") : str --> infinitive of the verb
			ending (default "") : str --> the verb's ending
			is_weak (default True) : bool --> indicator if a verb is weak (determines endings used)
			is_transitive (default True) : bool --> indicator if a verb is transitive (determines perfect auxiliary)
			present_endings (default empty) : tuple --> passed in tuple to override indicative present tense conjugation
		"""
		# stems (public)
		self.infinitive = infinitive
		self.ending = ending
		self.stem = ""
		self.past_stem = ""
		
        # flags
		self._override_present = len(present_endings) != 0
		self._present_endings = present_endings if self._override_present else self._present_endings
		self._is_transitive = is_transitive
		self._is_weak = is_weak
		
		# if not is_weak: # overrides default weak conjugations in affected tenses + moods
		#     self._is_weak = False

		# conjugation table
		self._conjugation_table = ["" for person in range(n_entries)]

	def _get_conjugation(self,
					    tense : int,
						mood : int,
						aspect : int,
						person : int,
						number : int) -> str:
		"""Return a fully constructed conjugation for given tense, mood, aspect, person, and number."""
		# auxiliary = (self._tense_to_auxiliary[tense])[person]
		# ending = (self._tense_to_ending[tense])[person]
		conjugation = ""
		#space = " " if auxiliary != "" else "" # so no space AFTER
		# if not is_none_value(tense, person):
		# 	conjugation = self._stems[tense] + ending + space + auxiliary
		return conjugation
	
	def conjugate(self,
			      tense : int = len(Tense),
				  mood : int = len(Mood),
				  aspect : int = len(Aspect),
				  person : int = len(Person),
				  number : int = len(Number)):
		"""
		Conjugate a verb according provided tense, mood, aspect, person, and number.

		Parameters:
			tense : int --> any one of the integer constants defined in IntEnum Tense
			mood : int --> any one of the integer constants defined in IntEnum Mood
			aspect : int --> any one of the integer constants defined in IntEnum Aspect
			person : int --> any one of the integer constants defined in IntEnum Person
			number : int --> any one of the integer constants defined in IntEnum Number
		"""
		
        # TODO:
		# make (recursive) function to get list of hashes
		indices = []
		for index in indices:
			self._conjugation_table[index] = self._get_conjugation(tense, mood, aspect, person, number)

	def get_conjugation_at(self,
						   tense: int,
						   mood: int,
						   aspect: int,
						   person: int,
						   number: int) -> str:
		"""Return a specified conjugation."""
		
		valid_cond = (tense >= 0 and tense < len(Tense)) and \
                     (mood >= 0 and mood < len(Mood)) and \
					 (aspect >= 0 and aspect < len(Aspect)) and \
			         (person >= 0 and person < len(Person)) and \
					 (number >= 0 and number < len(Number))
		return self._conjugation_table[table_hash(tense, mood, aspect, person, number)] if valid_cond else ""
	
	def clear_table(self):
		"""Clear the conjugation table."""
		for i in range(len(self._conjugation_table)):
				self._conjugation_table[i] = ""

	def get_table(self) -> list:
		"""Retrieve the conjugation hash table."""
		return self._conjugation_table
	
	def kind(self) -> str:
		"""Return type of class as string"""
		return "Verb"