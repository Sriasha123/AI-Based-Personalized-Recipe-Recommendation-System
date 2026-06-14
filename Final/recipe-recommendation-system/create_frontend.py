"""
Create All Frontend Files
Save as: create_frontend.py
Run from: Desktop/Final/recipe-recommendation-system/
"""

import os

files = {
    "frontend/vite.config.js": """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
""",

    "frontend/tailwind.config.js": """export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
}
""",

    "frontend/postcss.config.js": """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
""",

    "frontend/src/index.css": """@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
""",

    "frontend/src/main.jsx": """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
""",

    "frontend/src/App.jsx": """import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import Navbar from './components/Layout/Navbar'
import Login from './components/Auth/Login'
import Signup from './components/Auth/Signup'
import Home from './pages/Home'
import RecipeSearch from './components/Recipes/RecipeSearch'
import Recommendations from './components/Recommendations/RecommendationList'
import MealPlanner from './components/MealPlanner/MealPlanCalendar'

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth()
  return isAuthenticated ? children : <Navigate to="/login" />
}

function AppContent() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="container mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/recipes" element={<RecipeSearch />} />
          <Route path="/recommendations" element={
            <ProtectedRoute><Recommendations /></ProtectedRoute>
          } />
          <Route path="/meal-planner" element={
            <ProtectedRoute><MealPlanner /></ProtectedRoute>
          } />
        </Routes>
      </main>
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </BrowserRouter>
  )
}
""",

    "frontend/src/services/api.js": """import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

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

export const authAPI = {
  signup: (data) => api.post('/auth/signup', data),
  login: (data) => api.post('/auth/login', new URLSearchParams(data), {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  }),
}

export const recipesAPI = {
  search: (params) => api.get('/recipes/search', { params }),
  getById: (id) => api.get(`/recipes/${id}`),
}

export const recommendationsAPI = {
  get: (params) => api.get('/recommendations/', { params }),
  personalized: () => api.get('/recommendations/personalized'),
  similar: (recipeId) => api.get(`/recommendations/similar/${recipeId}`),
}

export const reviewsAPI = {
  create: (data) => api.post('/reviews/', data),
  getByRecipe: (recipeId) => api.get(`/reviews/recipe/${recipeId}`),
}

export const mealPlannerAPI = {
  generate: (data) => api.post('/meal-planner/generate', data),
  getPlans: () => api.get('/meal-planner/plans'),
  getPlan: (id) => api.get(`/meal-planner/plans/${id}`),
}

export const groceryAPI = {
  getList: (mealPlanId) => api.get(`/grocery/list/${mealPlanId}`),
}

export default api
""",

    "frontend/src/context/AuthContext.jsx": """import React, { createContext, useState, useContext, useEffect } from 'react'
import { authAPI } from '../services/api'

const AuthContext = createContext(null)

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      setUser(JSON.parse(storedUser))
    }
    setLoading(false)
  }, [])

  const login = async (email, password) => {
    try {
      const response = await authAPI.login({ username: email, password })
      const { access_token } = response.data
      
      localStorage.setItem('token', access_token)
      setToken(access_token)
      
      const userData = { email }
      localStorage.setItem('user', JSON.stringify(userData))
      setUser(userData)
      
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      }
    }
  }

  const signup = async (userData) => {
    try {
      await authAPI.signup(userData)
      return await login(userData.email, userData.password)
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Signup failed' 
      }
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setToken(null)
    setUser(null)
  }

  const value = {
    user,
    token,
    login,
    signup,
    logout,
    isAuthenticated: !!token,
    loading
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
""",

    "frontend/src/pages/Home.jsx": """import React from 'react'
import { Link } from 'react-router-dom'
import { ChefHat, Brain, Calendar, ShoppingCart } from 'lucide-react'

export default function Home() {
  return (
    <div className="text-center">
      <div className="mb-12">
        <h1 className="text-5xl font-bold text-gray-800 mb-4">
          AI-Powered Recipe Recommendations
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Discover personalized recipes, plan meals, and generate grocery lists with AI
        </p>
        <Link 
          to="/signup" 
          className="inline-block bg-indigo-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-indigo-700 transition"
        >
          Get Started Free
        </Link>
      </div>

      <div className="grid md:grid-cols-4 gap-8 mt-16">
        <div className="p-6 bg-white rounded-xl shadow-lg">
          <ChefHat className="mx-auto mb-4 text-indigo-600" size={48} />
          <h3 className="text-xl font-bold mb-2">Smart Search</h3>
          <p className="text-gray-600">Find recipes based on ingredients, cuisine, and dietary needs</p>
        </div>
        
        <div className="p-6 bg-white rounded-xl shadow-lg">
          <Brain className="mx-auto mb-4 text-indigo-600" size={48} />
          <h3 className="text-xl font-bold mb-2">AI Recommendations</h3>
          <p className="text-gray-600">Get personalized suggestions based on your taste</p>
        </div>
        
        <div className="p-6 bg-white rounded-xl shadow-lg">
          <Calendar className="mx-auto mb-4 text-indigo-600" size={48} />
          <h3 className="text-xl font-bold mb-2">Meal Planning</h3>
          <p className="text-gray-600">Generate weekly meal plans tailored to your goals</p>
        </div>
        
        <div className="p-6 bg-white rounded-xl shadow-lg">
          <ShoppingCart className="mx-auto mb-4 text-indigo-600" size={48} />
          <h3 className="text-xl font-bold mb-2">Grocery Lists</h3>
          <p className="text-gray-600">Auto-generate shopping lists from meal plans</p>
        </div>
      </div>
    </div>
  )
}
""",

    "frontend/src/components/Layout/Navbar.jsx": """import React from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { ChefHat, LogOut } from 'lucide-react'

export default function Navbar() {
  const { user, logout, isAuthenticated } = useAuth()

  return (
    <nav className="bg-indigo-600 text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center space-x-2 font-bold text-xl">
            <ChefHat size={28} />
            <span>AI Recipe</span>
          </Link>
          
          <div className="flex items-center space-x-6">
            <Link to="/recipes" className="hover:text-indigo-200 transition">Recipes</Link>
            {isAuthenticated ? (
              <>
                <Link to="/recommendations" className="hover:text-indigo-200 transition">Recommendations</Link>
                <Link to="/meal-planner" className="hover:text-indigo-200 transition">Meal Planner</Link>
                <button 
                  onClick={logout} 
                  className="flex items-center space-x-1 hover:text-indigo-200 transition"
                >
                  <LogOut size={18} />
                  <span>Logout</span>
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="hover:text-indigo-200 transition">Login</Link>
                <Link 
                  to="/signup" 
                  className="bg-white text-indigo-600 px-4 py-2 rounded-lg font-semibold hover:bg-indigo-50 transition"
                >
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}
""",

    "frontend/src/components/Auth/Login.jsx": """import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    
    const result = await login(email, password)
    
    if (result.success) {
      navigate('/recommendations')
    } else {
      setError(result.error)
    }
    setLoading(false)
  }

  return (
    <div className="max-w-md mx-auto mt-16 p-8 bg-white rounded-xl shadow-lg">
      <h2 className="text-3xl font-bold text-center mb-6">Login</h2>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
          <input
            type="email"
            placeholder="your@email.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Password</label>
          <input
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
        </div>
        
        <button 
          type="submit" 
          disabled={loading}
          className="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 transition disabled:bg-gray-400"
        >
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      
      <p className="text-center mt-4 text-gray-600">
        Don't have an account?{' '}
        <Link to="/signup" className="text-indigo-600 hover:underline font-semibold">
          Sign Up
        </Link>
      </p>
    </div>
  )
}
""",

    "frontend/src/components/Auth/Signup.jsx": """import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

export default function Signup() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    full_name: '',
    age: '',
    dietary_type: '',
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { signup } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    
    const result = await signup({
      ...formData,
      age: formData.age ? parseInt(formData.age) : null,
      health_conditions: []
    })
    
    if (result.success) {
      navigate('/recommendations')
    } else {
      setError(result.error)
    }
    setLoading(false)
  }

  return (
    <div className="max-w-2xl mx-auto mt-16 p-8 bg-white rounded-xl shadow-lg">
      <h2 className="text-3xl font-bold text-center mb-6">Sign Up</h2>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
            <input
              type="text"
              placeholder="John Doe"
              value={formData.full_name}
              onChange={(e) => setFormData({...formData, full_name: e.target.value})}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
            <input
              type="email"
              placeholder="your@email.com"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              required
            />
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Password</label>
            <input
              type="password"
              placeholder="••••••••"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Age (Optional)</label>
            <input
              type="number"
              placeholder="25"
              value={formData.age}
              onChange={(e) => setFormData({...formData, age: e.target.value})}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Dietary Preference (Optional)</label>
          <select
            value={formData.dietary_type}
            onChange={(e) => setFormData({...formData, dietary_type: e.target.value})}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="">Select...</option>
            <option value="vegetarian">Vegetarian</option>
            <option value="vegan">Vegan</option>
            <option value="keto">Keto</option>
            <option value="paleo">Paleo</option>
            <option value="gluten-free">Gluten-Free</option>
          </select>
        </div>
        
        <button 
          type="submit"
          disabled={loading}
          className="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 transition disabled:bg-gray-400"
        >
          {loading ? 'Creating Account...' : 'Sign Up'}
        </button>
      </form>
      
      <p className="text-center mt-4 text-gray-600">
        Already have an account?{' '}
        <Link to="/login" className="text-indigo-600 hover:underline font-semibold">
          Login
        </Link>
      </p>
    </div>
  )
}
"""
}

print("Creating all frontend files...\n")

for filepath, content in files.items():
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        print(f"✅ Created: {filepath}")
    except Exception as e:
        print(f"❌ Error creating {filepath}: {e}")

print("\n✅ Part 1 of frontend files created!")
print("Creating remaining components...\n")