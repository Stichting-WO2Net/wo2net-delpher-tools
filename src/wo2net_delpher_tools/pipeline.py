from wo2net_delpher_tools.oai import oai_get_record
from wo2net_delpher_tools.sru import get_issue_identifiers
from wo2net_delpher_tools.utils import save_issues_to_json
from wo2net_delpher_tools.models.issue import Issue

def process_ppn_to_json(ppn: str, output_file: str = "issues.json") -> list[Issue]:
    print(f"Verwerken gestart voor PPN: {ppn}")

    issue_identifiers = get_issue_identifiers(ppn)
    print(f"Gevonden {len(issue_identifiers)} issue-identifiers voor PPN {ppn}")

    issues = []
    for identifier in issue_identifiers:
        record = oai_get_record(identifier)
        issue = Issue.from_oai_record(record)
        issues.append(issue)
        print(f"Issue verwerkt: {issue.identifier}")

    save_issues_to_json(issues, output_file)
    print(f"Verwerken voltooid. Resultaten opgeslagen in {output_file}")

    return issues