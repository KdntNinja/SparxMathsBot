"""Main workflow module for SparxMathsBot."""

from .times_tables_workflow import TimesTablesWorkflow
from .general_questions_workflow import GeneralQuestionsWorkflow

# For backward compatibility
SparxTTWorkflow = TimesTablesWorkflow

__all__ = ["TimesTablesWorkflow", "GeneralQuestionsWorkflow", "SparxTTWorkflow"]
