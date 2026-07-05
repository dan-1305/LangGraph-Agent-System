"""
Context Bridge - Sovereign Context Pipeline cho external LLMs (Gemini/Claude/GPT)
============================================================================

Module ETL giúp bundle context thông minh trước khi gửi cho external LLM Web.

Pipeline: EXTRACT → TRANSFORM → ENRICH → ASSEMBLE

Public API:
    - context_pipeline.transform_content()
    - context_pipeline.enrich_section()
    - prepare_gemini_context.gather_context()
"""

from context_pipeline import (
    transform_content,
    enrich_section,
    get_file_meta,
    FileTransformer,
    SectionEnricher,
    FILE_REGISTRY,
)

__version__ = "3.0.0"
__all__ = [
    "transform_content",
    "enrich_section",
    "get_file_meta",
    "FileTransformer",
    "SectionEnricher",
    "FILE_REGISTRY",
]