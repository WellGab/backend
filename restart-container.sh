image_name="wellgab"

docker build -t "${image_name}" .
container_ids=$(docker ps -aq --filter name="${image_name}")
if [ -n "$container_ids" ]; then
    echo "Stopping and removing containers based on image: ${image_name} 🛑"
    docker stop $container_ids >/dev/null 2>&1
    docker rm $container_ids >/dev/null 2>&1
  else
    echo "No running containers found based on image: ${image_name} ❌"
  fi
docker run -p 8000:8000 "${image_name}"