# This file is part of hvspatialpy, a Python package for evaluating
# spatial variability of a site utilizing spatially distributed HVSR.

# Copyright (c) 2024 Francisco Javier Ornelas (jornela1@g.ucla.edu)

"""Functions for computing the spatial variability of a site."""

import os
import json
import logging
import numpy as np
import pandas as pd
from obspy import read_inventory
from scipy.spatial.distance import (
    euclidean, sqeuclidean, braycurtis, canberra, chebyshev, cityblock, correlation, cosine,
    jensenshannon, minkowski, dice, hamming, jaccard, kulczynski1, rogerstanimoto, russellrao,
    sokalmichener, sokalsneath, yule)
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import mean_absolute_error, mean_squared_error
from tslearn.metrics import lcss, dtw

logger = logging.getLogger(__name__)

__all__ = ['_find_nearest_trough', 'dist_from_vert_arr', 'create_frequency_dataframe', 'compute_correlations']


def _find_peaks(y, threshold=1.6, min_distance=1):
    """
    Find peaks in a 1D array.

    Parameters:
    y: array
        The input data array.
    threshold: float
        Minimum value of peaks.
    min_distance: int
        Minimum number of points between peaks.

    return:
        peaks: Indices of the peaks in the array.

    """
    peaks = []
    n = len(y)

    for i in range(1, n - 1):
        if y[i] > y[i - 1] and y[i] > y[i + 1] and y[i] > threshold:
            if not peaks or i - peaks[-1] >= min_distance:
                peaks.append(i)

    return peaks


def _find_troughs(y):
    """
    Finds troughs in a 1D array.

    Parameters:
    y: array
        The input data array.

    return
        troughs: Indicies of troughs

    """

    troughs = []
    # Find troughs (local minima) in the data
    n = len(y)
    for i in range(1, n - 1):
        if y[i] < y[i - 1] and y[i] < y[i + 1]:
            troughs.append(i)

    return troughs


def _find_nearest_trough(y, threshold=1.6, min_distance=1):
    """
    Find the indicies where a peak and two troughs were identified.

    Parameters

    y: array
        Input array
    threshold: float
        Minimum amplitude threshold.
    min_distance: int
        Minimum number of points between peaks.

    return
        Location of true peaks within an array

    """
    peaks = _find_peaks(y, threshold=threshold, min_distance=min_distance)
    troughs = _find_troughs(y)

    left_troughs = []
    right_troughs = []

    # Find the left and right troughs for each peak
    for peak in peaks:
        # Troughs to the left of the peak
        left_candidates = [t for t in troughs if t < peak]
        left_trough = max(left_candidates, default=None, key=lambda t: t) if left_candidates else 0

        # Troughs to the right of the peak
        right_candidates = [t for t in troughs if t > peak]
        right_trough = min(right_candidates, default=None, key=lambda t: t) if right_candidates else 0

        left_troughs.append(left_trough)
        right_troughs.append(right_trough)

    return np.asarray(left_troughs), np.asarray(right_troughs), peaks, troughs


def _compute_dist(lat_meas, lat_ref, long_meas, long_ref, r=6373.0):
    """
    Function to compute distance from two points using Haversine formula.

    lat_meas: float
        Latitude value that is measured.
    lat_ref: float
        Latitude value that is the reference.
    long_meas:  float
        Longitude that is measured.
    long_ref: float
        Longitude that is reference.
    r: float
        Radius of the earth.

    return
        Distance between a reference and measured point in meters.

    """

    dlat = np.radians(lat_meas) - np.radians(lat_ref)
    dlong = np.radians(long_meas) - np.radians(long_ref)

    a = np.sin(dlat / 2) ** 2 + np.cos(np.radians(lat_ref)) * np.cos(np.radians(lat_meas)) * np.sin(dlong / 2) ** 2

    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    distance = (r * c) * 1000

    return distance


