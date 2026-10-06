'use client'

import { useMemo, useState } from 'react'
import Link from 'next/link'
import { ArrowLeft, ArrowRight, Check, ChevronDown, MapPin, Plus, ShieldCheck, Train, X } from 'lucide-react'

type Neighborhood = {
  name: string
  borough: string
  rent: number
  vibe: string
  description: string
  scores: { label: string; value: number }[]
  highlights: string[]
}

const neighborhoods: Neighborhood[] = [
  { name: 'Astoria', borough: 'Queens', rent: 2600, vibe: 'Lively', description: 'A welcoming, food-forward neighborhood with a little more room to breathe.', scores: [{ label: 'Affordability', value: 7 }, { label: 'Transit', value: 8 }, { label: 'Safety', value: 7 }, { label: 'Accessibility', value: 8 }, { label: 'Parks', value: 7 }], highlights: ['15 min to Midtown', 'Great restaurants', 'Waterfront parks'] },
  { name: 'Park Slope', borough: 'Brooklyn', rent: 3200, vibe: 'Leafy', description: 'Tree-lined streets, brownstones, and a strong community feel beside Prospect Park.', scores: [{ label: 'Affordability', value: 5 }, { label: 'Transit', value: 9 }, { label: 'Safety', value: 8 }, { label: 'Accessibility', value: 7 }, { label: 'Parks', value: 10 }], highlights: ['Steps from Prospect Park', 'Family friendly', 'Express subway access'] },
  { name: 'Riverdale', borough: 'The Bronx', rent: 1900, vibe: 'Quiet', description: 'A greener, quieter option for more space and a slower pace without leaving the city.', scores: [{ label: 'Affordability', value: 8 }, { label: 'Transit', value: 6 }, { label: 'Safety', value: 8 }, { label: 'Accessibility', value: 6 }, { label: 'Parks', value: 9 }], highlights: ['More space for less', 'Van Cortlandt Park', 'Residential streets'] },
  { name: 'Williamsburg', borough: 'Brooklyn', rent: 3500, vibe: 'Creative', description: 'Creative energy, waterfront views, and an easy commute into Manhattan.', scores: [{ label: 'Affordability', value: 4 }, { label: 'Transit', value: 9 }, { label: 'Safety', value: 7 }, { label: 'Accessibility', value: 8 }, { label: 'Parks', value: 8 }], highlights: ['Waterfront views', 'L train access', 'Independent shops'] },
]

function ScoreBar({ value }: { value: number }) {
  return <div className="mt-2 h-2 overflow-hidden rounded-full bg-muted"><div className="h-full rounded-full bg-[#10b981]" style={{ width: `${value * 10}%` }} /></div>
}

function NeighborhoodColumn({ data, onRemove }: { data: Neighborhood; onRemove: () => void }) {
  return <article className="relative rounded-2xl border border-border bg-card p-5 shadow-sm md:p-7">
    <button onClick={onRemove} aria-label={`Remove ${data.name}`} className="absolute right-4 top-4 rounded-full p-2 text-muted-foreground hover:bg-muted hover:text-foreground"><X size={17} /></button>
    <div className="pr-8"><p className="text-sm font-semibold text-primary">{data.borough}</p><h2 className="mt-2 text-3xl font-bold tracking-tight">{data.name}</h2><span className="mt-3 inline-flex rounded-full bg-[#dcfce7] px-3 py-1 text-xs font-semibold text-[#15803d]">{data.vibe}</span><p className="mt-5 text-sm leading-6 text-muted-foreground">{data.description}</p></div>
    <div className="mt-7 border-y border-border py-5"><span className="text-xs font-bold tracking-[.16em] text-muted-foreground">AVERAGE 1BR RENT</span><div className="mt-1 text-3xl font-bold">${data.rent.toLocaleString()}<span className="text-sm font-normal text-muted-foreground"> / month</span></div></div>
    <div className="mt-6 space-y-5">{data.scores.map(score => <div key={score.label}><div className="flex justify-between text-sm"><span>{score.label}</span><strong>{score.value}/10</strong></div><ScoreBar value={score.value} /></div>)}</div>
    <div className="mt-7"><p className="text-xs font-bold tracking-[.16em] text-muted-foreground">GOOD TO KNOW</p><ul className="mt-4 space-y-3">{data.highlights.map(item => <li key={item} className="flex items-center gap-2 text-sm"><Check size={16} className="text-[#16a34a]" />{item}</li>)}</ul></div>
    <Link href="/#explore-form" className="button-secondary mt-7 w-full justify-center">View full profile <ArrowRight size={16} /></Link>
  </article>
}

