import os
import json
import logging
import fnmatch
import mimetypes
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from .exceptions import AnalysisError
from .cache_manager import CacheManager
from .prompt_generator import PromptGenerator
from .summarizer import Summarizer

logger = logging.getLogger(__name__)


class CodebaseAnalyzer:
    def __init__(
        self,
        root_dir: str,
        ignore_file: Optional[str] = None,
        cache_manager: Optional[CacheManager] = None,
        verbose: bool = False
    ):
        self.root_dir = Path(root_dir).resolve()
        self.ignore_patterns = self._load_ignore_patterns(ignore_file)
        self.cache_manager = cache_manager
        self.prompt_generator = PromptGenerator()
        self.summarizer = Summarizer(cache_manager) if cache_manager else None
        self.verbose = verbose
        if self.verbose:
            logger.info(f"Initialized CodebaseAnalyzer for directory: {self.root_dir}")
        if ignore_file:
            if self.verbose:
                logger.info(f"Using custom ignore file: {ignore_file}")
        elif (self.root_dir / ".codecachignore").exists():
            if self.verbose:
                logger.info(f"Using .codecachignore file found in {self.root_dir}")

    def _load_ignore_patterns(self, ignore_file: Optional[str]) -> List[str]:
        patterns = []

        if not ignore_file and (self.root_dir / ".codecachignore").exists():
            ignore_file = str(self.root_dir / ".codecachignore")

        if ignore_file and os.path.exists(ignore_file):
            with open(ignore_file, "r") as f:
                patterns = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            if self.verbose:
                logger.info(f"Loaded {len(patterns)} ignore patterns")
        return patterns

    def _should_ignore(self, path: Path) -> bool:
        rel_path = path.relative_to(self.root_dir)

        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(str(rel_path), pattern) or any(
                fnmatch.fnmatch(str(parent), pattern) for parent in rel_path.parents
            ):
                if self.verbose:
                    logger.info(f"Ignoring: {rel_path} (matched pattern: {pattern})")
                return True

        if path.is_dir():
            dir_name = path.name
            if dir_name in ["env", "venv", ".env", "__pycache__", "node_modules"]:
                if self.verbose:
                    logger.info(f"Ignoring directory: {rel_path}")
                return True

        return False

    def _is_text_file(self, file_path: Path) -> bool:
        mime_type, _ = mimetypes.guess_type(str(file_path))
        return mime_type is not None and mime_type.startswith("text/")

    def _analyze_file(self, file_path: Path) -> Dict[str, str]:
        try:
            if not self._is_text_file(file_path):
                if self.verbose:
                    logger.info(f"Skipping binary file: {file_path}")
                return {
                    "path": str(file_path),
                    "content": "Binary file",
                    "description": "Binary file",
                    "extension": file_path.suffix or "No extension",
                    "size": os.path.getsize(file_path),
                }

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception as e:
                logger.error(f"Error reading file {file_path}: {str(e)}")
                raise AnalysisError(f"Error reading file {file_path}: {str(e)}")

            file_info = {
                "path": str(file_path),
                "content": content[:1000] + ("..." if len(content) > 1000 else ""),
                "size": os.path.getsize(file_path),
                "extension": file_path.suffix or "No extension",
            }

            if self.cache_manager:
                if self.verbose:
                    logger.info(f"Generating description for file: {file_path}")
                file_info["description"] = self.cache_manager.generate_content_from_prompt(
                    self.prompt_generator.generate_file_description_prompt(
                        file_content=content,
                        file_path=str(file_path),
                        file_extension=file_info["extension"],
                        file_size=file_info["size"],
                    ),
                    max_tokens=100,
                    temperature=0.2,
                )
            else:
                file_info["description"] = (
                    "File description not available (no CacheManager provided)"
                )

            return file_info
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {str(e)}")
            raise AnalysisError(f"Error analyzing file {file_path}: {str(e)}")

    def analyze(self) -> List[Dict[str, str]]:
        analysis = []
        try:
            if self.verbose:
                logger.info(f"Starting analysis of directory: {self.root_dir}")
            for root, dirs, files in os.walk(self.root_dir):
                dirs[:] = [d for d in dirs if not self._should_ignore(Path(root) / d)]

                for file in files:
                    file_path = Path(root) / file
                    if not self._should_ignore(file_path):
                        if self.verbose:
                            logger.info(f"Analyzing file: {file_path}")
                        analysis.append(self._analyze_file(file_path))
                    else:
                        if self.verbose:
                            logger.info(f"Skipping file: {file_path}")
            if self.verbose:
                logger.info("File analysis complete.")
        except Exception as e:
            logger.error(f"Error during codebase analysis: {str(e)}")
            raise AnalysisError(f"Error during codebase analysis: {str(e)}")
        return analysis

    def save_summaries(self, summaries: Dict[str, Any], summary_mode: str, summary_file: Optional[Path] = None) -> Path:
        if not summary_file:
            filename = "detailed_summaries.json" if summary_mode == "detailed" else "quick_summary.txt"
            summary_file = self.root_dir / filename

        try:
            if summary_mode == "detailed":
                with open(summary_file, "w") as f:
                    json.dump(summaries, f, indent=2)
            else:
                with open(summary_file, "w") as f:
                    f.write(summaries["global_summary"])
            if self.verbose:
                logger.info(f"Summaries saved to {summary_file}")
        except Exception as e:
            logger.error(f"Error saving summaries: {str(e)}")
            raise AnalysisError(f"Error saving summaries: {str(e)}")

        return summary_file

    def generate_context(self, summary_mode: str = "quick") -> Tuple[str, Optional[Path]]:
        if self.verbose:
            logger.info(f"Generating context using {summary_mode} summary mode...")
        
        summary_file = None
        if self.summarizer:
            filename = "detailed_summaries.json" if summary_mode == "detailed" else "quick_summary.txt"
            summary_file = self.root_dir / filename

            if not summary_file.exists():
                if self.verbose:
                    logger.info(f"Summary file {filename} not found. Generating...")
                analysis = self.analyze()
                context = self.prompt_generator.generate(analysis)

                if summary_mode == "detailed":
                    summaries = {}
                    for file_info in analysis:
                        file_path = file_info["path"]
                        file_content = file_info["content"]
                        file_description = file_info["description"]
                        summaries[file_path] = {
                            "description": file_description,
                            "content": file_content,
                        }
                    self.save_summaries(summaries, summary_mode, summary_file)
                else:
                    summary = self.summarizer.summarize(analysis, mode="quick")
                    self.save_summaries(summary, summary_mode, summary_file)
            else:
                if self.verbose:
                    logger.info(f"Using existing summary file: {filename}")
                
                # Load existing summary
                if summary_mode == "detailed":
                    with open(summary_file, "r") as f:
                        summaries = json.load(f)
                else:
                    with open(summary_file, "r") as f:
                        summary = {"global_summary": f.read()}

        # Generate context based on summary
        context = self.prompt_generator.generate(summaries if summary_mode == "detailed" else summary)

        if self.verbose:
            logger.info("Context generation complete.")
        return context, summary_file
