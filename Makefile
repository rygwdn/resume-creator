OPENER=gnome-open

all: out/resume-eml.pdf out/resume-pub.pdf out/resume-print.pdf # out/resume.html out/resume.odt
open: out/resume-print.pdf
	${OPENER} out/resume-print.pdf
refresh: out/resume-print.pdf
go: open
	nosier -i 'make refresh'

# out/resume.html {{{

out/resume.html: build/resume-htm.rst
	rst2html.py --link-stylesheet --stylesheet=html4css1.css,resume.css build/resume-htm.rst build/res.html
	awk -f fixcols.awk < build/res.html > out/resume.html
	rm build/res.html

build/resume-htm.rst: resume-tpl.rst resume.yml resume.py
	./resume.py -t htm resume.yml resume-tpl.rst build/resume-htm.rst

# }}}
# out/resume.odt {{{

build/resume-odt.rst: resume-tpl.rst resume.yml resume.py
	./resume.py -t odt resume.yml resume-tpl.rst build/resume-odt.rst

out/resume.odt: build/resume-odt.rst styles.odt
	rst2odt.py --stylesheet=styles.odt build/resume-odt.rst out/resume.odt

# }}}
# out/resume-*.pdf {{{

out/resume-pub.pdf: build/resume-pub.tex build/resume.sty
	cd build && xelatex -interaction=batchmode resume-pub.tex
	mv -f build/resume-pub.pdf out/resume-pub.pdf

out/resume-print.pdf: build/resume-print.tex build/resume.sty
	cd build && xelatex -interaction=batchmode resume-print.tex
	mv -f build/resume-print.pdf out/resume-print.pdf

out/resume-eml.pdf: build/resume-eml.tex build/resume.sty
	cd build && xelatex -interaction=batchmode resume-eml.tex
	mv -f build/resume-eml.pdf out/resume-eml.pdf


build/resume.sty: resume.sty
	cp resume.sty build/resume.sty

build/resume-pub.tex: resume-tpl.tex resume.yml resume.py
	./resume.py --none resume.yml resume-tpl.tex build/resume-pub.tex

build/resume-print.tex: resume-tpl.tex resume.yml resume.py
	./resume.py --all --references resume.yml resume-tpl.tex build/resume-print.tex

build/resume-eml.tex: resume-tpl.tex resume.yml resume.py
	./resume.py resume.yml resume-tpl.tex build/resume-eml.tex

# }}}
# clean {{{
clean:
	rm -rf build/*

dist-clean clean-all: clean
	rm -rf out/*

# }}}

.PHONY: open

#vim: fdm=marker
