# LaTeX Docs Manager (ldm)

Easily manage your many LaTeX documents with ldm! Does each of these documents use your same preamble? Put that preamble and other needed files into a separate git repository and let ldm do the rest for you. Heres what you can do:

- `ldm init` of course, initiates your document by asking you for the git url of your LaTeX templates.
- `ldm update` is the most important command. It updates your LaTeX document folder as defined in your template repository.
- `ldm check` checks whether the templates have changed.

Some more things you can do:

- `ldm init-template` helps you creating a template.
- `ldm reset` resets your document by removing the template and disconnecting ldm from it.

## Build
1. Create a virtual environment: `python3 -m venv ldm`
2. Clone the repository into a temporary folder: `git clone git@github.com:seboschtion/latex-docs-manager.git temp`
3. Run `mv temp/* ldm && mv temp/.* ldm && rmdir temp`
4. `cd` into `ldm`
5. `source bin/activate`
6. Run `pip install -r requirements.txt`
7. Run `make`
8. The binary can be found under `dist/ldm`. Move it where you want ;-)

