import geopandas as gpd
import os
import pandas as pd
from glob import glob
from tqdm import tqdm

def process_all_geojson_to_single_csv(file_paths: list[str], output_csv_path: str):
    """
    Reads a list of GeoDataFrame files, gets a representative point for each
    polygon in each file, and saves the combined information to a single CSV file.

    Args:
        file_paths: A list of paths to the GeoJSON files.
        output_csv_path: The path to save the final unified CSV file.
    """
    # This list will hold all the data from all the files
    all_points_data = []

    # Iterate over each file path provided
    for file_path in tqdm(file_paths):
        try:
            # Read the GeoDataFrame from the specified file path
            gdf = gpd.read_file(file_path)

            print(f'Processing {os.path.basename(file_path)}... ({len(gdf)} rows)')

            # Skip if the GeoDataFrame is empty
            if gdf.empty:
                print(f"Warning: {os.path.basename(file_path)} is empty. Skipping.")
                continue

            for index, row in gdf.iterrows():
                polygon_geometry = row.geometry

                # Find a representative point within the polygon.
                # This point is guaranteed to be within the polygon.
                representative_point = polygon_geometry.representative_point()

                # Append the required data to our main list
                all_points_data.append({
                    'filename': os.path.basename(file_path),
                    'distrito': row['distrito'],
                    'cd_indice_vulnerabilidade_social': row['cd_indice_vulnerabilidade_social'],
                    'latitude': representative_point.y,
                    'longitude': representative_point.x
                })

        except Exception as e:
            print(f"An error occurred while processing {file_path}: {e}")

    # After processing all files, check if we have any data
    if not all_points_data:
        print("No data was collected from the files. CSV will not be created.")
        return

    # Create a single pandas DataFrame from our list of all collected data
    final_df = pd.DataFrame(all_points_data)

    # Save the unified DataFrame to a single CSV file
    final_df.to_csv(output_csv_path, index=False)
    print(f"\nProcessing complete. All data saved to '{output_csv_path}'")
    print(f"Total points collected: {len(final_df)}")


dfs = glob('samples/*')
output_csv_path = 'unified_points.csv'

process_all_geojson_to_single_csv(dfs, output_csv_path)