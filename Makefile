OPENER=gnome-open
IN_FILE=resume.yml

all: out/resume-eml.pdf out/resume-pub.pdf out/resume-print.pdf # out/resume.html out/resume.odt
open: out/resume-print.pdf
	${OPENER} out/resume-print.pdf
refresh: out/resume-print.pdf
go: open
	nosier -i 'make refresh'

spell spellcheck:
	aspell --lang=en_CA --add-filter=tex --add-filter=url -c ${IN_FILE}

# out/resume.html {{{

out/resume.html: build/resume-htm.rst
	rst2html.py --link-stylesheet --stylesheet=html4css1.css,resume.css build/resume-htm.rst build/res.html
	awk -f fixcols.awk < build/res.html > out/resume.html
	rm build/res.html

build/resume-htm.rst: resume-tpl.rst ${IN_FILE} resume.py
	./resume.py -t htm ${IN_FILE} resume-tpl.rst build/resume-htm.rst

# }}}
# out/resume.odt {{{

build/resume-odt.rst: resume-tpl.rst ${IN_FILE} resume.py
	./resume.py -t odt ${IN_FILE} resume-tpl.rst build/resume-odt.rst

out/resume.odt: build/resume-odt.rst styles.odt
	rst2odt.py --stylesheet=styles.odt build/resume-odt.rst out/resume.odt

# }}}
# out/resume-*.pdf {{{

out/resume-pub.pdf: build/resume-pub.tex build/resume.sty
	cd build && xelatex -interaction=nonstopmode resume-pub.tex
	mv -f build/resume-pub.pdf out/resume-pub.pdf

out/resume-print.pdf: build/resume-print.tex build/resume.sty
	cd build && xelatex -interaction=nonstopmode resume-print.tex
	mv -f build/resume-print.pdf out/resume-print.pdf

out/resume-eml.pdf: build/resume-eml.tex build/resume.sty
	cd build && xelatex -interaction=nonstopmode resume-eml.tex
	mv -f build/resume-eml.pdf out/resume-eml.pdf


build/resume.sty: resume.sty
	cp resume.sty build/resume.sty

build/resume-pub.tex: resume-tpl.tex ${IN_FILE} resume.py
	./resume.py --none ${IN_FILE} resume-tpl.tex build/resume-pub.tex

build/resume-print.tex: resume-tpl.tex ${IN_FILE} resume.py
	./resume.py --all --references ${IN_FILE} resume-tpl.tex build/resume-print.tex

build/resume-eml.tex: resume-tpl.tex ${IN_FILE} resume.py
	./resume.py --noreferences ${IN_FILE} resume-tpl.tex build/resume-eml.tex

# }}}
# clean {{{
clean:
	rm -rf build/*

dist-clean clean-all: clean
	rm -rf out/*

# }}}

.PHONY: open spellcheck

#vim: fdm=marker
