
docker build -f Dockerfile -t "duplocloud/anyservice:visiondemo-train-cpu-v1" .
docker push duplocloud/anyservice:visiondemo-train-cpu:v1


docker build -f  Dockerfile.inference -t "duplocloud/anyservice:visiondemo-inference-cpu-v1" .
docker push duplocloud/anyservice:visiondemo-inference-cpu:v1

