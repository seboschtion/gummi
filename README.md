# gummi

Do you have a bunch of preamble files for your LaTeX documents and you reuse them all the time? What happens when you want to update these templates? You'll need to modify all the files in all your documents! Very time-consuming work, very boring, but thankfully, _very easy to automate!_

With `gummi` you can do just that! You just create a git repository with your template files in it and you can use them in every LaTeX document you have!

## Table of Contents

1. [Install](#install)
2. [Commands](#commands)
3. [Example](#example): [Create template](#create-template), [Use template](#use-the-template), [Update template](#update-the-template)

## Install

Simply run

```bash
pip3 install gummi
```

## Commands

```
init      Initializes a LaTeX document
check     Checks if any updates to the update are available
detach    Deletes all the template files
update    Updates the templates

You can use -h on any command to get help for this particular command.
```

## Example

A LaTeX document of yours might usually look like this:

```
- .gitignore
- main.tex
- Makefile
- sections/
|      - section1.tex
|      - section2.tex
|      - section2.tex
- templates/
|      - logo/
|      |       logo.pdf
|      - preamle.tex
|      - header.tex
|      - footer.tex
```

Typically only the `main.tex` and `sections` change, the rest should be consistent over all your documents. Here is where `gummi` commes into play!

### Create Templates

First, create an empty folder and open a terminal window in it. Then run

```bash
gummi init --template
```

Basically, not much happended but a _gummi_ folder was created. Now, put all your template files into it as if the gummi folder was your root directory, like so:

```
- gummi/
|      - .gitignore
|      - Makefile
|      - templates/
|      |      - logo/
|      |      |       logo.pdf
|      |      - preamle.tex
|      |      - header.tex
|      |      - footer.tex
```

Push that stuff to the git service you prefer.

### Use the Template

Now, visit your LaTeX document folder and again, open a terminal inside it. The structure of your document looks probably like this:

```
- main.tex
- sections/
|      - section1.tex
|      - section2.tex
|      - section2.tex
```

Time to bring up the magic! Run

```bash
gummi init
```

When asked for the git repository, enter the HTTPS clone URL of the repository and press enter. And this is how your document looks like afterwards:

```
- .gitignore
- .gummi/...
- main.tex
- Makefile
- sections/
|      - section1.tex
|      - section2.tex
|      - section2.tex
- templates/
|      - logo/
|      |       logo.pdf
|      - preamle.tex
|      - header.tex
|      - footer.tex
```

### Update the Template

If your want to update your templates, for example remove the Makefile and add another one, do just that in your template repository and push the changes to the remote git server. Then, simply run

```bash
gummi update
```

in your LaTeX document. Your changes are applied immediately! Any changes made locally to a template file will not be lost, these files do not get updated.

The _.gummi_ folder is important, it is responsible for tracking changes to your templates.

Move the binary to a place where your `$PATH` points to or extend the variable.
