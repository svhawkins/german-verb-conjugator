# test Verb module

import pytest
import verbs as v

def test_test():
    assert True == True



## TODO:
## 1. test that the constructors work correctly for each verb class:
##  - Verb, Weak, Mixed, Strong
##  - stems, ending lists, etc.
##  - prefixes, motion or not etc.
## 2. test that the conjugate() method works for Weak verbs, simple tenses only
##  - test enum ranges as well
##  - test prefixes
## 3. test conjugation for auxiliary verbs, simple tenses only
## 4. test conjugation for Weak verbs, complex tenses
## 5. test conjugation for Mixed verbs, simple and complex (uses override)
##  - preterite-presents too
## 6. test conjugation for Strong verbs, simple and complex
##  - also test out umlauts (happens when 'getting' the conjugation)