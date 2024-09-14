import click
import logging
from pathlib import Path
from dotenv import load_dotenv

from .analyzer import CodebaseAnalyzer
from .cache_manager import CacheManager
from .config import Config
from .exceptions import ConfigurationError, AnalysisError, CacheError

load_dotenv()
logger = logging.getLogger(__name__)


@click.group()
@click.version_option()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, verbose):
    """CodeCache: Generate and cache system prompts for your codebase."""
    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    pass


@cli.command()
@click.argument(
    "directory", type=click.Path(exists=True, file_okay=False, dir_okay=True), default="."
)
@click.option(
    "--ignore-file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="Path to custom ignore file. If not provided, .codecachignore in the root directory will be used if it exists.",
)
@click.option("--ttl", type=int, default=3600, help="Cache time-to-live in seconds.")
@click.option(
    "--summary-mode",
    type=click.Choice(["quick", "detailed"]),
    default="quick",
    help="Summary mode to use (quick or detailed).",
)
@click.option(
    "--model", type=str, default=None, help="Gemini model to use (e.g., gemini-1.5-flash-001)."
)
@click.pass_context
def cache(ctx, directory, ignore_file, ttl, summary_mode, model):
    """Analyze codebase and cache context."""
    verbose = ctx.obj['VERBOSE']
    try:
        if verbose:
            click.echo("Starting codebase analysis and context caching...")
        config = Config(Path(directory))
        if model:
            config.set_gemini_model(model)
        gemini_model = config.get_gemini_model()
        if verbose:
            click.echo(f"Initializing CacheManager with Gemini model: {gemini_model}")
        cache_manager = CacheManager(config.get_gemini_api_key(), model=gemini_model)

        if verbose:
            click.echo(f"Analyzing codebase in directory: {directory}")
        analyzer = CodebaseAnalyzer(directory, ignore_file, cache_manager, verbose=verbose)

        if verbose:
            click.echo(f"Generating context using {summary_mode} summary mode...")
        context, summary_file = analyzer.generate_context(summary_mode)

        if summary_file:
            if verbose:
                click.echo(f"Summary file saved to: {summary_file.absolute()}")

        if verbose:
            click.echo(f"Caching context with TTL of {ttl} seconds...")
        cache_key = cache_manager.cache_context(context, ttl)

        click.echo(f"Context cached successfully. Cache key: {cache_key}")
    except (ConfigurationError, AnalysisError, CacheError) as e:
        logger.error(f"Error: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)


@cli.command()
@click.argument("cache_key")
@click.argument("query")
def query(cache_key: str, query: str):
    """Query the cached context."""
    try:
        logger.info(f"Querying cached context with key: {cache_key}")
        config = Config(Path.cwd())
        cache_manager = CacheManager(config.get_gemini_api_key())

        logger.info("Sending query to Gemini model...")
        response = cache_manager.query_context(cache_key, query)
        logger.info("Response received.")
        click.echo(response)
    except (ConfigurationError, CacheError) as e:
        logger.error(f"Error: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)


@cli.command()
def list_caches():
    """List all cached contexts."""
    try:
        config = Config(Path.cwd())
        cache_manager = CacheManager(config.get_gemini_api_key())

        caches = cache_manager.list_caches()
        if caches:
            for cache in caches:
                click.echo(
                    f"Key: {cache['key']}, TTL: {cache['ttl']} seconds, Size: {cache['size']} tokens"
                )
        else:
            click.echo("No caches found.")
    except (ConfigurationError, CacheError) as e:
        logger.error(f"Error: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)


@cli.command()
@click.argument("key")
@click.argument("new_ttl", type=int)
def update_ttl(key: str, new_ttl: int):
    """Update the TTL for a cached context."""
    try:
        config = Config(Path.cwd())
        cache_manager = CacheManager(config.get_gemini_api_key())

        success = cache_manager.update_cache_ttl(key, new_ttl)
        if success:
            click.echo(f"Updated TTL for cache {key} to {new_ttl} seconds")
        else:
            click.echo(f"Failed to update TTL for cache {key}")
    except (ConfigurationError, CacheError) as e:
        logger.error(f"Error: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)


@cli.command()
@click.argument("key")
def delete_cache(key: str):
    """Delete a cached context."""
    try:
        config = Config(Path.cwd())
        cache_manager = CacheManager(config.get_gemini_api_key())

        success = cache_manager.delete_cache(key)
        if success:
            click.echo(f"Deleted cache {key}")
        else:
            click.echo(f"Failed to delete cache {key}")
    except (ConfigurationError, CacheError) as e:
        logger.error(f"Error: {str(e)}")
        click.echo(f"Error: {str(e)}", err=True)


if __name__ == "__main__":
    cli()
