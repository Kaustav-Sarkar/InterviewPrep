### Repository Overview

- **Purpose**: Lifelong DSA + interview prep in Python and Java with clear structure, minimal duplication, and easy navigation.

### Directory Structure

- **`DataStructures/`**: Authoritative DS/Algo notes. Kept intact.
- **`DSA/Blind75/`**: Blind75 collection.
  - `index.yaml`: full list with metadata and code paths
  - `Blind75Python/`, `Blind75Java/`: solutions (self-contained)
- **`DSA/StriversSheet/`**: Striver’s SDE Sheet.
  - `index.yaml`: full list with metadata and code paths
- **`DSA/PythonDSA/`**: Flat, non-grouped Python solutions (CamelCase files, self-contained).
- **`DSA/JavaDSA/`**: Flat, non-grouped Java solutions (CamelCase files, `package DSA.JavaDSA`).
- **`CommonQuestions/`**: Common algorithms/designs (e.g., LRU, multithreading). Code-only.
- **`Past_interviews/`**: Interview notes (single Markdown per interview).
- **`Behavioral/`**, **`LLD/`**, **`docs/`**, **`scripts/`**: Supporting content and utilities.
- **`FinalPrepPlan.md`**: Personal plan (local; not tracked).

### Conventions

- **Naming**: Directories and filenames use CamelCase. YAML keys use snake_case.
- **Metadata**:
  - Non-grouped files include a top docstring/comment with: slug, title, difficulty, tags, link, time, space.
  - Collections live only in YAML (`DSA/Blind75/index.yaml`, `DSA/StriversSheet/index.yaml`) and store `python_path`/`java_path` to point at code.
- **No duplication**: Problems live once; collections reference them via paths.

### How to add new code

- **Non-grouped Python**
  1) Add `DSA/PythonDSA/MyProblem.py` (CamelCase filename)
  2) Add a top docstring with minimal metadata (slug, title, difficulty, tags, link, time, space)

- **Non-grouped Java**
  1) Add `DSA/JavaDSA/MyProblem.java` (CamelCase filename)
  2) Set first line `package DSA.JavaDSA;`
  3) Add a top block comment with the same minimal metadata

- **Blind75 / Striver**
  1) Put solutions in `DSA/Blind75/Blind75Python/` or `DSA/Blind75/Blind75Java/` (for Blind75)
  2) Update the corresponding `index.yaml` entry with `python_path`/`java_path`
  3) For Striver, you can point to the same files to avoid duplication

Sources: Blind75 (`https://leetcode.com/problem-list/oizxjoit/`), Striver’s SDE Sheet (`https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems`).
