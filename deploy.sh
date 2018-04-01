git pull
git add --all
git commit -m "jj"
git push origin master
gcloud compute scp * warthogs:/home/jj/flaskapp --recurse

