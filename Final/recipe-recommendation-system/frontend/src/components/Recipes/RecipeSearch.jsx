import React, { useState, useEffect } from 'react'
import { recipesAPI } from '../../services/api'
import { Search, Clock } from 'lucide-react'

export default function RecipeSearch() {
  const [recipes, setRecipes] = useState([])
  const [query, setQuery] = useState('')
  const [cuisine, setCuisine] = useState('')
  const [maxCalories, setMaxCalories] = useState('')
  const [loading, setLoading] = useState(false)
  const [expandedId, setExpandedId] = useState(null)

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

      {/* Search Filters */}
      <div className="bg-white p-6 rounded-xl shadow-lg mb-8">
        <div className="grid md:grid-cols-4 gap-4">
          <input
            type="text"
            placeholder="Search by name..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="px-4 py-3 border rounded-lg"
          />

          <select
            value={cuisine}
            onChange={(e) => setCuisine(e.target.value)}
            className="px-4 py-3 border rounded-lg"
          >
            <option value="">All Cuisines</option>
            <option value="Indian">Indian</option>
            <option value="Chinese">Chinese</option>
            <option value="Italian">Italian</option>
            <option value="American">American</option>
          </select>

          <input
            type="number"
            placeholder="Max Calories"
            value={maxCalories}
            onChange={(e) => setMaxCalories(e.target.value)}
            className="px-4 py-3 border rounded-lg"
          />

          <button
            onClick={searchRecipes}
            className="bg-indigo-600 text-white px-6 py-3 rounded-lg flex justify-center items-center"
          >
            <Search size={18} className="mr-2" /> Search
          </button>
        </div>
      </div>

      {/* Results */}
      {loading ? (
        <p className="text-center text-gray-600">Loading recipes...</p>
      ) : recipes.length > 0 ? (
        <div className="grid md:grid-cols-3 gap-6">
          {recipes.map((recipe) => (
            <div key={recipe.id} className="bg-white p-6 rounded-xl shadow">
              <h3 className="text-xl font-bold mb-2">{recipe.name}</h3>

              <div className="flex justify-between text-sm text-gray-600 mb-2">
                <div className="flex items-center">
                  <Clock size={14} className="mr-1" />
                  {recipe.minutes ?? 'N/A'} min
                </div>

                {recipe.nutrition?.calories && (
                  <span className="font-semibold text-indigo-600">
                    {Math.round(recipe.nutrition.calories)} cal
                  </span>
                )}
              </div>

              {recipe.cuisine && (
                <span className="inline-block bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full text-xs mb-3">
                  {recipe.cuisine}
                </span>
              )}

              {/* Steps */}
              <button
                onClick={() =>
                  setExpandedId(expandedId === recipe.id ? null : recipe.id)
                }
                className="text-indigo-600 font-medium mt-3"
              >
                {expandedId === recipe.id ? 'Hide Steps' : 'View Steps'}
              </button>

              {expandedId === recipe.id && (
                <ol className="list-decimal list-inside text-sm text-gray-700 mt-3 space-y-1">
                  {recipe.steps?.map((step, i) => (
                    <li key={i}>{step}</li>
                  ))}
                </ol>
              )}
            </div>
          ))}
        </div>
      ) : (
        <p className="text-center text-gray-600">
          No recipes found.
        </p>
      )}
    </div>
  )
}
