import axios from 'axios'

/* ----------------------------------
   AXIOS INSTANCE
----------------------------------- */
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

/* ----------------------------------
   AUTH TOKEN INTERCEPTOR
----------------------------------- */
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

/* ----------------------------------
   AUTH API
----------------------------------- */
export const authAPI = {
  signup: (data) => api.post('/auth/signup', data),
  login: (data) =>
    api.post('/auth/login', new URLSearchParams(data), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }),
}

/* ----------------------------------
   RECIPES API
----------------------------------- */
export const recipesAPI = {
  search: (params) => api.get('/recipes/search', { params }),
  getById: (id) => api.get(`/recipes/${id}`),
}

/* ----------------------------------
   REVIEWS API
----------------------------------- */
export const reviewsAPI = {
  create: (data) => api.post('/reviews/', data),
  getByRecipe: (recipeId) => api.get(`/reviews/recipe/${recipeId}`),
}

/* ----------------------------------
   RECOMMENDATIONS API
----------------------------------- */
export const recommendationsAPI = {
  get: (params) => api.get('/recommendations/', { params }),
  personalized: () =>
    api.get('/recommendations/enhanced/smart-personalized'),
  similar: (recipeId) =>
    api.get(`/recommendations/similar/${recipeId}`),
}

/* ----------------------------------
   MEAL PLANNER API
----------------------------------- */
export const mealPlannerAPI = {
  generate: (data) => api.post('/meal-planner/generate', data),
  getPlans: () => api.get('/meal-planner/plans'),
  getPlan: (id) => api.get(`/meal-planner/plans/${id}`),
}

/* ----------------------------------
   GROCERY API
----------------------------------- */
export const groceryAPI = {
  getList: (mealPlanId) =>
    api.get(`/grocery/list/${mealPlanId}`),
}

/* ----------------------------------
   ⭐ AI GENERATOR API (FIXED)
----------------------------------- */
export const aiGeneratorAPI = {
  // Rule-based generator
  generate: (data) =>
    api.post('/ai-generator/generate', data),

  // ⭐ SMART PROFILE-AWARE AI (LLM)
  generateSmart: (ingredients) =>
    api.post('/ai-generator/generate-smart', {
      ingredients,
    }),

  substitute: (data) =>
    api.post('/ai-generator/substitute', data),

  generateFromPantry: (items) =>
    api.post('/ai-generator/generate-from-pantry', items),

  getCuisines: () =>
    api.get('/ai-generator/cuisines'),

  getDifficultyLevels: () =>
    api.get('/ai-generator/difficulty-levels'),
}

export default api
