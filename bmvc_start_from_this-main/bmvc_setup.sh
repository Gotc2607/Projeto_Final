docker build -t bmetimg .
docker run --name bmetaap -p 8080:8080 -v $(pwd):/bmeta bmetimg
