import os
import openai
from openai import OpenAI
from typing import List

class ProfileGenerator:
    def __init__(self):
        self.system_prompt = """You are a world-class expert in leadership psychology, organizational behavior, and executive development. You specialize in synthesizing diverse data sources—such as personality assessments, 360 feedback, coaching notes, performance reviews, and CVs—into insightful, psychologically sophisticated leadership profiles. Your goal is to produce actionable insights, grounded in evidence, that support individual growth and organizational fit. Always cite the data source behind your claims and remain both rigorous and humanistic in tone."""
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        self.openai_client = OpenAI(api_key=openai_api_key)

    def generate_profile(self, document_chunks: List[str], document_metadatas: List) -> str:
        # Build the document type list for the LLM prompt and for the report
        doc_types = list(dict.fromkeys(meta.document_type for meta in document_metadatas))  # unique, preserve order
        doc_type_list = "\n".join(f"- {doc_type}" for doc_type in doc_types)
        doc_type_list_for_report = "\n".join(doc_types)

        # LLM prompt (not included in report)
        doc_summary_prompt = (
            "You have been provided with the following types of documents for your analysis:\n"
            f"{doc_type_list}\n\n"
            "You must only reference the document types listed above. Do not invent or assume the existence of other data sources. "
            "If a type of data (e.g., 'Coaching Notes') is not present in the provided documents, do not reference it.\n\n"
            "For each section of your analysis, make a good faith effort to use and reference insights from all provided document types, even if some are only briefly mentioned. "
            "If a document type does not contribute to a particular section, state this explicitly.\n\n"
        )

        context = "\n\n".join(document_chunks)

        prompt = (
            doc_summary_prompt +
            "Based on the following leadership documents, generate a comprehensive and psychologically insightful leadership profile. "
            "Integrate themes across the inputs and make sure to clearly reference which data points inform each insight.\n\n"
            f"{context}\n\n"
            "Structure your response as follows:\n\n"
            "1. **Leadership Summary** – A 3–5 sentence overview of the individual's leadership essence, style, and reputation.\n"
            "2. **Key Strengths** – Backed by examples or data, especially when seen across multiple sources.\n"
            "3. **Potential Derailers** – Risks or blind spots, particularly those that may emerge under stress, change, or growth pressure.\n"
            "4. **Leadership Style** – Include patterns in interpersonal behavior, decision-making, motivation, and influence style.\n"
            "5. **Role Fit Chart** – A table with 3–5 roles this person is highly suited for, and 3–5 they are less suited for, with explanations for each based on personality and leadership indicators.\n\n"
            "Your response should be concise, insightful, and evidence-based. Cite which document types (e.g., Hogan, 360, CV) informed each section."
        )
        response = self.openai_client.chat.completions.create(
            model="gpt-4.1-2025-04-14",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=2000
        )
        # Only show the document types at the top of the report, not the prompt or filenames
        report_header = "Documents Used for Analysis:\n" + doc_type_list_for_report + "\n\n"
        return report_header + response.choices[0].message.content

    def answer_question(self, document_chunks: List[str], question: str) -> str:
        context = "\n\n".join(document_chunks)
        prompt = f"""Based on the following leadership documents, answer this special question:

{context}

Question: {question}

Please provide a detailed, evidence-based answer, referencing the relevant data from the documents."""
        response = self.openai_client.chat.completions.create(
            model="gpt-4.1-2025-04-14",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=800
        )
        return response.choices[0].message.content
