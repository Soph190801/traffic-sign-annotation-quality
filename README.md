# Traffic Sign Detection – Programmatic Quality Checks

This project addresses a common challenge at scale: maintaining high-quality task output in large, human-annotated pipelines. When images are annotated at high volumes, even small lapses in quality can significantly impact the final deliverable.

Customers expect consistently high-quality tasks, which makes automated quality checks a valuable line of defense. These checks help catch issues early.

This project implements a configurable quality-checking framework that programmatically reviews completed tasks to flag potentially low-quality or suspicious annotations. The system is modular and reusable, enabling teams to easily apply and manage multiple checks across projects.

---

## Features

### Truncation Check

Compares truncation attribute values against the bounding box’s proximity to the image edges. See the `TruncationConfig` class in `typings.py` for configurable options.

### Attribute Conditions Check

Validates that certain attributes are correctly set for specific labels. See the `AttributeConditionConfig` class in `typings.py` for configurable options.

### Max Size Check

Flags annotations whose bounding boxes exceed defined height or width limits. See the `MaxSizeConfig` class in `typings.py` for configurable options.

---

## How to Use

### 1. Define Your Checks

In `run_checks.py`, create configurations for the checks you want to run. Each check requires:

- A config object (e.g., `TruncationConfig`)
- An `ErrorsContext` message with severity
- The actual check function call

### Example

```python
configName = ConfigClassName(
    config1=configValue1,
    config2=configValue2
)

errorContext = ErrorsContext(
    message="Desired error message",
    severity="error"  # or "warning"
)

functionCall(annotations, configName, errors, errorContext)  # Always pass `errors` to collect issues
```

### 2. Run the Checks
    - In `main.py`, initialize the error generator and run the checks.
    - Single Task Mode – Pass a `task_id`
    - Multiple Task Mode – Provide `filters` like project name and status

## Check the Output

Results are stored in:
- A dictionary: `{ task_id: [list of errors/warnings] }`
- A CSV file named `results/task_results.csv` with columns:

`task_id, verdict, errors, warnings`

The verdict is based on whether any errors were found, with messages and severity coming from the configured `ErrorsContext`.

---

## Notes

- All checks are designed to be reusable and composable.
- You can define multiple checks in `run_checks.py` by passing different configs.
- The system can be extended for additional checks such as overlap detection, attribute conflicts, or invalid label geometry.

---

## Installation

Clone the repository and install dependencies:
`git clone https://github.com/your-username/project-name.git`
`cd project-name`
`pip install -r requirements.txt`