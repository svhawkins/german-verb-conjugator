# tests conjugator utilties (conjutils) module

import pytest
import conjutils as conjutils
import verbs as v
from conjutils import IrregularIdx


def test_class_determination():
    '''Tests class determination using listed irregular verbs (closed class)'''
    irregular_verbs = conjutils.get_irregular_verbs()
    verbs = [verb[IrregularIdx.INFINITIVE] for verb in irregular_verbs[1:]]
    mixed_verbs = ["brennen", "bringen", "denken", "kennen", "nennen", "rennen", "senden", "wenden",
                    "wissen", "können", "dürfen", "sollen", "wollen", "mögen", "müssen",
                    "salzen", "spalten", "mahlen"]
    for verb in verbs:
        matches = conjutils.find_verb_matches(verb, irregular_verbs)
        assert_type = "Mixed" if verb in mixed_verbs else "Strong"
        status = conjutils.determine_verb_class(verb, matches).kind() == assert_type
        if not status:
            print(f"Exepcted {assert_type}, got {conjutils.determine_verb_class(verb, matches).kind()} for {verb}, match: {matches}")
            assert status is True


    # test some weak verbs too
    weak_verbs = ["lacheln", "studieren", "lieben", "leben", "lernen"]
    for verb in weak_verbs:
        matches = conjutils.find_verb_matches(verb, irregular_verbs)
        assert conjutils.determine_verb_class(verb, matches).kind() == "Weak"

    