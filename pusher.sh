black "." && isort .
echo "# Useful functions">useful.md && rg %t lightningaddon|cut -d'/' -f2| rev |cut -c6- |rev |sed 's/^/- / ; s/def/Function:/g ; s/class/Class :/g' >> useful.md;
pdoc --force --html -o docs lightningaddon
mv docs/lightningaddon/index.html docs/index.md
mv docs/lightningaddon/* docs/
if [[ ! -z $1 ]]; then
        git add . && git commit -m $1 && git push
fi
