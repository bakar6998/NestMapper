'use client'

import { useEffect, useRef } from 'react'
import mapboxgl from 'mapbox-gl'

type Neighborhood = {
  id: number
  name: string
  borough?: string
  latitude: number
  longitude: number
}

type NeighborhoodMapProps = {
  neighborhoods: Neighborhood[]
}

export default function NeighborhoodMap({
  neighborhoods,
}: NeighborhoodMapProps) {
  const mapContainer = useRef<HTMLDivElement | null>(null)
  const map = useRef<mapboxgl.Map | null>(null)

  useEffect(() => {
    if (!mapContainer.current || map.current) return

    const token = process.env.NEXT_PUBLIC_MAPBOX_TOKEN

    if (!token) {
      console.error('Mapbox token is missing')
      return
    }

    mapboxgl.accessToken = token

    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/light-v11',
      center: [-73.94, 40.70],
      zoom: 9.5,
    })

    map.current.addControl(
      new mapboxgl.NavigationControl(),
      'top-right'
    )

    return () => {
      map.current?.remove()
      map.current = null
    }
  }, [])

  useEffect(() => {
    if (!map.current || neighborhoods.length === 0) return

    const markers: mapboxgl.Marker[] = []

    neighborhoods.forEach((neighborhood) => {
      if (
        typeof neighborhood.latitude !== 'number' ||
        typeof neighborhood.longitude !== 'number'
      ) {
        return
      }

      const popup = new mapboxgl.Popup({
        offset: 25,
      }).setHTML(`
        <div>
          <strong>${neighborhood.name}</strong>
          <br />
          ${neighborhood.borough ?? 'NYC'}
        </div>
      `)

      const marker = new mapboxgl.Marker()
        .setLngLat([
          neighborhood.longitude,
          neighborhood.latitude,
        ])
        .setPopup(popup)
        .addTo(map.current!)

      markers.push(marker)
    })

    return () => {
      markers.forEach((marker) => marker.remove())
    }
  }, [neighborhoods])

  return (
    <div
      ref={mapContainer}
      className="h-[500px] w-full rounded-2xl"
    />
  )
}