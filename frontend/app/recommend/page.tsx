'use client'

import Link from 'next/link'
import {
  ArrowLeft,
  ArrowRight,
  Check,
  MapPin,
} from 'lucide-react'
import { useState } from 'react'
import { getRecommendations } from '@/lib/api'

const priorities = [
  'Affordability',
  'Safety',
  'Transit',
  'Parks',
  'Accessibility',
]

const situations = [
  'Student',
  'Professional',
  'Family',
  'Couple',
]

const scoreKeys = [
  ['affordability_score', 'Affordability'],
  ['transit_score', 'Transit'],
  ['safety_score', 'Safety'],
  ['family_score', 'Family'],
  ['accessibility_score', 'Accessibility'],
  ['convenience_score', 'Convenience'],
]

function ScoreBar({
  label,
  value,
}: {
  label: string
  value: number
}) {
  const safeValue = Math.max(
    0,
    Math.min(Number(value) || 0, 10)
  )

  return (
    <div>
      <div className="mb-1 flex justify-between text-sm">
        <span>{label}</span>

        <strong>
          {safeValue.toFixed(1)}/10
        </strong>
      </div>

      <div className="h-2 overflow-hidden rounded-full bg-muted">
        <div
          className="h-full rounded-full bg-primary"
          style={{
            width: `${safeValue * 10}%`,
          }}
        />
      </div>
    </div>
  )
}

