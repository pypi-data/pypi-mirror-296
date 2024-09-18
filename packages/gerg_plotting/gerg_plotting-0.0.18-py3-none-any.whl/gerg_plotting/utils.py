import numpy as np
import pandas as pd
import xarray as xr
import gsw
import datetime

def lat_min_smaller_than_max(instance, attribute, value):
    if value is not None:
        if value >= instance.lat_max:
            raise ValueError("'lat_min' must to be smaller than 'lat_max'")
    
def lon_min_smaller_than_max(instance, attribute, value):
    if value is not None:
        if value >= instance.lon_max:
            raise ValueError("'lon_min' must to be smaller than 'lon_max'")
        
def validate_array_lengths(instance,attribute,value):
    lengths = {attr.name:len(getattr(instance,attr.name)) for attr in instance.__attrs_attrs__ if isinstance(getattr(instance,attr.name),np.ndarray)}
    if len(set(lengths.values()))>1:
        raise ValueError(f'All Dims and Vars must be the same length, got lengths of {lengths}')

        
def get_center_of_mass(lon,lat,pressure) -> tuple:
    centroid = tuple([np.nanmean(lon), np.nanmean(lat), np.nanmean(pressure)])
    return centroid

def interp_data(ds:xr.Dataset) -> pd.DataFrame:
    new_time_values = ds['time'].values.astype('datetime64[s]').astype('float64')
    new_mtime_values = ds['m_time'].values.astype('datetime64[s]').astype('float64')

    # Create a mask of non-NaN values in the 'longitude' variable
    valid_longitude = ~np.isnan(ds['longitude'])
    # Now ds_filtered contains the data where NaN values have been dropped based on the longitude variable

    ds['latitude'] = xr.DataArray(np.interp(new_time_values, new_mtime_values[valid_longitude], ds['latitude'].values[valid_longitude]),[('time',ds.time.values)])
    ds['longitude'] = xr.DataArray(np.interp(new_time_values, new_mtime_values[valid_longitude], ds['longitude'].values[valid_longitude]),[('time',ds.time.values)])

    df = ds[['latitude','longitude','pressure','salinity','temperature']].to_dataframe().reset_index()
    df['time'] = df['time'].astype('datetime64[s]')
    # df = df.set_index(['time'])
    df = df.dropna()

    return df

def filter_var(var:pd.Series,min_value,max_value):
    var = var.where(var>min_value)
    var = var.where(var<max_value)
    return var

def calculate_range(var:np.ndarray):
    return [np.nanmin(var),np.nanmax(var)]

def calculate_pad(var,pad=0.15):
    start, stop = calculate_range(var)
    difference = stop - start
    pad = difference*pad
    start = start-pad
    stop = stop+pad
    return start,stop

def get_sigma_theta(salinity,temperature,cnt=False):
    # Subsample the data
    num_points = len(temperature)
    if num_points>300_000 and num_points<1_000_000:
        salinity = salinity[::250]
        temperature = temperature[::250]
    elif num_points>=1_000_000:
        salinity = salinity[::1000]
        temperature = temperature[::1000]        

    # Remove nan values
    salinity = salinity[~np.isnan(salinity)]
    temperature = temperature[~np.isnan(temperature)]

    mint=np.min(temperature)
    maxt=np.max(temperature)

    mins=np.min(salinity)
    maxs=np.max(salinity)

    num_points = len(temperature)

    tempL=np.linspace(mint-1,maxt+1,num_points)

    salL=np.linspace(mins-1,maxs+1,num_points)

    Tg, Sg = np.meshgrid(tempL,salL)
    sigma_theta = gsw.sigma0(Sg, Tg)

    if cnt:
        num_points = len(temperature)
        cnt = np.linspace(sigma_theta.min(), sigma_theta.max(),num_points)
        return Sg, Tg, sigma_theta, cnt
    else:
        return Sg, Tg, sigma_theta


def get_density(salinity,temperature):
    return gsw.sigma0(salinity, temperature)

def print_time(value: int = None, intervals: list = [10,50,100,500,1000]):
    """
    Prints the current time if the value matches any of the intervals specified.

    Args:
    - value (int): The value value.
    - intervals (list): A list of integers representing intervals.

    Returns:
    - None
    """

    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    if value is None:
        print(current_time)
        return

    # Check if intervals is at least 2 values long
    if not len(intervals) >= 2:
        raise ValueError(f'Not enough intervals, need at least 2 values, you passed {len(intervals)}')


    if value <= intervals[0]:
        print(f'{value = }, {current_time}')
        return
    elif value <= intervals[-2]:
        for idx,interval in enumerate(intervals[0:-1]):
            if value >= interval:
                if value < intervals[idx+1]:
                    if value % interval==0:
                        print(f'{value = }, {current_time}')
                        return
                    break
    elif value >= intervals[-1]:
        if value % intervals[-1]==0:
            print(f'{value = }, {current_time}')
            return