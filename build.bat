cd /D "%~dp0"
docker buildx bake postgres --pull --push
