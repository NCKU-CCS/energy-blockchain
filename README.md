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
