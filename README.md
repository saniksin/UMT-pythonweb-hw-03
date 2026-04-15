FullStack веб розробка на Python дз 3.


docker build -t homework3 .

docker run --name homework3 -d -p 3000:3000 -v $(pwd)/storage:/app/storage homework3

docker logs -f homework3