export default function RecommendPage() {
  const [budget, setBudget] = useState(2500)

  const [priority, setPriority] =
    useState('Affordability')

  const [borough, setBorough] =
    useState('Any borough')

  const [situation, setSituation] =
    useState('Professional')

  const [studentCampus, setStudentCampus] =
    useState('')

  const [professionalCommute, setProfessionalCommute] =
    useState('30')

  const [familyChildren, setFamilyChildren] =
    useState('Yes')

  const [coupleLifestyle, setCoupleLifestyle] =
    useState('Balanced')

  const [apiMatches, setApiMatches] =
    useState<any[]>([])

  const [loading, setLoading] =
    useState(false)

  const [apiError, setApiError] =
    useState('')

  const [submitted, setSubmitted] =
    useState(false)

  const fetchRecommendations = async () => {
    setLoading(true)
    setApiError('')
    setSubmitted(true)

    const preferences: Record<string, any> = {
      budget,
      priority,
      borough,
      life_situation: situation,
    }

    if (situation === 'Student') {
      preferences.campus = studentCampus
    }

    if (situation === 'Professional') {
      preferences.max_commute_minutes =
        Number(professionalCommute)
    }

    if (situation === 'Family') {
      preferences.has_children =
        familyChildren === 'Yes'
    }

    if (situation === 'Couple') {
      preferences.lifestyle =
        coupleLifestyle
    }

    try {
      const data =
        await getRecommendations(
          preferences
        )

      const results = Array.isArray(data)
        ? data
        : data?.results ||
          data?.recommendations ||
          []

      setApiMatches(
        results.slice(0, 5)
      )
    } catch (err) {
      console.error(err)

      setApiError(
        'Could not load recommendations from the backend.'
      )

      setApiMatches([])
    } finally {
      setLoading(false)
    }
  }

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
              className="text-sm text-muted-foreground hover:text-foreground"
            >
              Compare
            </Link>

            <Link
              href="/recommend"
              className="text-sm font-semibold text-primary"
            >
              Recommend
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
              YOUR PERSONALIZED SHORTLIST
            </p>

            <h1 className="mt-3 text-balance text-4xl font-bold tracking-tight md:text-6xl">
              Find the neighborhood that fits
              your life.
            </h1>

            <p className="mt-5 max-w-2xl text-base leading-7 text-muted-foreground md:text-lg">
              Share your budget, lifestyle,
              and priorities to find NYC
              neighborhoods that match your
              needs.
            </p>
          </div>
        </section>

        <section className="mx-auto grid max-w-7xl gap-6 px-5 pb-12 lg:grid-cols-[minmax(0,420px)_1fr] lg:px-8">
          {/* Preference form */}
          <div className="rounded-2xl border border-border bg-card p-6 shadow-sm md:p-8">
            <p className="eyebrow">
              TELL US WHAT MATTERS
            </p>

            <div className="mt-7 space-y-7">
              {/* Budget */}
              <div>
                <div className="flex items-center justify-between text-sm font-semibold">
                  <span>
                    Monthly budget
                  </span>

                  <span className="text-primary">
                    ${budget.toLocaleString()}
                    /mo
                  </span>
                </div>

                <input
                  className="budget-range mt-4 w-full"
                  type="range"
                  min="1000"
                  max="5000"
                  step="100"
                  value={budget}
                  onChange={(event) =>
                    setBudget(
                      Number(
                        event.target.value
                      )
                    )
                  }
                  aria-label="Monthly budget"
                />
              </div>

              {/* Borough */}
              <div>
                <label
                  htmlFor="borough"
                  className="text-sm font-semibold"
                >
                  Preferred borough
                </label>

                <select
                  id="borough"
                  value={borough}
                  onChange={(event) =>
                    setBorough(
                      event.target.value
                    )
                  }
                  className="mt-3 h-12 w-full rounded-xl border border-border bg-background px-4 text-sm"
                >
                  <option>
                    Any borough
                  </option>
                  <option>
                    Manhattan
                  </option>
                  <option>
                    Brooklyn
                  </option>
                  <option>
                    Queens
                  </option>
                  <option>
                    The Bronx
                  </option>
                  <option>
                    Staten Island
                  </option>
                </select>
              </div>

              {/* Priority */}
              <div>
                <span className="text-sm font-semibold">
                  Top priority
                </span>

                <div className="mt-3 flex flex-wrap gap-2">
                  {priorities.map(
                    (item) => (
                      <button
                        type="button"
                        key={item}
                        onClick={() =>
                          setPriority(item)
                        }
                        className={`preference-pill ${
                          priority === item
                            ? 'selected'
                            : ''
                        }`}
                      >
                        {priority ===
                          item && (
                          <Check
                            size={14}
                          />
                        )}

                        {item}
                      </button>
                    )
                  )}
                </div>
              </div>

              {/* Life situation */}
              <div>
                <span className="text-sm font-semibold">
                  Life situation
                </span>

                <div className="mt-3 grid grid-cols-2 gap-2">
                  {situations.map(
                    (item) => (
                      <button
                        type="button"
                        key={item}
                        onClick={() =>
                          setSituation(
                            item
                          )
                        }
                        className={`preference-pill justify-center ${
                          situation ===
                          item
                            ? 'selected'
                            : ''
                        }`}
                      >
                        {situation ===
                          item && (
                          <Check
                            size={14}
                          />
                        )}

                        {item}
                      </button>
                    )
                  )}
                </div>
              </div>

              {/* Student questions */}
              {situation ===
                'Student' && (
                <div className="rounded-xl border border-border bg-muted/30 p-4">
                  <label className="text-sm font-semibold">
                    School or campus
                  </label>

                  <input
                    type="text"
                    value={
                      studentCampus
                    }
                    onChange={(e) =>
                      setStudentCampus(
                        e.target.value
                      )
                    }
                    placeholder="Example: Brooklyn College"
                    className="mt-3 h-11 w-full rounded-lg border border-border bg-background px-3 text-sm outline-none"
                  />

                  <p className="mt-2 text-xs text-muted-foreground">
                    This can help prioritize
                    neighborhoods with an easier
                    commute to school.
                  </p>
                </div>
              )}

              {/* Professional questions */}
              {situation ===
                'Professional' && (
                <div className="rounded-xl border border-border bg-muted/30 p-4">
                  <label className="text-sm font-semibold">
                    Maximum commute
                  </label>

                  <select
                    value={
                      professionalCommute
                    }
                    onChange={(e) =>
                      setProfessionalCommute(
                        e.target.value
                      )
                    }
                    className="mt-3 h-11 w-full rounded-lg border border-border bg-background px-3 text-sm"
                  >
                    <option value="20">
                      20 minutes
                    </option>

                    <option value="30">
                      30 minutes
                    </option>

                    <option value="45">
                      45 minutes
                    </option>

                    <option value="60">
                      60 minutes
                    </option>
                  </select>
                </div>
              )}

              {/* Family questions */}
              {situation ===
                'Family' && (
                <div className="rounded-xl border border-border bg-muted/30 p-4">
                  <label className="text-sm font-semibold">
                    Children in household
                  </label>

                  <select
                    value={
                      familyChildren
                    }
                    onChange={(e) =>
                      setFamilyChildren(
                        e.target.value
                      )
                    }
                    className="mt-3 h-11 w-full rounded-lg border border-border bg-background px-3 text-sm"
                  >
                    <option>
                      Yes
                    </option>

                    <option>
                      No
                    </option>
                  </select>

                  <p className="mt-2 text-xs text-muted-foreground">
                    Family matches can give more
                    weight to schools, parks, and
                    safety.
                  </p>
                </div>
              )}

              {/* Couple questions */}
              {situation ===
                'Couple' && (
                <div className="rounded-xl border border-border bg-muted/30 p-4">
                  <label className="text-sm font-semibold">
                    Preferred lifestyle
                  </label>

                  <select
                    value={
                      coupleLifestyle
                    }
                    onChange={(e) =>
                      setCoupleLifestyle(
                        e.target.value
                      )
                    }
                    className="mt-3 h-11 w-full rounded-lg border border-border bg-background px-3 text-sm"
                  >
                    <option>
                      Balanced
                    </option>

                    <option>
                      Quiet
                    </option>

                    <option>
                      Nightlife
                    </option>

                    <option>
                      Outdoors
                    </option>
                  </select>
                </div>
              )}

              <button
                type="button"
                onClick={
                  fetchRecommendations
                }
                disabled={loading}
                className="button-primary w-full justify-center disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading
                  ? 'Finding matches...'
                  : 'Find my matches'}

                {!loading && (
                  <ArrowRight
                    size={16}
                  />
                )}
              </button>
            </div>
          </div>

          {/* Results */}
          <div>
            <div className="mb-5 flex items-end justify-between gap-4">
              <div>
                <p className="eyebrow">
                  RECOMMENDED FOR YOU
                </p>

                <h2 className="mt-2 text-2xl font-bold">
                  Your best matches
                </h2>
              </div>

              <span className="hidden items-center gap-2 text-sm text-muted-foreground sm:flex">
                <MapPin
                  size={16}
                  className="text-primary"
                />
                NYC data
              </span>
            </div>

            {/* Loading */}
            {loading && (
              <div className="flex items-center gap-3 rounded-xl border border-border p-5">
                <div className="h-5 w-5 animate-spin rounded-full border-2 border-muted border-t-primary" />

                <span className="text-sm text-muted-foreground">
                  Finding your best
                  neighborhoods...
                </span>
              </div>
            )}

            {/* Error */}
            {!loading &&
              apiError && (
                <div className="rounded-xl border border-red-200 bg-red-50 p-4">
                  <p className="text-sm text-red-600">
                    {apiError}
                  </p>
                </div>
              )}

            {/* Waiting */}
            {!loading &&
              !submitted && (
                <div className="rounded-2xl border border-dashed border-border p-8 text-center">
                  <h3 className="font-semibold">
                    Ready when you are
                  </h3>

                  <p className="mt-2 text-sm text-muted-foreground">
                    Choose your preferences and
                    click Find my matches to see
                    your top neighborhoods.
                  </p>
                </div>
              )}

            {/* No results */}
            {!loading &&
              submitted &&
              !apiError &&
              apiMatches.length ===
                0 && (
                <div className="rounded-2xl border border-border p-8 text-center">
                  <h3 className="font-semibold">
                    No matches found
                  </h3>

                  <p className="mt-2 text-sm text-muted-foreground">
                    Try increasing your budget or
                    changing your borough and
                    priority.
                  </p>
                </div>
              )}

            {/* Top 5 */}
            {!loading &&
              apiMatches.length >
                0 && (
                <div className="space-y-4">
                  {apiMatches.map(
                    (
                      match: any,
                      index
                    ) => {
                      const neighborhood =
                        match.neighborhood ||
                        match

                      const scores =
                        neighborhood.scores ||
                        match.scores ||
                        {}

                      const matchPercentage =
                        Number(
                          match.match_percentage ??
                            match.match_score ??
                            match.score ??
                            0
                        )

                      const reasons =
                        match.reasons ||
                        match.reason ||
                        []

                      const reasonText =
                        Array.isArray(
                          reasons
                        )
                          ? reasons.join(
                              ' • '
                            )
                          : reasons

                      const rent =
                        neighborhood.rent
                          ?.one_bedroom ??
                        neighborhood.rent
                          ?.average_1br ??
                        neighborhood.average_rent

                      return (
                        <article
                          key={
                            neighborhood.id ||
                            `${neighborhood.name}-${index}`
                          }
                          className="rounded-2xl border border-border bg-card p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md md:p-6"
                        >
                          <div className="flex flex-wrap items-start justify-between gap-4">
                            <div>
                              <p className="text-sm font-semibold text-primary">
                                {neighborhood.borough}
                              </p>

                              <h3 className="mt-1 text-2xl font-bold">
                                {
                                  neighborhood.name
                                }
                              </h3>

                              <span className="mt-2 inline-flex rounded-full bg-muted px-3 py-1 text-xs font-semibold">
                                #
                                {index +
                                  1}{' '}
                                match
                              </span>
                            </div>

                            <div className="text-right">
                              <strong className="text-3xl text-primary">
                                {Math.round(
                                  matchPercentage
                                )}
                                %
                              </strong>

                              <p className="text-xs text-muted-foreground">
                                match score
                              </p>
                            </div>
                          </div>

                          {reasonText && (
                            <div className="mt-5 border-t border-border pt-4">
                              <p className="text-sm font-semibold">
                                Why it matched
                              </p>

                              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                                {
                                  reasonText
                                }
                              </p>
                            </div>
                          )}

                          <div className="mt-5 space-y-4">
                            {scoreKeys.map(
                              ([
                                key,
                                label,
                              ]) => (
                                <ScoreBar
                                  key={
                                    key
                                  }
                                  label={
                                    label
                                  }
                                  value={Number(
                                    scores[
                                      key
                                    ] ||
                                      0
                                  )}
                                />
                              )
                            )}
                          </div>

                          <div className="mt-5 flex flex-wrap items-center justify-between gap-3 border-t border-border pt-4">
                            <div>
                              <span className="block text-xs text-muted-foreground">
                                AVG 1BR
                              </span>

                              <strong>
                                {rent
                                  ? `$${Number(
                                      rent
                                    ).toLocaleString()}/mo`
                                  : 'Rent data unavailable'}
                              </strong>
                            </div>

                            <div className="flex gap-3">
                              <Link
                                href="/compare"
                                className="button-secondary px-4 py-2.5"
                              >
                                Compare
                                <ArrowRight
                                  size={
                                    15
                                  }
                                />
                              </Link>

                              <Link
                                href="/explore"
                                className="text-sm font-semibold text-primary hover:underline"
                              >
                                View
                                profile
                              </Link>
                            </div>
                          </div>
                        </article>
                      )
                    }
                  )}
                </div>
              )}
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

          <span>
            Know before you move.
          </span>

          <Link
            href="/compare"
            className="hover:text-foreground"
          >
            Compare neighborhoods
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