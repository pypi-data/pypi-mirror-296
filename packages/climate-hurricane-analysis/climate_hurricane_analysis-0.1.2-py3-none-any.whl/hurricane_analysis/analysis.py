import numpy as np
import pandas as pd
from scipy import stats
from scipy.spatial.distance import cdist
from datetime import datetime, timedelta
import re
import os
from glob import glob

# sst_month_1_pcs

def calculate_start_date(year, lag_months, target_month):

    if not (1 <= target_month <= 12):
        raise ValueError(f"Invalid target month: {target_month}. Month must be between 1 and 12.")
    
    if lag_months < 0:
        raise ValueError(f"Invalid lag months: {lag_months}. Lag months must be non-negative.")
    
    end_date = datetime(year, target_month, 1)
    
    start_date = end_date - pd.DateOffset(months=lag_months)
    # print(f"Year: {year}, Target Month: {target_month}, Start Date: {start_date}, End Date: {end_date}")
    return start_date.strftime('%Y-%m-%d')

def numerical_sort(value):
    # Extracts the number in the file name for sorting
    numbers = re.findall(r'\d+', value)
    return int(numbers[-1]) if numbers else 0

def extract_month_from_filename(filename):
    match = re.search(r'sst_month_(\d+)_pcs\.csv', filename)
    if match:
        return int(match.group(1))
    return None

def read_ace_data(file_path):
    ace_data = pd.read_csv(file_path, delim_whitespace=True, header=None, names=['Year', 'ACE'])
    ace_data.set_index('Year', inplace=True)
    return ace_data


def read_pca_data(file_path):
    data = pd.read_csv(file_path)
    data['time'] = pd.to_datetime(data['time'])
    data.set_index('time', inplace=True)
    return data

def read_pca_data2(file_path):
    
    pca_data = pd.read_csv(file_path, delim_whitespace=True, header=None)

    #pca_data = pca_data.dropna(how='all')
    
    pca_data.set_index(0, inplace=True)

    pca_data.columns = [f'PC{i}' for i in range(1, pca_data.shape[1] + 1)]

    #pca_data = pca_data.drop(index=pca_data.index[0])
    
    return pca_data

def read_evr_data(evr_directory, num_pcs):
    all_evr_files = sorted(glob(os.path.join(evr_directory, '*.csv')), key=numerical_sort)
    evr_matrix = []

    for file in all_evr_files:
        evr_data = pd.read_csv(file, header=None)
        evr_values = evr_data.values.flatten().astype(float)
        evr_matrix.append(evr_values[0:num_pcs])  

    return np.array(evr_matrix)


def read_evr_data2(file_path):
    
    explained_variance = pd.read_csv(file_path, delim_whitespace=True, header=None)
    explained_variance_list = explained_variance.values.flatten().tolist()
    
    return explained_variance_list


