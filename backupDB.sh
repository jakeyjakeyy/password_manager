IMAGE_NAME="db"
DB_USER="postgres"
DB_NAME="vault"
BACKUP_PATH="./backup"
TIMESTAMP=$(date +"%F_%H-%M-%S")

docker-compose exec $IMAGE_NAME pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_PATH/${DB_NAME}_backup_$TIMESTAMP.sql.gz
