#!/bin/sh
# ./printVocabulary.py 0 WFD.md
function lazygit(){
    git add .
    git commit -am "Today's Progress"
    git push
}
lazygit