def create_yearly_pc_vectors(data_directory, evr_directory, num_pcs, lag_months, target_month):
    

    all_files = sorted(glob(os.path.join(data_directory, '*.csv')), key=numerical_sort)
    
    evr_matrix = read_evr_data(evr_directory, num_pcs)
    

    

    pc_vectors = {}

    for year in range(1983, 2024):
        start_date = calculate_start_date(year, lag_months, target_month)
        end_date = f'{year}-{target_month:02d}-01'
        
        yearly_pcs = []

        
        for file in all_files:
            
            month_number = extract_month_from_filename(file)
            
            evr_values = np.asarray(evr_matrix[month_number - 1][:num_pcs])
            

            monthly_data = read_pca_data(file)
            filtered_data = monthly_data.loc[start_date:end_date]
            

            if not filtered_data.empty:
                first_n_pcs = np.asarray(filtered_data.iloc[:, :num_pcs].values)  # Ensure this is a NumPy array
                first_n_pcs = first_n_pcs.flatten()
                total_length = len(first_n_pcs)
                repeated_evr_values = np.tile(evr_values, total_length // num_pcs)
                

                try:
                    # print(f"EVR values: {evr_values}")
                    # print(f"First 3 PCs: {first_three_pcs}")
                    
                    weighted_pcs = first_n_pcs * repeated_evr_values  # Perform element-wise multiplication
                except Exception as e:
                    print(f"Error occurred during multiplication: {e}")
                    print(f"Repeated EVR values: {repeated_evr_values}")
                    print(f"First N PCs: {first_n_pcs}")
                    continue  # Skip to the next file if there's an error

                # print(f"Weighted PCs: {weighted_pcs}")
                yearly_pcs.append(weighted_pcs.flatten())

        if yearly_pcs:
            pc_vectors[year] = np.concatenate(yearly_pcs)
        
        # print("Available years in pc_vectors:", list(pc_vectors.keys()))
        # print(f"Done with year: {year}")
        # print("\n")

    return pc_vectors


def find_top_analogs(pc_vectors, target_year, top_n=4):
    target_vector = pc_vectors[target_year].reshape(1, -1)
    years = list(pc_vectors.keys())
    vectors = np.array([pc_vectors[year] for year in years])

    # Calculate the Euclidean distances between the target year vector and all other year vectors
    distances = cdist(target_vector, vectors, metric='euclidean').flatten()

    
    distances_df = pd.DataFrame({'Year': years, 'Distance': distances})
    distances_df = distances_df.sort_values(by='Distance')

    # Get the top N analogs (excluding the target year itself)
    top_analogs = distances_df[distances_df['Year'] != target_year].head(top_n)

    return top_analogs


def calculate_ace_forecast(top_analogs, ace_data, target_year):
    # Calculate weights using the inverse square of the distance
    top_analogs['Weight'] = 1 / (top_analogs['Distance'] ** 2)

    # Map ACE values to the top analog years
    ace_values = top_analogs['Year'].map(ace_data['ACE'])

    # Calculate ACE-FCST using the weighted average formula
    weights = top_analogs['Weight'].values
    weighted_ace_sum = np.sum(weights * ace_values)
    total_weight = np.sum(weights)
    ace_fcst = weighted_ace_sum / total_weight

    # Add ACE values to the DataFrame
    top_analogs['ACE'] = ace_values
    actual_ace = ace_data.loc[target_year, 'ACE']

    # Calculate improvement (skil)
    erc = abs(121 - actual_ace)
    erf = abs(ace_fcst - actual_ace)
    skil = 100 * ((erc - erf)/erc)
    # if skil < -1000:
    #     print(f"ACE Forecast: {ace_fcst}, Actual ACE: {actual_ace}, ERC: {erc}, ERF: {erf}")
    #     print(f"Calculated Skil: {skil}")

    return ace_fcst, skil, top_analogs

def optimize_pc_analog_and_lag_configuration(data_directory, evr_directory, ace_data, target_year, target_month):
    best_num_pcs = None
    best_num_analogs = None
    best_lag_months = None
    highest_skil = -float('inf')
    best_ace_fcst = None
    best_top_analogs = None

    for num_pcs in range(1, 10):  # Iterate over 1 to 4 PCs
        for num_analogs in range(1,5):  # Iterate over 1 to 4 analog years
            for lag_months in range(1, 14):  # Iterate over 1 to 13 lag months
                pc_vectors = create_yearly_pc_vectors(data_directory, evr_directory, num_pcs, lag_months, target_month)
                top_analogs = find_top_analogs(pc_vectors, target_year, num_analogs)
                ace_fcst, skil, top_analogs_with_ace = calculate_ace_forecast(top_analogs, ace_data, target_year)

                print(f"PCs: {num_pcs}, Analogs: {num_analogs}, Lag Months: {lag_months}, Skil: {skil:.2f}%")

                if skil > highest_skil:
                    highest_skil = skil
                    best_num_pcs = num_pcs
                    best_num_analogs = num_analogs
                    best_lag_months = lag_months
                    best_ace_fcst = ace_fcst
                    best_top_analogs = top_analogs_with_ace

    return best_num_pcs, best_num_analogs, best_lag_months, highest_skil, best_ace_fcst, best_top_analogs



data_directory = './sst_csv'  
evr_directory = './evr_csv'
ace_file_path = './ACE-TOT.dat'  # Path to the ACE-TOT.dat file

# Load ACE data
# ace_data = read_ace_data(ace_file_path)

# pc_vectors = create_yearly_pc_vectors(data_directory, evr_directory)


# # year_1984_vector = pc_vectors.get(1984, None)
# # if year_1984_vector is not None:
# #     print(f"Vector for 1984: {year_1984_vector}")
# # else:
# #     print("No data for the year 1984")


# years_to_check = [1984, 2000, 2013, 2020]
# results = []

# for year in years_to_check:
#     top_analogs = find_top_analogs(pc_vectors, year, 4)
#     # print(f"Top analogs for {year}:")
#     # print(top_analogs)
    
    
#     for index, row in top_analogs.iterrows():
#         results.append([year, row['Year'], row['Distance']])


# results_df = pd.DataFrame(results, columns=['Year', 'Analog Year', 'Distance'])


# results_df.to_csv('top_analogs_results.csv', index=False)

# print("Results written to top_analogs_results.csv")

# top_analogs_1985 = find_top_analogs(pc_vectors, 1985, 4)
# ace_fcst_1985, percent_error_1985, top_analogs_1985_with_ace = calculate_ace_forecast(top_analogs_1985, ace_data, 1985)
# print("Top analogs for 1985 with ACE:")
# print(top_analogs_1985_with_ace)
# print(f"\nACE-FCST for 1985: {ace_fcst_1985}, ACE Value for 1985: {ace_data.loc[1985, 'ACE']}")
# print(f"Percent Error for 1985: {percent_error_1985:.2f}%")

# Example usage
# best_num_pcs, lowest_percent_error, best_ace_fcst, best_top_analogs = optimize_pc_configuration(
#     data_directory, evr_directory, ace_data, 1985)







def convert_to_original_format(file_path, counter, output_file=None):
    # Read the PCA data
    #print("Counter: ", counter)
    pca_data = pd.read_csv(file_path, delim_whitespace=True, header=None)
    
    # Drop the first column that corresponds to the indices
    pca_data = pca_data.drop(columns=[0])
    
    
    start_year = 1982
    start_month = counter

    # Generate the correct date range
    time_column = pd.date_range(start=f'{start_year}-{start_month:02d}-01', periods=len(pca_data), freq='12MS')
    
    
    pca_data.insert(0, 'time', time_column)
    
    # Rename the columns to match the original format (PC1, PC2, ..., PC20)
    pca_data.columns = ['time'] + [f'PC{i}' for i in range(1, pca_data.shape[1])]
    
    # Optionally, save the DataFrame to a CSV file
    if output_file:
        pca_data.to_csv(output_file, index=False)
    
    return pca_data


def convert_all_files(input_directory, output_directory):
    # Get all SST-*.PC files in the directory
    #all_files = sorted(glob(os.path.join(data_directory, '*.csv')), key=numerical_sort)
    file_paths = sorted(glob(os.path.join(input_directory, 'SST-*.PC')), key=numerical_sort)
    
    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    for counter, file_path in enumerate(file_paths, start=1):
        # Convert each file
        converted_data = convert_to_original_format(file_path, counter)
        
        # Debugging: print the converted data for June (counter == 6)
        # if counter == 6:
        #     print("Data for June before saving:")
        #     print(converted_data)
        
        # Generate the output file path
        output_file_name = f'sst_month_{counter}_pcs.csv'
        output_file_path = os.path.join(output_directory, output_file_name)
        
        # Save the converted data to a CSV file
        #print(f"Saving to {output_file_path}")
        converted_data.to_csv(output_file_path, index=False)
        
        # Debugging: confirm the file was saved
        
        # print(f"File saved: {output_file_path}")


def convert_evr_to_csv(file_path, output_file_path):

    # Read the EVR data as a DataFrame with no header
    evr_data = pd.read_csv(file_path, delim_whitespace=True, header=None)
    
    # Flatten the DataFrame to a single row
    evr_flat = evr_data.values.flatten()
    
    
    evr_df = pd.DataFrame([evr_flat])
    
    # Save to CSV
    evr_df.to_csv(output_file_path, index=False, header=False)
    
    # print(f"Converted {file_path} to {output_file_path}")

def convert_all_evr_files(input_directory, output_directory):
    
    file_paths = glob(os.path.join(input_directory, 'SST-*.Explaine'))
    
    
    os.makedirs(output_directory, exist_ok=True)
    
    for file_path in file_paths:
        
        output_file_name = os.path.basename(file_path) + '.csv'
        output_file_path = os.path.join(output_directory, output_file_name)
        
       
        convert_evr_to_csv(file_path, output_file_path)


# pca_inputdir = './sst_2'
# pca_outputdir = './sst_2_csv'
# evr_inputdir = './evr_2'  
# evr_outputdir = './evr_2_csv'  


# ace_data = read_ace_data(ace_file_path)
# converted_pca_data = convert_all_files(pca_inputdir, pca_outputdir)
# converted_evr_data = convert_all_evr_files(evr_inputdir, evr_outputdir)

# # print(calculate_start_date(2024, 13))  # Output: 2023-05-01
# # print(calculate_start_date(2024, 24))  # Output: 2022-06-01 

# # Example usage for the year 2010
# target_month = 10
# best_num_pcs, best_num_analogs, best_lag_months, highest_skil, best_ace_fcst, best_top_analogs = optimize_pc_analog_and_lag_configuration(
#     pca_outputdir, evr_outputdir, ace_data, 2010, target_month)

# print(f"\nOptimal number of PCs: {best_num_pcs}")
# print(f"Optimal number of Analogs: {best_num_analogs}")
# print(f"Optimal number of Lag Months: {best_lag_months}")
# print(f"Highest Skil/Improvement: {highest_skil:.2f}%")

# print(f"Best ACE-FCST: {best_ace_fcst}")
# print(f"ACE Value for 2010: {ace_data.loc[2010, 'ACE']}")
# print("Best Top Analogs with ACE:")
# print(best_top_analogs)

# output_file = 'hurricane_analysis_results.txt'

# with open(output_file, 'w') as f:
#     f.write(f"Optimal number of PCs: {best_num_pcs}\n")
#     f.write(f"Optimal number of Analogs: {best_num_analogs}\n")
#     f.write(f"Optimal number of Lag Months: {best_lag_months}\n")
#     f.write(f"Highest Skil/Improvement: {highest_skil:.2f}%\n")
#     f.write(f"\nBest ACE-FCST: {best_ace_fcst}\n")
#     f.write(f"ACE Value for 2010: {ace_data.loc[2010, 'ACE']}\n")
#     f.write("Best Top Analogs with ACE:\n")
#     f.write(best_top_analogs.to_string(index=False))  # Convert DataFrame to string without index











