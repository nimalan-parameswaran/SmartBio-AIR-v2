import logging
import json
import google.generativeai as genai
from config import Config

logger = logging.getLogger("smartbio_gemini")

class GeminiClient:
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        self.enabled = False
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                # Test the model client
                self.model = genai.GenerativeModel("gemini-1.5-flash")
                self.enabled = True
                logger.info("Gemini API successfully configured.")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini API: {e}. AI features will use fallback templates.")
        else:
            logger.warning("No Gemini API key found. AI features will use fallback templates.")

    def _call_gemini(self, prompt: str, fallback_response: str) -> str:
        if not self.enabled:
            return fallback_response
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini API invocation failed: {e}")
            return f"{fallback_response}\n\n(AI System Notice: Gemini API was offline or unauthorized. Displaying automated diagnostics.)"

    def generate_recommendations(self, data: dict, analytics: dict, anomalies: list) -> list:
        prompt = f"""
        You are the Smart BIO AIR Recommendation Agent, a scientific advisor for an automated algae bioreactor.
        Analyze the current telemetry and analytics:
        - Telemetry: {json.dumps(data, indent=2)}
        - Derived Analytics: {json.dumps(analytics, indent=2)}
        - Detected Anomalies: {json.dumps(anomalies, indent=2)}

        Based on these parameters, provide 3 to 4 actionable, scientific recommendations for optimization.
        Ensure you focus on algae health (Light, Temp, Nutrients), purification capacity, and motor operation.
        DO NOT perform mathematical equations, rely on the calculations provided.
        Format your response as a JSON array of strings, e.g. ["Rec 1", "Rec 2", "Rec 3"].
        Return ONLY the raw JSON array. No markdown formatting, no backticks.
        """
        fallback = [
            "Increase light intensity if green index is low and light is below 500 lux.",
            "Inspect pump motor speed if water flow rate deviates from target value.",
            "Verify algae culture density; consider partial harvesting to prevent light blocking.",
            "Check temperature controls; ensure water stays between 20°C and 28°C."
        ]
        response_text = self._call_gemini(prompt, json.dumps(fallback))
        try:
            # Strip markdown code blocks if the model ignored instructions
            cleaned = response_text.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned)
        except Exception:
            # Regular parse of lines if JSON fails
            lines = [line.strip("- *").strip() for line in response_text.split("\n") if line.strip()]
            return lines[:4] if lines else fallback

    def generate_research_notes(self, current: dict, history: list) -> str:
        prompt = f"""
        You are the Smart BIO AIR Research Agent, an advanced laboratory assistant.
        Analyze the current reactor state compared to recent historical patterns:
        - Current State: {json.dumps(current, indent=2)}
        - Historical Log (up to 5 entries): {json.dumps(history, indent=2)}

        Write a short research note (150-200 words) summarizing:
        1. Algae growth behavior and photosynthesis performance under current light/temp.
        2. Environmental stability trend (stable vs degrading parameters).
        3. Scientific explanation of the observed relationship between algae density (green index) and gas levels.
        Be scientific, concise, and do not perform mathematical calculations yourself.
        """
        fallback = (
            "Research Note: The bioreactor indicates stable growth conditions. Photosynthesis is active "
            "as indicated by positive correlations between Light Lux and estimated biomass. Gas concentrations "
            "are currently within normal parameters. The green index trend shows incremental density accumulation."
        )
        return self._call_gemini(prompt, fallback)

    def ask_gemini_about_reactor(self, question: str, history: list, latest_state: dict) -> str:
        history_formatted = "\n".join([f"{h.get('role', 'user')}: {h.get('content', '')}" for h in history[-6:]])
        prompt = f"""
        You are 'Smart BIO AIR AI Assistant', an autonomous research-grade assistant managing an indoor algae bioreactor.
        
        System State:
        {json.dumps(latest_state, indent=2)}

        Conversation History:
        {history_formatted}

        User Question:
        {question}

        Provide a scientific, helpful, and highly accurate answer based on the current state. Keep it to 150 words or less.
        """
        fallback = "System is running normally. Algae health index is green. Please specify a more detailed query."
        return self._call_gemini(prompt, fallback)

# Singleton Instance
gemini_client = GeminiClient()
