# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import json

class FactChecker(gl.Contract):
    result: str

    def __init__(self):
        self.result = "No fact checked yet"

    @gl.public.write
    def check_fact(self, claim: str) -> None:
        prompt = f"""
        Is this claim true or false? "{claim}"
        Respond using ONLY the following format:
        {{
        "reasoning": str,
        "verdict": "TRUE" or "FALSE" or "UNVERIFIABLE"
        }}
        It is mandatory that you respond only using the JSON format above,
        nothing else. Don't include any other words or characters,
        your output must be only JSON without any formatting prefix or suffix.
        This result should be perfectly parseable by a JSON parser without errors.
        """
        def get_answer():
            result = gl.nondet.exec_prompt(prompt)
            result = result.replace("```json", "").replace("```", "")
            print(result)
            return result

        result = gl.eq_principle.prompt_comparative(
            get_answer, "The value of verdict has to match"
        )
        parsed_result = json.loads(result)
        self.result = parsed_result["verdict"] + " - " + parsed_result["reasoning"]

    @gl.public.view
    def get_result(self) -> str:
        return self.result
