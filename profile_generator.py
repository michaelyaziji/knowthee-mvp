import os
from openai import OpenAI
from typing import List

class ProfileGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.system_prompt = """You are world class expert on leadership assessment AI. Your task is to analyze and synthesize leadership documents and generate a comprehensive leadership profile. 
        Focus on identifying key strengths, potential derailers, and development suggestions. Be specific and evidence-based in your analysis."""
    
    def generate_profile(self, document_chunks: List[str]) -> str:
        """Generate a leadership profile from document chunks."""
        # Combine document chunks
        context = "\n\n".join(document_chunks)
        
        # Create the prompt
        prompt = f"""Based on the following leadership documents, generate a comprehensive leadership profile:

{context}

Please structure your response in the following sections:
1. A sophisticated leadership profilte
2. Key Strengths
3. Potential Derailers
4. Overall Leadership Style
5. A chart indicating what types of jobs would be most and least sutiable for this person, and why

Be specific and evidence-based--meaning indicated which data fro mwhich reports informed your analysis-- in your analysis."""
        
        
        # Generate the profile
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content

    def answer_question(self, document_chunks: List[str], question: str) -> str:
        """Answer a user question based on the document context."""
        context = "\n\n".join(document_chunks)
        prompt = f"""Based on the following leadership documents, answer this special question:

{context}

Question: {question}

Please provide a detailed, evidence-based answer, referencing the relevant data from the documents."""
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content 