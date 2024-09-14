import netCDF4 as nc
import xarray as xr
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import os

def load_sst_data(file_path):
    """
    Load SST data from the NetCDF file.
    
    Parameters:
    - file_path (str): Path to the NetCDF file
    
    Returns:
    - dataset: Loaded NetCDF dataset
    - data: SST data as an xarray dataset
    """
    dataset = nc.Dataset(file_path, 'r')
    data = xr.open_dataset(file_path)
    return dataset, data

def extract_sst_for_region(data, lat_min, lat_max, lon_min, lon_max):
    """
    Extract SST data for a given latitude and longitude range.
    
    Parameters:
    - data: xarray dataset containing SST data
    - lat_min, lat_max: Latitude range
    - lon_min, lon_max: Longitude range
    
    Returns:
    - sst_df: DataFrame of SST data for the specified region
    """
    sst_box = data.sst.sel(lat=slice(lat_min, lat_max), lon=slice(lon_min, lon_max))
    sst_df = sst_box.to_dataframe().reset_index()
    sst_df['time'] = pd.to_datetime(sst_df['time'])
    return sst_df

def process_monthly_sst_data(sst_df, month):
    """
    Process SST data for a specific month, perform PCA, and return PCs and EVR values.
    
    Parameters:
    - sst_df (DataFrame): SST data for the region
    - month (int): Month for which to process data
    
    Returns:
    - pc_df (DataFrame): Principal Components DataFrame
    - explained_variance_ratio (array): Explained variance ratio for the PCs
    """
    sst_month = sst_df[sst_df['time'].dt.month == month]
    
    if sst_month.empty:
        print(f"No data points found for month {month} in the specified region.")
        return None, None
    
    # Pivot data into a lat/lon grid
    sst_pivot = sst_month.pivot(index='time', columns=['lat', 'lon'], values='sst')
    
    # Drop rows with missing values
    sst_pivot = sst_pivot.dropna(axis=0, how='any')
    
    if sst_pivot.isna().any().any():
        print(f"There are still NaN values in the data for month {month} after dropping.")
        return None, None
    
    # Standardize the SST data
    scaler = StandardScaler()
    try:
        sst_scaled = scaler.fit_transform(sst_pivot)
    except ValueError as e:
        print(f"Error during scaling for month {month}: {e}")
        return None, None
    
    # Perform PCA
    pca = PCA(n_components=20)
    principal_components = pca.fit_transform(sst_scaled)
    
    # Create a DataFrame for PCs
    pc_df = pd.DataFrame(data=principal_components, columns=[f'PC{i+1}' for i in range(20)], index=sst_pivot.index)
    
    # Get the explained variance ratio (EVR)
    explained_variance_ratio = pca.explained_variance_ratio_
    
    return pc_df, explained_variance_ratio

def save_pc_and_evr_data(pc_df, explained_variance_ratio, month):
    """
    Save the Principal Components and Explained Variance Ratio data to CSV files.
    
    Parameters:
    - pc_df (DataFrame): Principal Components DataFrame
    - explained_variance_ratio (array): Explained variance ratio
    - month (int): Month for which the data is being saved
    """
    # Save PCs to CSV
    # os.makedirs('sst_csv', exist_ok=True)
    # os.makedirs('evr_csv', exist_ok=True)
    # Save PCs to CSV in the 'sst_csv' directory
    pc_df.to_csv(f'sst_csv/sst_month_{month}_pcs.csv', index=True)
    
    # Save Explained Variance Ratio to CSV in the 'evr_csv' directory
    evr_df = pd.DataFrame(explained_variance_ratio)
    evr_df.to_csv(f'evr_csv/evr_month_{month}.csv', index=False, header=False)

def calculate_pcs_and_evr(file_path, lat_min, lat_max, lon_min, lon_max):
    """
    Main function to calculate PCs and EVRs for a specific region.
    
    Parameters:
    - file_path (str): Path to the NetCDF SST data
    - lat_min, lat_max: Latitude range
    - lon_min, lon_max: Longitude range
    
    Returns:
    - None (prints results and saves data)
    """
    os.makedirs('sst_csv', exist_ok=True)
    os.makedirs('evr_csv', exist_ok=True)

    # Load SST data
    dataset, data = load_sst_data(file_path)
    # print("Available latitude range:", data.lat.min().values, "to", data.lat.max().values)
    # print("Available longitude range:", data.lon.min().values, "to", data.lon.max().values)
    
    
    # Extract SST data for the given region
    sst_df = extract_sst_for_region(data, lat_min, lat_max, lon_min, lon_max)
    # print(sst_df.head())

    # Check if there's any valid SST data
    if sst_df.empty:
        print("No SST data found for the given latitude and longitude range.")
    else:
        print(f"Data found: {sst_df.shape[0]} rows.")
    
    
    for month in range(1, 13):
        print(f"Processing month {month}...")
        pc_df, explained_variance_ratio = process_monthly_sst_data(sst_df, month)
        
        # if pc_df is not None and explained_variance_ratio is not None:
        #     print(f'Explained Variance Ratio for Month {month}: {explained_variance_ratio}')
        #     save_pc_and_evr_data(pc_df, explained_variance_ratio, month)
        # else:
        #     print(f"Skipping month {month} due to insufficient data.")

