# This file is part of hvspatialpy, a Python package for evaluating
# spatial variability of a site utilizing spatially distributed HVSR.

# Copyright (c) 2024 Francisco Javier Ornelas (jornela1@g.ucla.edu)

"""Class definition of GUI for plotting correlations of spatial variability of HVSR."""

import os
import ipywidgets as widgets
from IPython.display import display, clear_output

from .pltspatial import update_correlations


class HVSpatialPYGui:
    """

    Class description of HVSpatialPYGUI

    A python graphical user interface (GUI) to evaluate the spatial variability of a site utilizing HVSR.

    Parameters:

    dist_range_list_widget: str
        String of tuple list to evaluate different distance ranges that were used in the study.
    sakoe_chiba_radius_widget: int
        Radius of warping window to allow a horizontal shift between different points in a curve. Note: only for 'lcss'
        and 'dtw'.
    eps_widget: float
        Matching threshold used in 'lcss' correlation. Note: only for 'lcss'.
    global_constraint_widget: str
        String indicating whether to use sakoe_chiba radius or itakura slope. Note: only for 'lcss' and 'dtw'.
    loc_df_manual_widget: str
        Path where the location dataframe (.csv) is stored, showing the true locations of the test points. Note: only use
        if the auto flag is not working.
    dist_meas_df_widget: str
        Path where the distance measured dataframe (.csv) is stored, showing the distances from the reference. Note:
        only use if the auto flag is not working.
    auto_dist_calc_flag_widget: boolean
        Indicated whether to use .xml files to identify locations of test points or use a .csv file (False).
    unique_flag_widget: boolean
        Indicates if the folder scheme is unique, meaning that more folders would need to be used to do computation.
        Use unique_folder_name if this is true.
    mean_file_name_widget: str
        Indicates the filename used for the mean HVSR curve.
    ref_test_name_widget: str
        Indicates the name of the reference test.
    unique_folder_name_widget: str
        Indicates the unique path where files are stored.
    freq_df_widget: dataframe
        The dataframe where the frequency interval information is stored.
    base_dir_widget: str
        Indicates the base directory where all the tests are stored.
    site_widget: str
        Indicates the site name where the tests for that site are stored.
    xml_folder_name_widget: str
        Indicates the folder name where the xml files are relative to site and tests.
    correlation_type_widget: str
        Indicates the type of correlation used in the analysis.

    return:
        The frequency, correlation dataframes and the figure used in the analysis.

    """

    def __init__(self):
        description_width = '50%'
        widget_width = '50%'

        self.base_dir_widget = widgets.Text(
            description='Base Directory:',
            description_width=description_width,
            value= \
                'C:/Users/Javier Ornelas/OneDrive/Documents/HVSRdata_Main/mHVSR Site Inv/VSPDB Data/CA Vertical Array Data/HVSRdata',
            layout=widgets.Layout(width='90%')
        )

        self.site_widget = widgets.Text(
            description='Site:',
            description_width=description_width,
            value='7',
            layout=widgets.Layout(width=widget_width)
        )

        self.xml_folder_name_widget = widgets.Text(
            description='XML Folder Name:',
            description_width=description_width,
            value='Raw_mseed_data',
            layout=widgets.Layout(width=widget_width)
        )

        self.unique_folder_name_widget = widgets.Text(
            description='Unique Folder Name:',
            description_width=description_width,
            value='Text_File_data/Raw_ascii_PEG_HH',
            layout=widgets.Layout(width=widget_width)
        )

        self.ref_test_name_widget = widgets.Text(
            description='Reference Test Name:',
            description_width=description_width,
            value='7.0.0',
            layout=widgets.Layout(width=widget_width)
        )

        self.mean_file_name_widget = widgets.Text(
            description='Mean File Name:',
            description_width=description_width,
            value='Test_hvsr_mean.csv',
            layout=widgets.Layout(width=widget_width)
        )

        self.unique_flag_widget = widgets.Checkbox(
            description='Unique Flag',
            description_width=description_width,
            value=True,
            layout=widgets.Layout(width=widget_width)
        )

        self.auto_dist_calc_flag_widget = widgets.Checkbox(
            description='Auto Distance Calculation Flag',
            description_width=description_width,
            value=True,
            layout=widgets.Layout(width=widget_width)
        )

        self.freq_trun_widget = widgets.FloatText(
            value=0.1,
            description='Freq. Truncated',
            description_width=description_width,
            layout=widgets.Layout(width=widget_width)
        )

        self.threshold_widget = widgets.FloatText(
            value=1.6,
            description='Amp. Threshold',
            description_width=description_width,
            layout=widgets.Layout(width=widget_width)
        )

        self.min_distance_widget = widgets.FloatText(
            value=1.0,
            description='Min Dist.',
            description_width=description_width,
            layout=widgets.Layout(width=widget_width)
        )

        self.correlation_type_widget = widgets.Dropdown(
            options=['lcss', 'dtw', 'pearson', 'spearman', 'mae', 'mse', 'euclidean', 'sqeuclidean', 'braycurtis',
                     'canberra', 'chebyshev', 'cityblock', 'correlation', 'cosine', 'jensenshannon', 'minkowski',
                     'dice', 'hamming', 'jaccard', 'kulczynski1', 'rogerstanimoto', 'russellrao', 'sokalmichener',
                     'sokalsneath', 'yule'],
            value='lcss',
            description='Corr. Type:',
            description_width=description_width,
            layout=widgets.Layout(width=widget_width)
        )

        self.global_constraint_widget = widgets.Dropdown(
            options=['sakoe_chiba', 'itakura'],
            value='sakoe_chiba',
            description='corr. global constraint:',
            description_width=description_width,
            layout=widgets.Layout(width=widget_width)
        )

        self.eps_widget = widgets.FloatText(
            value=0.75,
            description='matching thresh.:',
            description_width=description_width,
            layout=widgets.Layout(width=widget_width)
        )

        self.dist_range_list_widget = widgets.Text(
            description='dist range list:',
            description_width='50%',
            value='[[0, 75], [75, 300], [300, 600], [600, 1000]]',
            layout=widgets.Layout(width='90%')
        )

        self.frequency_interval_widget = widgets.IntText(
            value=0,
            description='Frequency Interval:',
            description_width=description_width,
            layout=widgets.Layout(width=widget_width)
        )

        self.sakoe_chiba_radius_widget = widgets.IntText(
            value=10,
            description='Sakoe_Chiba Radius:',
            description_width=description_width,
            layout=widgets.Layout(width=widget_width)
        )

        self.dist_meas_df_widget = widgets.Text(
            description='Distance Path:',
            description_width=description_width,
            value='C:/Users/Javier Ornelas/OneDrive/Documents/HVSRdata_Main/mHVSR Site Inv/VSPDB Data/CA Vertical Array Data - Afshari and Stewart/Site Peak Iden/Gaussian Pulse/Meta/site_ALL_distance_meas_from_vert_array.csv',
            layout=widgets.Layout(width='90%')
        )

        self.loc_df_manual_widget = widgets.Text(
            description='Location Path:',
            description_width=description_width,
            value='C:/Users/Javier Ornelas/OneDrive/Documents/HVSRdata_Main/mHVSR Site Inv/VSPDB Data/CA Vertical Array Data - Afshari and Stewart/Site Peak Iden/modified_Latitude_and_Longitude_CA_Vert_Array_spatial_study.csv',
            layout=widgets.Layout(width='90%')
        )

        self.save_dir_widget = widgets.Text(
            description='Save Directory:',
            description_width=description_width,
            value='C:/Users/Javier Ornelas/OneDrive/Documents/HVSRdata_Main/Outputs',
            layout=widgets.Layout(width='90%')
        )

        # Output widget to display results
        self.output_widget = widgets.Output()

        # Create a button widget
        self.button = widgets.Button(
            description="Run hvspatialpy GUI",
            layout=widgets.Layout(width='90%')
        )

        # Attach the button click event to the function
        self.button.on_click(self.on_button_click)

        # Layout widgets
        self.form_layout = widgets.VBox([
            widgets.HBox([self.base_dir_widget], layout=widgets.Layout(width='100%', margin='5px')),
            widgets.HBox([self.dist_meas_df_widget], layout=widgets.Layout(width='100%', margin='5px')),
            widgets.HBox([self.loc_df_manual_widget], layout=widgets.Layout(width='100%', margin='5px')),
            widgets.HBox([self.xml_folder_name_widget, self.unique_folder_name_widget],
                         layout=widgets.Layout(width='90%', margin='5px')),
            widgets.HBox([self.min_distance_widget, self.frequency_interval_widget],
                         layout=widgets.Layout(width='90%', margin='5px')),
            widgets.HBox([self.site_widget, self.ref_test_name_widget, self.mean_file_name_widget],
                         layout=widgets.Layout(width='90%', margin='5px')),
            widgets.HBox([self.freq_trun_widget, self.threshold_widget, self.correlation_type_widget],
                         layout=widgets.Layout(width='90%', margin='5px')),
            widgets.HBox([self.eps_widget, self.global_constraint_widget, self.sakoe_chiba_radius_widget],
                         layout=widgets.Layout(width='90%', margin='5px')),
            widgets.HBox([self.dist_range_list_widget], layout=widgets.Layout(width='100%', margin='5px')),
            widgets.HBox([self.unique_flag_widget, self.auto_dist_calc_flag_widget],
                         layout=widgets.Layout(width='90%', margin='5px')),
            widgets.HBox([self.save_dir_widget], layout=widgets.Layout(width='100%', margin='5px')),
            widgets.HBox([self.button], layout=widgets.Layout(width='100%', margin='5px'))
        ])

        display(self.form_layout, self.output_widget)

    def on_button_click(self, b):
        with self.output_widget:
            clear_output(wait=True)

            freq_int_df, correlation_df, figure = update_correlations(base_dir=self.base_dir_widget.value,
                                                                      site=self.site_widget.value,
                                                                      xml_folder_name=self.xml_folder_name_widget.value,
                                                                      unique_folder_name=self.unique_folder_name_widget.value,
                                                                      ref_test_name=self.ref_test_name_widget.value,
                                                                      mean_file_name=self.mean_file_name_widget.value,
                                                                      unique_flag=self.unique_flag_widget.value,
                                                                      auto_dist_calc_flag=self.auto_dist_calc_flag_widget.value,
                                                                      freq_trun=self.freq_trun_widget.value,
                                                                      dist_meas_df=self.dist_meas_df_widget.value,
                                                                      loc_df_manual=self.loc_df_manual_widget.value,
                                                                      correlation_type=self.correlation_type_widget.value,
                                                                      frequency_interval=self.frequency_interval_widget.value,
                                                                      threshold=self.threshold_widget.value,
                                                                      min_distance=self.min_distance_widget.value,
                                                                      global_constraint=self.global_constraint_widget.value,
                                                                      eps=self.eps_widget.value,
                                                                      sakoe_chiba_radius=self.sakoe_chiba_radius_widget.value,
                                                                      dist_range_list=self.dist_range_list_widget.value)

            save_dir = self.save_dir_widget.value
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            freq_int_df_path = os.path.join(save_dir, 'frequency_interval_df.csv')
            correlation_df_path = os.path.join(save_dir, 'correlation_df.csv')

            freq_int_df.to_csv(freq_int_df_path, index=False)
            correlation_df.to_csv(correlation_df_path, index=False)

            figdir = os.path.join(save_dir, 'spatial_figure.png')

            figure.savefig(figdir, dpi=500)
