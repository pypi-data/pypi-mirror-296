import os
import logging
from pathlib import Path
from typing import Optional
import toml

from .exceptions import ConfigurationError

logger = logging.getLogger(__name__)


class Config:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.config_file = project_root / ".codebase_context"
        self.config = self._load_config()

    def _load_config(self) -> dict:
        if self.config_file.exists():
            try:
                return toml.load(self.config_file)
            except toml.TomlDecodeError as e:
                logger.error(f"Error parsing config file: {str(e)}")
                raise ConfigurationError(f"Error parsing config file: {str(e)}")
        return {}

    def _save_config(self):
        with open(self.config_file, "w") as f:
            toml.dump(self.config, f)

    def get_gemini_api_key(self) -> str:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY environment variable is not set")
            raise ConfigurationError("GEMINI_API_KEY environment variable is not set")
        return api_key

    def get_gemini_model(self) -> str:
        return self.config.get("gemini_model", "gemini-1.5-flash-001")

    def set_gemini_model(self, model: str):
        self.config["gemini_model"] = model
        self._save_config()

    def get_ignore_file(self) -> Optional[Path]:
        ignore_file = self.config.get("ignore_file")
        if ignore_file:
            return self.project_root / ignore_file
        return None

    def set_ignore_file(self, ignore_file: str):
        self.config["ignore_file"] = ignore_file
        self._save_config()

    def get_default_ttl(self) -> int:
        return self.config.get("default_ttl", 3600)
