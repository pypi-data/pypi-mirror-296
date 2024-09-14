from typing import List, Dict, Union


class PromptGenerator:
    def generate(self, analysis: Union[List[Dict[str, str]], Dict[str, str]]) -> str:
        prompt = "Code Base Summary:\n\n"
        if isinstance(analysis, list):
            for file_info in analysis:
                prompt += f"File: {file_info['path']}\n"
                prompt += f"Extension: {file_info['extension']}\n"
                prompt += f"Size: {file_info['size']} bytes\n"
                if "description" in file_info:
                    prompt += f"Description: {file_info['description']}\n"
                prompt += "Content Preview:\n"
                prompt += file_info["content"][:500] + "...\n\n"  # First 500 characters
        elif isinstance(analysis, dict):
            for file_path, summary in analysis.items():
                prompt += f"File: {file_path}\n"
                if isinstance(summary, dict):
                    prompt += f"Description: {summary.get('description', 'N/A')}\n"
                    prompt += f"Content Preview: {summary.get('content', '')[:500]}...\n\n"
                else:
                    prompt += f"Summary: {summary}\n\n"
        return prompt

    def generate_query_prompt(self, cached_context: str, query: str) -> str:
        return f"""
        Based on the following codebase context, please answer the query:

        {cached_context}

        Query: {query}

        Answer:
        """

    def generate_file_description_prompt(
        self, file_content: str, file_path: str, file_extension: str, file_size: int
    ) -> str:
        return f"""
        Given the following file information and content preview, provide a brief description of the file's purpose and main characteristics:

        File Path: {file_path}
        File Extension: {file_extension}
        File Size: {file_size} bytes

        Content Preview:
        {file_content[:1000]}  # Limit to first 1000 characters for brevity

        Description:
        """

    def generate_from_detailed_summary(self, summaries: Dict[str, str]) -> str:
        prompt = "Code Base Summary:\n\n"
        for file_path, summary in summaries.items():
            prompt += f"File: {file_path}\n"
            prompt += f"Summary: {summary}\n\n"
        return prompt
