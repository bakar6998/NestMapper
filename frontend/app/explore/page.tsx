'use client'

import { useEffect, useMemo, useState } from 'react'
import { Search, X } from 'lucide-react'
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

const scoreKeys = [
  ['affordability', 'Affordability'],
  ['transit', 'Transit'],
  ['safety', 'Safety'],
  ['family', 'Family'],
  ['accessibility', 'Accessibility'],
  ['convenience', 'Convenience'],
]

export default function ExplorePage() {
  const [neighborhoods, setNeighborhoods] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  const [search, setSearch] = useState('')
  const [selectedBorough, setSelectedBorough] = useState('All')
  const [selectedNeighborhood, setSelectedNeighborhood] =
    useState<any | null>(null)

  useEffect(() => {
    getNeighborhoods()
      .then((data) => {
        setNeighborhoods(Array.isArray(data) ? data : [])
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

  const clearFilters = () => {
    setSearch('')
    setSelectedBorough('All')
  }

  const formatRent = (neighborhood: any) => {
    const rent =
      neighborhood.rent?.average_1br ??
      neighborhood.rent?.median_rent ??
      neighborhood.average_rent

    if (rent === null || rent === undefined || rent === '') {
      return 'Rent data will appear here.'
    }

    if (typeof rent === 'number') {
      return `$${rent.toLocaleString()}`
    }

    return String(rent)
  }

  const hasActiveFilters =
    search.trim() !== '' || selectedBorough !== 'All'

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

        <div className="mb-5 flex items-center gap-3 rounded-xl border bg-background px-4 py-3">
          <Search size={20} className="text-muted-foreground" />

          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search neighborhood..."
            className="w-full bg-transparent outline-none"
          />

          {search && (
            <button
              type="button"
              onClick={() => setSearch('')}
              className="rounded-md p-1 text-muted-foreground hover:bg-muted"
              aria-label="Clear search"
            >
              <X size={18} />
            </button>
          )}
        </div>

        <div className="mb-6 flex flex-wrap items-center gap-2">
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

          {hasActiveFilters && (
            <button
              type="button"
              onClick={clearFilters}
              className="ml-1 text-sm font-medium text-muted-foreground hover:text-foreground"
            >
              Clear filters
            </button>
          )}
        </div>

        <NeighborhoodMap neighborhoods={filteredNeighborhoods} />

        {loading && (
          <div className="flex items-center gap-3 py-8">
            <div className="h-5 w-5 animate-spin rounded-full border-2 border-muted border-t-primary" />

            <span className="text-sm text-muted-foreground">
              Loading neighborhoods...
            </span>
          </div>
        )}

        {error && (
          <p className="mt-5 text-sm text-muted-foreground">
            Map boundaries are available. Neighborhood details are temporarily unavailable.
          </p>
        )}

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
                <button
                  key={neighborhood.id}
                  type="button"
                  onClick={() => setSelectedNeighborhood(neighborhood)}
                  className="rounded-xl border p-4 text-left transition hover:bg-muted/40"
                >
                  <h2 className="text-lg font-semibold">
                    {neighborhood.name}
                  </h2>

                  <p className="mt-1 text-sm text-muted-foreground">
                    {neighborhood.borough}
                  </p>
                </button>
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

      {selectedNeighborhood && (
        <div
          className="fixed inset-0 z-50 flex justify-end bg-black/30"
          onClick={() => setSelectedNeighborhood(null)}
        >
          <div
            className="h-full w-full max-w-md overflow-y-auto bg-background p-6 shadow-xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="mb-6 flex items-start justify-between">
              <div>
                <h2 className="text-2xl font-bold">
                  {selectedNeighborhood.name}
                </h2>

                <p className="mt-1 text-muted-foreground">
                  {selectedNeighborhood.borough}
                </p>
              </div>

              <button
                type="button"
                onClick={() => setSelectedNeighborhood(null)}
                className="rounded-lg border p-2 hover:bg-muted"
                aria-label="Close neighborhood details"
              >
                <X size={18} />
              </button>
            </div>

            <div className="space-y-6">
              <div>
                <h3 className="mb-3 font-semibold">
                  Neighborhood Scores
                </h3>

                <div className="space-y-4">
                  {scoreKeys.map(([key, label]) => {
                    const rawValue =
                      selectedNeighborhood.scores?.[key] ??
                      selectedNeighborhood[`${key}_score`] ??
                      0

                    const value = Number(rawValue) || 0
                    const percentage = Math.min(
                      Math.max(value * 10, 0),
                      100
                    )

                    return (
                      <div key={key}>
                        <div className="mb-1 flex justify-between text-sm">
                          <span>{label}</span>
                          <span>{value}/10</span>
                        </div>

                        <div className="h-2 overflow-hidden rounded-full bg-muted">
                          <div
                            className="h-full rounded-full bg-primary"
                            style={{ width: `${percentage}%` }}
                          />
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>

              <div className="rounded-xl border p-4">
                <h3 className="font-semibold">
                  Rent
                </h3>

                <p className="mt-2 text-sm text-muted-foreground">
                  {formatRent(selectedNeighborhood)}
                </p>
              </div>

              <div className="rounded-xl border p-4">
                <h3 className="font-semibold">
                  Transit
                </h3>

                <p className="mt-2 text-sm text-muted-foreground">
                  {selectedNeighborhood.transit?.description ||
                    selectedNeighborhood.transit_info ||
                    'Transit information will appear here.'}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </main>
  )
}