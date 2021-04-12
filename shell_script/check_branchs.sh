for a in $(git branch -a | grep remotes | awk '{print $1}' | sed 's/remotes\/origin\///'); do 
  echo -n ${a} -\ ; 
  git clean -d -x -f > /dev/null 2>&1;
  git checkout ${a} > /dev/null 2>&1; 
  du -hs --exclude-dir=.git .;
done
