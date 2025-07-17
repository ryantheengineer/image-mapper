# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 10:21:52 2025

@author: Ryan.Larson
"""

import os
import exifread
import folium

def get_decimal_from_dms(dms, ref):
    degrees = float(dms[0].num) / dms[0].den
    minutes = float(dms[1].num) / dms[1].den
    seconds = float(dms[2].num) / dms[2].den

    decimal = degrees + minutes / 60 + seconds / 3600
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

def extract_gps_from_image(image_path):
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f)

    try:
        gps_lat = tags['GPS GPSLatitude']
        gps_lat_ref = tags['GPS GPSLatitudeRef'].printable
        gps_lon = tags['GPS GPSLongitude']
        gps_lon_ref = tags['GPS GPSLongitudeRef'].printable

        lat = get_decimal_from_dms(gps_lat.values, gps_lat_ref)
        lon = get_decimal_from_dms(gps_lon.values, gps_lon_ref)
        return lat, lon
    except KeyError:
        return None

def collect_gps_coords_from_folder(folder_path):
    coords = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            path = os.path.join(folder_path, filename)
            result = extract_gps_from_image(path)
            if result:
                coords.append((filename, result[0], result[1]))
    return coords

def display_map_with_points(coords, output_html='map.html'):
    if not coords:
        print("No GPS data found.")
        return

    # # Center map on first point
    # m = folium.Map(location=[coords[0][1], coords[0][2]], zoom_start=12)
    
    m = folium.Map(location=[0, 0], zoom_start=2)

    for name, lat, lon in coords:
        folium.Marker([lat, lon], popup=name).add_to(m)
        
    bounds = [[lat, lon] for _, lat, lon in coords]
    m.fit_bounds(bounds)

    m.save(output_html)
    print(f"Map saved to {output_html}")

if __name__ == '__main__':
    folder = 'C:/Users/Ryan.Larson.ROCKWELLINC/github/image-mapper/images'
    coords = collect_gps_coords_from_folder(folder)
    display_map_with_points(coords)
