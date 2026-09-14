---
name: meal-log
description: Manage dietary and nutritional logs for the user using a specialized Excel-based system in the grandchildrice/life repository.
---

# Meal Log Management

This skill governs the recording, auditing, and synchronization of the user's meal and nutrition logs. The system is centered around a structured Excel workbook (`meal_log.xlsx`) that tracks daily intake and generates nutritional aggregates (Kcal, P, F, C).

## Core System Architecture
The system resides in `grandchildrice/life/meal/` and consists of:
- `meal_log.xlsx`: The primary data store. Contains sheets for raw records (`記録`), daily aggregates (`日次`), weekly (`週次`), and monthly (`月次`) summaries, plus a configuration sheet (`使い方・設定`).
- `append_meal.py`: The primary tool for adding new meal items. It validates input, updates the workbook, extends aggregate sheets, and rebuilds charts.
- `check_meal.py`: A sanity checker that ensures the workbook structure, formulas, and charts are intact.
- `build_meal_log.py`: Initializes a new workbook from scratch.
- `meal_lib.py`: Shared logic for styles, formats, and workbook manipulation.
- `sync_meal.sh`: Synchronizes the local workbook to Google Drive (via rclone) and GitHub.

## Workflow: Recording a Meal

When the user provides a meal description or image:
1. **Nutrition Estimation**: Estimate the kcal, P (Protein), F (Fat), and C (Carbohydrate) for each item.
2. **JSON Preparation**: Format the data into a JSON array of records. Each record must have:
   - `date`: YYYY-MM-DD
   - `time`: HH:MM (approximate if unknown)
   - `type`: One of `朝食`, `昼食`, `夕食`, `間食`, `飲み物`
   - `menu`: Item name
   - `amount`: Weight or volume (e.g., "100g")
   - `kcal`, `p`, `f`, `c`: Numeric values
   - `confidence`: `high`, `medium`, or `low`
3. **Execution**: Run the append script via `uv run`:
   ```bash
   cd grandchildrice/life/meal && uv run append_meal.py /path/to/records.json
   ```
4. **Verification**:
   - Check the output of `append_meal.py` for success.
   - Run `uv run check_meal.py` to ensure the workbook remains healthy.
5. **Synchronization**: Push changes to GitHub and (if requested/configured) Google Drive.

## Pitfalls & Constraints

- **No Guessing without Confidence**: `append_meal.py` will reject records with `confidence: low` or vague menu names (e.g., "something") unless `--allow-uncertain` is passed. If unsure, ask the user.
- **Zero kcal**: Only water/tea-like items are allowed to have 0 kcal. Others require `--allow-zero`.
- **Recalculation**: The workbook uses LibreOffice (`soffice`) for headless recalculation of cached formula values. If `soffice` is missing, values may not update until the file is opened in a spreadsheet app.
- **Graph Latency**: If the user reports a graph isn't updating, verify that the data was actually appended to the `記録` sheet and that the `日次`/`週次`/`月次` sheets were extended to cover the new date.

## Verification Steps
- `uv run check_meal.py`: Confirms sheets, charts, and formulas are correct.
- `meal_lib.read_records()`: Use a small python snippet to verify the last few rows of the `記録` sheet.
