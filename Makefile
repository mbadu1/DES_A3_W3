install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m unittest test_spx_analysis.py -v

format:	
	black *.py 

lint:
	flake8 *.py

deploy:
	#deploy goes here

refactor: format lint
		
all: install lint test format