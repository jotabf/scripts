




for 1; do
  idle=$(sinfo -t idle -p cluster -ho "%D");
  if [[ idle > 0 ]]; then
  	slack 
  fi
  sleep 10m;
done

