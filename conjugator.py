import conjutils
import verbs as v

# TODO: actually make this a 'main' function
############## MAIN PROGRAM ####################

#irregular_verbs = conjutils.get_irregular_verbs()
#prefixes = conjutils.get_prefixes()

# TODO: determine verb class: Strong, Weak, Mixed

# partial conjugation of auxiliaries
v.Haben = v.Strong(infinitive = "", use_haben = True, parts = {})
v.Haben.conjugate(aspect = (v.Aspect.SIMPLE),
				  tense = (v.Tense.PRESENT, v.Tense.PAST),
				  mood = (v.Mood.INDICATIVE, v.Mood.SUBJUNCTIVE_1, v.Mood.SUBJUNCTIVE_2))

v.Sein = v.Strong(infinitive = "", use_haben = False, parts = {})
v.Sein.conjugate(aspect = v.Aspect.SIMPLE,
				  tense = (v.Tense.PRESENT, v.Tense.PAST),
				  mood = (v.Mood.INDICATIVE, v.Mood.SUBJUNCTIVE_1, v.Mood.SUBJUNCTIVE_2))

v.Werden = v.Strong(infinitive = "", use_haben = False, parts = {})
v.Werden.conjugate(aspect = v.Aspect.SIMPLE,
				  tense = (v.Tense.PRESENT, v.Tense.PAST),
				  mood = (v.Mood.INDICATIVE, v.Mood.SUBJUNCTIVE_1, v.Mood.SUBJUNCTIVE_2))


# TODO: somehow determine verb transitivity/is motion or not
while(1):
	word = input("enter a verb infinitive (or 'q' to quit): ")
	if word == "q":
		break

	#matches = conjutils.find_verb_matches(word, irregular_verbs)
	#(not_root, root) = conjutils.get_prefix(word, prefixes)

	# verb = None
	# if verb:
	# 	verb.conjugate()
		# TODO: display the conjugation