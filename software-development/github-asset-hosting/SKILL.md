---
name: github-asset-hosting
description: Workflow for hosting images and assets that need to be visible in GitHub Issues/PRs when the primary project repository is private.
---

# GitHub Asset Hosting

When a project repository is private, images uploaded to that repository (via `raw.githubusercontent.com`) are not visible to users who are not authenticated or to the GitHub UI in certain contexts (e.g., external links in comments). To ensure assets are publicly visible and render correctly in Markdown, they must be hosted in a public repository.

## Workflow

1. **Create a Public Asset Repository**: 
   - Create a separate public repository (e.g., `user/project-assets`).
   - This repository acts as a CDN for the private project.
2. **Upload Assets**:
   - Push the required images/files to the `main` branch of the public asset repository.
3. **Reference via Raw URL**:
   - Use the format: `https://raw.githubusercontent.com/<owner>/<asset-repo>/main/<path-to-file>`
   - In GitHub comments, use the `<img>` tag or markdown image syntax: `![alt](url)`

## Pitfalls & Lessons

## Pitfalls & Lessons\n\n- **Private Repo Limitation**: Never assume `raw.githubusercontent.com` links from a private repo will work for general visibility; they require a valid GitHub token in the request header, which the browser's `<img>` tag cannot provide.\n- **Authentication Failure**: If images appear as broken links (404/403) in an issue, check the repository visibility of the source.\n- **Publicity**: Since the asset repo is public, ensure no sensitive data or private internal screenshots are uploaded.\n- **Local-to-Public Sync**: When using a local workspace for chart generation, the sync flow should be: `generate` → `copy to asset-repo` → `git commit/push` → `verify 200 OK` → `update markdown`.\n\n## Verification\n- Use `curl -I` or `curl -s -o /dev/null -w \"%{http_code}\"` to verify the URL returns a `200 OK` from a non-authenticated environment. Do this *before* posting the link to a GitHub issue.\n

## Verification
- Use `curl -I` or `curl -s -o /dev/null -w "%{http_code}"` to verify the URL returns a `200 OK` from a non-authenticated environment.
