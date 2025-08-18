
"""
This script processes functional imaging data from six z-planes
of a larval zebrafish brain, computes ΔF/F (percent change in fluorescence)
for four visual stimuli (left/rightward random dots and sine gratings),
and saves the trial-averaged and trial-resolved responses into an HDF5 file.

For each neuron, it stores:
- Average ΔF/F traces per stimulus
- Trial-by-trial ΔF/F responses
- Original and ANTs-registered unit centroid coordinates (with z-plane)

Output:
A structured HDF5 file where each neuron is saved under its own group.

Author: Jonathan Boulanger-Weill
Project: Fish1.5 dataset
"""

import numpy as np
import h5py

# Initialize a neuron counter
neuron_counter = 0

# Data was stored 
container_functional_hdf5 = h5py.File("/Users/jonathanboulanger-weill/Code/fish1.5_scripts/data/fish1.5_functional_data.hdf5", "r", libver='latest', swmr=True)
    
# Create the HDF5 file
with h5py.File("/Users/jonathanboulanger-weill/Code/fish1.5_scripts/data/fish1.5_functional_data.h5", "w") as hdf_file:
    for z_plane in range(6):

        segmentation_hdf5 = container_functional_hdf5[f"{z_plane}/manual_segmentation"]
        number_of_units = segmentation_hdf5.attrs["number_of_units"]
        dt = segmentation_hdf5["stimulus_aligned_dynamics"].attrs["dt"]

        print(f"Processing z_plane {z_plane}, number of units: {number_of_units}")

        # Load trial-wise raw fluorescence data for each stimulus
        F_left_dots  = np.array(segmentation_hdf5["stimulus_aligned_dynamics/0/F"])
        F_right_dots = np.array(segmentation_hdf5["stimulus_aligned_dynamics/1/F"])
        F_left_sine  = np.array(segmentation_hdf5["stimulus_aligned_dynamics/2/F"])
        F_right_sine = np.array(segmentation_hdf5["stimulus_aligned_dynamics/3/F"])

        # Compute ΔF/F for each stimulus
        F0_left_dots  = np.nanmean(F_left_dots[:, :, int(10 / dt):int(20 / dt)], axis=2, keepdims=True)
        F0_right_dots = np.nanmean(F_right_dots[:, :, int(10 / dt):int(20 / dt)], axis=2, keepdims=True)
        F0_left_sine  = np.nanmean(F_left_sine[:, :, int(10 / dt):int(20 / dt)], axis=2, keepdims=True)
        F0_right_sine = np.nanmean(F_right_sine[:, :, int(10 / dt):int(20 / dt)], axis=2, keepdims=True)

        df_F_left_dots  = 100 * (F_left_dots - F0_left_dots) / F0_left_dots
        df_F_right_dots = 100 * (F_right_dots - F0_right_dots) / F0_right_dots
        df_F_left_sine  = 100 * (F_left_sine - F0_left_sine) / F0_left_sine
        df_F_right_sine = 100 * (F_right_sine - F0_right_sine) / F0_right_sine

        # Load centroids
        unit_centroids = np.array(segmentation_hdf5["unit_centroids"])
        unit_centroids_ants_registered = np.array(segmentation_hdf5["unit_centroids_ants_registered"])

        for neuron_idx in range(number_of_units):
            neuron_counter += 1

            # Trial data for each stimulus
            df_left_dots  = df_F_left_dots[:, neuron_idx, :]
            df_right_dots = df_F_right_dots[:, neuron_idx, :]
            df_left_sine  = df_F_left_sine[:, neuron_idx, :]
            df_right_sine = df_F_right_sine[:, neuron_idx, :]

            # Average responses
            avg_left_dots  = np.nanmean(df_left_dots, axis=0)
            avg_right_dots = np.nanmean(df_right_dots, axis=0)
            avg_left_sine  = np.nanmean(df_left_sine, axis=0)
            avg_right_sine = np.nanmean(df_right_sine, axis=0)

            # Create group per neuron
            neuron_group = hdf_file.create_group(f"neuron_{neuron_counter}")

            # Store averaged responses
            neuron_group.create_dataset("average_dff_left_dots", data=avg_left_dots)
            neuron_group.create_dataset("average_dff_right_dots", data=avg_right_dots)
            neuron_group.create_dataset("average_dff_left_sine", data=avg_left_sine)
            neuron_group.create_dataset("average_dff_right_sine", data=avg_right_sine)

            # Store trial-by-trial ΔF/F
            neuron_group.create_dataset("dff_trials_left_dots", data=df_left_dots)
            neuron_group.create_dataset("dff_trials_right_dots", data=df_right_dots)
            neuron_group.create_dataset("dff_trials_left_sine", data=df_left_sine)
            neuron_group.create_dataset("dff_trials_right_sine", data=df_right_sine)

            # Store centroid positions
            centroid = unit_centroids[neuron_idx]
            centroid_ants = unit_centroids_ants_registered[neuron_idx]
            neuron_group.create_dataset("unit_centroid", data=np.append(centroid, z_plane))
            neuron_group.create_dataset("unit_centroid_ants_registered", data=np.append(centroid_ants, z_plane))

print(f"Total neurons processed: {neuron_counter}")