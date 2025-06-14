def mistral_7b_score(resume_text, job_desc): # way 2
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    api_key = "Your API key"  # Get from OpenRouter.ai
    
    prompt = """You are an expert hiring assistant. Analyze the resume against the job description and:
        1. Provide a compatibility score (0-100%)
        2. Give a brief reason for the score
        Return ONLY a JSON object with 'score' and 'reason' fields."""
    
    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"Resume: {resume_text}\nJob Description: {job_desc}\n\nScore compatibility."
            }
        ],
        "temperature": 0.3,
        "response_format": {"type": "json_object"}
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)

    llm_content = response.json()["choices"][0]["message"]["content"]
    return json.loads(llm_content)
