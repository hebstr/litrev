# BibTeX Format Reference

Reference for generating BibTeX entries in the review markdown and in the `.bib` file.

## Entry Types

### `@article` (journal articles)

```bibtex
@article{Smith_2023,
  author  = {Smith, John D. and Johnson, Mary L. and Williams, Karen R.},
  title   = {GLP-1 receptor agonists and cardiovascular outcomes in type 2 diabetes},
  journal = {The Lancet Diabetes \& Endocrinology},
  year    = {2023},
  volume  = {11},
  number  = {5},
  pages   = {319--332},
  doi     = {10.xxxx/example-article-doi},
  pmid    = {00000000}
}
```

Required fields: `author`, `title`, `journal`, `year`
Recommended fields: `volume`, `number`, `pages`, `doi`, `pmid`

### `@book`

```bibtex
@book{Kumar_2021,
  author    = {Kumar, Vinay and Abbas, Abul K. and Aster, Jon C.},
  title     = {Robbins and Cotran Pathologic Basis of Disease},
  edition   = {10},
  publisher = {Elsevier},
  address   = {Philadelphia},
  year      = {2021},
  isbn      = {978-0000000000}
}
```

Required fields: `author`, `title`, `publisher`, `year`
Recommended fields: `edition`, `address`, `isbn`

### `@incollection` (book chapters)

```bibtex
@incollection{Ridker_2022,
  author    = {Ridker, Paul M.},
  title     = {Inflammation and atherothrombosis},
  booktitle = {Braunwald's Heart Disease},
  editor    = {Libby, Peter and Bonow, Robert O.},
  edition   = {12},
  publisher = {Elsevier},
  address   = {Philadelphia},
  year      = {2022},
  pages     = {1045--1062}
}
```

### `@article` (preprints)

```bibtex
@article{Zhang_2024,
  author  = {Zhang, Yi and Chen, Lei and Wang, Hui},
  title   = {Novel therapeutic targets in Alzheimer's disease},
  journal = {medRxiv},
  year    = {2024},
  doi     = {10.xxxx/example-preprint-doi},
  note    = {Preprint}
}
```

### `@inproceedings` (conference papers)

```bibtex
@inproceedings{Lee_2023,
  author    = {Lee, Soo-Jin and Park, Min-Ho},
  title     = {Deep learning for drug-drug interaction prediction},
  booktitle = {Proceedings of the AMIA Annual Symposium},
  year      = {2023},
  pages     = {412--419}
}
```

### `@techreport` (technical reports, guidelines)

```bibtex
@techreport{WHO_2023,
  author      = {{World Health Organization}},
  title       = {Use of GLP-1 receptor agonists: policy brief},
  institution = {World Health Organization},
  year        = {2023},
  number      = {WHO/NMH/NHD/23.1},
  address     = {Geneva},
  url         = {https://www.who.int/publications/i/item/example}
}
```

Required fields: `author`, `title`, `institution`, `year`
Recommended fields: `number`, `address`, `url`

### `@misc` (websites, datasets, software, other)

```bibtex
@misc{ClinicalTrials_2024,
  author       = {{U.S. National Library of Medicine}},
  title        = {ClinicalTrials.gov},
  year         = {2024},
  url          = {https://clinicaltrials.gov},
  note         = {Accessed: 2024-06-15}
}
```

Required fields: `title`, `year`
Recommended fields: `author`, `url`, `note` (access date for online resources)

## Key Format

`FirstAuthorLastName_Year` — e.g. `Smith_2023`

In case of collision, suffix with `a`, `b`, `c`: `Smith_2023a`, `Smith_2023b`

## Field Conventions

- **author**: `Last, First and Last, First and Last, First` (use `and` as separator, never `&`)
- **pages**: `319--332` (double dash for ranges)
- **doi**: bare identifier without `https://doi.org/` prefix
- **journal**: full name preferred (abbreviation handled by CSL at render time)
- **special characters**: escape with `\` — `\&`, `\%`, `\"`, `\{`, `\}`

## Journal Name Abbreviations

Full names are preferred in BibTeX entries. The CSL style handles abbreviation at render time. For reference:

| Full Name | Abbreviation |
|-----------|-------------|
| New England Journal of Medicine | N Engl J Med |
| The Lancet | Lancet |
| JAMA | JAMA |
| BMJ | BMJ |
| Annals of Internal Medicine | Ann Intern Med |
| Circulation | Circulation |
| Diabetes Care | Diabetes Care |
| Nature Medicine | Nat Med |
| Cochrane Database of Systematic Reviews | Cochrane Database Syst Rev |

## DOI Best Practices

1. Always verify DOIs with `verify_citations.py`
2. Store as bare identifier in BibTeX: `doi = {10.xxxx/yyyy}` (not as URL)
3. No trailing punctuation after DOI
4. Cross-check resolution against article metadata
