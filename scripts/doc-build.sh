#/bin/sh

rm -rf ./docs/mdfix ./docs/_build
sphinx-apidoc -o ./docs/mdfix ./mdfix
sphinx-build -M markdown ./docs ./docs/_build
