pdoc --html --force --config 'lunr_search={"fuzziness": 1}' --output-dir docs/master concur
cp -r docs/master/concur/* docs/master
rm -r docs/master/concur
