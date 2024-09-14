from typing import Dict, List
from .cache_manager import CacheManager
from .prompt_generator import PromptGenerator


class Summarizer:
    def __init__(self, cache_manager: CacheManager):
        self.cache_manager = cache_manager
        self.prompt_generator = PromptGenerator()

    def detailed_summary(self, analysis: List[Dict[str, str]]) -> Dict[str, str]:
        summaries = {}
        for file_info in analysis:
            prompt = self.prompt_generator.generate_file_description_prompt(
                file_content=file_info["content"],
                file_path=file_info["path"],
                file_extension=file_info["extension"],
                file_size=file_info["size"],
            )
            summary = self.cache_manager.generate_content_from_prompt(
                prompt, max_tokens=100, temperature=0.2
            )
            summaries[file_info["path"]] = summary
        return summaries

    def quick_summary(self, analysis: List[Dict[str, str]]) -> str:
        codebase_overview = self.prompt_generator.generate(analysis)

        prompt = f"""
        Given the following overview of a codebase, provide a brief summary
        of the project structure and main components (max 200 words):

        {codebase_overview}

        Summary:
        """
        return self.cache_manager.generate_content_from_prompt(
            prompt, max_tokens=200, temperature=0.2
        )

    def summarize(self, analysis: List[Dict[str, str]], mode: str = "quick") -> Dict[str, str]:
        if mode == "detailed":
            return self.detailed_summary(analysis)
        elif mode == "quick":
            return {"global_summary": self.quick_summary(analysis)}
        else:
            raise ValueError("Invalid summarization mode. Choose 'detailed' or 'quick'.")
