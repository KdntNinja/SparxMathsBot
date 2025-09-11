# SparxMathsBot - Workflow Structure

This project now supports multiple workflow types for different math question categories.

## Workflow Types

### 1. Times Tables Workflow
- **File**: `src/times_tables_workflow.py`
- **Purpose**: Specialized for SparxMaths Times Tables / 100 Club Check
- **Usage**: `WORKFLOW_TYPE=times_tables python3 main.py`

### 2. General Questions Workflow  
- **File**: `src/general_questions_workflow.py`
- **Purpose**: Handles various math question types (algebra, arithmetic, etc.)
- **Usage**: `WORKFLOW_TYPE=general python3 main.py`

## Key Features

✅ **Modular Design**: Separate workflows for different question types
✅ **Base Class**: Common functionality shared through `BaseSparxWorkflow`
✅ **Backward Compatibility**: Original `SparxTTWorkflow` still works
✅ **Runtime Selection**: Choose workflow type via environment variable
✅ **Extensible**: Easy to add new workflow types

## Quick Start

```bash
# Times Tables (default)
python3 main.py

# General Questions
WORKFLOW_TYPE=general python3 main.py
```

Your code is now properly separated and ready for different question types! 🚀
