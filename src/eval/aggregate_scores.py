import csv
import os
from typing import Dict, List, Any

OUTPUT_FOLDER = "data/eval_outputs"
MAPPING_CSV = os.path.join(OUTPUT_FOLDER, "xy_mapping.csv")
SCORES_CSV = os.path.join(OUTPUT_FOLDER, "scores.csv")


def load_xy_mapping(path: str) -> Dict[str, Dict[str, str]]:
    """
    Returns: { clip: {"X": "baseline|structured", "Y": "baseline|structured"} }
    """
    mapping: Dict[str, Dict[str, str]] = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            clip = (row.get("clip") or "").strip()
            x_cond = (row.get("X_condition") or "").strip()
            y_cond = (row.get("Y_condition") or "").strip()
            if clip:
                mapping[clip] = {"X": x_cond, "Y": y_cond}
    return mapping


def load_scores(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def normalize_rows(
    score_rows: List[Dict[str, Any]],
    mapping: Dict[str, Dict[str, str]],
) -> List[Dict[str, Any]]:

    normalized: List[Dict[str, Any]] = []

    for row in score_rows:
        clip = (row.get("clip") or "").strip()
        set_label = (row.get("set") or "").strip().upper()

        if clip not in mapping:
            continue

        if set_label not in ("X", "Y"):
            continue

        condition = mapping[clip][set_label]

        new_row = dict(row)
        new_row["condition"] = condition

        normalized.append(new_row)

    return normalized


def main():
    if not os.path.exists(MAPPING_CSV):
        raise FileNotFoundError(f"Missing mapping: {MAPPING_CSV}")

    mapping = load_xy_mapping(MAPPING_CSV)
    print(f"[OK] xy_mapping rows: {len(mapping)}")

    if os.path.exists(SCORES_CSV):
        scores = load_scores(SCORES_CSV)
        print(f"[OK] scores rows: {len(scores)}")
    else:
        print(f"[INFO] scores.csv not found yet: {SCORES_CSV}")

    if os.path.exists(SCORES_CSV):
        scores = load_scores(SCORES_CSV)
        print(f"[OK] scores rows: {len(scores)}")

        normalized = normalize_rows(scores, mapping)
        print(f"[OK] normalized rows: {len(normalized)}")
   
    else:
        print(f"[INFO] scores.csv not found yet: {SCORES_CSV}")


if __name__ == "__main__":
    main()
