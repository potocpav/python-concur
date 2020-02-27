pdoc --html  --force --output-dir docs/master concur
cp -r docs/master/concur/* docs/master
rm -r docs/master/concur
