OPENER=gnome-open
IN_FILE=resume.yml

all: out/resume-eml.pdf out/resume-pub.pdf out/resume-print.pdf out/resume.odt out/resume.txt # out/resume.html
open: out/resume-print.pdf
	${OPENER} out/resume-print.pdf
refresh: out/resume-print.pdf
go: open
	nosier -i 'make refresh'

spell spellcheck:
	aspell --lang=en_CA --add-filter=tex --add-filter=url -c ${IN_FILE}

# out/resume.txt {{{

out/resume.txt: build/resume.rst
	rst2html.py build/resume.rst | pandoc -f html -t plain -o out/resume.txt

# }}}
# out/resume.html {{{

out/resume.html out/html4css1.css: build/resume.rst
	rst2html.py --link-stylesheet --stylesheet=html4css1.css,resume.css build/resume.rst build/res.html
	cp -f html4css1.css out/html4css1.css
	awk -f fixcols.awk < build/res.html > out/resume.html
	rm build/res.html

out/resume-print.css out/resume-print.html: build/resume-print.tex build/resume.sty
	cd build && mk4ht htlatex resume-print.tex "xhtml, charset=utf-8" " -cunihtf -utf8"
	mv -f build/resume-print.css build/resume-print.html out/

# }}}
# out/resume.odt {{{

build/resume.rst: resume-tpl.rst ${IN_FILE} resume.py
	./resume.py --tex --all --references ${IN_FILE} resume-tpl.rst build/resume.rst

out/resume.odt: build/resume.rst styles.odt post_process_odt.py
	rst2odt.py --traceback --stylesheet=styles.odt build/resume.rst out/resume.odt
	post_process_odt.py
	rm out/resume.odt.bak

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
	./resume.py --tex --none ${IN_FILE} resume-tpl.tex build/resume-pub.tex

build/resume-print.tex: resume-tpl.tex ${IN_FILE} resume.py
	./resume.py --tex --all --references ${IN_FILE} resume-tpl.tex build/resume-print.tex

build/resume-eml.tex: resume-tpl.tex ${IN_FILE} resume.py
	./resume.py --tex --noreferences ${IN_FILE} resume-tpl.tex build/resume-eml.tex

# }}}
# clean {{{
clean:
	rm -rf build/*

dist-clean clean-all: clean
	rm -rf out/*

# }}}

.PHONY: open spellcheck

#vim: fdm=marker
