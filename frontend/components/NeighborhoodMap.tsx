'use client'

import { useEffect, useRef } from 'react'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

type Neighborhood = {
  id: number
  name: string
  borough: string
  latitude: number
  longitude: number
}

type Props = {
  neighborhoods: Neighborhood[]
}

export default function NeighborhoodMap({ neighborhoods }: Props) {
  const mapContainer = useRef<HTMLDivElement | null>(null)
  const map = useRef<mapboxgl.Map | null>(null)
  const markers = useRef<mapboxgl.Marker[]>([])

  useEffect(() => {
    if (!mapContainer.current || map.current) return

    const token = process.env.NEXT_PUBLIC_MAPBOX_TOKEN

    if (!token) {
      console.error('Mapbox token is missing')
      return
    }

    mapboxgl.accessToken = token

    const newMap = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/light-v11',
      center: [-73.94, 40.70],
      zoom: 9.5,
    })

    newMap.addControl(
      new mapboxgl.NavigationControl(),
      'top-right'
    )

    newMap.on('load', () => {
      newMap.addSource('nyc-neighborhoods', {
        type: 'geojson',
        data: '/nyc-neighborhoods.geojson',
      })

      newMap.addLayer({
        id: 'neighborhood-fill',
        type: 'fill',
        source: 'nyc-neighborhoods',
        paint: {
          'fill-color': '#9ca3af',
          'fill-opacity': 0.25,
        },
      })

      newMap.addLayer({
        id: 'neighborhood-border',
        type: 'line',
        source: 'nyc-neighborhoods',
        paint: {
          'line-color': '#ffffff',
          'line-width': 1.5,
        },
      })

      newMap.on('mouseenter', 'neighborhood-fill', () => {
        newMap.getCanvas().style.cursor = 'pointer'
      })

      newMap.on('mouseleave', 'neighborhood-fill', () => {
        newMap.getCanvas().style.cursor = ''
      })

      newMap.on('click', 'neighborhood-fill', (e) => {
        const feature = e.features?.[0]

        if (!feature) return

        const properties =
          (feature as { properties?: Record<string, unknown> }).properties ?? {}

        const name = String(
          properties.ntaname ||
          properties.NTAName ||
          'Neighborhood'
        )

        const borough = String(
          properties.boroname ||
          properties.BoroName ||
          'New York City'
        )

        const popupContent = document.createElement('div')

        const title = document.createElement('strong')
        title.textContent = name

        const boroughText = document.createElement('div')
        boroughText.textContent = borough

        popupContent.appendChild(title)
        popupContent.appendChild(boroughText)

        new mapboxgl.Popup()
          .setLngLat(e.lngLat)
          .setDOMContent(popupContent)
          .addTo(newMap)
      })
    })

    map.current = newMap

    return () => {
      markers.current.forEach((marker) => marker.remove())
      markers.current = []

      newMap.remove()
      map.current = null
    }
  }, [])

  useEffect(() => {
    if (!map.current) return

    markers.current.forEach((marker) => marker.remove())
    markers.current = []

    neighborhoods.forEach((neighborhood) => {
      if (
        typeof neighborhood.latitude !== 'number' ||
        typeof neighborhood.longitude !== 'number'
      ) {
        return
      }

      const popupContent = document.createElement('div')

      const title = document.createElement('strong')
      title.textContent = neighborhood.name

      const boroughText = document.createElement('div')
      boroughText.textContent = neighborhood.borough

      popupContent.appendChild(title)
      popupContent.appendChild(boroughText)

      const popup = new mapboxgl.Popup({
        offset: 25,
      }).setDOMContent(popupContent)

      const marker = new mapboxgl.Marker()
        .setLngLat([
          neighborhood.longitude,
          neighborhood.latitude,
        ])
        .setPopup(popup)
        .addTo(map.current!)

      markers.current.push(marker)
    })
  }, [neighborhoods])

  return (
    <div
      ref={mapContainer}
      className="h-[550px] w-full overflow-hidden rounded-2xl border"
    />
  )
}