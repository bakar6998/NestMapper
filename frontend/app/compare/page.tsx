'use client'

import { useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import {
  ArrowLeft,
  ArrowRight,
  Check,
  ChevronDown,
  ShieldCheck,
  X,
} from 'lucide-react'

import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from 'recharts'

import {
  getNeighborhoods,
  compareNeighborhoods,
} from '@/lib/api'

function ScoreBar({ value }: { value: number }) {
  const safeValue = Number.isFinite(value) ? value : 0

  return (
    <div className="mt-2 h-2 overflow-hidden rounded-full bg-muted">
      <div
        className="h-full rounded-full bg-[#10b981]"
        style={{
          width: `${Math.min(Math.max(safeValue, 0), 10) * 10}%`,
        }}
      />
    </div>
  )
}

function NeighborhoodColumn({
  data,
  onRemove,
}: {
  data: any
  onRemove: () => void
}) {
  const scores = data.scores
    ? [
        {
          label: 'Affordability',
          value: Math.round(
            Number(data.scores.affordability_score) || 0
          ),
        },
        {
          label: 'Transit',
          value: Math.round(
            Number(data.scores.transit_score) || 0
          ),
        },
        {
          label: 'Safety',
          value: Math.round(
            Number(data.scores.safety_score) || 0
          ),
        },
        {
          label: 'Family',
          value: Math.round(
            Number(data.scores.family_score) || 0
          ),
        },
        {
          label: 'Accessibility',
          value: Math.round(
            Number(data.scores.accessibility_score) || 0
          ),
        },
        {
          label: 'Convenience',
          value: Math.round(
            Number(data.scores.convenience_score) || 0
          ),
        },
      ]
    : []

  const rent = Number(data.rent?.one_bedroom) || 0

  const highlights = [
    data.transit?.nearest_station
      ? `Near ${data.transit.nearest_station}`
      : '',
    data.amenities?.schools_count
      ? `${data.amenities.schools_count} schools nearby`
      : '',
    data.amenities?.parks_count
      ? `${data.amenities.parks_count} parks nearby`
      : '',
  ].filter(Boolean)

  return (
    <article className="relative rounded-2xl border border-border bg-card p-5 shadow-sm md:p-7">
      <button
        type="button"
        onClick={onRemove}
        aria-label={`Remove ${data.name}`}
        className="absolute right-4 top-4 rounded-full p-2 text-muted-foreground hover:bg-muted hover:text-foreground"
      >
        <X size={17} />
      </button>

      <div className="pr-8">
        <p className="text-sm font-semibold text-primary">
          {data.borough}
        </p>

        <h2 className="mt-2 text-3xl font-bold tracking-tight">
          {data.name}
        </h2>

        {data.vibe && (
          <span className="mt-3 inline-flex rounded-full bg-[#dcfce7] px-3 py-1 text-xs font-semibold text-[#15803d]">
            {data.vibe}
          </span>
        )}

        <p className="mt-5 text-sm leading-6 text-muted-foreground">
          {data.description ||
            'Neighborhood information from NestMapper NYC.'}
        </p>
      </div>

      <div className="mt-7 border-y border-border py-5">
        <span className="text-xs font-bold tracking-[.16em] text-muted-foreground">
          AVERAGE 1BR RENT
        </span>

        <div className="mt-1 text-3xl font-bold">
          {rent > 0 ? `$${rent.toLocaleString()}` : 'N/A'}

          {rent > 0 && (
            <span className="text-sm font-normal text-muted-foreground">
              {' '}
              / month
            </span>
          )}
        </div>
      </div>

      <div className="mt-6 space-y-5">
        {scores.map((score) => (
          <div key={score.label}>
            <div className="flex justify-between text-sm">
              <span>{score.label}</span>
              <strong>{score.value}/10</strong>
            </div>

            <ScoreBar value={score.value} />
          </div>
        ))}
      </div>

      {highlights.length > 0 && (
        <div className="mt-7">
          <p className="text-xs font-bold tracking-[.16em] text-muted-foreground">
            GOOD TO KNOW
          </p>

          <ul className="mt-4 space-y-3">
            {highlights.map((item) => (
              <li
                key={item}
                className="flex items-center gap-2 text-sm"
              >
                <Check
                  size={16}
                  className="text-[#16a34a]"
                />
                {item}
              </li>
            ))}
          </ul>
        </div>
      )}

      <Link
        href="/explore"
        className="button-secondary mt-7 w-full justify-center"
      >
        View full profile
        <ArrowRight size={16} />
      </Link>
    </article>
  )
}

export default function ComparePage() {
  const [apiNeighborhoods, setApiNeighborhoods] =
    useState<any[]>([])

  const [first, setFirst] = useState('')
  const [second, setSecond] = useState('')

  const [comparisonData, setComparisonData] =
    useState<any[]>([])

  const [loading, setLoading] = useState(true)
  const [compareLoading, setCompareLoading] =
    useState(false)

  const [error, setError] = useState('')

  // Load all neighborhoods
  useEffect(() => {
    getNeighborhoods()
      .then((data) => {
        setApiNeighborhoods(data)

        if (data.length >= 2) {
          setFirst(data[0].name)
          setSecond(data[1].name)
        }

        setError('')
      })
      .catch((err) => {
        console.error(err)
        setError(
          'Could not load neighborhoods from backend.'
        )
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  // Compare whenever selections change
  useEffect(() => {
    if (
      !first ||
      !second ||
      apiNeighborhoods.length === 0
    ) {
      return
    }

    const firstN = apiNeighborhoods.find(
      (n) => n.name === first
    )

    const secondN = apiNeighborhoods.find(
      (n) => n.name === second
    )

    if (!firstN || !secondN) return

    if (firstN.id === secondN.id) {
      setComparisonData([])
      return
    }

    setCompareLoading(true)

    compareNeighborhoods([
      firstN.id,
      secondN.id,
    ])
      .then((data) => {
        setComparisonData(
          Array.isArray(data)
            ? data
            : data?.neighborhoods || []
        )
      })
      .catch((err) => {
        console.error(err)
        setComparisonData([])
      })
      .finally(() => {
        setCompareLoading(false)
      })
  }, [first, second, apiNeighborhoods])

  const compared = useMemo(() => {
    if (
      comparisonData &&
      comparisonData.length === 2
    ) {
      return comparisonData
    }

    return [
      apiNeighborhoods.find(
        (n) => n.name === first
      ),
      apiNeighborhoods.find(
        (n) => n.name === second
      ),
    ].filter(Boolean)
  }, [
    first,
    second,
    comparisonData,
    apiNeighborhoods,
  ])

  const radarData = useMemo(() => {
    if (compared.length !== 2) return []

    const firstScores =
      compared[0]?.scores || {}

    const secondScores =
      compared[1]?.scores || {}

    return [
      {
        subject: 'Affordability',
        first:
          Number(
            firstScores.affordability_score
          ) || 0,
        second:
          Number(
            secondScores.affordability_score
          ) || 0,
      },
      {
        subject: 'Transit',
        first:
          Number(firstScores.transit_score) ||
          0,
        second:
          Number(
            secondScores.transit_score
          ) || 0,
      },
      {
        subject: 'Safety',
        first:
          Number(firstScores.safety_score) ||
          0,
        second:
          Number(
            secondScores.safety_score
          ) || 0,
      },
      {
        subject: 'Family',
        first:
          Number(firstScores.family_score) ||
          0,
        second:
          Number(
            secondScores.family_score
          ) || 0,
      },
      {
        subject: 'Accessibility',
        first:
          Number(
            firstScores.accessibility_score
          ) || 0,
        second:
          Number(
            secondScores.accessibility_score
          ) || 0,
      },
      {
        subject: 'Convenience',
        first:
          Number(
            firstScores.convenience_score
          ) || 0,
        second:
          Number(
            secondScores.convenience_score
          ) || 0,
      },
    ]
  }, [compared])

  const boroughs = [
    'Manhattan',
    'Brooklyn',
    'Queens',
    'The Bronx',
    'Staten Island',
  ]

  return (
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-50 border-b border-border/80 bg-background/95 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4 lg:px-8">
          <Link
            href="/"
            className="text-xl font-bold tracking-tight"
          >
            NestMapper{' '}
            <span className="text-primary">
              NYC
            </span>
          </Link>

          <nav className="flex items-center gap-4 md:gap-7">
            <Link
              href="/explore"
              className="hidden text-sm text-muted-foreground hover:text-foreground sm:block"
            >
              Explore
            </Link>

            <Link
              href="/compare"
              className="text-sm font-semibold text-primary"
            >
              Compare
            </Link>

            <Link
              href="/recommend"
              className="button-primary px-4 py-2.5"
            >
              Get started
            </Link>
          </nav>
        </div>
      </header>

      <main>
        <section className="mx-auto max-w-7xl px-5 pb-10 pt-12 lg:px-8 lg:pb-14 lg:pt-20">
          <Link
            href="/explore"
            className="inline-flex items-center gap-2 text-sm font-semibold text-muted-foreground hover:text-foreground"
          >
            <ArrowLeft size={16} />
            Back to explore
          </Link>

          <div className="mt-9 max-w-3xl">
            <p className="eyebrow">
              SIDE BY SIDE, CLEAR AS DAY
            </p>

            <h1 className="mt-3 text-balance text-4xl font-bold tracking-tight md:text-6xl">
              Compare neighborhoods with
              confidence.
            </h1>

            <p className="mt-5 max-w-2xl text-base leading-7 text-muted-foreground md:text-lg">
              Put two NYC neighborhoods next to
              each other and see what really
              matters: rent, commute, safety,
              accessibility, and the feeling of
              home.
            </p>
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-5 lg:px-8">
          {loading && (
            <div className="flex items-center gap-3 py-4">
              <div className="h-5 w-5 animate-spin rounded-full border-2 border-muted border-t-primary" />

              <span className="text-sm text-muted-foreground">
                Loading neighborhoods...
              </span>
            </div>
          )}

          {error && (
            <p className="text-sm text-red-500">
              {error}
            </p>
          )}

          {!loading &&
            apiNeighborhoods.length > 0 && (
              <div className="grid gap-4 rounded-2xl border border-border bg-card p-4 md:grid-cols-[1fr_auto_1fr] md:items-end md:p-5">
                <label className="block text-sm font-semibold">
                  First neighborhood

                  <span className="relative mt-2 block">
                    <select
                      value={first}
                      onChange={(e) =>
                        setFirst(e.target.value)
                      }
                      className="h-12 w-full appearance-none rounded-xl border border-border bg-background px-4 pr-10 text-base"
                    >
                      {boroughs.map(
                        (borough) => (
                          <optgroup
                            key={borough}
                            label={borough}
                          >
                            {apiNeighborhoods
                              .filter(
                                (n) =>
                                  n.borough ===
                                  borough
                              )
                              .map((n) => (
                                <option
                                  key={n.id}
                                  value={n.name}
                                >
                                  {n.name}
                                </option>
                              ))}
                          </optgroup>
                        )
                      )}
                    </select>

                    <ChevronDown
                      className="pointer-events-none absolute right-4 top-3.5 text-muted-foreground"
                      size={18}
                    />
                  </span>
                </label>

                <div className="hidden items-center justify-center md:flex">
                  <span className="flex size-10 items-center justify-center rounded-full bg-primary text-xs font-bold text-primary-foreground">
                    VS
                  </span>
                </div>

                <label className="block text-sm font-semibold">
                  Second neighborhood

                  <span className="relative mt-2 block">
                    <select
                      value={second}
                      onChange={(e) =>
                        setSecond(
                          e.target.value
                        )
                      }
                      className="h-12 w-full appearance-none rounded-xl border border-border bg-background px-4 pr-10 text-base"
                    >
                      {boroughs.map(
                        (borough) => (
                          <optgroup
                            key={borough}
                            label={borough}
                          >
                            {apiNeighborhoods
                              .filter(
                                (n) =>
                                  n.borough ===
                                  borough
                              )
                              .map((n) => (
                                <option
                                  key={n.id}
                                  value={n.name}
                                >
                                  {n.name}
                                </option>
                              ))}
                          </optgroup>
                        )
                      )}
                    </select>

                    <ChevronDown
                      className="pointer-events-none absolute right-4 top-3.5 text-muted-foreground"
                      size={18}
                    />
                  </span>
                </label>
              </div>
            )}

          {first &&
            second &&
            first === second && (
              <p className="mt-3 text-sm text-amber-600">
                Select two different
                neighborhoods to compare.
              </p>
            )}

          {compareLoading && (
            <p className="mt-4 text-sm text-muted-foreground">
              Updating comparison...
            </p>
          )}
        </section>

        <section className="mx-auto max-w-7xl px-5 py-8 lg:px-8 lg:py-10">
          <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
            <div>
              <p className="eyebrow">
                YOUR SHORTLIST
              </p>

              <h2 className="mt-2 text-2xl font-bold">
                The details side by side
              </h2>
            </div>

            <span className="inline-flex items-center gap-2 text-sm text-muted-foreground">
              <ShieldCheck
                size={17}
                className="text-[#16a34a]"
              />
              Independent neighborhood data
            </span>
          </div>

          <div className="grid gap-5 lg:grid-cols-2">
            {compared.map(
              (item, index) =>
                item && (
                  <NeighborhoodColumn
                    key={`${item.name}-${index}`}
                    data={item}
                    onRemove={() =>
                      index === 0
                        ? setFirst(
                            apiNeighborhoods[0]
                              ?.name || ''
                          )
                        : setSecond(
                            apiNeighborhoods[1]
                              ?.name || ''
                          )
                    }
                  />
                )
            )}
          </div>
        </section>

        {compared.length === 2 &&
          radarData.length > 0 && (
            <section className="mx-auto max-w-7xl px-5 pb-10 lg:px-8">
              <div className="rounded-2xl border border-border bg-card p-5 shadow-sm md:p-7">
                <div className="mb-6">
                  <p className="eyebrow">
                    SCORE COMPARISON
                  </p>

                  <h2 className="mt-2 text-2xl font-bold">
                    Compare all six dimensions
                  </h2>

                  <p className="mt-2 text-sm text-muted-foreground">
                    See how both neighborhoods
                    compare across NestMapper's
                    six scoring dimensions.
                  </p>
                </div>

                <div className="h-[420px] w-full">
                  <ResponsiveContainer
                    width="100%"
                    height="100%"
                  >
                    <RadarChart
                      data={radarData}
                    >
                      <PolarGrid />

                      <PolarAngleAxis
                        dataKey="subject"
                        tick={{
                          fontSize: 12,
                        }}
                      />

                      <PolarRadiusAxis
                        angle={30}
                        domain={[0, 10]}
                        tickCount={6}
                      />

                      <Tooltip />

                      <Radar
                        name={
                          compared[0]?.name ||
                          'Neighborhood 1'
                        }
                        dataKey="first"
                        stroke="#2563eb"
                        fill="#2563eb"
                        fillOpacity={0.25}
                      />

                      <Radar
                        name={
                          compared[1]?.name ||
                          'Neighborhood 2'
                        }
                        dataKey="second"
                        stroke="#10b981"
                        fill="#10b981"
                        fillOpacity={0.25}
                      />

                      <Legend />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </section>
          )}

        <section className="mx-auto max-w-7xl px-5 pb-16 lg:px-8">
          <div className="grid gap-4 rounded-2xl bg-[#0f1b31] p-7 text-white md:grid-cols-[1fr_auto] md:items-center md:p-10">
            <div>
              <p className="text-xs font-bold tracking-[.18em] text-[#6ee7b7]">
                MAKE THE NEXT MOVE
              </p>

              <h2 className="mt-3 text-2xl font-bold md:text-3xl">
                Not sure what fits your life?
              </h2>

              <p className="mt-3 max-w-xl text-sm leading-6 text-white/70">
                Tell us your budget, lifestyle,
                and priorities. We'll help you
                build a shortlist worth seeing in
                person.
              </p>
            </div>

            <Link
              href="/recommend"
              className="button-light whitespace-nowrap"
            >
              Get my match
              <ArrowRight size={16} />
            </Link>
          </div>
        </section>
      </main>

      <footer className="border-t border-border">
        <div className="mx-auto flex max-w-7xl flex-col gap-3 px-5 py-8 text-sm text-muted-foreground sm:flex-row sm:items-center sm:justify-between lg:px-8">
          <Link
            href="/"
            className="font-semibold text-foreground"
          >
            NestMapper{' '}
            <span className="text-primary">
              NYC
            </span>
          </Link>

          <span>Know before you move.</span>

          <Link
            href="/explore"
            className="hover:text-foreground"
          >
            Explore neighborhoods
            <ArrowRight
              className="ml-1 inline"
              size={14}
            />
          </Link>
        </div>
      </footer>
    </div>
  )
}