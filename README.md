# energy-blockchain
Green Energy Blockchain Project cooperate with NCKU-EE

## API
+ Now support data receive.
    + Hems
        + aggregator_distribution
    + Bems
        + appliances

## Usage

curl

`curl http://localhost:5000/{ems}/{type} -X POST --data @{json_file}`

Example for Sending appliances data

`curl http://localhost:5000/bems/appliances -X POST --data @bems_appliances.json`

## Response
+ `200 OK`
    request accept

+ `400 Bad Request`
    json data error

+ `403 Forbidden`
    request type not included

## Dockerize Restful Server
+ needed files:
    + Dockerfile
    + requirements.txt
        + auto produce by pipenv : `pipenv lock --requirements > requirements.txt`
### Docker Build Command
`docker build -t hello_docker_flask:latest .`

### Re-Tag
`docker tag hello_docker_flask ttw225/hello_docker_flask`

### Docker Push Command
`docker push ttw225/hello_docker_flask`

#### update
`docker push ttw225/hello_docker_flask:tagname`

### Docker Pull Command
`docker pull ttw225/hello_docker_flask`