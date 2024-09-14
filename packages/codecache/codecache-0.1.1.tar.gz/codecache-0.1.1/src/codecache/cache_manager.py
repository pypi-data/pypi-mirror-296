import os
import datetime
import logging
from typing import Dict, List, Optional
import google.generativeai as genai
from google.generativeai import caching

from .exceptions import CacheError

logger = logging.getLogger(__name__)


class CacheManager:
    MIN_TOKENS = 32768

    def __init__(self, api_key: str, model: str = "gemini-1.5-flash-001"):
        if not api_key:
            logger.error("Gemini API key is not set")
            raise CacheError("Gemini API key is not set")
        genai.configure(api_key=api_key)
        self.model_name = model
        self.model = genai.GenerativeModel(model)
        logger.info(f"Initialized CacheManager with model: {model}")

    def count_tokens(self, text: str) -> int:
        try:
            response = self.model.count_tokens(text)
            if hasattr(response, 'total_tokens'):
                return response.total_tokens
            elif hasattr(response, 'token_count'):
                return response.token_count
            else:
                return len(text.split())
        except Exception as e:
            logger.error(f"Error counting tokens: {str(e)}")
            raise CacheError(f"Failed to count tokens: {str(e)}")

    def cache_context(self, context: str, ttl_seconds: int = 3600, display_name: Optional[str] = None) -> str:
        try:
            token_count = self.count_tokens(context)
            logger.info(f"Context token count: {token_count}")

            if token_count < self.MIN_TOKENS:
                logger.warning(
                    f"Context has insufficient tokens ({token_count}). Minimum required: {self.MIN_TOKENS}"
                )
                raise CacheError(
                    f"Context has insufficient tokens ({token_count}). Minimum required: {self.MIN_TOKENS}"
                )

            system_prompt = (
                f"You are an AI assistant with detailed knowledge of the following codebase. "
                f"Use this information to assist with queries about the code:\n\n{context}"
            )

            logger.info(f"Caching context with TTL of {ttl_seconds} seconds...")
            cache = caching.CachedContent.create(
                model=self.model_name,
                display_name=display_name or f"Codebase context: {context[:50]}...",
                contents=[{"role": "user", "parts": [{"text": system_prompt}]}],
                ttl=datetime.timedelta(seconds=ttl_seconds),
            )
            logger.info(f"Context cached successfully. Cache key: {cache.name}")
            return cache.name
        except Exception as e:
            logger.error(f"Failed to cache context: {str(e)}")
            raise CacheError(f"Failed to cache context: {str(e)}")

    def query_context(self, cache_key: str, query: str) -> str:
        try:
            logger.info(f"Retrieving cached content for key: {cache_key}")
            cached_content = caching.CachedContent.get(cache_key)
            model_with_cache = genai.GenerativeModel.from_cached_content(
                cached_content=cached_content
            )
            logger.info("Sending query to Gemini model...")
            response = model_with_cache.generate_content(query)
            logger.info("Response received from Gemini model.")
            return response.text
        except Exception as e:
            logger.error(f"Failed to query cached context: {str(e)}")
            raise CacheError(f"Failed to query cached context: {str(e)}")

    def generate_content_from_prompt(
        self, prompt: str, max_tokens: int = 100, temperature: float = 0.2
    ) -> str:
        try:
            logger.info("Generating content from prompt.")
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens, temperature=temperature
                ),
            )
            logger.info("Content generated successfully.")
            return response.text
        except Exception as e:
            logger.error(f"Failed to generate content: {str(e)}")
            raise CacheError(f"Failed to generate content: {str(e)}")

    def list_caches(self) -> List[Dict]:
        try:
            caches = []
            for cache in caching.CachedContent.list():
                ttl_seconds = int(
                    (
                        cache.expire_time - datetime.datetime.now(datetime.timezone.utc)
                    ).total_seconds()
                )
                caches.append(
                    {
                        "key": cache.name,
                        "ttl": ttl_seconds,
                        "size": cache.usage_metadata.total_token_count,
                        "display_name": cache.display_name,
                        "create_time": cache.create_time,
                        "update_time": cache.update_time,
                        "expire_time": cache.expire_time,
                    }
                )
            return caches
        except Exception as e:
            logger.error(f"Failed to list caches: {str(e)}")
            raise CacheError(f"Failed to list caches: {str(e)}")

    def update_cache_ttl(self, cache_key: str, new_ttl_seconds: int) -> bool:
        try:
            cache = caching.CachedContent.get(cache_key)
            cache.update(ttl=datetime.timedelta(seconds=new_ttl_seconds))
            return True
        except Exception as e:
            logger.error(f"Failed to update cache TTL: {str(e)}")
            raise CacheError(f"Failed to update cache TTL: {str(e)}")

    def delete_cache(self, cache_key: str) -> bool:
        try:
            cache = caching.CachedContent.get(cache_key)
            cache.delete()
            return True
        except Exception as e:
            logger.error(f"Failed to delete cache: {str(e)}")
            raise CacheError(f"Failed to delete cache: {str(e)}")
