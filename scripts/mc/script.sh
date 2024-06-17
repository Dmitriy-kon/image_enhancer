#!/bin/sh

# sleep 5
# /usr/bin/mc alias set myminio http://minio:9000 minioadmin minioadmin

# # if [ ! -d "/data/storage" ]; then
# if /usr/bin/mc ls myminio > /dev/null 2>&1; then
#     echo "bucket storage exists"
# else
#     echo "bucket storage try to create"
#     /usr/bin/mc mb myminio/storage
# fi

# output=$(/usr/bin/mc anonymous get myminio/storage)

# if echo "$output" | grep -q "public"; then
#     echo "Bucket already public."
# else
#     /usr/bin/mc anonymous set public myminio/storage
# fi

# events=$(/usr/bin/mc event list myminio/storage)
# for event in $events; do
#     echo "${event}"
# done



# /usr/bin/mc admin config set myminio notify_webhook:primary endpoint="http://host.docker.internal:8000/minio-event" queue_limit="10";
# /usr/bin/mc admin service restart myminio;
# /usr/bin/mc event add myminio/storage arn:minio:sqs::primary:webhook --event put;
# exit 0;

sleep 5;
/usr/bin/mc alias set myminio http://minio:9000 minioadmin minioadmin;
/usr/bin/mc mb myminio/storage;
/usr/bin/mc anonymous set public myminio/storage;
/usr/bin/mc admin config set myminio notify_webhook:primary endpoint="http://host.docker.internal:8000/minio-event" queue_limit="10";
/usr/bin/mc admin service restart myminio;
/usr/bin/mc event add myminio/storage arn:minio:sqs::primary:webhook --event put;
exit 0;