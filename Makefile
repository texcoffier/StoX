
SRC = $(shell echo ????-*.py)

run-tests:TMP/StoX.js
	./tests

run:TMP/xxx.py
	python3 TMP/xxx.py

TMP/xxx.py: $(SRC) RapydScript concatenate.py
	@-[ ! -d TMP ] && ( mkdir TMP ; touch TMP/recompute_required)
	@echo "Concatenate Python files"
	@./concatenate.py $(SRC) >$@
	@if [ -f TMP/recompute_required ] ; then \
	      $(MAKE) TMP/required.py ; \
	     rm TMP/recompute_required ; \
	     ./concatenate.py $(SRC) >$@ ; \
	     fi

RapydScript:
	git clone https://github.com/atsepkov/RapydScript.git
	# Works with this commit
	# git checkout f121b356dea6dfc558884af69dd780754d8c5332

TMP/StoX.js:TMP/xxx.py RapydScript $(addprefix TMP/,$(SRC:.py=.py.html))
	@echo "Generate JavaScript"
	RapydScript/bin/rapydscript --prettify --bare TMP/xxx.py | \
		sed -e 's/x.__class__.__name__/typeof(x)/'  >$@

TMP/required.py:
	@echo "Compute required.py. Wait a long time..."
	@(echo "required = {" ; \
	for F in $(SRC:.py=) ; \
	do (python3 TMP/xxx.py -$$F >/dev/null 2>&1 ; echo "'$$F':$$?,") ; \
	done ; echo '"":0}') | sed -u 's/[.]py//' | tee $@

clean:
	-rm -r TMP

install:run-tests
	cp -r --update TMP StoX.html StoX-empty.html StoX.css highlight.css \
	               $(HOME)/public_html/PARSER

TMP/%.py.html:%.py
	@echo "highlight $*"
	@cd TMP ; \
	highlight --syntax=python \
	          <../$*.py | \
	   sed 's/highlight\.css/..\/highlight.css/' >xxx
	@uconv -f utf-8 -t utf-8 --add-signature <TMP/xxx  >TMP/$*.py.html
