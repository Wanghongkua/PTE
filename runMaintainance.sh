#!/bin/sh
# sed -i -e 's/^        /     /g' WFD.md
./printVocabulary.py 0 WFD.md
function lazygit(){
    git add .
    git commit -am "Today's Progress"
    git push
}
lazygit
