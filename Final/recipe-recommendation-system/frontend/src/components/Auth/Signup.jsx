// frontend/src/components/Auth/Signup.jsx
// Enhanced version with full personalization options

import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { User, Mail, Lock, Calendar, Utensils, AlertCircle, Heart, Globe } from 'lucide-react'

export default function Signup() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    full_name: '',
    age: '',
    dietary_type: '',
    health_conditions: [],
    allergies: [],
    preferred_cuisines: []
  })
  
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [currentStep, setCurrentStep] = useState(1)
  
  const { signup } = useAuth()
  const navigate = useNavigate()

  // Available options
  const dietaryTypes = [
    { value: 'vegetarian', label: 'Vegetarian', icon: '🥬' },
    { value: 'vegan', label: 'Vegan', icon: '🌱' },
    { value: 'keto', label: 'Keto', icon: '🥑' },
    { value: 'paleo', label: 'Paleo', icon: '🥩' },
    { value: 'gluten-free', label: 'Gluten-Free', icon: '🌾' },
    { value: 'dairy-free', label: 'Dairy-Free', icon: '🥛' },
    { value: 'none', label: 'No Restriction', icon: '🍽️' }
  ]

  const healthConditions = [
    { value: 'diabetes', label: 'Diabetes', icon: '💉' },
    { value: 'hypertension', label: 'High Blood Pressure', icon: '❤️' },
    { value: 'heart-disease', label: 'Heart Disease', icon: '💓' },
    { value: 'obesity', label: 'Weight Management', icon: '⚖️' },
    { value: 'cholesterol', label: 'High Cholesterol', icon: '🩺' }
  ]

  const allergens = [
    { value: 'gluten', label: 'Gluten', icon: '🌾' },
    { value: 'dairy', label: 'Dairy', icon: '🥛' },
    { value: 'nuts', label: 'Nuts', icon: '🥜' },
    { value: 'shellfish', label: 'Shellfish', icon: '🦐' },
    { value: 'eggs', label: 'Eggs', icon: '🥚' },
    { value: 'soy', label: 'Soy', icon: '🫘' },
    { value: 'fish', label: 'Fish', icon: '🐟' }
  ]

  const cuisines = [
    { value: 'italian', label: 'Italian', icon: '🍝', flag: '🇮🇹' },
    { value: 'indian', label: 'Indian', icon: '🍛', flag: '🇮🇳' },
    { value: 'mexican', label: 'Mexican', icon: '🌮', flag: '🇲🇽' },
    { value: 'chinese', label: 'Chinese', icon: '🥢', flag: '🇨🇳' },
    { value: 'japanese', label: 'Japanese', icon: '🍱', flag: '🇯🇵' },
    { value: 'thai', label: 'Thai', icon: '🍜', flag: '🇹🇭' },
    { value: 'mediterranean', label: 'Mediterranean', icon: '🥗', flag: '🌍' },
    { value: 'american', label: 'American', icon: '🍔', flag: '🇺🇸' }
  ]

  const toggleArrayItem = (array, item) => {
    if (array.includes(item)) {
      return array.filter(i => i !== item)
    } else {
      return [...array, item]
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (currentStep < 3) {
      // Validate current step before proceeding
      if (currentStep === 1) {
        if (!formData.email || !formData.password || !formData.full_name) {
          setError('Please fill in all required fields')
          return
        }
        if (formData.password !== formData.confirmPassword) {
          setError('Passwords do not match')
          return
        }
        if (formData.password.length < 6) {
          setError('Password must be at least 6 characters')
          return
        }
      }
      
      setError('')
      setCurrentStep(currentStep + 1)
      return
    }
    
    // Final submission
    setLoading(true)
    setError('')
    
    const result = await signup({
      email: formData.email,
      password: formData.password,
      full_name: formData.full_name,
      age: formData.age ? parseInt(formData.age) : null,
      dietary_type: formData.dietary_type || null,
      health_conditions: formData.health_conditions.length > 0 
        ? formData.health_conditions 
        : [],
      allergies: formData.allergies,
      preferred_cuisines: formData.preferred_cuisines
    })
    
    if (result.success) {
      navigate('/recommendations')
    } else {
      setError(result.error)
      setCurrentStep(1) // Go back to first step if error
    }
    setLoading(false)
  }

  const renderStep1 = () => (
    <div className="space-y-4">
      <h3 className="text-xl font-semibold mb-4 flex items-center">
        <User className="mr-2" size={24} />
        Basic Information
      </h3>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          <User size={16} className="inline mr-1" />
          Full Name *
        </label>
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
        <label className="block text-sm font-medium text-gray-700 mb-2">
          <Mail size={16} className="inline mr-1" />
          Email Address *
        </label>
        <input
          type="email"
          placeholder="your@email.com"
          value={formData.email}
          onChange={(e) => setFormData({...formData, email: e.target.value})}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          required
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Lock size={16} className="inline mr-1" />
            Password *
          </label>
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
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Lock size={16} className="inline mr-1" />
            Confirm Password *
          </label>
          <input
            type="password"
            placeholder="••••••••"
            value={formData.confirmPassword}
            onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
            required
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          <Calendar size={16} className="inline mr-1" />
          Age (Optional)
        </label>
        <input
          type="number"
          placeholder="25"
          value={formData.age}
          onChange={(e) => setFormData({...formData, age: e.target.value})}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          min="1"
          max="120"
        />
      </div>
    </div>
  )

  const renderStep2 = () => (
    <div className="space-y-6">
      <h3 className="text-xl font-semibold mb-4 flex items-center">
        <Heart className="mr-2" size={24} />
        Health & Dietary Preferences
      </h3>

      {/* Dietary Type */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          <Utensils size={16} className="inline mr-1" />
          Dietary Preference
        </label>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {dietaryTypes.map((diet) => (
            <button
              key={diet.value}
              type="button"
              onClick={() => setFormData({...formData, dietary_type: diet.value})}
              className={`p-3 border-2 rounded-lg text-center transition ${
                formData.dietary_type === diet.value
                  ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
                  : 'border-gray-200 hover:border-indigo-300'
              }`}
            >
              <div className="text-2xl mb-1">{diet.icon}</div>
              <div className="text-sm font-medium">{diet.label}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Health Conditions */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          <AlertCircle size={16} className="inline mr-1" />
          Health Conditions (Select all that apply)
        </label>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {healthConditions.map((condition) => (
            <button
              key={condition.value}
              type="button"
              onClick={() => setFormData({
                ...formData,
                health_conditions: toggleArrayItem(formData.health_conditions, condition.value)
              })}
              className={`p-3 border-2 rounded-lg text-left flex items-center transition ${
                formData.health_conditions.includes(condition.value)
                  ? 'border-red-500 bg-red-50'
                  : 'border-gray-200 hover:border-red-300'
              }`}
            >
              <span className="text-2xl mr-3">{condition.icon}</span>
              <span className="text-sm font-medium">{condition.label}</span>
              {formData.health_conditions.includes(condition.value) && (
                <span className="ml-auto text-red-600">✓</span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Allergies */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          <AlertCircle size={16} className="inline mr-1" />
          Food Allergies (Select all that apply)
        </label>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {allergens.map((allergen) => (
            <button
              key={allergen.value}
              type="button"
              onClick={() => setFormData({
                ...formData,
                allergies: toggleArrayItem(formData.allergies, allergen.value)
              })}
              className={`p-3 border-2 rounded-lg text-center transition ${
                formData.allergies.includes(allergen.value)
                  ? 'border-orange-500 bg-orange-50'
                  : 'border-gray-200 hover:border-orange-300'
              }`}
            >
              <div className="text-2xl mb-1">{allergen.icon}</div>
              <div className="text-xs font-medium">{allergen.label}</div>
              {formData.allergies.includes(allergen.value) && (
                <div className="text-orange-600 text-xs mt-1">✓ Avoid</div>
              )}
            </button>
          ))}
        </div>
      </div>
    </div>
  )

  const renderStep3 = () => (
    <div className="space-y-6">
      <h3 className="text-xl font-semibold mb-4 flex items-center">
        <Globe className="mr-2" size={24} />
        Cuisine Preferences
      </h3>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Select Your Favorite Cuisines (Choose at least 2)
        </label>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {cuisines.map((cuisine) => (
            <button
              key={cuisine.value}
              type="button"
              onClick={() => setFormData({
                ...formData,
                preferred_cuisines: toggleArrayItem(formData.preferred_cuisines, cuisine.value)
              })}
              className={`p-4 border-2 rounded-lg text-center transition ${
                formData.preferred_cuisines.includes(cuisine.value)
                  ? 'border-green-500 bg-green-50'
                  : 'border-gray-200 hover:border-green-300'
              }`}
            >
              <div className="text-3xl mb-2">{cuisine.flag}</div>
              <div className="text-2xl mb-1">{cuisine.icon}</div>
              <div className="text-sm font-medium">{cuisine.label}</div>
              {formData.preferred_cuisines.includes(cuisine.value) && (
                <div className="text-green-600 text-xs mt-1">✓ Selected</div>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Summary */}
      <div className="mt-8 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <h4 className="font-semibold text-blue-900 mb-2">Your Personalization Summary:</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>✓ Dietary: {formData.dietary_type || 'No restriction'}</li>
          <li>✓ Health conditions: {formData.health_conditions.length > 0 ? formData.health_conditions.join(', ') : 'None'}</li>
          <li>✓ Allergies: {formData.allergies.length > 0 ? formData.allergies.join(', ') : 'None'}</li>
          <li>✓ Preferred cuisines: {formData.preferred_cuisines.length > 0 ? formData.preferred_cuisines.join(', ') : 'All'}</li>
        </ul>
      </div>
    </div>
  )

  return (
    <div className="max-w-4xl mx-auto mt-8 mb-16">
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-6 text-white">
          <h2 className="text-3xl font-bold text-center">Create Your Account</h2>
          <p className="text-center mt-2 text-indigo-100">
            Tell us about your preferences for personalized recommendations
          </p>
        </div>

        {/* Progress Bar */}
        <div className="px-6 pt-6">
          <div className="flex items-center justify-between mb-2">
            <span className={`text-sm font-medium ${currentStep >= 1 ? 'text-indigo-600' : 'text-gray-400'}`}>
              Basic Info
            </span>
            <span className={`text-sm font-medium ${currentStep >= 2 ? 'text-indigo-600' : 'text-gray-400'}`}>
              Health & Diet
            </span>
            <span className={`text-sm font-medium ${currentStep >= 3 ? 'text-indigo-600' : 'text-gray-400'}`}>
              Cuisine Preferences
            </span>
          </div>
          <div className="flex gap-2">
            <div className={`flex-1 h-2 rounded-full ${currentStep >= 1 ? 'bg-indigo-600' : 'bg-gray-200'}`} />
            <div className={`flex-1 h-2 rounded-full ${currentStep >= 2 ? 'bg-indigo-600' : 'bg-gray-200'}`} />
            <div className={`flex-1 h-2 rounded-full ${currentStep >= 3 ? 'bg-indigo-600' : 'bg-gray-200'}`} />
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6">
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              {error}
            </div>
          )}

          {currentStep === 1 && renderStep1()}
          {currentStep === 2 && renderStep2()}
          {currentStep === 3 && renderStep3()}

          {/* Navigation Buttons */}
          <div className="flex gap-4 mt-8">
            {currentStep > 1 && (
              <button
                type="button"
                onClick={() => setCurrentStep(currentStep - 1)}
                className="flex-1 bg-gray-200 text-gray-800 py-3 rounded-lg font-semibold hover:bg-gray-300 transition"
              >
                ← Previous
              </button>
            )}
            
            <button
              type="submit"
              disabled={loading}
              className={`${currentStep === 1 ? 'w-full' : 'flex-1'} bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-3 rounded-lg font-semibold hover:from-indigo-700 hover:to-purple-700 transition disabled:opacity-50`}
            >
              {loading ? 'Creating Account...' : currentStep === 3 ? 'Create Account' : 'Next →'}
            </button>
          </div>
        </form>

        {/* Footer */}
        <div className="px-6 pb-6 text-center text-gray-600">
          Already have an account?{' '}
          <Link to="/login" className="text-indigo-600 hover:underline font-semibold">
            Login
          </Link>
        </div>
      </div>
    </div>
  )
}