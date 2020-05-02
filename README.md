energy-blockchain
===
Green Energy Blockchain Project cooperate with NCKU-EE

## Getting Started

### Prerequisites

environment
- python 3.6.8
- docker 19.03.5

encrypt key files (put in `/ami/rsa/`)
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

### Running Production

1. update the .env file
2. run docker
```bash
# Default environment
docker run --name uploader -d --net=host --restart=always uploader
# Customized environment
docker run --env-file .env --name uploader -d --net=host --restart=always uploader
```
Notice: --net is only work on Linux system

### Dockerize Restful Server
+ needed files:
    + Dockerfile
    + requirements.txt
        + auto produce by pipenv : `pipenv lock --requirements > requirements.txt`

#### Docker Build Command
```bash
pipenv lock --requirements > ami/requirements.txt
docker build -t uploader:latest ami/ --no-cache
```
or just use
```bash
make
```

## API - Upload AMI Data
### Data Types

+ Support Bems
    + Carlab_BEMS
    + SGESC_C_BEMS
    + SGESC_D_BEMS
    + ABRI_BEMS

+ Support Data Types
    + bems_homepage_information(總用電)
        |property|Type|Possible values|Description|
        | ----- | ----- | ----- | ----- |
        | id | string | `3d3d7ab1-3166-468f-8a70-d78cf844c1cc` | Identity of data |
        | field | string | "NCKU" | 場域 |
        | grid | float | 2.516 | 電網即時功率 |
        | pv | float | 0.000 | 太陽能即時功率 |
        | building | float | 2.466 | 大樓即時用電 |
        | ess | float | -0.050 | 儲能即時功率 |
        | ev | float | 0.000 | 充電樁即時功率 |
        | updated_at | datetime | "2019-09-04T12:00:00" | %Y-%m-%dT%H:%M:%S |
    + bems_ess_display(儲能系統)
        |property|Type|Possible values|Description|
        | ----- | ----- | ----- | ----- |
        | id | string | `2a0d3a64-b813-4c39-8bbd-db4831e1d14b` | Identity of data |
        | field | string | "NCKU" | 場域 |
        | cluster | int | 1 | ESS編號 |
        | power_display | float | -0.035 | 讀取實功輸出(kW)  |
        | updated_at | datetime | "2019-09-04T12:00:00" | %Y-%m-%dT%H:%M:%S |
    + bems_ev_display(充電樁)
        |property|Type|Possible values|Description|
        | ----- | ----- | ----- | ----- |
        | id | string | `e827067a-3c41-4664-9950-c737138a32c5` | Identity of data |
        | field | string | "NCKU" | 場域 |
        | cluster | int | 1 | 充電柱編號 |
        | power | float | 0.000 | 充電功率(kW) |
        | updated_at | datetime | "2019-09-04T12:00:00" | %Y-%m-%dT%H:%M:%S |
    + bems_pv_display(太陽光電)
        |property|Type|Possible values|Description|
        | ----- | ----- | ----- | ----- |
        | id | string | `089c81a1-577b-4c09-90d8-21d3e69c1feb` | Identity of data |
        | field | string | "NCKU" | 場域 |
        | cluster | int | 1 | 太陽能編號 |
        | PAC | float | 0.000 | 市電功率 |
        | updated_at | datetime | "2019-09-04T12:00:00" | %Y-%m-%dT%H:%M:%S |
    + bems_wt_display(中小型風力機)
        |property|Type|Possible values|Description|
        | ----- | ----- | ----- | ----- |
        | id | string | `ce230f85-bddc-477d-8833-a5bf55a20254` | Identity of data |
        | field | string | "NCKU" | 場域 |
        | cluster | int | 1 | 風機編號 |
        | WindGridPower | float | 0.000 | 風機功率 |
        | updated_at | datetime | "2019-09-04T12:00:00" | %Y-%m-%dT%H:%M:%S |

### Usage

curl

`curl http://localhost:4000/bems/upload -X POST --header 'Content-Type: application/json' --data @{json_file}`

Example for Sending AMI data:

`curl http://localhost:4000/bems/upload -X POST --header 'Content-Type: application/json' --data @upload.json`

[examples](./ami/example)
+ [bash file](./ami/example/upload.sh)
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
