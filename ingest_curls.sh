NODE1_TOKEN=
NODE2_TOKEN=
CANDIG_URL_NODE_1=https://candig1.dev.dhdp.ca
CANDIG_URL_NODE_2=http://10.11.0.12:5080
CANDIG_URL_NODE_3=http://10.11.0.13:5080

NODE1_DATA_PATH=`pwd`/holton-etal-2023/node1_omop.json
NODE2_DATA_PATH=`pwd`/holton-etal-2023/node2_omop.json

NODE1_DATASET1_INFO_PATH=`pwd`/holton-etal-2023/NODE1-P1-dataset_info.json
NODE1_DATASET2_INFO_PATH=`pwd`/holton-etal-2023/NODE1-P2-dataset_info.json

NODE2_DATASET1_INFO_PATH=`pwd`/holton-etal-2023/NODE2-P3-dataset_info.json
NODE2_DATASET2_INFO_PATH=`pwd`/holton-etal-2023/NODE2-P4-dataset_info.json

## register datasets

curl -s --request POST \
 --url $CANDIG_URL_NODE_1'/candig-api/v1/authz/dataset' \
 -H 'accept: application/json' \
 -H 'Content-Type: application/json' \
 -H 'Authorization: Bearer '$NODE1_TOKEN \
 -d '{"dataset_id": "NODE1~P1", "dataset_curators": ["user1@test.ca"], "team_members": []}'

curl -s --request POST \
 --url $CANDIG_URL_NODE_1'/candig-api/v1/authz/dataset' \
 -H 'accept: application/json' \
 -H 'Content-Type: application/json' \
 -H 'Authorization: Bearer '$NODE1_TOKEN \
 -d '{"dataset_id": "NODE1~P2", "dataset_curators": ["user2@test.ca"], "team_members": []}'

 curl -s --request POST \
 --url $CANDIG_URL_NODE_2'/candig-api/v1/authz/dataset' \
 -H 'accept: application/json' \
 -H 'Content-Type: application/json' \
 -H 'Authorization: Bearer '$NODE2_TOKEN \
 -d '{"dataset_id": "NODE2~P3", "dataset_curators": ["user1@test.ca"], "team_members": []}'

curl -s --request POST \
 --url $CANDIG_URL_NODE_2'/candig-api/v1/authz/dataset' \
 -H 'accept: application/json' \
 -H 'Content-Type: application/json' \
 -H 'Authorization: Bearer '$NODE2_TOKEN \
 -d '{"dataset_id": "NODE2~P4", "dataset_curators": ["user2@test.ca"], "team_members": []}'

 ## ingest dataset files

curl -X POST $CANDIG_URL_NODE_1'/candig-api/v1/datasets/upload' \
  -H "Authorization: Bearer $NODE1_TOKEN" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@"$NODE1_DATA_PATH

curl -X POST $CANDIG_URL_NODE_2'/candig-api/v1/datasets/upload' \
  -H "Authorization: Bearer $NODE2_TOKEN" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@"$NODE2_DATA_PATH

## ingest dataset info
curl -X PATCH $CANDIG_URL_NODE_1'/candig-api/v1/datasets/NODE1~P1/info' \
  -H "Authorization: Bearer $NODE1_TOKEN" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d "@"$NODE1_DATASET1_INFO_PATH

curl -X PATCH $CANDIG_URL_NODE_1'/candig-api/v1/datasets/NODE1~P2/info' \
  -H "Authorization: Bearer $NODE1_TOKEN" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d "@"$NODE1_DATASET2_INFO_PATH

curl -X PATCH $CANDIG_URL_NODE_2'/candig-api/v1/datasets/NODE2~P3/info' \
  -H "Authorization: Bearer $NODE2_TOKEN" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d "@"$NODE2_DATASET1_INFO_PATH

curl -X PATCH $CANDIG_URL_NODE_2'/candig-api/v1/datasets/NODE2~P4/info' \
  -H "Authorization: Bearer $NODE2_TOKEN" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d "@"$NODE2_DATASET2_INFO_PATH

curl -X GET $CANDIG_URL_NODE_2'/candig-api/v1/datasets/NODE2~P4/info' \
  -H "Authorization: Bearer $NODE2_TOKEN" \
  -H 'accept: application/json'


