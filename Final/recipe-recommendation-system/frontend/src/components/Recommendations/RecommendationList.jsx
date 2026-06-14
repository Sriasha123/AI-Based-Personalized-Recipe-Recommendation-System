import React, { useEffect, useState } from 'react'
import { recommendationsAPI, reviewsAPI } from '../../services/api'
import { Star, Clock, X } from 'lucide-react'

export default function RecommendationList() {
  const [recipes, setRecipes] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedRecipe, setSelectedRecipe] = useState(null)
  const [rating, setRating] = useState(0)

  useEffect(() => {
    fetchRecommendations()
  }, [])

  const fetchRecommendations = async () => {
    setLoading(true)
    try {
      const res = await recommendationsAPI.personalized()
      setRecipes(res.data)
    } catch (err) {
      alert('Error loading recommendations. Login required.')
    }
    setLoading(false)
  }

  // ⭐ Submit feedback
  const submitRating = async (recipeId, value) => {
    try {
      await reviewsAPI.create({
        recipe_id: recipeId,
        rating: value
      })
      alert('Feedback saved! 👍')
      fetchRecommendations()
    } catch (err) {
      alert('Failed to save feedback')
    }
  }

  return (
    <div>
      <h1 className="text-4xl font-bold mb-8">Personalized Recommendations</h1>

      {loading ? (
        <p className="text-center">Loading...</p>
      ) : (
        <div className="grid md:grid-cols-3 gap-6">
          {recipes.map(recipe => (
            <div
              key={recipe.id}
              onClick={() => setSelectedRecipe(recipe)}
              className="bg-white rounded-xl shadow-lg p-6 cursor-pointer hover:shadow-xl transition"
            >
              <h3 className="text-xl font-bold mb-2">{recipe.name}</h3>

              <p className="text-gray-600 line-clamp-2">
                Click to view full recipe
              </p>

              <div className="flex justify-between items-center mt-4 text-sm text-gray-500">
                <div className="flex items-center">
                  <Clock size={16} className="mr-1" />
                  {recipe.minutes || 'N/A'} min
                </div>
                {recipe.cuisine && (
                  <span className="bg-indigo-100 text-indigo-700 px-2 py-1 rounded-full text-xs">
                    {recipe.cuisine}
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* 🧾 MODAL */}
      {selectedRecipe && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
          <div className="bg-white w-full max-w-3xl rounded-xl p-6 overflow-y-auto max-h-[90vh]">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-bold">{selectedRecipe.name}</h2>
              <X
                className="cursor-pointer"
                onClick={() => {
                  setSelectedRecipe(null)
                  setRating(0)
                }}
              />
            </div>

            {/* ⏱ Info */}
            <div className="flex gap-4 text-sm text-gray-600 mb-4">
              <span>⏱ {selectedRecipe.minutes || 'N/A'} min</span>
              <span>🍽 {selectedRecipe.cuisine || 'General'}</span>
            </div>

            {/* 🥕 Ingredients */}
            <h3 className="font-semibold mb-2">Ingredients</h3>
            <ul className="list-disc pl-6 mb-4">
              {selectedRecipe.ingredients.map((ing, idx) => (
                <li key={idx}>{ing}</li>
              ))}
            </ul>

            {/* 👩‍🍳 Steps */}
            <h3 className="font-semibold mb-2">Cooking Steps</h3>
            <ol className="list-decimal pl-6 space-y-2 mb-6">
              {selectedRecipe.steps.map((step, idx) => (
                <li key={idx}>{step}</li>
              ))}
            </ol>

            {/* ⭐ FEEDBACK */}
            <h3 className="font-semibold mb-2">Rate this recipe</h3>
            <div className="flex gap-2 mb-4">
              {[1, 2, 3, 4, 5].map(num => (
                <Star
                  key={num}
                  size={28}
                  className={`cursor-pointer ${
                    num <= rating
                      ? 'text-yellow-400 fill-yellow-400'
                      : 'text-gray-400'
                  }`}
                  onClick={() => {
                    setRating(num)
                    submitRating(selectedRecipe.recipe_id, num)
                  }}
                />
              ))}
            </div>

            <button
              onClick={() => setSelectedRecipe(null)}
              className="mt-4 bg-indigo-600 text-white px-4 py-2 rounded"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
