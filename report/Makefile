pg-mk-report.pdf: pg-mk-report.md Makefile
	pandoc pg-mk-report.md -o pg-mk-report.pdf -N --toc --toc-depth=3 --template=template.latex

clean:
	rm pg-mk-report.pdf

.PHONY: clean
