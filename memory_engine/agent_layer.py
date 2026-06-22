import os
import logging
from typing import List, Optional
from dotenv import load_dotenv
from groq import Groq
from models import SearchResult

load_dotenv()

logger = logging.getLogger(__name__)

class AgentLayer:
    """
    The brain of the Second Brain AI.
    Takes retrieved context chunks and the user query to synthesize a conversational answer.
    """
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = None
        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
                logger.info("Agent Layer initialized successfully with Groq.")
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
        else:
            logger.warning("GROQ_API_KEY not found in environment variables. Agent Layer will be disabled.")

    def synthesize_answer(self, query: str, results: List[SearchResult]) -> Optional[str]:
        """
        Uses an LLM to generate an answer based on the provided search results.
        """
        if not self.client:
            return None
        
        if not results:
            return "I couldn't find any relevant information in your memory to answer this."

        # Compile the context
        context_parts = []
        for i, res in enumerate(results):
            # Clean up text for prompt
            text = res.text.strip()
            context_parts.append(f"--- Document snippet {i+1} ---\n{text}")
        
        context_str = "\n\n".join(context_parts)
        
        system_prompt = (
            "You are the 'Agent Layer' of a Second Brain AI. Your job is to answer the user's "
            "question accurately based strictly on the provided document context. "
            "If the context does not contain the answer, say so directly. "
            "Keep your answer concise, conversational, and cite the information naturally."
        )
        
        user_prompt = f"Context:\n{context_str}\n\nQuestion: {query}"
        
        try:
            logger.info(f"Generating synthesized answer for query: '{query}'")
            response = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=400,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error during synthesis: {e}")
            return "Sorry, I encountered an error while trying to synthesize the answer with the LLM."
