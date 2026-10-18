'use client'

import { useEffect, useMemo, useState } from 'react'
import { Search } from 'lucide-react'
import { getNeighborhoods } from '@/lib/api'
import NeighborhoodMap from '@/components/NeighborhoodMap'

const boroughs = [
  'All',
  'Manhattan',
  'Brooklyn',
  'Queens',
  'The Bronx',
  'Staten Island',
]

export default function ExplorePage() {
  const [neighborhoods, setNeighborhoods] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  const [search, setSearch] = useState('')
  const [selectedBorough, setSelectedBorough] = useState('All')

  useEffect(() => {
    getNeighborhoods()
      .then((data) => {
        setNeighborhoods(data)
        setError(false)
      })
      .catch((err) => {
        console.error('Failed to load neighborhoods:', err)
        setError(true)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  const filteredNeighborhoods = useMemo(() => {
    return neighborhoods.filter((neighborhood) => {
      const name = neighborhood.name?.toLowerCase() || ''
      const borough = neighborhood.borough || ''

      const matchesSearch = name.includes(search.toLowerCase())

      const normalizedBorough =
        borough === 'Bronx' ? 'The Bronx' : borough

      const matchesBorough =
        selectedBorough === 'All' ||
        normalizedBorough === selectedBorough

      return matchesSearch && matchesBorough
    })
  }, [neighborhoods, search, selectedBorough])

  return (
    <main className="min-h-screen bg-background px-5 py-8 lg:px-8">
      <div className="mx-auto max-w-7xl">

        <div className="mb-6">
          <h1 className="text-3xl font-bold">
            Explore Neighborhoods
          </h1>

          <p className="mt-2 text-muted-foreground">
            Search and explore neighborhoods across New York City.
          </p>
        </div>

        {/* Search box */}
        <div className="mb-5 flex items-center gap-3 rounded-xl border bg-background px-4 py-3">
          <Search
            size={20}
            className="text-muted-foreground"
          />

          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search neighborhood..."
            className="w-full bg-transparent outline-none"
          />
        </div>

        {/* Borough filters */}
        <div className="mb-6 flex flex-wrap gap-2">
          {boroughs.map((borough) => (
            <button
              key={borough}
              type="button"
              onClick={() => setSelectedBorough(borough)}
              className={`rounded-full border px-4 py-2 text-sm font-medium transition ${
                selectedBorough === borough
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-background hover:bg-muted'
              }`}
            >
              {borough}
            </button>
          ))}
        </div>

        {/* Map */}
        <NeighborhoodMap
          neighborhoods={filteredNeighborhoods}
        />

        {/* Loading */}
        {loading && (
          <div className="flex items-center gap-3 py-8">
            <div className="h-5 w-5 animate-spin rounded-full border-2 border-muted border-t-primary" />

            <span className="text-sm text-muted-foreground">
              Loading neighborhoods...
            </span>
          </div>
        )}

        {/* API error */}
        {error && (
          <p className="mt-5 text-sm text-muted-foreground">
            Map boundaries are available. Neighborhood details are temporarily unavailable.
          </p>
        )}

        {/* Neighborhood results */}
        {!loading && !error && (
          <>
            <p className="mt-6 text-sm text-muted-foreground">
              {filteredNeighborhoods.length}{' '}
              {filteredNeighborhoods.length === 1
                ? 'neighborhood'
                : 'neighborhoods'}{' '}
              found
            </p>

            <div className="mt-4 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {filteredNeighborhoods.map((neighborhood) => (
                <div
                  key={neighborhood.id}
                  className="rounded-xl border p-4 transition hover:bg-muted/40"
                >
                  <h2 className="text-lg font-semibold">
                    {neighborhood.name}
                  </h2>

                  <p className="mt-1 text-sm text-muted-foreground">
                    {neighborhood.borough}
                  </p>
                </div>
              ))}
            </div>

            {filteredNeighborhoods.length === 0 && (
              <div className="py-10 text-center text-muted-foreground">
                No neighborhoods found.
              </div>
            )}
          </>
        )}
      </div>
    </main>
  )
}