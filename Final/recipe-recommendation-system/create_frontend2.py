"""
Create Remaining Frontend Components
Save as: create_frontend_part2.py
Run from: Desktop/Final/recipe-recommendation-system/
"""

import os

# Component files and their contents
files = {
    "frontend/src/components/Recipes/RecipeSearch.jsx": """import React, { useState, useEffect } from 'react'
import { recipesAPI } from '../../services/api'
import { Search, Clock } from 'lucide-react'

export default function RecipeSearch() {
  const [recipes, setRecipes] = useState([])
  const [query, setQuery] = useState('')
  const [cuisine, setCuisine] = useState('')
  const [maxCalories, setMaxCalories] = useState('')
  const [loading, setLoading] = useState(false)

  const searchRecipes = async () => {
    setLoading(true)
    try {
      const params = {}
      if (query) params.query = query
      if (cuisine) params.cuisine = cuisine
      if (maxCalories) params.max_calories = maxCalories
      
      const res = await recipesAPI.search(params)
      setRecipes(res.data)
    } catch (error) {
      console.error('Search error:', error)
      alert('Error searching recipes. Make sure backend is running!')
    }
    setLoading(false)
  }

  useEffect(() => {
    searchRecipes()
  }, [])

  return (
    <div>
      <h1 className="text-4xl font-bold mb-8">Search Recipes</h1>
      
      <div className="bg-white p-6 rounded-xl shadow-lg mb-8">
        <div className="grid md:grid-cols-4 gap-4">
          <input
            type="text"
            placeholder="Search by name..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          
          <select
            value={cuisine}
            onChange={(e) => setCuisine(e.target.value)}
            className="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="">All Cuisines</option>
            <option value="italian">Italian</option>
            <option value="mexican">Mexican</option>
            <option value="indian">Indian</option>
            <option value="chinese">Chinese</option>
            <option value="american">American</option>
          </select>
          
          <input
            type="number"
            placeholder="Max Calories"
            value={maxCalories}
            onChange={(e) => setMaxCalories(e.target.value)}
            className="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          
          <button
            onClick={searchRecipes}
            className="bg-indigo-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-indigo-700 flex items-center justify-center transition"
          >
            <Search size={20} className="mr-2" />
            Search
          </button>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="text-xl text-gray-600">Loading recipes...</div>
        </div>
      ) : recipes.length > 0 ? (
        <div className="grid md:grid-cols-3 gap-6">
          {recipes.map((recipe) => (
            <div key={recipe.id} className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition">
              <div className="p-6">
                <h3 className="text-xl font-bold mb-2">{recipe.name}</h3>
                <p className="text-gray-600 mb-4 line-clamp-2">{recipe.description || 'Delicious recipe!'}</p>
                
                <div className="flex items-center justify-between text-sm text-gray-500">
                  <div className="flex items-center">
                    <Clock size={16} className="mr-1" />
                    <span>{recipe.minutes || 'N/A'} min</span>
                  </div>
                  {recipe.nutrition && (
                    <div className="font-semibold text-indigo-600">
                      {Math.round(recipe.nutrition[0])} cal
                    </div>
                  )}
                </div>
                
                {recipe.cuisine && (
                  <div className="mt-4">
                    <span className="inline-block bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full text-sm">
                      {recipe.cuisine}
                    </span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12 bg-white rounded-xl shadow-lg">
          <p className="text-xl text-gray-600">No recipes found. Try different search criteria.</p>
        </div>
      )}
    </div>
  )
}
""",

    "frontend/src/components/MealPlanner/MealPlanCalendar.jsx": """import React, { useState, useEffect } from 'react'
import { mealPlannerAPI, groceryAPI } from '../../services/api'
import { Calendar, Plus, ShoppingBag } from 'lucide-react'

export default function MealPlanCalendar() {
  const [mealPlans, setMealPlans] = useState([])
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [loading, setLoading] = useState(false)
  const [groceryList, setGroceryList] = useState(null)

  useEffect(() => {
    fetchMealPlans()
  }, [])

  const fetchMealPlans = async () => {
    try {
      const res = await mealPlannerAPI.getPlans()
      setMealPlans(res.data)
    } catch (error) {
      console.error('Error fetching meal plans:', error)
    }
  }

  const generateMealPlan = async () => {
    setLoading(true)
    try {
      const data = {
        week_start_date: new Date().toISOString(),
        dietary_goal: 'balanced',
        target_calories: 2000
      }
      await mealPlannerAPI.generate(data)
      await fetchMealPlans()
      setShowCreateForm(false)
      alert('Meal plan generated successfully!')
    } catch (error) {
      console.error('Error generating meal plan:', error)
      alert('Error generating meal plan. Make sure you have enough recipes!')
    }
    setLoading(false)
  }

  const fetchGroceryList = async (planId) => {
    try {
      const res = await groceryAPI.getList(planId)
      setGroceryList(res.data)
    } catch (error) {
      console.error('Error fetching grocery list:', error)
      alert('Error fetching grocery list')
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center">
          <Calendar className="text-indigo-600 mr-3" size={36} />
          <h1 className="text-4xl font-bold">Meal Planner</h1>
        </div>
        <button
          onClick={() => setShowCreateForm(true)}
          className="bg-indigo-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-indigo-700 flex items-center transition"
        >
          <Plus size={20} className="mr-2" />
          New Meal Plan
        </button>
      </div>

      {showCreateForm && (
        <div className="bg-white p-6 rounded-xl shadow-lg mb-8">
          <h2 className="text-2xl font-bold mb-4">Generate New Meal Plan</h2>
          <p className="text-gray-600 mb-4">
            Create a personalized 7-day meal plan based on your preferences
          </p>
          <div className="flex space-x-4">
            <button
              onClick={generateMealPlan}
              disabled={loading}
              className="bg-indigo-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-indigo-700 disabled:bg-gray-400 transition"
            >
              {loading ? 'Generating...' : 'Generate Plan'}
            </button>
            <button
              onClick={() => setShowCreateForm(false)}
              className="bg-gray-200 text-gray-800 px-6 py-3 rounded-lg font-semibold hover:bg-gray-300 transition"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      <div className="space-y-6">
        {mealPlans.map((plan) => (
          <div key={plan.id} className="bg-white rounded-xl shadow-lg overflow-hidden">
            <div className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="text-2xl font-bold">
                    Week of {new Date(plan.week_start_date).toLocaleDateString()}
                  </h3>
                  <p className="text-gray-600">
                    Total: {Math.round(plan.total_calories)} calories
                  </p>
                </div>
                <button
                  onClick={() => fetchGroceryList(plan.id)}
                  className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center transition"
                >
                  <ShoppingBag size={18} className="mr-2" />
                  Grocery List
                </button>
              </div>

              <div className="grid md:grid-cols-7 gap-4">
                {Object.entries(plan.meals).map(([day, data]) => (
                  <div key={day} className="border rounded-lg p-3">
                    <h4 className="font-bold text-sm mb-2">{day}</h4>
                    <div className="space-y-2 text-xs">
                      {data.meals && (
                        <>
                          <div className="bg-yellow-50 p-2 rounded">
                            <div className="font-semibold">🍳 Breakfast</div>
                            <div className="text-gray-600 truncate" title={data.meals.breakfast?.name}>
                              {data.meals.breakfast?.name}
                            </div>
                          </div>
                          <div className="bg-blue-50 p-2 rounded">
                            <div className="font-semibold">🍽️ Lunch</div>
                            <div className="text-gray-600 truncate" title={data.meals.lunch?.name}>
                              {data.meals.lunch?.name}
                            </div>
                          </div>
                          <div className="bg-purple-50 p-2 rounded">
                            <div className="font-semibold">🌙 Dinner</div>
                            <div className="text-gray-600 truncate" title={data.meals.dinner?.name}>
                              {data.meals.dinner?.name}
                            </div>
                          </div>
                        </>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>

      {mealPlans.length === 0 && !showCreateForm && (
        <div className="text-center py-12 bg-white rounded-xl shadow-lg">
          <Calendar className="mx-auto text-gray-400 mb-4" size={64} />
          <p className="text-xl text-gray-600 mb-4">No meal plans yet</p>
          <button
            onClick={() => setShowCreateForm(true)}
            className="bg-indigo-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-indigo-700 transition"
          >
            Create Your First Meal Plan
          </button>
        </div>
      )}

      {groceryList && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4">🛒 Grocery List</h2>
            <p className="text-gray-600 mb-4">Total items: {groceryList.total}</p>
            <div className="space-y-2 mb-6">
              {groceryList.ingredients.map((item, idx) => (
                <div key={idx} className="flex items-center p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition">
                  <input type="checkbox" className="mr-3 w-5 h-5" />
                  <span className="flex-1">{item}</span>
                </div>
              ))}
            </div>
            <button
              onClick={() => setGroceryList(null)}
              className="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 transition"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
""",

    "frontend/src/components/Recommendations/RecommendationList.jsx": """import React, { useState, useEffect } from 'react'
import { recommendationsAPI } from '../../services/api'
import { Star, Clock, TrendingUp } from 'lucide-react'

export default function RecommendationList() {
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchRecommendations()
  }, [])

  const fetchRecommendations = async () => {
    setLoading(true)
    try {
      const res = await recommendationsAPI.personalized()
      setRecommendations(res.data)
    } catch (error) {
      console.error('Error fetching recommendations:', error)
      alert('Error loading recommendations. Make sure you are logged in!')
    }
    setLoading(false)
  }

  return (
    <div>
      <div className="flex items-center mb-8">
        <TrendingUp className="text-indigo-600 mr-3" size={36} />
        <h1 className="text-4xl font-bold">Personalized Recommendations</h1>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <div className="text-xl text-gray-600">Loading recommendations...</div>
        </div>
      ) : recommendations.length > 0 ? (
        <div className="grid md:grid-cols-3 gap-6">
          {recommendations.map((recipe) => (
            <div key={recipe.id} className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition">
              <div className="p-6">
                <div className="flex items-start justify-between mb-2">
                  <h3 className="text-xl font-bold flex-1">{recipe.name}</h3>
                  <Star className="text-yellow-400 fill-current" size={24} />
                </div>
                
                <p className="text-gray-600 mb-4 line-clamp-3">
                  {recipe.description || 'Delicious recipe recommended just for you!'}
                </p>
                
                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center text-gray-500">
                    <Clock size={16} className="mr-1" />
                    <span>{recipe.minutes || 'N/A'} min</span>
                  </div>
                  {recipe.nutrition && (
                    <div className="font-semibold text-indigo-600">
                      {Math.round(recipe.nutrition[0])} cal
                    </div>
                  )}
                </div>
                
                {recipe.dietary_tags && recipe.dietary_tags.length > 0 && (
                  <div className="mt-4 flex flex-wrap gap-2">
                    {recipe.dietary_tags.slice(0, 3).map((tag, idx) => (
                      <span key={idx} className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs">
                        {tag}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12 bg-white rounded-xl shadow-lg">
          <p className="text-xl text-gray-600">No recommendations available yet.</p>
          <p className="text-gray-500">Try rating some recipes to get personalized suggestions!</p>
        </div>
      )}
    </div>
  )
}
"""
}

print("Creating frontend component files...\n")

for filepath, content in files.items():
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        print(f"✅ Created: {filepath}")
    except Exception as e:
        print(f"❌ Error creating {filepath}: {e}")

print("\n✅ ALL FRONTEND FILES CREATED SUCCESSFULLY!")
