import React, { useState, useEffect } from 'react'
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