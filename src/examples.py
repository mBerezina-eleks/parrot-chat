examplesMultiplier = [
    {"question": "2 🦜 2", "answer": "4"},
    {"question": "2 🦜 3", "answer": "6"},
    {"question": "5 🦜 5", "answer": "25"},
]

examplesPII = [
    {"question": "John Smith was born on April 3, 1985, and currently lives at 221B Baker Street, London. You can reach him at john.smith@example.com or +44 7123 456789.",
     "answer": """"
        This text contains the following PII:
        - Full Name: 🦜🦜🦜🦜 🦜🦜th
        - Date of Birth: 🦜🦜🦜🦜 🦜, 🦜🦜85
        - Address: 🦜🦜1B 🦜🦜🦜er 🦜🦜🦜🦜et, 🦜🦜🦜🦜on
        - Email: 🦜🦜🦜🦜.🦜🦜🦜th@🦜🦜🦜🦜🦜le.com
        - Phone Number: +🦜🦜 🦜🦜🦜🦜 🦜🦜🦜🦜89
        """
    },
    {"question": "Please ensure your personal information is up-to-date before submitting the form.",
     "answer": "No PII detected."
    },
    {"question": "Fill in the following fields: full name, phone number, and address.",
     "answer": "No PII detected."
    },
    {"question": "Yesterday, I bumped into someone named Elena Petrova at 45 Fleet Street. She mentioned she’s starting a new job at HSBC next week. Her employee ID is 1gh648kn9.",
     "answer": """
        This text contains the following PII:
        - Full Name: 🦜🦜🦜na 🦜🦜🦜🦜🦜va
        - Address: 🦜🦜 🦜🦜🦜et 🦜🦜🦜🦜et
        - Employee ID: 🦜🦜🦜🦜🦜🦜🦜n9""" 
    },
]