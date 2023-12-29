#------------------------------------------------------------
#                                       
# Mobility Lab                            
#                 
# caleb@mobilitylab.co.nz
# 2023
#                    
#------------------------------------------------------------

# this script converts a series of input csv files that contain geometry data to shapefiles.

#------------------------------------------------------------
# DISCLAIMER
#------------------------------------------------------------
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import geopandas as gpd
import pandas as pd
from shapely import wkt

# define the coordinate system the model is in
model_epsg = 'epsg:2193'
# define the file list of csvs
file_lst = ['turnings','sections','bus_stops','centroids','centroids_connections','nodes']

def convert_to_shp(filename):
    input_path = f'DYNAMEQ-Aimsun-Files/{filename}.csv'
    df = pd.read_csv(input_path)
    df['geometry'] = df['geometry'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(df, crs=model_epsg)
    output_path = f'outputs/{filename}.shp'
    gdf.to_file(output_path)

for file in file_lst:
    print(file)
    convert_to_shp(file)

print('Finished creating shapefiles from csvs')