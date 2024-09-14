class CodebaseContextError(Exception):
    """Base exception for codebase_context package."""


class ConfigurationError(CodebaseContextError):
    """Raised when there's an issue with configuration."""


class AnalysisError(CodebaseContextError):
    """Raised when there's an error during codebase analysis."""


class CacheError(CodebaseContextError):
    """Raised when there's an error related to caching operations."""
