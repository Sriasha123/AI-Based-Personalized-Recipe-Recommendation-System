import React from 'react'
import { X, Clock } from 'lucide-react'

export default function RecipeDetailsModal({ recipe, onClose }) {
  if (!recipe) return null

  return (
    <div className="fixed inset-0 z-50 bg-black bg-opacity-50 flex justify-center items-center p-4">
      <div className="bg-white rounded-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto shadow-xl">
        
        {/* Header */}
        <div className="flex justify-between items-center p-6 border-b">
          <h2 className="text-2xl font-bold">{recipe.name}</h2>
          <button onClick={onClose}>
            <X size={28} />
          </button>
        </div>

        {/* Body */}
        <div className="p-6 space-y-6">

          {/* Meta */}
          <div className="flex flex-wrap gap-4 text-sm text-gray-600">
            {recipe.cuisine && (
              <span className="bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full">
                {recipe.cuisine}
              </span>
            )}

            <div className="flex items-center">
              <Clock size={16} className="mr-1" />
              {recipe.minutes || 'N/A'} min
            </div>
          </div>

          {/* Ingredients */}
          {recipe.ingredients?.length > 0 && (
            <div>
              <h3 className="text-lg font-semibold mb-2">Ingredients</h3>
              <ul className="list-disc list-inside space-y-1 text-gray-700">
                {recipe.ingredients.map((item, idx) => (
                  <li key={idx}>{item}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Steps */}
          {recipe.steps?.length > 0 && (
            <div>
              <h3 className="text-lg font-semibold mb-2">Cooking Steps</h3>
              <ol className="list-decimal list-inside space-y-2 text-gray-700">
                {recipe.steps.map((step, idx) => (
                  <li key={idx}>{step}</li>
                ))}
              </ol>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
