'use client'

import {
  useEffect,
  useRef,
  useState,
} from 'react'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

type NeighborhoodMapProps = {
  neighborhoods?: any[]
}

type ScoreLayer =
  | 'overall'
  | 'rent'
  | 'safety'
  | 'transit'
  | 'accessibility'

type GeoJsonFeature = {
  type: 'Feature'
  properties?: Record<string, any>
  geometry?: {
    type: string
    coordinates: any
  }
}

type GeoJsonCollection = {
  type: 'FeatureCollection'
  features: GeoJsonFeature[]
}

const scoreLayers: {
  key: ScoreLayer
  label: string
}[] = [
  {
    key: 'overall',
    label: 'Overall',
  },
  {
    key: 'rent',
    label: 'Rent',
  },
  {
    key: 'safety',
    label: 'Safety',
  },
  {
    key: 'transit',
    label: 'Transit',
  },
  {
    key: 'accessibility',
    label: 'Accessibility',
  },
]

function getFeatureName(
  feature: GeoJsonFeature
) {
  const properties =
    feature.properties || {}

  return (
    properties.NTAName ||
    properties.ntaname ||
    properties.name ||
    properties.NTA2020 ||
    ''
  )
}

function normalizeName(name: string) {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]/g, '')
}

function collectCoordinates(
  coordinates: any,
  points: number[][] = []
) {
  if (
    Array.isArray(coordinates) &&
    typeof coordinates[0] === 'number' &&
    typeof coordinates[1] === 'number'
  ) {
    points.push(coordinates)

    return points
  }

  if (Array.isArray(coordinates)) {
    coordinates.forEach((item) =>
      collectCoordinates(
        item,
        points
      )
    )
  }

  return points
}

function getFeatureCenter(
  feature: GeoJsonFeature
) {
  if (!feature.geometry?.coordinates) {
    return null
  }

  const points = collectCoordinates(
    feature.geometry.coordinates
  )

  if (points.length === 0) {
    return null
  }

  let minLng = Infinity
  let maxLng = -Infinity
  let minLat = Infinity
  let maxLat = -Infinity

  points.forEach(([lng, lat]) => {
    minLng = Math.min(
      minLng,
      lng
    )

    maxLng = Math.max(
      maxLng,
      lng
    )

    minLat = Math.min(
      minLat,
      lat
    )

    maxLat = Math.max(
      maxLat,
      lat
    )
  })

  return {
    lng:
      (minLng + maxLng) / 2,

    lat:
      (minLat + maxLat) / 2,
  }
}

function getNeighborhoodScore(
  neighborhood: any,
  layer: ScoreLayer
) {
  const scores =
    neighborhood?.scores || {}

  if (layer === 'rent') {
    return Number(
      scores.rent_score ??
        scores.affordability_score ??
        neighborhood.rent_score ??
        neighborhood.affordability_score ??
        0
    )
  }

  if (layer === 'safety') {
    return Number(
      scores.safety_score ??
        neighborhood.safety_score ??
        0
    )
  }

  if (layer === 'transit') {
    return Number(
      scores.transit_score ??
        neighborhood.transit_score ??
        0
    )
  }

  if (
    layer ===
    'accessibility'
  ) {
    return Number(
      scores.accessibility_score ??
        neighborhood.accessibility_score ??
        0
    )
  }

  const values = [
    Number(
      scores.affordability_score ??
        neighborhood.affordability_score
    ),
    Number(
      scores.transit_score ??
        neighborhood.transit_score
    ),
    Number(
      scores.safety_score ??
        neighborhood.safety_score
    ),
    Number(
      scores.family_score ??
        neighborhood.family_score
    ),
    Number(
      scores.accessibility_score ??
        neighborhood.accessibility_score
    ),
    Number(
      scores.convenience_score ??
        neighborhood.convenience_score
    ),
  ].filter(
    (value) =>
      Number.isFinite(value) &&
      value > 0
  )

  if (values.length === 0) {
    return 0
  }

  return (
    values.reduce(
      (sum, value) =>
        sum + value,
      0
    ) / values.length
  )
}

function getScoreColor(
  score: number
) {
  if (score <= 0) {
    return '#6b7280'
  }

  if (score < 4) {
    return '#ef4444'
  }

  if (score < 6) {
    return '#f59e0b'
  }

  if (score < 8) {
    return '#22c55e'
  }

  return '#059669'
}

