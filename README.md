# pyradigms

pyradigms is a python package for composing and decomposing linguistic paradigms.

## Installation
Use `pip(3) install pyradigms` or get the latest version from gitlab with `pip(3) install git+https://gitlab.com/florianmatter/pyradigms.git`.


## Using pyradigms

Basically, pyradigms is intended to convert between tables like this, where every row represents a linguistic form and every column represents a paradigm:

|    | Verb   | Form   | Tense   | Person   | Number   | Mood   |
|---:|:-------|:-------|:--------|:---------|:---------|:-------|
|  0 | ma     | ngamam | NFUT    | 1        | SG       | RLS    |
|  1 | ma     | nam    | NFUT    | 2        | SG       | RLS    |
|  2 | ma     | mam    | NFUT    | 3        | SG       | RLS    |
|  3 | ma     | thamam | NFUT    | 1+2      | SG       | RLS    |
|  4 | ma     | ngamam | NFUT    | 1        | PL       | RLS    |
|  5 | ma     | namam  | NFUT    | 2        | PL       | RLS    |
|  6 | ma     | pamam  | NFUT    | 3        | PL       | RLS    |
|  7 | ma     | ngama  | NFUT    | 1        | SG       | IRR    |
|  8 | ma     | thama  | NFUT    | 2        | SG       | IRR    |
|  9 | ma     | kama   | NFUT    | 3        | SG       | IRR    |
|  … |…     | …   | …    | …        | …       | …    |

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


## composing paradigms

## decomposing paradigms
 