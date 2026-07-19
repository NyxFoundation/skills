# External Issue Auto-Close Workflow

This workflow closes issues opened by users who are not members of the organization (collaborators with write/admin access), ensuring that only the core team can initiate research threads while allowing the public to participate via comments.

## Implementation Logic

The core logic relies on the GitHub REST API to check the permission level of the issue creator.

### Workflow Trigger
- Event: `issues`
- Type: `opened`

### Permission Check
Use `github.rest.repos.getCollaboratorPermissionLevel`:
- **Admin/Write**: Keep open (Member).
- **Read/None**: Close and notify (External).

### Notification Content
The comment should:
1. Acknowledge the contribution.
2. Explain the policy (Member-only issue creation).
3. Encourage participation via comments on existing issues.

## Example Workflow File
See `templates/close-external-issues.yml` for a production-ready implementation.
