'use client'

import { useEffect, useState } from 'react'
import { getNeighborhoods } from '@/lib/api'

export default function ExplorePage() {
  const [neighborhoods, setNeighborhoods] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getNeighborhoods()
      .then((data) => {
        setNeighborhoods(data)
        setLoading(false)
      })
      .catch((err) => {
        console.error(err)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return <div>Loading neighborhoods...</div>
  }

  return (
    <main>
      <h1>Explore Neighborhoods</h1>

      {neighborhoods.map((n: any) => (
        <div key={n.id}>
          <h2>{n.name}</h2>
          <p>{n.borough}</p>
        </div>
      ))}
    </main>
  )
}
