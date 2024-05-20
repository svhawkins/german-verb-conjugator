""""
Verbs

Module containing verb classes necessary to conjugate a German verb. 

Consists of the base class Verb and the following subclasses:

1. Strong --> for Strong and Irregular verbs (stem changes in present and past)
2. Weak --> for verbs that take 'regular' endings (no stem changes)
3. Mixed --> Mixed and preterite-present verbs (stem changes and 'regular' endings)

The Verb class does most of the work in the conjugations.
A Verb is constructed from the following:
    - Its infinitive
	- Haben/Sein perfect aspect auxiliary indicator
	- (Optional) Prefix and whether it is separable
	- (Optional) Parts to override default values from Verbs dataframe:
            - infinitive : TODO: make as present stem instead?
            - past stem
            - past participle
            - present endings (for irregular and preterite presents)
"""

import re
from enum import IntEnum
from typing import Union

# Auxiliary verbs, have partial conjugations: simple present + past indicative or subjunctive only
# These are preconjugated before conjugating anything (so always available to non-auxiliary Verb __init__)
Haben = None
Werden = None
Sein = None

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
	PAST = 1
	FUTURE = 2
	
class Aspect(IntEnum):
	SIMPLE = 0
	PERFECT = 1

class Mood(IntEnum):
	INDICATIVE = 0
	IMPERATIVE = 1 # present only
	SUBJUNCTIVE_1 = 2 # future has 2 subjunctives, present stem subjunctive
	SUBJUNCTIVE_2 = 3 # future has 2 subjunctives, past stem subjunctive
                      # past stem subjunctive for future is the conditional
	

# imperative is present indicative simple only, 2nd person sg/pl or 1st person pl
# subjunctive_1 is future and present only
# subjunctive_2 is future and past only
def is_none_value(tense : int, mood : int, aspect : int, person : int, number : int) -> bool:
	valid_imperative = (tense == Tense.PRESENT) and \
                       (mood == Mood.IMPERATIVE) and \
					   (aspect == Aspect.SIMPLE) and \
					   ((person == Person.SECOND) or (person == Person.FIRST and number == Number.PLURAL))
	valid_subjunctive = ((mood == Mood.SUBJUNCTIVE_1) and (tense == Tense.PRESENT)) or \
                        ((mood == Mood.SUBJUNCTIVE_2) and (tense == Tense.PAST)) or \
						(tense == Tense.FUTURE)
	return (not valid_imperative) or (not valid_subjunctive)

# hash function
# offsets
n_entries = len(Tense) * len(Mood) * len(Aspect) * len(Person) * len(Number) # 3 * 4 * 2 * 3 * 2 = 144
MOOD_OFFSET = n_entries / len(Mood) # 144 / 4 = 36
TENSE_OFFSET = MOOD_OFFSET / len(Tense) # 36 / 3 = 12
ASPECT_OFFSET = TENSE_OFFSET / len(Aspect) # 12 / 2 = 6
PERSON_OFFSET = ASPECT_OFFSET / len(Person) # 6 / 3 = 2
NUMBER_OFFSET = PERSON_OFFSET / len(Number) # 2 / 2 = 1

def table_hash(mood : int, tense : int, aspect : int, person : int, number : int) -> int: 
	index = (MOOD_OFFSET * mood) + \
	(TENSE_OFFSET * tense) + \
	(ASPECT_OFFSET * aspect) + \
	(PERSON_OFFSET * person) + \
	(NUMBER_OFFSET * number)
	return int(index)


