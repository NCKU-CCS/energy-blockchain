energy-blockchain
===
Green Energy Blockchain Project cooperate with NCKU-EE

# API
## Data Receive.
Now Support:

+ Hems
    + aggregator_distribution
    + aggregator_dr_event
+ Bems
    + appliances

### Usage

curl

`curl http://localhost:5000/{ems}/{type} -X POST --data @{json_file}`

+ Parameters:

    + ems : Type of ems. Should be `bems` or `hems`

    + type : Type of upload data.

Example for Sending DR Event:

`curl http://localhost:5000/hems/aggregator_dr_event -X POST --data @dr_event.json`

### Response

+ Json Type Data
    + Tx : string : Transaction Hash.
    Example:
    ```json
    {
        "Tx": "J9RSSOQWFIRYBCUBXIE9JUGKDL9PMFDBVJNVUXSKBALBAVBRQVGPLKHFLLRKGFYHBGDCRPPMUNNCZ9999"
    }
    ```

+ Status code
    + `200 OK`
        request accept

    + `400 Bad Request`
        json data error

    + `403 Forbidden`
        request type not included


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
        "is_confirmed": true,
        "message": "{\"eventID\": \"c14164d1a259670a0338\", \"date\": \"2019-05-03T00:00:24\", \"value\": \"ODY1Nzg0ODliNjMwMTRjYTgyMTQxZmNkOGVmMDk2OWViY2FiN2Q5ZWVjMWExZGM1YmYzY2E0ZjljMjM1MTkwNw==\"}"
    }
    ```

+ Status code
    + `200 OK`
        query accept

    + `400 Bad Request`
        Tx Hash length error

    + `403 Forbidden`
        request reject by Tangle

# Run
Pull from docker hub

`docker pull ttw225/api_docker`

Run in background

`docker run -p 5000:5000 ttw225/api_docker:latest &`

# Dockerize Restful Server
+ needed files:
    + Dockerfile
    + requirements.txt
        + auto produce by pipenv : `pipenv lock --requirements > requirements.txt`
## Docker Build Command
`docker build -t api_docker:latest .`

## Re-Tag
`docker tag api_docker ttw225/api_docker`

## Docker Push Command
`docker push ttw225/api_docker`

### update
`docker push ttw225/api_docker:tagname`

## Docker Pull Command
`docker pull ttw225/api_docker`