def _get_locations(base_dir, site, xml_folder_name):
    """
    Retrieves location data from XML files and returns a DataFrame with test names, latitudes, and longitudes.

    Parameters:

    base_dir: str
        The base directory containing site-specific folders.
    site: str
        The site number to navigate to.
    xml_folder_name: str
        The folder name containing the XML files.

    return
        A DataFrame with columns 'tests', 'latitude', and 'longitude'.

    """

    # Initialize lists to store data
    test_list = []
    latitude_list = []
    longitude_list = []

    # Define the site directory path
    site_dir = os.path.join(base_dir, site)

    # Iterate over items in the site directory
    for test_dir in os.listdir(site_dir):
        test_dir_path = os.path.join(site_dir, test_dir)

        # Skip non-directory files and specific directory names
        if not os.path.isdir(test_dir_path) or test_dir == 'Mean Curves' or test_dir.endswith('.csv'):
            continue

        # Define the path to the XML folder
        xml_folder_path = os.path.join(test_dir_path, xml_folder_name)

        # Skip if the XML folder does not exist
        if not os.path.isdir(xml_folder_path):
            continue

        # Iterate over XML files in the XML folder
        for xml_file in os.listdir(xml_folder_path):
            if xml_file.endswith('.xml'):
                xml_file_path = os.path.join(xml_folder_path, xml_file)

                try:
                    # Read inventory from the XML file
                    inv_test = read_inventory(xml_file_path, format="STATIONXML")
                    cha_test = inv_test[0][0][0]

                    # Extract latitude and longitude
                    latitude = cha_test.latitude
                    longitude = cha_test.longitude

                    # Append data to lists
                    test_list.append(test_dir)
                    latitude_list.append(latitude)
                    longitude_list.append(longitude)

                except Exception as e:
                    print(f"Error processing {xml_file_path}: {e}")

    # Create a DataFrame from the collected data
    loc_df = pd.DataFrame({
        'tests': test_list,
        'latitude': latitude_list,
        'longitude': longitude_list
    })

    return loc_df


def dist_from_vert_arr(base_dir, site, xml_folder_name):
    """
    Computes distances from the reference location to all other locations.

    Parameters:

    base_dir: str
        The base directory containing site-specific folders.
    site: str
        The site number to navigate to.
    xml_folder_name: str
        The folder name containing the XML files.

    return
        A DataFrame with 'tests' and 'distance' columns.
    """

    # Retrieve location data
    loc_df = _get_locations(base_dir, site, xml_folder_name)

    # Extract values from DataFrame
    tests = loc_df.tests.values
    latitudes = loc_df.latitude.values
    longitudes = loc_df.longitude.values

    # Initialize reference coordinates
    latitude_ref = None
    longitude_ref = None

    # Identify the reference location
    for test, latitude, longitude in zip(tests, latitudes, longitudes):
        if test == f'{site}.0.0':
            latitude_ref = latitude
            longitude_ref = longitude
            break

    # Check if reference location was found
    if latitude_ref is None or longitude_ref is None:
        raise ValueError(f"Reference location with test '{site}.0.0' not found.")

    # Compute distances
    distances = []
    for latitude, longitude in zip(latitudes, longitudes):
        distance = _compute_dist(latitude, latitude_ref, longitude, longitude_ref)
        distances.append(distance)

    # Add distances to DataFrame
    loc_df['distance'] = distances

    return loc_df


