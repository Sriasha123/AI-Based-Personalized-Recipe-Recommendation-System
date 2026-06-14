import React from 'react'
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