#!/bin/bash

function pause(){
   read -p "Press [Enter] key to continue..."
}

applist=`ls *.redmine`

for page in $applist
do
xclip -sel clip < $page
echo $page
pause
done