class Verb:
	"""
	Base class to store a verb's conjugation.

	This base class houses the majority of a verb's necessary conjugation(s), and stems.

	Class members:
		_empty : tuple --> empty/default endings
		_present_endings : tuple --> default present tense endings
		_past_endings : tuple ---> default past tense endings
		_subjunctive1_endings : tuple --> default subjunctive 1 mood endings
		_subjunctive2_endings : tuple --> default subjunctive 2 mood endings

	Attributes:
		infinitive : str --> a verb's infinitive
		stem : str --> a verb's stem (infinitive sans the ending)
		past_stem : str --> a verb's past tense stem
		participle : str --> a verb's (past) participle
		imperative_stem : str --> a verb's stem for imperative mood
		subjunctive1_stem : str --> a verb's stem for present-stem-based subjunctive (Konjuktiv I)
		subjunctive2_stem : str --> a verb's stem for past-stem-based subjunctive (Konjuktiv II)
	
	Methods:
		conjugate(self, tense : int = len(Tense),
                        mood: int = len(Mood),
						aspect : int = len(Aspect),
		                person: int = len(Person),
						number : int = len(Number))
			conjugate a verb
		get_conjugation_at(self, tense : int, mood : int, aspect : int, person : int, number : int) -> str
			get specified conjugation with specified qualities (index)
		clear_table(self)
			clear conjugation table
		get_table(self)
			get conjugation table
	"""
	# static/protected class members --> constant for ALL verbs

	_empty = ["", "", "", "", "", ""]
	_present_endings = ["e", "st", "t", "en", "t", "en"]
	_past_endings = _empty # dependent on class
	_subjunctive1_endings = ["e", "est", "e", "en", "et", "en"]
	_subjunctive2_endings = _empty # dependent on class
	
    # set up future auxiliary
	_future_aux = Werden if Werden is not None else None

	def __init__(self, infinitive : str = "",
                 use_haben : bool = True,
			     prefix : tuple = ("", False),
				 parts = {}):
		"""
		Construct a Verb object.

		Parameters:
			infinitive (default "") : str --> infinitive of the verb
			use_haben (default True) : bool --> indicator if a verb uses haben or sein in perfect aspect
			prefix (default ("", False)) : tuple --> passed in tuple to indicate prefix portion and whether it is separable
			parts (default {}) : dict str : str --> passed in parts to override default stems
		"""
		# stems
		self.infinitive = infinitive
		self.stem = "" # derived in derived classes
		self.past_stem = "" # derived in derived classes
		self.participle = "" # derived in derived classes
		self.imperative_stem = ""  # later derived
		self.subjunctive1_stem = "" # later derived
		self.subjunctive2_stem = "" # later derived
		
        # prefix
		self._prefix = prefix[0]
		self._is_separable = prefix[1]

        # flags
		self._use_haben = use_haben
		
        # perfect auxiliary
		self._perfect_aux = None
		if Haben is not None and self._use_haben == True:
			self._perfect_aux = Haben
		elif Sein is not None and self._use_haben == False:
			self._perfect_aux = Sein

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
	
	def _get_range(self, enum_val : Union[Tense, tuple], enum_length : int, enum_type : IntEnum) -> tuple:
		enum_range = []
		if type(enum_val) is tuple:
			enum_range = enum_val # leave as is
		elif enum_val < enum_length:
			enum_range.append(enum_type(enum_val)) # append singleton
		else:
			enum_range = [enum_type(val) for val in range(len(enum_type))] # just do 'em all
		return tuple(enum_range)

	
	def conjugate(self,
			      tense : Union[Tense, tuple]  = len(Tense),
				  mood : Union[Mood, tuple] = len(Mood),
				  aspect : Union[Aspect, tuple] = len(Aspect),
				  person : Union[Person, tuple] = len(Person),
				  number : Union[Number, tuple] = len(Number)):
		"""
		Conjugate a verb according provided tense(s), mood(s), aspect(s), person(s), and number(s).

		Parameters:
			tense : Tense or tuple(Tense) --> any of the integer constants defined in IntEnum Tense
			mood : Mood or tuple(Mood) --> any of the integer constants defined in IntEnum Mood
			aspect : Aspect or tuple(Aspect) --> any of the integer constants defined in IntEnum Aspect
			person : Person or tuple(Person) --> any of the integer constants defined in IntEnum Person
			number : Number or tuple(Number) --> any of the integer constants defined in IntEnum Number
		
			By default, all parameters are set to having the length of their enumeration as the default unless explicitly
			defined.
		"""

		# get table ranges
		mood_range = self._get_range(mood, len(Tense), Tense)
		aspect_range = self._get_range(aspect, len(Aspect), Aspect)
		tense_range = self._get_range(tense, len(Tense), Tense)
		person_range = self._get_range(person, len(Person), Person)
		number_range = self._get_range(number, len(Number), Number)

		for mood_idx in mood_range:
			for tense_idx in aspect_range:
				for aspect_idx in tense_range:
					for person_idx in person_range:
						for number_idx in number_range:
							index = table_hash(mood_idx, tense_idx, aspect_idx, person_idx, number_idx)
							self._conjugation_table[index] = self._get_conjugation(tense_idx,
															  					   mood_idx,
																				   aspect_idx,
																				   person_idx,
																				   number_idx)

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
	
