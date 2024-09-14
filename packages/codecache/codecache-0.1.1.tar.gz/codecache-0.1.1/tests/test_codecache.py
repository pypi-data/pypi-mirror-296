import unittest
from pathlib import Path
from codecache.cache_manager import CacheManager
from codecache.config import Config
from codecache.exceptions import ConfigurationError, CacheError


class TestCacheManager(unittest.TestCase):
    def setUp(self):
        # Use a fake API key for testing
        self.api_key = "fake_api_key"
        self.model_name = "gemini-1.5-flash-001"
        self.cache_manager = CacheManager(api_key=self.api_key, model=self.model_name)

    def test_initialization(self):
        self.assertEqual(self.cache_manager.model_name, self.model_name)

    def test_get_gemini_api_key_failure(self):
        with self.assertRaises(ConfigurationError):
            config = Config(Path.cwd())
            config.get_gemini_api_key()

    def test_count_tokens_failure(self):
        with self.assertRaises(CacheError):
            self.cache_manager.count_tokens("Test text")

    def test_cache_context_failure(self):
        with self.assertRaises(CacheError):
            self.cache_manager.cache_context("Test context")


if __name__ == "__main__":
    unittest.main()
