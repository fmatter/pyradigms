# pyradigms

pyradigms is a python package for composing and decomposing linguistic paradigms.

## Installation
Use `pip(3) install pyradigms` or get the latest version from gitlab with `pip(3) install git+https://gitlab.com/florianmatter/pyradigms.git`.


## Using pyradigms

Basically, pyradigms is intended to convert between tables like this, where every row represents a linguistic form and every column represents a parameter:

| Verb   | Form   | Tense   | Person   | Number   | Mood   |
|:-------|:-------|:--------|:---------|:---------|:-------|
| ma     | ngamam | NFUT    | 1        | SG       | RLS    |
| ma     | nam    | NFUT    | 2        | SG       | RLS    |
| ma     | mam    | NFUT    | 3        | SG       | RLS    |
| ma     | thamam | NFUT    | 1+2      | SG       | RLS    |
| ma     | ngamam | NFUT    | 1        | PL       | RLS    |
| ma     | namam  | NFUT    | 2        | PL       | RLS    |
| ma     | pamam  | NFUT    | 3        | PL       | RLS    |
| ma     | ngama  | NFUT    | 1        | SG       | IRR    |
| ma     | thama  | NFUT    | 2        | SG       | IRR    |
| ma     | kama   | NFUT    | 3        | SG       | IRR    |
|…     | …   | …    | …        | …       | …    |

and paradigms, where columns and rows both represent parameters, with forms in the cells:

| *ma*    | PST.IRR   | PST.RLS   | NFUT.IRR   | NFUT.RLS   |
|:------|:----------|:----------|:-----------|:-----------|
| 1SG   | *ngimi*   | *me*      | *ngama*    | *ngamam*   |
| 2SG   | *ni*      | *ne*      | *thama*    | *nam*      |
| 3SG   | *mi*      | *me*      | *kama*     | *mam*      |
| 1+2SG | *thumi*   | *thume*   | *pama*     | *thamam*   |
| 1PAUC | *ngumi*   | *ngume*   | *nguyema*  |            |
| 2PAUC | *numi*    | *nume*    | *nuyema*   |            |
| 3PAUC | *pumi*    | *pume*    | *kuyema*   |            |
| 1PL   | *ngumi*   | *ngume*   | *nguyema*  | *ngamam*   |
| 2PL   | *numi*    | *nume*    | *nuyema*   | *namam*    |
| 3PL   | *pumi*    | *pume*    | *kuyema*   | *pamam*    |

The two basic functionalities are composing paradigms, which creates tables like the latter form tables like the former, and decomposing paradigms, which does the opposite.

## composing paradigms

`pyradigms` takes a list such as the one seen in the first table, which is available under [examples/murrinhpatha_verb_entries.csv](examples/murrinhpatha_verb_entries.csv).

There are three methods for composing paradigms:

`compose_from_csv`

## decomposing paradigms
 