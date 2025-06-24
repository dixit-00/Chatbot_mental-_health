from flask import Flask, request, jsonify
from flask_cors import CORS
from emotion_model import detect_emotion
from sad_questions import sad_questions  # Import the sad questions list

app = Flask(__name__)
CORS(app)

# Mental health Q&A pairs (simple keyword-based)
MENTAL_HEALTH_QA = {
    'anxious': "It's normal to feel anxious sometimes. Try deep breathing or mindfulness exercises. Would you like some resources?",
    'depressed': "I'm sorry you're feeling this way. Remember, you're not alone. Talking to someone you trust can help. If you need urgent help, please reach out to a professional.",
    'sleep': "Good sleep hygiene is important. Try to keep a regular schedule and avoid screens before bed. Would you like more tips?",
    'stress': "Managing stress is tough. Taking breaks, talking to friends, or going for a walk can help. Want some relaxation techniques?",
    'lonely': "Feeling lonely is hard. Connecting with others, even online, can help. Would you like some ideas for reaching out?",
    'panic': "If you're having a panic attack, try to focus on your breathing and remind yourself it will pass. Would you like some grounding exercises?",
    'sad': "It's okay to feel sad. Allow yourself to feel, and consider talking to someone you trust. Would you like some uplifting resources?",
    'angry': "Anger is a valid emotion. Try to express it in healthy ways, like physical activity or journaling. Need some tips?",
    'help': "If you need help, please consider reaching out to a mental health professional or a trusted person. I can provide resources if you'd like."
}

# Multi-solution dictionary for demo
SOLUTION_TYPES = [
    'Physical Fitness',
    'Ayurvedic/Herbal',
    'Therapy/Counseling',
    'Nutrition',
    'Mindfulness/Relaxation',
    'Community/Support Groups'
]
SOLUTION_RESPONSES = {
    'Physical Fitness': "Try regular exercise, yoga, or stretching to help manage your issue.",
    'Ayurvedic/Herbal': "Consider herbal remedies like Ashwagandha, Brahmi, or herbal teas. Consult a professional before use.",
    'Therapy/Counseling': "Talking to a counselor or therapist can provide valuable support and coping strategies.",
    'Nutrition': "Maintain a balanced diet, stay hydrated, and avoid excessive caffeine or sugar.",
    'Mindfulness/Relaxation': "Practice mindfulness, meditation, or deep breathing exercises daily.",
    'Community/Support Groups': "Connecting with support groups or communities can help you feel less alone."
}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').lower()
    solution_type = data.get('solution_type')
    emotion = detect_emotion(user_message)
    # Multi-solution logic
    if solution_type and solution_type in SOLUTION_RESPONSES:
        reply = SOLUTION_RESPONSES[solution_type]
        return jsonify({'reply': reply, 'emotion': emotion, 'solution_type': solution_type})
    # If user message looks like a problem description, offer solution types
    if any(kw in user_message for kw in ['problem', 'issue', 'describe', 'title:', 'description:', 'severity:', 'triggers:']):
        reply = "Which type of solution would you like to explore?"
        return jsonify({'reply': reply, 'emotion': emotion, 'solution_types': SOLUTION_TYPES})
    # Q&A logic
    reply = None
    for keyword, answer in MENTAL_HEALTH_QA.items():
        if keyword in user_message:
            reply = answer
            break
    if not reply:
        reply = "Thank you for sharing. I'm here to listen and support you. Would you like to talk more or get some resources?"
    response = {
        'reply': reply,
        'emotion': emotion
    }
    return jsonify(response)

@app.route('/checkin', methods=['POST'])
def checkin():
    data = request.get_json()
    mood = data.get('mood', '')
    # Simple supportive response
    response = {
        'message': f"Thank you for checking in. It's good to acknowledge your feelings. If you'd like to talk more, I'm here for you.",
        'mood': mood
    }
    return jsonify(response)

@app.route('/sad-questions', methods=['GET'])
def get_sad_questions():
    return jsonify(sad_questions)

if __name__ == '__main__':
    app.run(debug=True, port=5001) 