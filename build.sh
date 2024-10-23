if [ "$1" == "p" ] || [ "$1" == "prod" ]; then
  cp frontend/Dockerfile-Prod frontend/Dockerfile
  cp backend/Dockerfile-Prod backend/Dockerfile
  cp frontend/.env-Prod frontend/.env
elif [ "$1" == "d" ] || [ "$1" == "dev" ]; then
  cp frontend/Dockerfile-Dev frontend/Dockerfile
  cp backend/Dockerfile-Dev backend/Dockerfile
  cp frontend/.env-Dev frontend/.env
else
  echo "Usage: ./build.sh [prod|dev]"
  exit 1
fi