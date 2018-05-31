
SRC = $(shell echo ????-*.py)

run-tests:xxx.py
	./tests

run:xxx.py
	python3 xxx.py

xxx.py: $(SRC)
	cat $(SRC) >xxx.py