def create_frequency_dataframe(base_dir, site, freq, mean_arr):
    """
    Creates a DataFrame with frequency data from directories and provides an interactive plot for manual adjustment.

    Parameters:

    base_dir: str
        The base directory where the site directories are located.
    site: str
        The specific site directory to process.
    freq: list
        List of frequency values.
    mean_arr: ndarray
        Array containing mean frequency values for identifying intervals.

    return
        DataFrame containing the site, test, and frequency intervals.
    """

    # Find initial frequency intervals
    left_troughs, right_troughs, peaks, troughs = _find_nearest_trough(mean_arr)
    min_freq_idx = np.asarray(left_troughs)
    max_freq_idx = np.asarray(right_troughs)

    num_peaks = len(min_freq_idx)

    min_freq = [freq[i] for i in min_freq_idx]
    max_freq = [freq[i] for i in max_freq_idx]

    # Initialize lists to store the data
    test_list = []
    site_list = []
    freq_min_list = []
    freq_max_list = []
    num_peaks_list = []

    # Iterate over directories and populate lists
    site_dir_path = os.path.join(base_dir, site)
    for test in os.listdir(site_dir_path):
        test_dir_path = os.path.join(site_dir_path, test)

        if not os.path.isdir(test_dir_path) or test.endswith('.csv') or test == 'Mean Curves':
            continue

        for i, (min_f, max_f) in enumerate(zip(min_freq, max_freq)):
            # Ensure frequency values are within bounds
            if min_f in freq and max_f in freq:
                test_list.append(test)
                site_list.append(site)
                freq_min_list.append(min_f)
                freq_max_list.append(max_f)
                num_peaks_list.append(num_peaks)

    # Create a DataFrame from the collected data
    freq_df = pd.DataFrame({
        'site': site_list,
        'tests': test_list,
        'numPeaks': num_peaks_list
    })

    # Initialize lists for frequency intervals
    for i in range(len(min_freq)):
        min_vals = []
        max_vals = []

        for j in range(len(test_list)):
            if min_freq[i] in freq and max_freq[i] in freq:
                min_vals.append(min_freq[i])
                max_vals.append(max_freq[i])
            else:
                min_vals.append(np.nan)
                max_vals.append(np.nan)

        freq_df[f'freq_int_{i}_min'] = min_vals
        freq_df[f'freq_int_{i}_max'] = max_vals

    return freq_df


