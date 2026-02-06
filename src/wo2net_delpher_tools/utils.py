import json
from wo2net_delpher_tools.models.issue import Issue

def save_issues_to_json(issues: list[Issue], file_path: str) -> None:
    issues_data = [issue.to_dict() for issue in issues]

    with open(file_path, 'w') as f:
        json.dump(issues_data, f, indent=4)