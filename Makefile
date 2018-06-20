
SRC = $(shell echo ????-*.py)

run-tests:StoX.js
	./tests

run:xxx.py
	python3 xxx.py

xxx.py: $(SRC) RapydScript concatenate.py $(SRC:.py=.py.html)
	./concatenate.py $(SRC) >xxx.py

RapydScript:
	git clone https://github.com/atsepkov/RapydScript.git
	# Works with this commit
	# git checkout f121b356dea6dfc558884af69dd780754d8c5332

StoX.js:xxx.py RapydScript
	RapydScript/bin/rapydscript --prettify --bare xxx.py | \
		sed -e 's/x.__class__.__name__/typeof(x)/'  >$@

clean:
	-rm xxx* *.py.html

install:run-tests
	cp --update StoX.html StoX.css StoX.js *.py.html highlight.css \
	   $(HOME)/public_html/PARSER

%.py.html:%.py
	highlight $*.py >$*.py.html