export default function NeighborhoodMap({
  neighborhoods = [],
}: NeighborhoodMapProps) {
  const mapContainer =
    useRef<HTMLDivElement | null>(
      null
    )

  const mapRef =
    useRef<mapboxgl.Map | null>(
      null
    )

  const geojsonRef =
    useRef<GeoJsonCollection | null>(
      null
    )

  const markersRef =
    useRef<mapboxgl.Marker[]>(
      []
    )

  const neighborhoodsRef =
    useRef<any[]>(
      neighborhoods
    )

  const [
    selectedLayer,
    setSelectedLayer,
  ] =
    useState<ScoreLayer>(
      'overall'
    )

  const [
    minimumScore,
    setMinimumScore,
  ] = useState(0)

  const selectedLayerRef =
    useRef<ScoreLayer>(
      selectedLayer
    )

  const minimumScoreRef =
    useRef(minimumScore)

  useEffect(() => {
    selectedLayerRef.current =
      selectedLayer

    updateMapScores()
  }, [selectedLayer])

  useEffect(() => {
    minimumScoreRef.current =
      minimumScore

    updateMapScores()
  }, [minimumScore])

  useEffect(() => {
    neighborhoodsRef.current =
      neighborhoods

    const map =
      mapRef.current

    if (
      map &&
      geojsonRef.current &&
      map.loaded()
    ) {
      addNeighborhoodMarkers(
        map,
        geojsonRef.current,
        neighborhoodsRef.current
      )

      updateMapScores()
    }
  }, [neighborhoods])

  function clearMarkers() {
    markersRef.current.forEach(
      (marker) =>
        marker.remove()
    )

    markersRef.current = []
  }

  function buildScoreGeoJson() {
    const original =
      geojsonRef.current

    if (!original) {
      return null
    }

    const layer =
      selectedLayerRef.current

    const minScore =
      minimumScoreRef.current

    const updatedFeatures =
      original.features.map(
        (feature) => {
          const featureName =
            getFeatureName(
              feature
            )

          const neighborhood =
            neighborhoodsRef.current.find(
              (item) =>
                normalizeName(
                  item?.name || ''
                ) ===
                normalizeName(
                  featureName
                )
            )

          const score =
            neighborhood
              ? getNeighborhoodScore(
                  neighborhood,
                  layer
                )
              : 0

          const visible =
            score === 0 ||
            score >= minScore

          return {
            ...feature,

            properties: {
              ...feature.properties,

              nestMapperScore:
                score,

              nestMapperColor:
                visible
                  ? getScoreColor(
                      score
                    )
                  : '#d1d5db',

              nestMapperOpacity:
                visible
                  ? score > 0
                    ? 0.7
                    : 0.55
                  : 0.15,
            },
          }
        }
      )

    return {
      ...original,

      features:
        updatedFeatures,
    }
  }

  function updateMapScores() {
    const map =
      mapRef.current

    if (
      !map ||
      !geojsonRef.current
    ) {
      return
    }

    const source =
      map.getSource(
        'neighborhoods'
      ) as
        | mapboxgl.GeoJSONSource
        | undefined

    if (!source) {
      return
    }

    const updated =
      buildScoreGeoJson()

    if (!updated) return

    source.setData(
      updated as any
    )

    if (
      map.getLayer(
        'neighborhood-fill'
      )
    ) {
      map.setPaintProperty(
        'neighborhood-fill',
        'fill-color',
        [
          'get',
          'nestMapperColor',
        ]
      )

      map.setPaintProperty(
        'neighborhood-fill',
        'fill-opacity',
        [
          'get',
          'nestMapperOpacity',
        ]
      )
    }
  }

  function addNeighborhoodMarkers(
    map: mapboxgl.Map,
    geojson: GeoJsonCollection,
    neighborhoodList: any[]
  ) {
    clearMarkers()

    if (
      !Array.isArray(
        neighborhoodList
      )
    ) {
      return
    }

    neighborhoodList.forEach(
      (neighborhood) => {
        const neighborhoodName =
          neighborhood?.name ||
          ''

        if (!neighborhoodName) {
          return
        }

        const matchingFeature =
          geojson.features.find(
            (feature) => {
              const featureName =
                getFeatureName(
                  feature
                )

              return (
                normalizeName(
                  featureName
                ) ===
                normalizeName(
                  neighborhoodName
                )
              )
            }
          )

        if (!matchingFeature) {
          return
        }

        const center =
          getFeatureCenter(
            matchingFeature
          )

        if (!center) return

        const score =
          getNeighborhoodScore(
            neighborhood,
            selectedLayerRef.current
          )

        const popup =
          new mapboxgl.Popup({
            offset: 20,
          }).setHTML(`
            <div style="padding:4px;">
              <strong>
                ${neighborhoodName}
              </strong>

              <div
                style="
                  font-size:12px;
                  margin-top:4px;
                "
              >
                ${
                  neighborhood.borough ||
                  'New York City'
                }
              </div>

              ${
                score > 0
                  ? `
                    <div
                      style="
                        font-size:12px;
                        margin-top:4px;
                      "
                    >
                      Score:
                      ${score.toFixed(1)}/10
                    </div>
                  `
                  : ''
              }

              ${
                neighborhood.rent
                  ?.one_bedroom
                  ? `
                    <div
                      style="
                        font-size:12px;
                        margin-top:4px;
                      "
                    >
                      1BR Rent:
                      $${Number(
                        neighborhood
                          .rent
                          .one_bedroom
                      ).toLocaleString()}
                    </div>
                  `
                  : ''
              }
            </div>
          `)

        const marker =
          new mapboxgl.Marker({
            color:
              score > 0
                ? getScoreColor(
                    score
                  )
                : '#2563eb',
          })
            .setLngLat([
              center.lng,
              center.lat,
            ])
            .setPopup(
              popup
            )
            .addTo(map)

        markersRef.current.push(
          marker
        )
      }
    )
  }

  useEffect(() => {
    if (
      !mapContainer.current
    ) {
      return
    }

    const token =
      process.env
        .NEXT_PUBLIC_MAPBOX_TOKEN

    if (!token) {
      console.error(
        'Mapbox token is missing.'
      )

      return
    }

    mapboxgl.accessToken =
      token

    const map =
      new mapboxgl.Map({
        container:
          mapContainer.current,

        style:
          'mapbox://styles/mapbox/light-v11',

        center: [
          -73.98,
          40.72,
        ],

        zoom: 9.5,
      })

    mapRef.current = map

    map.addControl(
      new mapboxgl.NavigationControl(),
      'top-right'
    )

    map.on(
      'load',
      async () => {
        try {
          const response =
            await fetch(
              '/nyc-neighborhoods.geojson'
            )

          const geojson =
            (await response.json()) as GeoJsonCollection

          geojsonRef.current =
            geojson

          const initialData = {
            ...geojson,

            features:
              geojson.features.map(
                (feature) => ({
                  ...feature,

                  properties: {
                    ...feature.properties,

                    nestMapperScore:
                      0,

                    nestMapperColor:
                      '#6b7280',

                    nestMapperOpacity:
                      0.6,
                  },
                })
              ),
          }

          map.addSource(
            'neighborhoods',
            {
              type: 'geojson',

              data:
                initialData as any,
            }
          )

          map.addLayer({
            id:
              'neighborhood-fill',

            type: 'fill',

            source:
              'neighborhoods',

            paint: {
              'fill-color': [
                'get',
                'nestMapperColor',
              ],

              'fill-opacity': [
                'get',
                'nestMapperOpacity',
              ],
            },
          })

          map.addLayer({
            id:
              'neighborhood-outline',

            type: 'line',

            source:
              'neighborhoods',

            paint: {
              'line-color':
                '#ffffff',

              'line-width':
                1.5,

              'line-opacity':
                0.95,
            },
          })

          const hoverPopup =
            new mapboxgl.Popup({
              closeButton:
                false,

              closeOnClick:
                false,

              offset: 10,
            })

          map.on(
            'mousemove',
            'neighborhood-fill',
            (event) => {
              map
                .getCanvas()
                .style
                .cursor =
                'pointer'

              const feature =
                event
                  .features?.[0] as
                  | GeoJsonFeature
                  | undefined

              if (!feature) {
                return
              }

              const neighborhoodName =
                getFeatureName(
                  feature
                ) ||
                'NYC Neighborhood'

              const score =
                Number(
                  feature
                    .properties
                    ?.nestMapperScore
                ) || 0

              hoverPopup
                .setLngLat(
                  event.lngLat
                )
                .setHTML(`
                  <div
                    style="
                      font-size:13px;
                      font-weight:600;
                    "
                  >
                    ${neighborhoodName}
                  </div>

                  ${
                    score > 0
                      ? `
                        <div
                          style="
                            font-size:12px;
                            margin-top:3px;
                          "
                        >
                          Score:
                          ${score.toFixed(
                            1
                          )}/10
                        </div>
                      `
                      : ''
                  }
                `)
                .addTo(map)
            }
          )

          map.on(
            'mouseleave',
            'neighborhood-fill',
            () => {
              map
                .getCanvas()
                .style
                .cursor =
                ''

              hoverPopup.remove()
            }
          )

          map.on(
            'click',
            'neighborhood-fill',
            (event) => {
              const feature =
                event
                  .features?.[0] as
                  | GeoJsonFeature
                  | undefined

              if (!feature) {
                return
              }

              const neighborhoodName =
                getFeatureName(
                  feature
                ) ||
                'NYC Neighborhood'

              const score =
                Number(
                  feature
                    .properties
                    ?.nestMapperScore
                ) || 0

              new mapboxgl.Popup()
                .setLngLat(
                  event.lngLat
                )
                .setHTML(`
                  <div style="padding:4px;">
                    <strong>
                      ${neighborhoodName}
                    </strong>

                    ${
                      score > 0
                        ? `
                          <div
                            style="
                              font-size:12px;
                              margin-top:4px;
                            "
                          >
                            ${
                              selectedLayerRef
                                .current
                            } score:
                            ${score.toFixed(
                              1
                            )}/10
                          </div>
                        `
                        : `
                          <div
                            style="
                              font-size:12px;
                              margin-top:4px;
                            "
                          >
                            Score data will appear when the backend is connected.
                          </div>
                        `
                    }
                  </div>
                `)
                .addTo(
                  map
                )
            }
          )

          addNeighborhoodMarkers(
            map,
            geojson,
            neighborhoodsRef.current
          )

          updateMapScores()
        } catch (error) {
          console.error(
            'Failed to load neighborhood boundaries:',
            error
          )
        }
      }
    )

    return () => {
      clearMarkers()

      map.remove()

      mapRef.current = null
    }
  }, [])

  return (
    <div className="overflow-hidden rounded-2xl border bg-muted">
      <div className="border-b bg-background p-4">
        <div className="flex flex-col gap-4">
          <div>
            <p className="text-sm font-semibold">
              Map Score Layer
            </p>

            <p className="mt-1 text-xs text-muted-foreground">
              Change the map based on different neighborhood scores.
            </p>
          </div>

          <div className="flex flex-wrap gap-2">
            {scoreLayers.map(
              (layer) => (
                <button
                  key={layer.key}
                  type="button"
                  onClick={() =>
                    setSelectedLayer(
                      layer.key
                    )
                  }
                  className={`rounded-full border px-3 py-1.5 text-xs font-semibold transition ${
                    selectedLayer ===
                    layer.key
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-background hover:bg-muted'
                  }`}
                >
                  {layer.label}
                </button>
              )
            )}
          </div>

          <div>
            <div className="mb-2 flex items-center justify-between text-xs">
              <span className="font-medium">
                Minimum score
              </span>

              <strong>
                {minimumScore}/10
              </strong>
            </div>

            <input
              type="range"
              min="0"
              max="10"
              step="1"
              value={
                minimumScore
              }
              onChange={(e) =>
                setMinimumScore(
                  Number(
                    e.target
                      .value
                  )
                )
              }
              className="w-full"
              aria-label="Minimum neighborhood score"
            />
          </div>
        </div>
      </div>

      <div className="relative">
        <div
          ref={mapContainer}
          className="h-[500px] w-full"
        />

        <div className="absolute bottom-4 left-4 z-10 rounded-lg border bg-background/95 px-3 py-2 text-xs shadow-sm">
          <div className="mb-2 font-semibold">
            Score Legend
          </div>

          <div className="space-y-1 text-muted-foreground">
            <div className="flex items-center gap-2">
              <span className="h-3 w-3 rounded-sm bg-gray-500" />
              No score data
            </div>

            <div className="flex items-center gap-2">
              <span className="h-3 w-3 rounded-sm bg-red-500" />
              Low score
            </div>

            <div className="flex items-center gap-2">
              <span className="h-3 w-3 rounded-sm bg-amber-500" />
              Medium score
            </div>

            <div className="flex items-center gap-2">
              <span className="h-3 w-3 rounded-sm bg-green-500" />
              Good score
            </div>

            <div className="flex items-center gap-2">
              <span className="h-3 w-3 rounded-sm bg-emerald-600" />
              High score
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}