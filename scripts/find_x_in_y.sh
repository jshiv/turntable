# This script searches for instances matching the first argument in all 
# files matching the second argument and reports these. It skips any SVN 
# "magic files" as well as any binary files.

for file in $(find . -type f -iname "*${2}*" -not -path '*.svn*'); 
do 
    grep -s -I -H -n -i "$1" $file; 
done
