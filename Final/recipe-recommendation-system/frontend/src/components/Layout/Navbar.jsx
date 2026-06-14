import React from 'react'
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
                <Link to="/ai-generator" className="hover:text-indigo-200 transition">AI Generator</Link>
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