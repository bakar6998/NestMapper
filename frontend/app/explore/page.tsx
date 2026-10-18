'use client'

import { useEffect, useState } from 'react'
import { getNeighborhoods } from '@/lib/api'
import NeighborhoodMap from '@/components/NeighborhoodMap'

export default function ExplorePage() {
  const [neighborhoods, setNeighborhoods] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  useEffect(() => {
    getNeighborhoods()
      .then((data) => {
        setNeighborhoods(data)
        setError(false)
      })
      .catch((err) => {
        console.error(err)
        setError(true)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  return (
    <main className="min-h-screen p-6">
      <h1 className="mb-6 text-3xl font-bold">
        Explore Neighborhoods
      </h1>

      <NeighborhoodMap neighborhoods={neighborhoods} />

      {loading && (
        <p className="mt-6">
          Loading neighborhoods...
        </p>
      )}

      {error && (
        <p className="mt-6">
          Neighborhood details could not be loaded right now.
        </p>
      )}

      {!loading && !error && (
        <div className="mt-8">
          {neighborhoods.map((n: any) => (
            <div
              key={n.id}
              className="mb-4 rounded-lg border p-4"
            >
              <h2 className="text-xl font-semibold">
                {n.name}
              </h2>

              <p>{n.borough}</p>
            </div>
          ))}
        </div>
      )}
    </main>
  )
}