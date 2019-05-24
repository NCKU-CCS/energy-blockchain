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

Example for Sending aggregator_distribution data
`curl http://localhost:5000/hems/aggregator_distribution -X POST --data @aggregator_distribution.json`
