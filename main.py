import csv
from errorGenerator import ErrorGenerator
from typing import List
from typings import ErrorsContext, Severity

def format_messages_by_severity(issues: List[ErrorsContext], severity_level: Severity):
    return ", ".join(
        issue.message
        for issue in issues
        if issue.severity == severity_level
    )

def write_results_to_csv(results: dict, output_file: str):
    with open(output_file, mode="w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["task_id", "verdict", "errors", "warnings"])
        writer.writeheader()

        for task_id, issues in results.items():
            errors = format_messages_by_severity(issues, "error")
            warnings = format_messages_by_severity(issues, "warning")
            verdict = "failed" if errors or warnings else "passed"

            writer.writerow({
                "task_id": task_id,
                "verdict": verdict,
                "errors": errors,
                "warnings": warnings
            })

if __name__ == "__main__":
    runner = ErrorGenerator(
        mode="single",
        task_id="5f127f5f3a6b100017232099"
    )

    results = runner.getErrorsByTask()
    write_results_to_csv(results, "results/task_results.csv")
    print("Results written to task_results.csv")
