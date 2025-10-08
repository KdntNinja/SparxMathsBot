from src.workflow import SparxTTWorkflow
from src.logger_setup import setup_logger

logger = setup_logger()

if __name__ == "__main__":
    sparx = SparxTTWorkflow()
    sparx.run_workflow()
    logger.info("Workflow run completed.")