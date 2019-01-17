.PHONY: clean build

build:
	pyinstaller --workpath=build --clean --onefile --distpath=dist --name ldm main.py

clean:
	rm -rf dist build

