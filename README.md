# pyradigms

pyradigms is a python package for composing and decomposing linguistic paradigms.

## Installation
Use `pip(3) install pyradigms` or get the latest version from gitlab with `pip(3) install git+https://gitlab.com/florianmatter/pyradigms.git`.


## Using pyradigms

Basically, pyradigms is intended to convert between tables like this:

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

and this:

|       | PST.RLS   | PST.IRR   | NFUT.IRR   | NFUT.RLS   |
|:------|:----------|:----------|:-----------|:-----------|
| 1SG   | *me*      | *ngimi*   | *ngama*    | *ngamam*   |
| 2SG   | *ne*      | *ni*      | *thama*    | *nam*      |
| 3SG   | *me*      | *mi*      | *kama*     | *mam*      |
| 1+2SG | *thume*   | *thumi*   | *pama*     | *thamam*   |
| 1PAUC | *ngume*   | *ngumi*   | *nguyema*  |            |
| 2PAUC | *nume*    | *numi*    | *nuyema*   |            |
| 3PAUC | *pume*    | *pumi*    | *kuyema*   |            |
| 1PL   | *ngume*   | *ngumi*   | *nguyema*  | *ngamam*   |
| 2PL   | *nume*    | *numi*    | *nuyema*   | *namam*    |
| 3PL   | *pume*    | *pumi*    | *kuyema*   | *pamam*    |

## composing paradigms

## decomposing paradigms
 