import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy import stats
import pkg_resources

# Remove outliers


def rm_outliers(data, factor=1.5, print_out=False):
    """
    Removes outliers from numeric columns of a DataFrame using the IQR method.

    Parameters:
    - data: DataFrame containing the data.
    - factor: The multiplier for the IQR to determine outlier bounds (default is 1.5).
    - print_out: If True, prints the count of outliers for each column.

    Returns:
    - df: DataFrame with outliers replaced by NaN.
    - outliers_df: DataFrame containing the identified outliers.
    """
    df = data.copy()
    outliers_df = pd.DataFrame(index=df.index, columns=df.columns)  # Initialize a DataFrame for outliers

    for column in df.select_dtypes(include=['float64', 'int64']).columns:
        # Calculate IQR while ignoring NaN values
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - factor * IQR
        upper_bound = Q3 + factor * IQR

        # Identify outliers
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        outliers_df.loc[outliers.index, column] = outliers[column]

        # Count outliers and optionally print the count
        outlier_count = outliers[column].count()
        if print_out:
            print(f"Column '{column}' has {outlier_count} outliers.")

        # Replace outliers with NaN
        df.loc[outliers.index, column] = np.nan

    return df, outliers_df


# Function to sum the values in specified columns and replicate across the group
def sum_and_replicate(df, col_suffix):
    # Identify the columns that end with the specified suffix
    cols = [col for col in df.columns if col.endswith(col_suffix)]
    # Sum these columns row-wise
    summed_values = df[cols].sum(axis=1)
    # Replicate the summed values across the columns
    for col in cols:
        df[col] = summed_values


def apply_sum(df):
    # Applying the function to each column group
    split_col_names = [re.match(r'(\d+)([A-Za-z]+)', header).groups() for header in df.columns]
    elements = {name[1] for name in split_col_names if len(name) > 1}
    df_copy = df.copy()
    for suffix in elements:
        sum_and_replicate(df_copy, suffix)
    return df_copy


def fractional_abundances(df):
    df_copy = df.copy()
    df_sum = apply_sum(df_copy)
    df_fa = df/df_sum
    df_fa.rename(columns=lambda x: f"F{x}", inplace=True)
    return df_fa


# To generate standard curves

def generate_standard_curves(
    std_conc: pd.DataFrame,
    std_counts: pd.DataFrame,
    spl_counts: pd.DataFrame,
    result_path: str,
    exp_name: str
):
    """
    Generate standard curves, perform linear regression, and save the results.

    Parameters:
    - std_conc: DataFrame containing standard concentrations with 'Label' as the index.
    - std_counts: DataFrame containing standard counts per second with 'Label' as the index.
    - spl_counts: DataFrame containing sample counts per second with 'Label' as the index.
    - result_path: Path to save the output files.
    - exp_name: Experiment name to be used in the output file names.
    
    Outputs:
    - Saves regression results and predicted concentrations to Excel.
    - Saves plots of standard curves to a PDF.
    """
    
    # Create a dictionary to store the regression results
    regression_results = {}

    # Create an empty DataFrame to store the predicted concentrations
    sample_conc = pd.DataFrame()

    # Define the path for saving the PDF and Excel outputs
    pdf_path = f'{result_path}{exp_name}_standard_curves.pdf'

    # Create a PdfPages object to save plots into a single PDF
    with PdfPages(pdf_path) as pdf:
        
        # Iterate over each element (columns in std_conc DataFrame)
        for column in std_conc.columns:
            
            # Convert data to numeric, handling missing values as NaN
            xa = std_counts.apply(lambda x: pd.to_numeric(x, errors='coerce'))
            ya = std_conc.apply(lambda x: pd.to_numeric(x, errors='coerce'))
            za = spl_counts.apply(lambda x: pd.to_numeric(x, errors='coerce')).fillna(0)
            
            # Create a mask to filter out NaN values for accurate regression
            mask = ~np.isnan(xa.loc[:, column]) & ~np.isnan(ya.loc[:, column])
            
            x = xa.loc[mask, column].astype(float)  # X-axis: counts
            y = ya.loc[mask, column].astype(float)  # Y-axis: concentrations
            z = za.loc[:, column].astype(float)     # Sample counts for prediction
        
            # Perform a linear regression between counts and concentrations
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            
            # Store the regression results in a dictionary
            regression_results[column] = {
                'slope': slope,
                'intercept': intercept,
                'r_value': r_value,
                'R-squared': r_value**2,
                'p_value': p_value,
                'std_err': std_err
            }
            
            # Predict sample concentrations using the regression model
            spl_val = z * slope + intercept
            sample_conc[column] = spl_val
            
            # Create and save the plot for each element's standard curve
            plt.figure()
            plt.plot(x, y, 'o', label='Data Points')
            plt.plot(x, intercept + slope * x, 'r', label='Fitted Line')
            plt.title(f'Element: {column}')
            plt.xlabel('Count')
            plt.ylabel('PPB')
            plt.legend()
            plt.grid(True)
            
            # Display regression metrics on the plot
            plt.text(0.95, 0.05, f'R-squared: {r_value**2:.4f}; Slope: {slope:.4f}',
                     transform=plt.gca().transAxes, verticalalignment='bottom', horizontalalignment='right')

            # Save the figure into the PDF
            pdf.savefig()
            plt.close()

    # Save the regression results and predicted sample concentrations to Excel files
    results_df = pd.DataFrame(regression_results).T
    # results_df.to_excel(regression_results_path, index=True)
    # sample_conc.to_excel(sample_conc_path, index=True)
    return results_df, sample_conc


