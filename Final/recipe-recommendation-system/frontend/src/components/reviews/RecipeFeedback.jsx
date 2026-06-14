import React, { useState } from 'react'
import { Star } from 'lucide-react'
import { reviewsAPI } from '../../services/api'

export default function RecipeFeedback({ recipeId, onSubmitted }) {
  const [rating, setRating] = useState(0)
  const [review, setReview] = useState('')
  const [loading, setLoading] = useState(false)

  const submitFeedback = async () => {
    if (rating === 0) {
      alert('Please select a rating')
      return
    }

    setLoading(true)
    try {
      await reviewsAPI.create({
        recipe_id: recipeId,
        rating,
        review_text: review
      })
      alert('Feedback submitted successfully!')
      setReview('')
      setRating(0)
      onSubmitted && onSubmitted()
    } catch (err) {
      alert('Error submitting feedback')
    }
    setLoading(false)
  }

  return (
    <div className="mt-4 border-t pt-4">
      <h4 className="font-semibold mb-2">Rate this recipe</h4>

      <div className="flex mb-2">
        {[1,2,3,4,5].map((i) => (
          <Star
            key={i}
            size={22}
            className={`cursor-pointer ${
              i <= rating ? 'text-yellow-400 fill-current' : 'text-gray-300'
            }`}
            onClick={() => setRating(i)}
          />
        ))}
      </div>

      <textarea
        placeholder="Optional feedback..."
        value={review}
        onChange={(e) => setReview(e.target.value)}
        className="w-full border rounded p-2 text-sm"
      />

      <button
        onClick={submitFeedback}
        disabled={loading}
        className="mt-2 bg-indigo-600 text-white px-4 py-2 rounded text-sm"
      >
        Submit Feedback
      </button>
    </div>
  )
}