def compute_correlations(base_dir, site, freq_df, xml_folder_name, unique_folder_name, ref_test_name, mean_file_name,
                         unique_flag=True, auto_dist_calc_flag=True, correlation_type='lcss',
                         dist_meas_df=None, loc_df_manual=None, global_constraint='sakoe_chiba',
                         eps=0.75, sakoe_chiba_radius=10, dist_range_list=None):
    """
    A function which evaluates the correlation of various spatially distributed HVSR curves at a site.

    Parameters:

    dist_range_list: str
        String of tuple list to evaluate different distance ranges that were used in the study.
    sakoe_chiba_radius: int
        Radius of warping window to allow a horizontal shift between different points in a curve. Note: only for 'lcss'
        and 'dtw'.
    eps: float
        Matching threshold used in 'lcss' correlation. Note: only for 'lcss'.
    global_constraint: str
        String indicating whether to use sakoe_chiba radius or itakura slope. Note: only for 'lcss' and 'dtw'.
    loc_df_manual: str
        Path where the location dataframe (.csv) is stored, showing the true locations of the test points. Note: only use
        if the auto flag is not working.
    dist_meas_df: str
        Path where the distance measured dataframe (.csv) is stored, showing the distances from the reference. Note:
        only use if the auto flag is not working.
    auto_dist_calc_flag: boolean
        Indicated whether to use .xml files to identify locations of test points or use a .csv file (False).
    unique_flag: boolean
        Indicates if the folder scheme is unique, meaning that more folders would need to be used to do computation.
        Use unique_folder_name if this is true.
    mean_file_name: str
        Indicates the filename used for the mean HVSR curve.
    ref_test_name: str
        Indicates the name of the reference test.
    unique_folder_name: str
        Indicates the unique path where files are stored.
    freq_df: dataframe
        The dataframe where the frequency interval information is stored.
    base_dir: str
        Indicates the base directory where all the tests are stored.
    site: str
        Indicates the site name where the tests for that site are stored.
    xml_folder_name: str
        Indicates the folder name where the xml files are relative to site and tests.
    correlation_type: str
        Indicates the type of correlation used in the analysis.

    return
        Dataframe indicating the correlation values, distances, and locations.

    """

    if auto_dist_calc_flag:
        dist = dist_from_vert_arr(base_dir, site, xml_folder_name)
    else:
        meas_dist = pd.read_csv(dist_meas_df)
        loc = pd.read_csv(loc_df_manual)
        loc.columns = ['site', 'site_name', 'tests', 'instrument_name', 'latitude', 'longitude', 'lat_mod', 'long_mod',
                       'comment']
        meas_dist.columns = ['site', 'tests', 'distance']
        loc.drop('site', axis=1, inplace=True)
        dist = meas_dist.merge(loc, on='tests')
        dist = dist[dist['site'].astype(str) == site]

    if dist_range_list is None:
        dist_range_list = [[0, 75], [75, 300], [300, 600], [600, 1000]]
    else:
        dist_range_list = json.loads(dist_range_list)

    if freq_df.empty:
        raise pd.errors.EmptyDataError('Frequency Dataframe is empty, lower amplitude threshold in peak algorithm.')

    num_peaks = freq_df.numPeaks.values[0]

    df = {}
    test_list = []
    corr_list = []
    dist_list = []
    fi_list = []
    avg_corr_list = []

    for fi in range(num_peaks):
        for min_dist, max_dist in dist_range_list:
            test_w_dist = dist.tests.loc[(dist.distance >= min_dist) & (dist.distance <= max_dist)]
            correlation_list = []

            for test in test_w_dist:
                peak_f_lower = freq_df[freq_df.tests == test].iloc[:, 3 + fi * 2].values[0]
                peak_f_upper = freq_df[freq_df.tests == test].iloc[:, 4 + fi * 2].values[0]

                if peak_f_lower == 'NA' or peak_f_upper == 'NA':
                    continue

                min_freq = peak_f_lower
                max_freq = peak_f_upper

                if unique_flag:
                    hvsr_df = pd.read_csv(
                        os.path.join(base_dir, site, test, unique_folder_name, mean_file_name),
                        header=None)
                    hvsr_ref_df = pd.read_csv(os.path.join(base_dir, site, ref_test_name,
                                                           unique_folder_name, mean_file_name),
                                              header=None)

                else:
                    hvsr_df = pd.read_csv(
                        os.path.join(base_dir, site, test, mean_file_name),
                        header=None)
                    hvsr_ref_df = pd.read_csv(
                        os.path.join(base_dir, site, ref_test_name, mean_file_name),
                        header=None)

                hvsr_ref_df = hvsr_ref_df[1:].astype(float)
                hvsr_df = hvsr_df[1:].astype(float)

                hvsr_mean_ref = hvsr_ref_df[1].loc[(hvsr_ref_df[0] >= min_freq) & (hvsr_ref_df[0] <= max_freq)].values
                hvsr_mean = hvsr_df[1].loc[(hvsr_df[0] >= min_freq) & (hvsr_df[0] <= max_freq)].values

                if len(hvsr_mean) == len(hvsr_mean_ref) and len(hvsr_mean) > 0:
                    if correlation_type == 'dtw':
                        corr = dtw(hvsr_mean_ref, hvsr_mean, global_constraint=global_constraint,
                                   sakoe_chiba_radius=sakoe_chiba_radius)
                        correlation_list.append(corr)
                    elif correlation_type == 'lcss':
                        corr = lcss(hvsr_mean_ref, hvsr_mean, eps=eps, global_constraint=global_constraint,
                                    sakoe_chiba_radius=sakoe_chiba_radius)
                        correlation_list.append(corr)
                    elif correlation_type == 'mae':
                        corr = mean_absolute_error(hvsr_mean_ref, hvsr_mean)
                        correlation_list.append(corr)
                    elif correlation_type == 'mse':
                        corr = mean_squared_error(hvsr_mean_ref, hvsr_mean)
                        correlation_list.append(corr)
                    elif correlation_type == 'pearson':
                        corr, _ = pearsonr(hvsr_mean_ref, hvsr_mean)
                        correlation_list.append(corr)
                    elif correlation_type == 'spearman':
                        corr, _ = spearmanr(hvsr_mean_ref, hvsr_mean)
                        correlation_list.append(corr)
                    elif correlation_type == 'euclidean':
                        corr = euclidean(hvsr_mean_ref, hvsr_mean)
                        correlation_list.append(corr)
                    elif correlation_type == 'sqeuc':
                        corr = sqeuclidean(hvsr_mean_ref, hvsr_mean)
                        correlation_list.append(corr)
                    elif correlation_type == 'braycurtis':
                        corr = braycurtis(hvsr_mean_ref, hvsr_mean)
                        correlation_list.append(corr)
                    elif correlation_type == 'canberra':
                        corr = canberra(hvsr_mean_ref, hvsr_mean)
                        correlation_list.append(corr)
                    elif correlation_type == 'chebyshev':
                        corr = chebyshev(hvsr_mean_ref, hvsr_mean)
                        correlation_list.append(corr)
                    elif correlation_type == 'cityblock':
                        corr = cityblock(hvsr_mean_ref, hvsr_mean)
                        correlation_list.append(corr)
                    elif correlation_type == 'correlation':
                        corr = correlation(hvsr_mean_ref, hvsr_mean)
                        correlation_list.append(corr)
                    elif correlation_type == 'cosine':
                        corr = cosine(hvsr_mean_ref, hvsr_mean)
                        correlation_list.append(corr)
                    elif correlation_type == 'jensenshannon':
                        corr = jensenshannon(hvsr_mean_ref, hvsr_mean)
                        correlation_list.append(corr)
                    elif correlation_type == 'minkowski':
                        corr = minkowski(hvsr_mean_ref, hvsr_mean)
                        correlation_list.append(corr)
                    elif correlation_type == 'dice':
                        corr = dice(hvsr_mean_ref, hvsr_mean)
                        correlation_list.append(corr)
                    elif correlation_type == 'hamming':
                        corr = hamming(hvsr_mean_ref, hvsr_mean)
                        correlation_list.append(corr)
                    elif correlation_type == 'jaccard':
                        corr = jaccard(hvsr_mean_ref, hvsr_mean)
                        correlation_list.append(corr)
                    elif correlation_type == 'kul':
                        corr = kulczynski1(hvsr_mean_ref, hvsr_mean)
                        correlation_list.append(corr)
                    elif correlation_type == 'roger':
                        corr = rogerstanimoto(hvsr_mean_ref, hvsr_mean)
                        correlation_list.append(corr)
                    elif correlation_type == 'russell':
                        corr = russellrao(hvsr_mean_ref, hvsr_mean)
                        correlation_list.append(corr)
                    elif correlation_type == 'sokalmichener':
                        corr = sokalmichener(hvsr_mean_ref, hvsr_mean)
                        correlation_list.append(corr)
                    elif correlation_type == 'sokalsneath':
                        corr = sokalsneath(hvsr_mean_ref, hvsr_mean)
                        correlation_list.append(corr)
                    elif correlation_type == 'yule':
                        corr = yule(hvsr_mean_ref, hvsr_mean)
                        correlation_list.append(corr)
                    else:
                        corr = 0
                        correlation_list.append(corr)
                else:
                    continue

                test_list.append(test)
                fi_list.append(fi)
                dist_list.append(min_dist)
                corr_list.append(corr)
                avg_corr_list.append(sum(correlation_list) / len(correlation_list) if correlation_list else 0)

    df['tests'] = test_list
    df['freq_interval'] = fi_list
    df['distance_bin'] = dist_list
    df['correlation_value'] = corr_list

    df_site = pd.DataFrame(df)

    df_all = dist.merge(df_site, on='tests')

    return df_all
