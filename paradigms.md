* uses for paradigms?
	* what is encoded in paradigms?
		* INFLECTION
			* wide range of values
			* can have many different values
			* forms in cell can be morphologically complex (no multiple exponence needed)
			* typically nouns and verbs with different forms
			* LEXEME as a central concept
			* paradigms with pure inflection ([example](https://cariban.clld.org/construction/apa_main)) basically have empty placeholders for stems
		* PRONOUNS
			* person (which is not an inflectional value here...)
			* gender also not inflectional value (as it is neither in nouns)
			* also inflectional values (typically nominal: number, case)
		* note that non-inflectional parameters *can* be inflectional in other POS

* what formats are there?
	* pyradigms: doesn't care about kinds of values, inflectional values are encoded identically to even the forms themselves
	* CLDF: ?
	* [unimorph](https://unimorph.github.io/schema/): 
		* no header
		* three columns (lexeme, form, feature bundle) (potentially empty rows)
		* no morphological segmentation, purely word-based approach
		* more computational, machine-learning oriented purpose
		* JSG left academia in 2017 and now works at facebook, some activity on the github repos from various (?) people
		* feature bundle: 23 dimensions, >212 features (see b)
		* aktionsart, animacy, aspect, case, comparison, definiteness, deixis, evidentiality, finiteness, gender, information structure, interrogativity, mood, number, part of speech, person, polarity, politeness, switch-reference, tense, valency, and voice
||||
| -------------- | ------------------- | --------------------------- |
| aʼáád          | aʼáád               | N;PSS0                      |
| aʼáád          | biʼáád              | N;PSS3                      |
| aʼáád          | danihiʼáád          | PSS1P                       |
| aʼáád          | danihiʼáád          | PSS2P                       |
| aʼáád          | haʼáád              | N;PSS4                      |
| aʼáád          | niʼáád              | N;PSS2S                     |
| aʼáád          | nihiʼáád            | N;PSS1D                     |
| aʼáád          | nihiʼáád            | N;PSS2D                     |
| aʼáád          | shiʼáád             | N;PSS1S                     |
| aʼáád          | yiʼáád              | N;PSS4;ARGAC3S              |
| aadaaní        | aadaaní             | N;PSS0                      |
| aadaaní        | baadaaní            | N;PSS3                      |
| aadaaní        | danihaadaaní        | PSS1P                       |
| aadaaní        | danihaadaaní        | PSS2P                       |
| aadaaní        | haadaaní            | N;PSS4                      |

* reference catalogs provide a standard inventory
	* [unimorph](https://unimorph.github.io/): [OWL-encoded ontology](https://github.com/acoli-repo/olia/blob/master/owl/experimental/unimorph/zips/unimorph-2017-08-16-2157.owl) (not by project itself, most [up to date](https://unimorph.github.io/doc/unimorph-schema.pdf) scheme is PDF)
	