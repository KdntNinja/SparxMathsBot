#!/usr/bin/env python3
"""
SparxMathsBot - Automated Math Quiz Solver

This is the main entry point for the SparxMathsBot application.
The actual workflow implementation is modularized in the src/ package.
"""

import os
from src.geckodriver_setup import ensure_geckodriver
from src.logging_utils import setup_logger
from src.workflow import TimesTablesWorkflow, GeneralQuestionsWorkflow


def main():
    """Main entry point for the application."""
    # Ensure geckodriver is available
    ensure_geckodriver()

    # Set up logging
    logger = setup_logger()

    # Determine workflow type from environment or default to times tables
    workflow_type = os.getenv("WORKFLOW_TYPE", "times_tables").lower()

    # Run the appropriate workflow
    try:
        if workflow_type == "times_tables":
            workflow = TimesTablesWorkflow()
            logger.info("Starting Times Tables workflow...")
        elif workflow_type == "general":
            workflow = GeneralQuestionsWorkflow()
            logger.info("Starting General Questions workflow...")
        else:
            logger.warning(
                f"Unknown workflow type: {workflow_type}. Defaulting to Times Tables."
            )
            workflow = TimesTablesWorkflow()

        workflow.run_workflow()
        logger.info("Workflow run completed successfully.")
    except Exception as e:
        logger.error(f"Workflow failed: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
