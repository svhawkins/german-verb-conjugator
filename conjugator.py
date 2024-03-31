import conjutils

# TODO: actually make this a 'main' function
############## MAIN PROGRAM ####################

irregular_verbs = conjutils.get_irregular_verbs()
prefixes = conjutils.get_prefixes()

# TODO: construct + conjugate auxiliary verbs (sein, haben, werden)

# TODO: somehow determine verb transitivity/is motion or not
while(1):
	word = input("enter a verb infinitive (or 'q' to quit): ")
	if word == "q":
		break

	matches = conjutils.find_verb_matches(word, irregular_verbs)
	(not_root, root) = conjutils.get_prefix(word, prefixes)

	# verb = None
	# if verb:
	# 	verb.conjugate()
		# TODO: display the conjugation