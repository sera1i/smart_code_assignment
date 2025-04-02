import subprocess
import tempfile
import shutil
import os

def evaluate_code(code_path: str, test_cases: list, language: str = "c") -> dict:
    results = {
        "compiled": False,
        "compile_errors": "",
        "test_results": [],
        "passed": 0,
        "failed": 0,
        "total": len(test_cases)
    }

    temp_dir = tempfile.mkdtemp()
    try:
        if language == "c":
            compile_cmd = ["gcc", code_path, "-o", f"{temp_dir}/program"]
        elif language == "cpp":
            compile_cmd = ["g++", code_path, "-o", f"{temp_dir}/program"]
        else:
            raise ValueError("Unsupported language")

        compile_process = subprocess.run(
            compile_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if compile_process.returncode != 0:
            results["compile_errors"] = compile_process.stderr
            return results
        else:
            results["compiled"] = True

        for test_case in test_cases:
            input_data = test_case.get("input", "")
            expected_output = test_case.get("expected_output", "").strip()

            run_process = subprocess.run(
                [f"{temp_dir}/program"],
                input=input_data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5
            )

            actual_output = run_process.stdout.strip()

            test_result = {
                "input": input_data,
                "expected_output": expected_output,
                "actual_output": actual_output,
                "passed": actual_output == expected_output
            }

            results["test_results"].append(test_result)
            results["passed" if test_result["passed"] else "failed"] += 1

    except subprocess.TimeoutExpired:
        results["test_results"].append({
            "input": input_data,
            "expected_output": expected_output,
            "actual_output": "Timeout",
            "passed": False
        })
        results["failed"] += 1
    except Exception as e:
        results["compile_errors"] = f"Error: {str(e)}"
    finally:
        shutil.rmtree(temp_dir)

    return results