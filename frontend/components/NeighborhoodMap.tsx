'use client'

import { useEffect, useRef } from 'react'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

type NeighborhoodMapProps = {
  neighborhoods?: any[]
}

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

function getFeatureName(feature: GeoJsonFeature) {
  const properties = feature.properties || {}

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
      collectCoordinates(item, points)
    )
  }

  return points
}

function getFeatureCenter(feature: GeoJsonFeature) {
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
    minLng = Math.min(minLng, lng)
    maxLng = Math.max(maxLng, lng)
    minLat = Math.min(minLat, lat)
    maxLat = Math.max(maxLat, lat)
  })

  return {
    lng: (minLng + maxLng) / 2,
    lat: (minLat + maxLat) / 2,
  }
}

export default function NeighborhoodMap({
  neighborhoods = [],
}: NeighborhoodMapProps) {
  const mapContainer =
    useRef<HTMLDivElement | null>(null)

  const mapRef =
    useRef<mapboxgl.Map | null>(null)

  const geojsonRef =
    useRef<GeoJsonCollection | null>(null)

  const markersRef =
    useRef<mapboxgl.Marker[]>([])

  const neighborhoodsRef =
    useRef<any[]>(neighborhoods)

  useEffect(() => {
    neighborhoodsRef.current = neighborhoods

    const map = mapRef.current

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
    }
  }, [neighborhoods])

  function clearMarkers() {
    markersRef.current.forEach((marker) =>
      marker.remove()
    )

    markersRef.current = []
  }

  function addNeighborhoodMarkers(
    map: mapboxgl.Map,
    geojson: GeoJsonCollection,
    neighborhoodList: any[]
  ) {
    clearMarkers()

    if (!Array.isArray(neighborhoodList)) {
      return
    }

    neighborhoodList.forEach((neighborhood) => {
      const neighborhoodName =
        neighborhood?.name || ''

      if (!neighborhoodName) return

      const matchingFeature =
        geojson.features.find((feature) => {
          const featureName =
            getFeatureName(feature)

          return (
            normalizeName(featureName) ===
            normalizeName(neighborhoodName)
          )
        })

      if (!matchingFeature) {
        return
      }

      const center =
        getFeatureCenter(matchingFeature)

      if (!center) return

      const popup = new mapboxgl.Popup({
        offset: 20,
      }).setHTML(`
        <div style="padding:4px;">
          <strong>${neighborhoodName}</strong>

          <div
            style="
              font-size:12px;
              margin-top:4px;
            "
          >
            ${neighborhood.borough || 'New York City'}
          </div>

          ${
            neighborhood.rent?.one_bedroom
              ? `
                <div
                  style="
                    font-size:12px;
                    margin-top:4px;
                  "
                >
                  1BR Rent:
                  $${Number(
                    neighborhood.rent.one_bedroom
                  ).toLocaleString()}
                </div>
              `
              : ''
          }
        </div>
      `)

      const marker =
        new mapboxgl.Marker({
          color: '#2563eb',
        })
          .setLngLat([
            center.lng,
            center.lat,
          ])
          .setPopup(popup)
          .addTo(map)

      markersRef.current.push(marker)
    })
  }

  useEffect(() => {
    if (!mapContainer.current) return

    const token =
      process.env.NEXT_PUBLIC_MAPBOX_TOKEN

    if (!token) {
      console.error(
        'Mapbox token is missing.'
      )
      return
    }

    mapboxgl.accessToken = token

    const map = new mapboxgl.Map({
      container: mapContainer.current,
      style:
        'mapbox://styles/mapbox/light-v11',
      center: [-73.98, 40.72],
      zoom: 9.5,
    })

    mapRef.current = map

    map.addControl(
      new mapboxgl.NavigationControl(),
      'top-right'
    )

    map.on('load', async () => {
      try {
        const response = await fetch(
          '/nyc-neighborhoods.geojson'
        )

        const geojson =
          (await response.json()) as GeoJsonCollection

        geojsonRef.current = geojson

        map.addSource('neighborhoods', {
          type: 'geojson',
          data: geojson as any,
        })

        // Gray neighborhood polygons
        map.addLayer({
          id: 'neighborhood-fill',
          type: 'fill',
          source: 'neighborhoods',
          paint: {
            'fill-color': '#6b7280',
            'fill-opacity': 0.6,
          },
        })

        // White neighborhood boundary lines
        map.addLayer({
          id: 'neighborhood-outline',
          type: 'line',
          source: 'neighborhoods',
          paint: {
            'line-color': '#ffffff',
            'line-width': 1.5,
            'line-opacity': 0.95,
          },
        })

        const hoverPopup =
          new mapboxgl.Popup({
            closeButton: false,
            closeOnClick: false,
            offset: 10,
          })

        map.on(
          'mousemove',
          'neighborhood-fill',
          (event) => {
            map.getCanvas().style.cursor =
              'pointer'

            const feature =
              event.features?.[0] as
                | GeoJsonFeature
                | undefined

            if (!feature) return

            const neighborhoodName =
              getFeatureName(feature) ||
              'NYC Neighborhood'

            hoverPopup
              .setLngLat(event.lngLat)
              .setHTML(`
                <div
                  style="
                    font-size:13px;
                    font-weight:600;
                  "
                >
                  ${neighborhoodName}
                </div>
              `)
              .addTo(map)
          }
        )

        map.on(
          'mouseleave',
          'neighborhood-fill',
          () => {
            map.getCanvas().style.cursor =
              ''

            hoverPopup.remove()
          }
        )

        map.on(
          'click',
          'neighborhood-fill',
          (event) => {
            const feature =
              event.features?.[0] as
                | GeoJsonFeature
                | undefined

            if (!feature) return

            const neighborhoodName =
              getFeatureName(feature) ||
              'NYC Neighborhood'

            new mapboxgl.Popup()
              .setLngLat(event.lngLat)
              .setHTML(`
                <div style="padding:4px;">
                  <strong>
                    ${neighborhoodName}
                  </strong>

                  <div
                    style="
                      font-size:12px;
                      margin-top:3px;
                    "
                  >
                    Click a marker or neighborhood
                    card for more details.
                  </div>
                </div>
              `)
              .addTo(map)
          }
        )

        // Add the neighborhood pins
        addNeighborhoodMarkers(
          map,
          geojson,
          neighborhoodsRef.current
        )
      } catch (error) {
        console.error(
          'Failed to load neighborhood boundaries:',
          error
        )
      }
    })

    return () => {
      clearMarkers()

      map.remove()
      mapRef.current = null
    }
  }, [])

  return (
    <div className="relative overflow-hidden rounded-2xl border bg-muted">
      <div
        ref={mapContainer}
        className="h-[500px] w-full"
      />

      <div className="absolute bottom-4 left-4 z-10 rounded-lg border bg-background/95 px-3 py-2 text-xs shadow-sm">
        <div className="mb-2 font-semibold">
          Map Legend
        </div>

        <div className="flex items-center gap-2 text-muted-foreground">
          <span className="h-3 w-3 rounded-sm border border-white bg-gray-500" />
          Neighborhood boundary
        </div>

        <div className="mt-1 flex items-center gap-2 text-muted-foreground">
          <span className="h-3 w-3 rounded-full bg-blue-600" />
          Neighborhood marker
        </div>
      </div>
    </div>
  )
}