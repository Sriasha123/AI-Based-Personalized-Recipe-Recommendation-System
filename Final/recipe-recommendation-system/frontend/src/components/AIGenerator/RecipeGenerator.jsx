import React, { useState } from 'react'
import { Wand2, Plus, X, Image as ImageIcon } from 'lucide-react'
import api from '../../services/api'

export default function RecipeGenerator() {
  const [ingredients, setIngredients] = useState([])
  const [currentIngredient, setCurrentIngredient] = useState('')
  const [imageFile, setImageFile] = useState(null)
  const [generatedRecipe, setGeneratedRecipe] = useState(null)
  const [detectedIngredients, setDetectedIngredients] = useState([])
  const [loading, setLoading] = useState(false)

  /* ===========================
     INGREDIENT INPUT
  ============================ */
  const addIngredient = () => {
    if (currentIngredient.trim()) {
      setIngredients((prev) => [...prev, currentIngredient.trim()])
      setCurrentIngredient('')
    }
  }

  const removeIngredient = (index) => {
    setIngredients((prev) => prev.filter((_, i) => i !== index))
  }

  /* ===========================
     IMAGE INPUT
  ============================ */
  const handleImageChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      setImageFile(file)
      setIngredients([]) // avoid confusion
    }
  }

  /* ===========================
     TEXT → SMART AI
  ============================ */
  const generateFromText = async () => {
    if (ingredients.length < 2) {
      alert('Please add at least 2 ingredients')
      return
    }

    setLoading(true)
    setGeneratedRecipe(null)
    setDetectedIngredients([])

    try {
      const res = await api.post('/ai-generator/generate-smart', {
        ingredients,
      })

      setGeneratedRecipe(res.data.recipe ?? res.data)
    } catch (error) {
      console.error(error)
      alert(error.response?.data?.detail || 'Recipe generation failed')
    } finally {
      setLoading(false)
    }
  }

  /* ===========================
     IMAGE → SMART AI
  ============================ */
  const generateFromImage = async () => {
    if (!imageFile) {
      alert('Please upload an ingredient image')
      return
    }

    setLoading(true)
    setGeneratedRecipe(null)
    setDetectedIngredients([])

    try {
      const formData = new FormData()
      formData.append('image', imageFile)

      const res = await api.post(
        '/ai-generator/generate-from-image',
        formData,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      )

      setDetectedIngredients(res.data.detected_ingredients || [])
      setGeneratedRecipe(res.data.recipe)
    } catch (error) {
      console.error(error)
      alert(error.response?.data?.detail || 'Image processing failed')
    } finally {
      setLoading(false)
    }
  }

  /* ===========================
     SAFE RENDER
  ============================ */
  const renderIngredient = (ing) => {
    if (typeof ing === 'string') return ing
    if (typeof ing === 'object' && ing !== null) {
      return `${ing.name || ''} ${ing.quantity || ''} ${ing.notes || ''}`.trim()
    }
    return ''
  }

  /* ===========================
     UI
  ============================ */
  return (
    <div className="max-w-6xl mx-auto px-4 py-6">
      {/* HEADER */}
      <div className="flex items-center mb-8">
        <Wand2 className="text-purple-600 mr-3" size={36} />
        <h1 className="text-4xl font-bold">AI Recipe Generator</h1>
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        {/* ================= INPUT PANEL ================= */}
        <div className="bg-white p-6 rounded-xl shadow-lg space-y-6">
          <h2 className="text-2xl font-bold">Ingredients Input</h2>

          {/* MANUAL INGREDIENTS */}
          <div>
            <label className="font-semibold block mb-2">
              Manual Ingredients
            </label>

            <div className="flex gap-2 mb-3">
              <input
                type="text"
                value={currentIngredient}
                onChange={(e) => setCurrentIngredient(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && addIngredient()}
                placeholder="Add ingredient..."
                className="flex-1 px-4 py-2 border rounded-lg"
              />
              <button
                onClick={addIngredient}
                className="bg-purple-600 text-white px-4 py-2 rounded-lg"
              >
                <Plus size={18} />
              </button>
            </div>

            <div className="flex flex-wrap gap-2">
              {ingredients.map((ing, idx) => (
                <span
                  key={idx}
                  className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full flex items-center gap-2"
                >
                  {ing}
                  <X size={14} onClick={() => removeIngredient(idx)} />
                </span>
              ))}
            </div>

            <button
              onClick={generateFromText}
              disabled={loading}
              className="mt-4 w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3 rounded-lg font-semibold"
            >
              Generate from Ingredients
            </button>
          </div>

          {/* IMAGE INPUT */}
          <div>
            <label className="font-semibold block mb-2">
              Upload Ingredient Image
            </label>

            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              className="block w-full text-sm"
            />

            <button
              onClick={generateFromImage}
              disabled={loading}
              className="mt-3 w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white py-3 rounded-lg font-semibold flex items-center justify-center gap-2"
            >
              <ImageIcon size={18} />
              Generate from Image
            </button>
          </div>
        </div>

        {/* ================= RESULT PANEL ================= */}
        <div className="bg-white p-6 rounded-xl shadow-lg overflow-y-auto max-h-[80vh]">
          {generatedRecipe ? (
            <>
              {/* DETECTED INGREDIENTS */}
              {detectedIngredients.length > 0 && (
                <div className="mb-4 text-sm text-gray-600">
                  <strong>Detected Ingredients:</strong>{' '}
                  {detectedIngredients.join(', ')}
                </div>
              )}

              <h2 className="text-2xl font-bold mb-2">
                {generatedRecipe.name}
              </h2>

              <p className="text-gray-600 mb-4">
                {generatedRecipe.description}
              </p>

              {/* ================= NUTRITION ================= */}
              {generatedRecipe.nutrition && (
                <div className="grid grid-cols-4 gap-3 mb-6 text-sm">
                  <div className="bg-red-50 p-3 rounded-lg text-center">
                    🔥
                    <div className="font-semibold">
                      {generatedRecipe.nutrition.calories ?? 0}
                    </div>
                    <div className="text-xs text-gray-600">Calories</div>
                  </div>

                  <div className="bg-green-50 p-3 rounded-lg text-center">
                    🥩
                    <div className="font-semibold">
                      {generatedRecipe.nutrition.protein ?? 0} g
                    </div>
                    <div className="text-xs text-gray-600">Protein</div>
                  </div>

                  <div className="bg-yellow-50 p-3 rounded-lg text-center">
                    🥑
                    <div className="font-semibold">
                      {generatedRecipe.nutrition.fat ?? 0} g
                    </div>
                    <div className="text-xs text-gray-600">Fat</div>
                  </div>

                  <div className="bg-blue-50 p-3 rounded-lg text-center">
                    🍞
                    <div className="font-semibold">
                      {generatedRecipe.nutrition.carbs ?? 0} g
                    </div>
                    <div className="text-xs text-gray-600">Carbs</div>
                  </div>
                </div>
              )}

              {/* INGREDIENTS */}
              <h3 className="font-semibold mb-2">Ingredients</h3>
              <ul className="list-disc pl-5 mb-6">
                {(generatedRecipe.ingredients || []).map((ing, i) => (
                  <li key={i}>{renderIngredient(ing)}</li>
                ))}
              </ul>

              {/* STEPS */}
              <h3 className="font-semibold mb-2">Steps</h3>
              <ol className="list-decimal pl-5 space-y-2">
                {(generatedRecipe.steps || []).map((s, i) => (
                  <li key={i}>{s}</li>
                ))}
              </ol>
            </>
          ) : (
            <div className="text-center text-gray-500 py-20">
              <Wand2 size={64} className="mx-auto mb-4 opacity-20" />
              <p>Enter ingredients or upload an image 🍳</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
