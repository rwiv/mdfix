#/bin/sh

sphinx-apidoc -o ./docs/mdfix ./mdfix
sphinx-build -M markdown ./docs ./docs/_build
