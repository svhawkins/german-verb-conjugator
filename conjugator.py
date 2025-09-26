import conjutils
import verbs as v
from conjutils import IrregularIdx

# TODO: actually make this a 'main' function
############## MAIN PROGRAM ####################

irregular_verbs = conjutils.get_irregular_verbs()
#prefixes = conjutils.get_prefixes()

# TODO: determine verb class: Strong, Weak, Mixed

# partial conjugation of auxiliaries

word = "haben"
match = conjutils.find_verb_matches(word, irregular_verbs)
v.Haben = v.Strong(infinitive = word, use_haben = True, parts = {})
v.Haben.conjugate(aspect = (v.Aspect.SIMPLE),
				  tense = (v.Tense.PRESENT, v.Tense.PAST),
				  mood = (v.Mood.INDICATIVE, v.Mood.SUBJUNCTIVE_1, v.Mood.SUBJUNCTIVE_2))

word = "sein"
match = conjutils.find_verb_matches(word, irregular_verbs)
v.Sein = v.Strong(infinitive = word, use_haben = False, parts = {})
v.Sein.conjugate(aspect = v.Aspect.SIMPLE,
				  tense = (v.Tense.PRESENT, v.Tense.PAST),
				  mood = (v.Mood.INDICATIVE, v.Mood.SUBJUNCTIVE_1, v.Mood.SUBJUNCTIVE_2))

word = "werden"
match = conjutils.find_verb_matches(word, irregular_verbs)
v.Werden = v.Strong(infinitive = word, use_haben = False, parts = {})
v.Werden.conjugate(aspect = v.Aspect.SIMPLE,
				  tense = (v.Tense.PRESENT, v.Tense.PAST),
				  mood = (v.Mood.INDICATIVE, v.Mood.SUBJUNCTIVE_1, v.Mood.SUBJUNCTIVE_2))
# TODO: somehow determine verb transitivity/is motion or not
while(1):
	word = input("enter a verb infinitive (or 'q' to quit): ")
	if word == "q":
		break

	matches = conjutils.find_verb_matches(word, irregular_verbs)
	#(not_root, root) = conjutils.get_prefix(word, prefixes)
	verb = conjutils.determine_verb_class(word, matches)
	print(verb.kind())
	if verb:
		verb.conjugate()
		# TODO: display the conjugation
		print(verb.get_table())