energy-blockchain
===
Green Energy Blockchain Project cooperate with NCKU-EE

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


## Transaction Content Inquiry

### Usage

curl

`curl http://localhost:5000/get_transaction/{TxHash}`

+ Parameters:

    + TxHash : Transaction Hash. Length must be 81 characters.

Example for Sending DR Event

`curl http://localhost:5000/get_transaction/J9RSSOQWFIRYBCUBXIE9JUGKDL9PMFDBVJNVUXSKBALBAVBRQVGPLKHFLLRKGFYHBGDCRPPMUNNCZ9999`

### Response

+ Json Type Data
    + is_confirmed : bool : The Transaction has been confirmed or not.
    + message : json : The Transaction's messages on Tangle.
    Example:
    ```json
    {
        "is_confirmed": false,
        "message": {
            "eventID": "c14164d1a259670a0338",
            "date": "2019-05-03T00:00:24",
            "value": "ODY1Nzg0ODliNjMwMTRjYTgyMTQxZmNkOGVmMDk2OWViY2FiN2Q5ZWVjMWExZGM1YmYzY2E0ZjljMjM1MTkwNw=="
        }
    }
    ```

+ Status code
    + `200 OK`
        query accept

    + `400 Bad Request`
        Tx Hash length error

    + `403 Forbidden`
        request reject by Tangle

## Getting Started

### Prerequisites

- python 3.6.8
- docker 19.03.5

### Running Development

Installing Packages & Running
```
pipenv install
pipenv shell
cd ami/
pipenv run python app.py
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
