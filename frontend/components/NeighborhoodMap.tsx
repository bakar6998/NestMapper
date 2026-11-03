'use client'

import { useEffect, useRef } from 'react'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

type NeighborhoodMapProps = {
  neighborhoods?: any[]
}

export default function NeighborhoodMap({
  neighborhoods = [],
}: NeighborhoodMapProps) {
  const mapContainer = useRef<HTMLDivElement | null>(null)
  const mapRef = useRef<mapboxgl.Map | null>(null)

  useEffect(() => {
    if (!mapContainer.current) return

    const token = process.env.NEXT_PUBLIC_MAPBOX_TOKEN

    if (!token) {
      console.error('Mapbox token is missing.')
      return
    }

    mapboxgl.accessToken = token

    const map = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/light-v11',
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

        const geojson = await response.json()

        map.addSource('neighborhoods', {
          type: 'geojson',
          data: geojson,
        })

        // Gray neighborhood fill
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

        const hoverPopup = new mapboxgl.Popup({
          closeButton: false,
          closeOnClick: false,
          offset: 10,
        })

        map.on(
          'mousemove',
          'neighborhood-fill',
          (event) => {
            map.getCanvas().style.cursor = 'pointer'

            const feature = event.features?.[0]

            if (!feature) return

            const properties =
              (feature.properties as Record<
                string,
                any
              >) || {}

            const neighborhoodName =
              properties.NTAName ||
              properties.ntaname ||
              properties.name ||
              properties.NTA2020 ||
              'NYC Neighborhood'

            hoverPopup
              .setLngLat(event.lngLat)
              .setHTML(
                `<div style="font-size:13px;font-weight:600;">
                  ${neighborhoodName}
                </div>`
              )
              .addTo(map)
          }
        )

        map.on(
          'mouseleave',
          'neighborhood-fill',
          () => {
            map.getCanvas().style.cursor = ''
            hoverPopup.remove()
          }
        )

        map.on(
          'click',
          'neighborhood-fill',
          (event) => {
            const feature = event.features?.[0]

            if (!feature) return

            const properties =
              (feature.properties as Record<
                string,
                any
              >) || {}

            const neighborhoodName =
              properties.NTAName ||
              properties.ntaname ||
              properties.name ||
              properties.NTA2020 ||
              'NYC Neighborhood'

            new mapboxgl.Popup()
              .setLngLat(event.lngLat)
              .setHTML(
                `
                <div style="padding:4px;">
                  <strong>${neighborhoodName}</strong>
                  <div style="font-size:12px;margin-top:3px;">
                    Click the neighborhood card below for more details.
                  </div>
                </div>
                `
              )
              .addTo(map)
          }
        )
      } catch (error) {
        console.error(
          'Failed to load neighborhood boundaries:',
          error
        )
      }
    })

    return () => {
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
        <div className="mb-1 font-semibold">
          Neighborhood Boundaries
        </div>

        <div className="flex items-center gap-2 text-muted-foreground">
          <span className="h-3 w-3 rounded-sm border border-white bg-gray-500" />
          NYC neighborhood
        </div>
      </div>
    </div>
  )
}