# Calculate Natural Abundances

def check_col_name(col_names):
    if re.match(r'^\d', col_names):
        return "Number"
    elif re.match(r'^[A-Za-z]', col_names):
        return "Letter"
    else:
        return "None"
        

def natural_abundances(df):
    """
    Converts relative concentrations of samples to isotope concentrations using natural abundances.

    Parameters:
    - df: DataFrame containing the relative concentrations of isotopes.

    Returns:
    - spl_df: DataFrame with isotope concentrations adjusted by natural abundances.
    """
    # remove if any space in column name and check whether col names start with letter or number
    df.columns = df.columns.str.replace(' ', '')
    
    col_name2 = check_col_name(df.columns[2])
    col_name3 = check_col_name(df.columns[3])
    if col_name2 == col_name3:
        col_name = col_name2
    else:
        "None"
        
    # Load natural abundances data from the Excel file
    file_path = pkg_resources.resource_filename('xID', 'xApp/data/Isotope_abundance.xlsx')
    try:
        iso_na = pd.read_excel(file_path, header=0, index_col=0)
    except Exception as e:
        raise FileNotFoundError(f"Error loading natural abundances data: {e}")

    # Keep rows in isotopes_natural_abundances where 'Symbol' is present in df.columns
    if col_name == "Letter":
        f_na = iso_na[iso_na['Symbol'].isin(df.columns)]
        f_na.reset_index(drop=False, inplace=True)
        f_na = f_na.set_index('Symbol')
        df_plus = f_na.join(df.T).sort_values(by='SL').set_index('SymbolR').drop(columns=['SL', 'Z', 'Name', 'Mass'])
        nat_abundances = df_plus[['Abundance']].T
        df = df_plus.drop(columns='Abundance').T
    elif col_name == "Number":
        f_na = iso_na[iso_na['SymbolR'].isin(df.columns)]
        f_na.reset_index(drop=False, inplace=True)
        f_na = f_na.set_index('SymbolR')
        df_plus = f_na.join(df.T).sort_values(by='SL').drop(columns=['SL', 'Z', 'Name', 'Mass', 'Symbol'])
        nat_abundances = df_plus[['Abundance']].T
        df = df_plus.drop(columns='Abundance').T
    else:
        raise ValueError('Error in column names')

    # Create a copy of the input DataFrame and ensure all values are numeric, filling NaNs with zeros
    rel_spl_df = df.apply(pd.to_numeric, errors='coerce').fillna(0)

    # Prepare an empty DataFrame to store the adjusted isotope concentrations
    spl_df = pd.DataFrame(index=rel_spl_df.index, columns=rel_spl_df.columns)

    # Loop through each column to calculate isotope concentrations using natural abundances
    for col in rel_spl_df.columns:
        try:
            # Get the natural abundance value for the current isotope column
            nat_ab = nat_abundances.loc[:, col].astype(float).values[0]
        except KeyError:
            raise KeyError(f"Isotope '{col}' not found in natural abundances data.")
        except IndexError:
            raise ValueError(f"Natural abundance data for isotope '{col}' is missing or malformed.")

        # Compute the adjusted concentration based on natural abundance
        spl_df[col] = (rel_spl_df[col] * nat_ab) / 100

    # Return the DataFrame with adjusted concentrations
    return spl_df
