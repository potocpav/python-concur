# This doesn't work yet
pdoc --html concur && \
    mv html html_ && \
    git checkout gh-pages && \
    cp -r html_/concur html/ && \
    rm -r html_ && \
    git add html/concur && \
    git commit -am 'Update documentation' && \
    git push
git checkout master
