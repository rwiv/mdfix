@echo off

cd ..

if exist "docs\mdfix" rd /s /q "docs\mdfix"
if exist "docs\_build" rd /s /q "docs\_build"

uv run sphinx-apidoc -o ./docs/mdfix ./mdfix
uv run sphinx-build -M markdown ./docs ./docs/_build
pause
