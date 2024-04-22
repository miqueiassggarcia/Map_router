"use client";

import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet';

interface GeoJSONData extends GeoJSON.GeoJsonObject {
    "generator": string;
    "copyright": string;
    "sequence": number[][][];
    "feature": {
        "type": string;
        "geometry": {
            "type": string;
            "coordinates": number[][][];
        };
    }
}

const MapComponent: React.FC = () => {
  const [position, setPosition] = useState<[number, number]>([0, 0]);
  const [geojsonData, setGeojsonData] = useState<GeoJSONData>({
    "type": "LineString",
    "generator": "",
    "copyright": "",
    "sequence": [[], []],
    "feature": {
        "type": "",
        "geometry": {
            "type": "",
            "coordinates": [[], []],
        },
    }
  });

  useEffect(() => {
    // Fetch GeoJSON data from your API
    fetch('http://localhost:5000/routes')
      .then(response => response.json())
      .then(data => {
        console.log(data);
        setGeojsonData(data);
      })
      .catch(error => {
        console.error('Error fetching GeoJSON data:', error);
      });

    // Get user's current position
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const { latitude, longitude } = pos.coords;
          setPosition([latitude, longitude]);
        },
        (err) => {
          console.error(err);
        }
      );
    } else {
      console.error('Geolocation is not supported by this browser.');
    }
  }, []);

  return (
    <MapContainer center={[-7.0303346, -37.290117]} zoom={13}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="OpenStreetMap"
      />
      {geojsonData && <GeoJSON data={geojsonData} />}
    </MapContainer>
  );
};

export default MapComponent;