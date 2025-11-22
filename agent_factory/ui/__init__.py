"""
Zero-config UI generator - Generate web UIs for agents.
"""

from agent_factory.ui.generator import generate_ui
from agent_factory.ui.schema_inference import infer_ui_schema

__all__ = ["generate_ui", "infer_ui_schema"]
