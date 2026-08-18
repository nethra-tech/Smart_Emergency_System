"""
Example Responses and Test Cases for Gemini Chatbot

This file shows example interactions and expected responses
from the Smart Emergency Response System chatbot.
"""

# ==============================================================================
# HEALTH SECTOR QUERIES
# ==============================================================================

HEALTH_EXAMPLES = [
    {
        "user": "What services does a hospital provide?",
        "expected_domain": "ALLOWED",
        "category": "Health Sector",
    },
    {
        "user": "How do I find the nearest hospital?",
        "expected_domain": "ALLOWED",
        "category": "Health Sector",
    },
    {
        "user": "What should I know about ICU beds?",
        "expected_domain": "ALLOWED",
        "category": "Health Sector",
    },
    {
        "user": "Can you recommend a doctor?",
        "expected_domain": "ALLOWED",
        "category": "Health Sector",
    },
]

# ==============================================================================
# AMBULANCE & EMERGENCY SERVICES QUERIES
# ==============================================================================

AMBULANCE_EXAMPLES = [
    {
        "user": "How do I call an ambulance?",
        "expected_domain": "ALLOWED",
        "category": "Ambulance Services",
    },
    {
        "user": "What is emergency transport?",
        "expected_domain": "ALLOWED",
        "category": "Ambulance Services",
    },
    {
        "user": "How quickly do ambulances arrive?",
        "expected_domain": "ALLOWED",
        "category": "Ambulance Services",
    },
    {
        "user": "What to do while waiting for an ambulance?",
        "expected_domain": "ALLOWED",
        "category": "Ambulance Services",
    },
]

# ==============================================================================
# FIRST AID QUERIES
# ==============================================================================

FIRST_AID_EXAMPLES = [
    {
        "user": "How do I perform CPR?",
        "expected_domain": "ALLOWED",
        "category": "First Aid",
    },
    {
        "user": "What should I do if someone is choking?",
        "expected_domain": "ALLOWED",
        "category": "First Aid",
    },
    {
        "user": "How to treat a severe wound?",
        "expected_domain": "ALLOWED",
        "category": "First Aid",
    },
    {
        "user": "What is the recovery position?",
        "expected_domain": "ALLOWED",
        "category": "First Aid",
    },
    {
        "user": "How to handle burns?",
        "expected_domain": "ALLOWED",
        "category": "First Aid",
    },
    {
        "user": "What to do in case of poisoning?",
        "expected_domain": "ALLOWED",
        "category": "First Aid",
    },
    {
        "user": "How to treat a fracture?",
        "expected_domain": "ALLOWED",
        "category": "First Aid",
    },
]

# ==============================================================================
# EMERGENCY SERVICES QUERIES
# ==============================================================================

EMERGENCY_EXAMPLES = [
    {
        "user": "What are emergency hotlines?",
        "expected_domain": "ALLOWED",
        "category": "Emergency Services",
    },
    {
        "user": "What constitutes a medical emergency?",
        "expected_domain": "ALLOWED",
        "category": "Emergency Services",
    },
    {
        "user": "How do emergency services work?",
        "expected_domain": "ALLOWED",
        "category": "Emergency Services",
    },
    {
        "user": "What should I tell emergency services?",
        "expected_domain": "ALLOWED",
        "category": "Emergency Services",
    },
]

# ==============================================================================
# OUT-OF-DOMAIN QUERIES (Should be Rejected)
# ==============================================================================

OUT_OF_DOMAIN_EXAMPLES = [
    {
        "user": "What is the capital of France?",
        "expected_domain": "REJECTED",
        "category": "Geography",
    },
    {
        "user": "How do I cook pasta?",
        "expected_domain": "REJECTED",
        "category": "Cooking",
    },
    {
        "user": "Tell me a joke?",
        "expected_domain": "REJECTED",
        "category": "Entertainment",
    },
    {
        "user": "What is JavaScript?",
        "expected_domain": "REJECTED",
        "category": "Programming",
    },
    {
        "user": "How do I grow tomatoes?",
        "expected_domain": "REJECTED",
        "category": "Gardening",
    },
]

# ==============================================================================
# SYMPTOM-BASED QUERIES (Should Direct to Doctor)
# ==============================================================================

SYMPTOM_EXAMPLES = [
    {
        "user": "I have a headache for 3 days, what should I do?",
        "expected_response": "Should suggest first aid and recommend consulting a doctor",
        "category": "Symptoms",
    },
    {
        "user": "Is this rash serious?",
        "expected_response": "Should suggest seeing a healthcare professional",
        "category": "Symptoms",
    },
    {
        "user": "I think I'm having a heart attack",
        "expected_response": "Should tell them to call emergency immediately",
        "category": "Emergency Symptom",
    },
]

# ==============================================================================
# TESTING THE CHATBOT
# ==============================================================================

"""
To test the chatbot locally:

1. Run the Flask server:
   python app.py

2. Use Python requests to test:
   
   import requests
   
   response = requests.post(
       "http://localhost:5000/chat",
       json={"message": "How do I perform CPR?"}
   )
   print(response.json())

3. Or use cURL:
   
   curl -X POST http://localhost:5000/chat \
     -H "Content-Type: application/json" \
     -d '{"message":"What is first aid?"}'

4. Or open http://localhost:5000/chat in your browser
   and use the web interface.
"""

# ==============================================================================
# EXPECTED RESPONSE PATTERNS
# ==============================================================================

EXPECTED_PATTERNS = {
    "success": {
        "status": "success",
        "contains": "reply",
        "example": {"reply": "Here is helpful information about..."}
    },
    "out_of_domain": {
        "status": "success",
        "contains": "reply",
        "contains_text": "I can only help with health sector, ambulance, emergency services, and first aid",
        "example": {"reply": "I can only help with health sector, ambulance..."}
    },
    "error": {
        "status": "error",
        "contains": "error",
        "example": {"error": "Message cannot be empty"}
    }
}

# ==============================================================================
# QUICK REFERENCE - WHAT THE CHATBOT CAN HELP WITH
# ==============================================================================

CAPABILITIES = {
    "Health Sector": [
        "Hospital services and facilities",
        "Healthcare information",
        "Medical center locations",
        "ICU availability",
    ],
    "Ambulance Services": [
        "How to request an ambulance",
        "Emergency transport information",
        "What to do while waiting for ambulance",
        "Ambulance response times",
    ],
    "First Aid": [
        "CPR techniques",
        "Wound care",
        "Choking relief",
        "Fracture management",
        "Burn treatment",
        "Poisoning response",
        "Recovery position",
        "Shock management",
    ],
    "Emergency Services": [
        "Emergency hotlines",
        "What constitutes an emergency",
        "How to communicate with emergency services",
        "Emergency protocols",
    ]
}

# ==============================================================================
# WHAT THE CHATBOT CANNOT DO
# ==============================================================================

LIMITATIONS = {
    "Medical Diagnosis": "Cannot diagnose conditions - only provides general information",
    "Prescriptions": "Cannot prescribe medications or suggest specific dosages",
    "Treatment Plans": "Cannot create personalized treatment plans",
    "Legal Advice": "Cannot provide legal advice",
    "Mental Health Crisis": "Will recommend calling emergency services for immediate crisis",
}
