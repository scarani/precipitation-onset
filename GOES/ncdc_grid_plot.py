import os
import cartopy.crs as ccrs
from netCDF4 import Dataset as netcdf_dataset
import numpy as np
from timeit import default_timer as timer
import pyart
from tint import Cell_tracks
from tint.grid_utils import get_grid_size as ggs
import gc

start = timer()

def get_grid():
   
    _time = {'calendar': 'gregorian','data': np.array([ 0.934]),
            'long_name': 'Time of grid', 'standard_name': 'time',
            'units': str('seconds since ' + nc.time_coverage_end)}
    
    _fields = {'reflectivity': {'_FillValue': -9999.0, 'data': np.ma.masked_array(c, mask= False),
                       'long_name': 'reflectivity',
                       'standard_name': 'equivalent_reflectivity_factor',
                       'units': 'dBZ', 'valid_max': c.max(), 'valid_min': c.min()}}
    
    _metadata = {'Conventions': '', 'comment': '',
                'history': '', 'institution': '', 'instrument_name': '',
                'original_container': 'NEXRAD Level II', 'references': '',
                'source': '', 'title': '', 'vcp_pattern': '', 'version': ''}
    
    _origin_latitude = {'data': np.array([0]),
                       'long_name': 'Latitude at grid origin',
                       'standard_name': 'latitude',
                       'units': 'degrees_north', 'valid_max': 90.0,
                       'valid_min': -90.0}
    
    _origin_longitude = {'data': np.array([-75]), 
                        'long_name': 'Longitude at grid origin', 
                        'standard_name': 'longitude', 'units': 'degrees_east', 
                        'valid_max': 180.0, 'valid_min': -180.0}
    
    _origin_altitude = {'data': np.ma.masked_array(np.array([0]), mask= False), 
                       'long_name': 'Altitude at grid origin', 
                       'standard_name': 'altitude', 'units': 'm'}
    
    _x = {'axis': 'X', 'data': x, 
          'long_name': 'X distance on the projection plane from the origin', 
          'standard_name': 'projection_x_coordinate', 'units': 'm'}
    
    _y = {'axis': 'Y', 'data': x, 
          'long_name': 'Y distance on the projection plane from the origin', 
          'standard_name': 'projection_x_coordinate', 'units': 'm'}
    
    _z = {'axis': 'Z', 'data': np.array([0]),
          'long_name': 'Z distance on the projection plane from the origin',
          'positive': 'up', 'standard_name': 'projection_z_coordinate',
          'units': 'm'}
    
    _projection = {'_include_lon_0_lat_0': True, 'proj': proj}
    
    grid = pyart.core.grid.Grid(time=_time, fields=_fields, metadata=_metadata,
         origin_latitude=_origin_latitude, origin_longitude=_origin_longitude,
         origin_altitude=_origin_altitude, x=_x, y=_y, z=_z, projection=_projection,
         radar_longitude= _origin_longitude, radar_latitude=_origin_latitude, radar_altitude=_origin_altitude)
    return grid

# Presets
filelist = sorted(os.listdir('/home/scarani/Desktop/data/goes/001/'))
channel = 13
gridlist = []
grids = []


for i in filelist[0:20]:
    
    file = str('/home/scarani/Desktop/data/goes/001/' + i)   

    filename = os.path.join(os.path.dirname(ccrs.__file__),'data', 'netcdf', file)
    nc = netcdf_dataset(filename)
    
    sat_height = nc.variables['goes_imager_projection'].perspective_point_height
    
    
    x = nc.variables['x'][:].data * sat_height
    y = nc.variables['y'][:].data * sat_height
    a = nc.variables['CMI_C13'][:]
    c = a[~np.isnan(x)]
    data = nc.variables['CMI_C13']
    satvar = nc.variables.keys()
    proj_var = nc.variables[data.grid_mapping]
    
    globe = ccrs.Globe(ellipse='sphere', semimajor_axis=proj_var.semi_major_axis,
                       semiminor_axis=proj_var.semi_minor_axis)
    
    proj = ccrs.Geostationary(central_longitude=-75,sweep_axis='x',
                              satellite_height=sat_height, globe = globe)
    
    
    
    grid = get_grid()
    
    gridlist.append(grid)
    


    
#grid_gen = (pyart.io.read_grid(grid_name) for file_name in grid_files)

# Instantiate tracks object and view parameter defaults
tracks_obj = Cell_tracks(field='reflectivity')
print(tracks_obj.params)

# Adjust size parameter
#tracks_obj.params['MIN_SIZE'] = 4

# Get tracks from grid generator
tracks_obj.get_tracks(iter(gridlist))

# Inspect tracks
print(tracks_obj.tracks)



#for i in range(0,500,1):
#    for j in range(0,500,1):
#        k = b[i][j]
#        u = str(k)
#        if k == 'nan':
#            print('[' + str(i) + ']' + '[' + str(j) + ']' + '\n')
        

# Create generator of the same grids for animator
#anim_gen = (pyart.io.read_grid(file_name) for file_name in grid_files)

# Create animation in current working directory
#animate(tracks_obj, anim_gen, 'tint_test_animation', alt=1500)
        
    

        

#xlist = x.tolist()
#ylist = y.tolist()
#loc = []
#
#for i in range(0,500,1):
#    
#    loc.append((xlist[i],ylist[i]))
    