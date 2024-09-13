from .base_assistant import BaseAssistant
import os
from .get_code_from_input import get_code_from_input

class CodeFileNameGenerator(BaseAssistant):
    """
    CodeFileNameGenerator is a utility class for generating meaningful file names based on Python code content.
    """

    def __init__(self, model="llama-3.1-70b-versatile", temperature=0.7, max_tokens=50, top_p=1):
        """
        Initializes the CodeFileNameGenerator class with model, temperature, max_tokens, and top_p attributes.
        """
        super().__init__(model, temperature, max_tokens, top_p)

    def generate_file_name(self, code):
        """
        Generates a meaningful file name based on the provided Python code.

        Args:
            code (str): The Python code from which to generate a file name.

        Returns:
            str: A file name that reflects the primary functionality of the code.
        """
        code = get_code_from_input(code)

        prompt = f"Based on the provided Python code description, generate a simple and contextually appropriate file name as a string. The file name should reflect the main purpose of the code in a straightforward manner, without any file extensions. Here is the input: {code}"

        file_name = self._get_completion(prompt)
        file_name = file_name.strip().split("\n")[0].strip().replace(" ", "_").replace('"', '').replace("'", '')

        return file_name