class Strong(Verb):
	"""Class for strong verbs"""

	# verb class specific endings:
	# conjugations use same endings as present-tense moods, though there is ablaut in stems.
	_past_endings = ("", "st", "", "en", "et", "en")
	_subjunctive2_endings = ("e", "est", "e", "en", "et", "en")

	def __init__(self, infinitive : str = "",
                 use_haben : bool = True,
			     prefix : tuple = ("", False),
				 parts = {}):
		super().__init__(infinitive, use_haben, prefix, parts)
		
        # get stems. they are non-derivable.
		if len(parts) > 0:
			self.stem = parts["present"][:-2] # remove the [ei]n
			self.past_stem = parts["past"]
			self.participle = parts["participle"]
			if len(parts["conjugation"] > 0):
				self._present_endings = parts["conjugation"]
			
		self.subjunctive1_stem = self.stem
		self.subjunctive2_stem = self.past_stem
		self.imperative_stem = self.stem
		
        # TODO: account for umlauts

	def kind(self) -> str:
		"""Return type of class as string"""
		return "Strong"
	
class Weak(Verb):
	"""Class for weak verbs"""

	# verb class specific endings:
	_past_endings = ("te, test", "te", "ten", "tet", "ten")
	_subjunctive2_endings = _past_endings

	def __init__(self, infinitive : str = "",
                 use_haben : bool = True,
			     prefix : tuple = ("", False),
				 parts = {}):
		super().__init__(infinitive, use_haben, prefix, parts)
		
        # derive stems
		self.stem = self.infinitive[:-2] # TODO: not always last 2
		self.past_stem = self.stem # TODO: = -(e)ten verbs and few others have extra rules
		self.participle = "ge" + self.past_stem + "t" # TODO: not all have participles like this
		self.imperative_stem = self.stem
		self.subjunctive1_stem = self.stem
		self.subjunctive2_stem = self.past_stem
		
        # TODO: account for umlauts

	def kind(self) -> str:
		"""Return type of class as string"""
		return "Weak"
	
class Mixed(Verb):
	"""Class for mixed and preterite present verbs"""

	# verb class specific endings:
	_past_endings = ("te, test", "te", "ten", "tet", "ten")
	_subjunctive2_endings = _past_endings

	def __init__(self, infinitive : str = "",
                 use_haben : bool = True,
			     prefix : tuple = ("", False),
				 parts = {}):
		super().__init__(infinitive, use_haben, prefix, parts)
		
        # get stems. they are non-derivable.
		if len(parts) > 0:
			self.stem = parts["present"][:-2] # remove the [ei]n
			self.past_stem = parts["past"]
			self.participle = parts["participle"]
			if len(parts["conjugation"] > 0):
				self._present_endings = parts["conjugation"]
			
		self.subjunctive1_stem = self.stem
		self.subjunctive2_stem = self.past_stem
		self.imperative_stem = self.stem
		
        # TODO: account for umlauts

	def kind(self) -> str:
		"""Return type of class as string"""
		return "Mixed"