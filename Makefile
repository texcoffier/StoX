
SRC = $(shell echo ????-*.py)

run-tests:xxx.js
	./tests

run:xxx.py
	python3 xxx.py

xxx.py: $(SRC) RapydScript
	cat $(SRC) >xxx.py

RapydScript:
	git clone https://github.com/atsepkov/RapydScript.git
	# Works with this commit
	# git checkout f121b356dea6dfc558884af69dd780754d8c5332

xxx.js:xxx.py RapydScript
	RapydScript/bin/rapydscript --prettify --bare xxx.py | \
		sed -e 's/x.__class__.__name__/typeof(x)/'  >$@

clean:
	-rm xxx*

install:run-tests
	cp xxx.js StoX.html $(HOME)/public_html/PARSER