export default function ComparePage() {
  const [first, setFirst] = useState('Astoria')
  const [second, setSecond] = useState('Park Slope')
  const compared = useMemo(() => [neighborhoods.find(item => item.name === first)!, neighborhoods.find(item => item.name === second)!], [first, second])

  return <div className="min-h-screen bg-background"><header className="sticky top-0 z-50 border-b border-border/80 bg-background/95 backdrop-blur"><div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4 lg:px-8"><Link href="/" className="text-xl font-bold tracking-tight">NestMapper <span className="text-primary">NYC</span></Link><nav className="flex items-center gap-4 md:gap-7"><Link href="/" className="hidden text-sm text-muted-foreground hover:text-foreground sm:block">Explore</Link><Link href="/compare" className="text-sm font-semibold text-primary">Compare</Link><Link href="/#explore-form" className="button-primary px-4 py-2.5">Get started</Link></nav></div></header>
    <main><section className="mx-auto max-w-7xl px-5 pb-10 pt-12 lg:px-8 lg:pb-14 lg:pt-20"><Link href="/" className="inline-flex items-center gap-2 text-sm font-semibold text-muted-foreground hover:text-foreground"><ArrowLeft size={16} /> Back to explore</Link><div className="mt-9 max-w-3xl"><p className="eyebrow">SIDE BY SIDE, CLEAR AS DAY</p><h1 className="mt-3 text-balance text-4xl font-bold tracking-tight md:text-6xl">Compare neighborhoods with confidence.</h1><p className="mt-5 max-w-2xl text-base leading-7 text-muted-foreground md:text-lg">Put two NYC neighborhoods next to each other and see what really matters: rent, commute, safety, accessibility, and the feeling of home.</p></div></section>
      <section className="mx-auto max-w-7xl px-5 lg:px-8"><div className="grid gap-4 rounded-2xl border border-border bg-card p-4 md:grid-cols-[1fr_auto_1fr] md:items-end md:p-5"><label className="block text-sm font-semibold">First neighborhood<span className="relative mt-2 block"><select value={first} onChange={event => setFirst(event.target.value)} className="h-12 w-full appearance-none rounded-xl border border-border bg-background px-4 pr-10 text-base"><option value="Astoria">Astoria</option><option value="Park Slope">Park Slope</option><option value="Riverdale">Riverdale</option><option value="Williamsburg">Williamsburg</option></select><ChevronDown className="pointer-events-none absolute right-4 top-3.5 text-muted-foreground" size={18} /></span></label><div className="hidden items-center justify-center md:flex"><span className="flex size-10 items-center justify-center rounded-full bg-primary text-xs font-bold text-primary-foreground">VS</span></div><label className="block text-sm font-semibold">Second neighborhood<span className="relative mt-2 block"><select value={second} onChange={event => setSecond(event.target.value)} className="h-12 w-full appearance-none rounded-xl border border-border bg-background px-4 pr-10 text-base"><option value="Astoria">Astoria</option><option value="Park Slope">Park Slope</option><option value="Riverdale">Riverdale</option><option value="Williamsburg">Williamsburg</option></select><ChevronDown className="pointer-events-none absolute right-4 top-3.5 text-muted-foreground" size={18} /></span></label></div></section>
      <section className="mx-auto max-w-7xl px-5 py-8 lg:px-8 lg:py-10"><div className="mb-6 flex flex-wrap items-center justify-between gap-3"><div><p className="eyebrow">YOUR SHORTLIST</p><h2 className="mt-2 text-2xl font-bold">The details side by side</h2></div><span className="inline-flex items-center gap-2 text-sm text-muted-foreground"><ShieldCheck size={17} className="text-[#16a34a]" /> Independent neighborhood data</span></div><div className="grid gap-5 lg:grid-cols-2">{compared.map((item, index) => <NeighborhoodColumn key={`${item.name}-${index}`} data={item} onRemove={() => index === 0 ? setFirst('Astoria') : setSecond('Park Slope')} />)}</div></section>
      <section className="mx-auto max-w-7xl px-5 pb-16 lg:px-8"><div className="grid gap-4 rounded-2xl bg-[#0f1b31] p-7 text-white md:grid-cols-[1fr_auto] md:items-center md:p-10"><div><p className="text-xs font-bold tracking-[.18em] text-[#6ee7b7]">MAKE THE NEXT MOVE</p><h2 className="mt-3 text-2xl font-bold md:text-3xl">Not sure what fits your life?</h2><p className="mt-3 max-w-xl text-sm leading-6 text-white/70">Tell us your budget, lifestyle, and priorities. We'll help you build a shortlist worth seeing in person.</p></div><Link href="/#explore-form" className="button-light whitespace-nowrap">Get my match <ArrowRight size={16} /></Link></div></section>
    </main><footer className="border-t border-border"><div className="mx-auto flex max-w-7xl flex-col gap-3 px-5 py-8 text-sm text-muted-foreground sm:flex-row sm:items-center sm:justify-between lg:px-8"><Link href="/" className="font-semibold text-foreground">NestMapper <span className="text-primary">NYC</span></Link><span>Know before you move.</span><Link href="/" className="hover:text-foreground">Explore neighborhoods <ArrowRight className="ml-1 inline" size={14} /></Link></div></footer>
  </div>
}

function _unusedIcons() { return <><MapPin /><Train /><Plus /></> }
void _unusedIcons

export { neighborhoods }
