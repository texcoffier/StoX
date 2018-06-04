
SRC = $(shell echo ????-*.py)

run-tests:xxx.py
	./tests

run:xxx.py
	python3 xxx.py

xxx.py: $(SRC) RapydScript
	cat $(SRC) >xxx.py

RapydScript:
	git clone https://github.com/atsepkov/RapydScript.git
	# Works with this commit
	# git checkout f121b356dea6dfc558884af69dd780754d8c5332

clean:
	-rm xxx*

install:run-tests
	cp xxx.js StoX.html $(HOME)/public_html/PARSER
