energy-blockchain
===
Green Energy Blockchain Project cooperate with NCKU-EE

## Getting Started

### Prerequisites

environment
- python 3.6.8
- docker 19.03.5

encrypt key files (put in `ami/rsa/`)
- plat_rsa_public.pem
- ami_rsa_private.pem
```
# Generate AMI Key
openssl genrsa -out ami_rsa_private.pem 1024
# 使用 RSA 私鑰產生公鑰
openssl rsa -in ami_rsa_private.pem -out ami_rsa_public.pem -outform PEM -pubout
# Generate Platform Key
openssl genrsa -out plat_rsa_private.pem 4096
# 使用 RSA 私鑰產生公鑰
openssl rsa -in plat_rsa_private.pem -out plat_rsa_public.pem -outform PEM -pubout
```

### Running Development

Installing Packages & Running
```
pipenv install
pipenv shell
cd ami/
python app.py
```

### Production

#### Dockerize Restful Server
+ needed files:
    + Dockerfile
    + requirements.txt
        + auto produce by pipenv : `pipenv lock --requirements > requirements.txt`

#### Docker Build Command
```sh
pipenv lock --requirements > ami/requirements.txt
docker build -t uploader:latest ami/ --no-cache
```
or just use
```sh
make
```

### Running Production

1. update the .env file
2. run docker
```sh
# Default environment
docker run --name uploader -d --net=host --restart=always uploader
# Customized environment
docker run --env-file .env --name uploader -d --net=host --restart=always uploader
```
Notice: `--net=host` only applies to Linux systems.

## API - Upload AMI Data
### Data Types

+ Support Bems
    + Carlab_BEMS
    + SGESC_C_BEMS
    + SGESC_D_BEMS
    + ABRI_BEMS

+ Support Data Types
    + bems_homepage_information(總用電)
    ```json
    {
        "id": "string, uuid4",
        "field": "string, 場域",
        "grid": "float, 電網即時功率",
        "pv": "float, 太陽能即時功率",
        "building": "float, 大樓即時用電",
        "ess": "float, 儲能即時功率",
        "ev": "float, 充電樁即時功率",
        "updated_at": "datetime, timestamp without time zone"
    }
    ```
    + bems_ess_display(儲能系統)
    ```json
    {
        "id": "string, uuid4",
        "field": "string, 場域",
        "cluster": "int, ESS編號",
        "power_display": "float, 讀取實功輸出(kW)",
        "updated_at": "datetime, timestamp without time zone"
    }
    ```
    + bems_ev_display(充電樁)
    ```json
    {
        "id": "string, uuid4",
        "field": "string, 場域",
        "cluster": "int, ESS編號",
        "power": "float, 充電功率(kW)",
        "updated_at": "datetime, timestamp without time zone"
    }
    ```
    + bems_pv_display(太陽光電)
    ```json
    {
        "id": "string, uuid4",
        "field": "string, 場域",
        "cluster": "int, ESS編號",
        "pac": "float, 市電功率",
        "updated_at": "datetime, timestamp without time zone"
    }
    ```
    + bems_wt_display(中小型風力機)
    ```json
    {
        "id": "string, uuid4",
        "field": "string, 場域",
        "cluster": "int, ESS編號",
        "wind_grid_power": "float, 風機功率",
        "updated_at": "datetime, timestamp without time zone"
    }
    ```

### Usage

curl

`curl http://localhost:4000/bems/upload -X POST --header 'Content-Type: application/json' --data-raw {json type data}`

Example for Sending AMI data:

```sh
curl http://localhost:4000/bems/upload -X POST \
--header 'Content-Type: application/json' \
--data-raw '{
        "Carlab_BEMS": {
            "bems_homepage_information": {
            "id": "fd180573-34b7-428d-860b-430875dda453",
            "field": "Carlab_BEMS",
            "grid": 10.048,
            "pv": 3.683,
            "building": 2.933,
            "ess": 0.923,
            "ev": 2.784,
            "updated_at": "2020-04-30T22:33:56.270416"
        },
            "bems_ess_display": {
            "id": "216e3701-aa98-4b24-980e-8e56a37341e9",
            "field": "Carlab_BEMS",
            "cluster": 1,
            "power_display": 0.923,
            "updated_at": "2020-04-30T22:33:56.270438"
        },
            "bems_ev_display": {
            "id": "27cd4221-347d-4433-aee0-01c55fdf4704",
            "field": "Carlab_BEMS",
            "cluster": 1,
            "power": 2.784,
            "updated_at": "2020-04-30T22:33:56.270450"
        },
            "bems_pv_display": {
            "id": "99e7121a-f707-4cc9-9c56-b075e41a0a3b",
            "field": "Carlab_BEMS",
            "cluster": 1,
            "pac": 3.683,
            "updated_at": "2020-04-30T22:33:56.270505"
        },
            "bems_wt_display": {
            "id": "c24d2677-05b6-4fab-a441-189358507b6a",
            "field": "Carlab_BEMS",
            "cluster": 1,
            "wind_grid_power": -2.945,
            "updated_at": "2020-04-30T22:33:56.270561"
        }
    }
}'
```

[examples](./ami/example)
+ [sh file](./ami/example/upload.sh)
    run: `./upload.sh`
    This example will upload [upload.json](./ami/example/upload.json)
+ [Python example](./ami/example/upload_example.py)
    run: `python3 upload_example.py`
    This example will generate random data and upload.

### Response

+ Json Type Data
    + message : string : ACCEPT or Error Message
    Example:
    ```json
    {
        "message": "ACCEPT"
    }
    ```

+ Status code
    + `200 OK`
        request accept
        ```json
        {
            "message": "ACCEPT"
        }
        ```

    + `400 Bad Request`
        json data error
        ```json
        {
            "message": "JSON data error"
        }
        ```

    + `403 Forbidden`
        request content not included
        ```json
        {
            "message": [
                {
                    "ev": [
                        "Missing data for required field."
                    ]
                },
                "",
                "",
                ""
            ]
        }
        ```
