import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import Navbar from './components/Layout/Navbar'
import Login from './components/Auth/Login'
import Signup from './components/Auth/Signup'
import Home from './pages/Home'
import RecipeSearch from './components/Recipes/RecipeSearch'
import Recommendations from './components/Recommendations/RecommendationList'
import MealPlanner from './components/MealPlanner/MealPlanCalendar'
import RecipeGenerator from './components/AIGenerator/RecipeGenerator'

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
          <Route path="/ai-generator" element={
            <ProtectedRoute><RecipeGenerator /></ProtectedRoute>
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