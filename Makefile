.PHONY: clean upload

default: upload

clean:
	rm -rf dist build *.egg-info

upload: clean
	python3 setup.py bdist_wheel
	# python3 -m twine upload dist/*
