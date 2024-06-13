#!/bin/sh

sleep 5;
/usr/bin/mc alias set myminio http://minio:9000 minioadmin minioadmin;
/usr/bin/mc mb myminio/storage;
/usr/bin/mc anonymous set public myminio/storage;
/usr/bin/mc admin config set myminio notify_webhook:primary endpoint="http://host.docker.internal:8000/minio-event" queue_limit="10";
/usr/bin/mc admin service restart myminio;
/usr/bin/mc event add myminio/storage arn:minio:sqs::primary:webhook --event put;
exit 0;