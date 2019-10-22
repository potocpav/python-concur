pdoc --html concur
mv html html_
git checkout gh-pages
cp -ru html_/concur html/
rm -r html_
git commit -am 'Update documentation'
git push
git checkout master
