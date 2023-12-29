# aimsun-to-dynameq
This repo contains a number of scripts designed to assist in exporting Aimsun network and data into the format required by DYNAMEQ's Aimsun import tool.

Add the export-data scripts to your Aimsun model.  

The scripts are run by executing the master script (export-data.py). You will be prompted to select a scenario to export from.

The scripts will split merged nodes into individual nodes. If centroids are connected to nodes, this may delete them - the script to split nodes is run after centroid and centroid connection data is exported  

Files are exported into a folder called 'DYNAMEQ-Aimsun-Files'. This folder will be created within the model directory if it does not exist.  


The scripts were developed and run for Aimsun Next version 23.

The 'convert-csv-to-gis.py' script is included in order to convert the exported csvs that contain geometry information into a shapefile (that is required for the DYNAMEQ conversion tool). This script is run outside of the Aimsun environment and requires GeoPandas and Shapely packages to run.

## Mobility Lab      
### caleb@mobilitylab.co.nz
