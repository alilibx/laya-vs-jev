# Technical report (draft)

`main.tex` is the System One Bench technical report, for arXiv. Every number in it comes from the results files
through `make_tables.py`, so rebuild after each round:

```bash
python3 paper/make_tables.py          # writes paper/tables.tex and paper/numbers.tex
cd paper && pdflatex main && bibtex main && pdflatex main && pdflatex main
```

`docs/system-one-bench-report.docx` is a Word copy of the same draft for review. It isn't generated from these files,
so bring it in line by hand when the paper changes.

Before submitting:

- Resolve every orange `\draftnote`, then delete the `\draftnote` definition in `main.tex`.
- Confirm the author line and affiliation.
- arXiv asks first-time submitters in most CS categories for an endorsement from an existing author in that category
  (cs.CL or cs.LG would fit). Ask one before submitting.
- Upload `main.tex`, `refs.bib`, `tables.tex` and `numbers.tex` (or the generated `main.bbl` in place of `refs.bib`).
