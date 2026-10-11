import axios from 'axios'

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Get all neighborhoods
export const getNeighborhoods = async () => {
  const response = await api.get('/api/neighborhoods/')
  return response.data
}

// Get single neighborhood
export const getNeighborhood = async (id: number) => {
  const response = await api.get(`/api/neighborhoods/${id}/`)
  return response.data
}

// Get neighborhoods by borough
export const getNeighborhoodsByBorough = async (borough: string) => {
  const response = await api.get(`/api/boroughs/${borough}/`)
  return response.data
}

// Search neighborhoods
export const searchNeighborhoods = async (query: string) => {
  const response = await api.get(`/api/search/?q=${query}`)
  return response.data
}

// Get similar neighborhoods
export const getSimilarNeighborhoods = async (id: number) => {
  const response = await api.get(`/api/neighborhoods/${id}/similar/`)
  return response.data
}

// Get neighborhood trend
export const getNeighborhoodTrend = async (id: number) => {
  const response = await api.get(`/api/neighborhoods/${id}/trend/`)
  return response.data
}

// Get affordability
export const getAffordability = async (id: number, income?: number) => {
  const url = income
    ? `/api/neighborhoods/${id}/affordability/?income=${income}`
    : `/api/neighborhoods/${id}/affordability/`

  const response = await api.get(url)
  return response.data
}

// Compare neighborhoods
export const compareNeighborhoods = async (ids: number[]) => {
  const response = await api.get(`/api/compare/?ids=${ids.join(',')}`)
  return response.data
}

// Get recommendations
export const getRecommendations = async (preferences: object) => {
  const response = await api.post('/api/recommend/', preferences)
  return response.data
}

// Get all trends
export const getAllTrends = async () => {
  const response = await api.get('/api/trends/')
  return response.data
}

export default api