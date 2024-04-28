"use client";
import 'leaflet/dist/leaflet.css';
import { useState } from 'react';
import { MapContainer, TileLayer, GeoJSONProps } from 'react-leaflet';
import { geoJSON } from "leaflet";

interface GeoJSONData extends GeoJSONProps {
  type: string;
  generator: string;
  sequence: number[][];
  copyright: string;
  timestamp: string;
  features: Feature[];
}

interface Feature {
  type: "Feature";
  geometry: {
    type: string;
    coordinates: number[][];
  };
}

export default function MapComponent() {
  const [geojsonData, setGeojsonData] = useState<GeoJSONData>(
    {
      "type": "FeatureCollection",
      "generator": "overpass-turbo",
      "copyright": "The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.",
      "sequence": [
          [
              -37.2668079,
              -7.0136892
          ],
          [
              -37.2771612,
              -7.0181882
          ],
          [
              -37.2814152,
              -7.014979
          ],
          [
              -37.2823117,
              -7.0119349
          ],
          [
              -37.2888355,
              -7.010285
          ],
          [
              -37.2884224,
              -7.0202999
          ],
          [
              -37.2893867,
              -7.0204656
          ],
          [
              -37.2943367,
              -7.0285211
          ],
          [
              -37.2966716,
              -7.0398071
          ],
          [
              -37.2860849,
              -7.0487276
          ],
          [
              -37.2771956,
              -7.0504911
          ],
          [
              -37.2730525,
              -7.0533453
          ],
          [
              -37.2797134,
              -7.0260716
          ],
          [
              -37.2731948,
              -7.0245
          ],
          [
              -37.2522568,
              -7.0193296
          ],
          [
              -37.2437435,
              -7.0134822
          ],
          [
              -37.2919844,
              -6.992176
          ],
          [
              -37.3100129,
              -7.0342857
          ],
          [
              -37.2310111,
              -7.0845885
          ],
          [
              -37.3981134,
              -6.949261
          ],
          [
              -37.4307633,
              -6.9574402
          ]
      ],
      "features": [
          {
              "type": "Feature",
              "geometry": {
                  "type": "LineString",
                  "coordinates": [
                      [
                          -37.2668079,
                          -7.0136892
                      ],
                      [
                          -37.2673608,
                          -7.0137175
                      ],
                      [
                          -37.2680316,
                          -7.0137466
                      ],
                      [
                          -37.2686667,
                          -7.0137837
                      ],
                      [
                          -37.2695638,
                          -7.0138343
                      ],
                      [
                          -37.2703879,
                          -7.0138835
                      ],
                      [
                          -37.2704409,
                          -7.0138842
                      ],
                      [
                          -37.2714111,
                          -7.0139487
                      ],
                      [
                          -37.2724794,
                          -7.014006
                      ],
                      [
                          -37.2724405,
                          -7.0147374
                      ],
                      [
                          -37.2729789,
                          -7.014785
                      ],
                      [
                          -37.2732787,
                          -7.0148273
                      ],
                      [
                          -37.274011,
                          -7.0148997
                      ],
                      [
                          -37.2740196,
                          -7.0155308
                      ],
                      [
                          -37.2740213,
                          -7.0156451
                      ],
                      [
                          -37.2740431,
                          -7.0161703
                      ],
                      [
                          -37.2747418,
                          -7.0162608
                      ],
                      [
                          -37.2751375,
                          -7.0163167
                      ],
                      [
                          -37.2750798,
                          -7.0168279
                      ],
                      [
                          -37.2750798,
                          -7.0168705
                      ],
                      [
                          -37.2750818,
                          -7.0168949
                      ],
                      [
                          -37.2750868,
                          -7.0169111
                      ],
                      [
                          -37.2750964,
                          -7.0169265
                      ],
                      [
                          -37.2751142,
                          -7.0169369
                      ],
                      [
                          -37.2751348,
                          -7.0169423
                      ],
                      [
                          -37.2754662,
                          -7.0169894
                      ],
                      [
                          -37.2760134,
                          -7.0170567
                      ],
                      [
                          -37.2759676,
                          -7.0174235
                      ],
                      [
                          -37.2759669,
                          -7.0174608
                      ],
                      [
                          -37.2759743,
                          -7.0174927
                      ],
                      [
                          -37.2759884,
                          -7.0175167
                      ],
                      [
                          -37.2760233,
                          -7.017536
                      ],
                      [
                          -37.2760655,
                          -7.0175413
                      ],
                      [
                          -37.276559,
                          -7.0176052
                      ],
                      [
                          -37.2772109,
                          -7.0176867
                      ],
                      [
                          -37.2771612,
                          -7.0181882
                      ]
                ]
          }
        }
      ]
    }
  );

  return (
    <MapContainer className='w-[100vw] h-[50vh]'
      center={[-7.0303346, -37.290117]}
      zoom={13}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
    </MapContainer>
  );
}