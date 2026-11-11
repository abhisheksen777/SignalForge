"""Pipeline-specific exception types.

"""


class PipelineError(Exception):
    """Base class for all pipeline errors."""


class IntentParsingError(PipelineError):
    """Raised when intent parsing fails (LLM or validation)."""


class ExtractionError(PipelineError):
    """Raised when competitor extraction from raw results fails."""


class AggregationError(PipelineError):
    """Raised when deduplication / market analysis fails."""
