black "." && isort .
pdoc --force --html -o lightningaddon
mv docs/lightningaddon/index.html docs/index.md
mv docs/lightningaddon/* docs/
if [[ ! -z $1 ]]; then
        git add . && git commit -m $1 && git push
fi
