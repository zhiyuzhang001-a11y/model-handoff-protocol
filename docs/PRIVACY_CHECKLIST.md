# Privacy checklist for publishing examples or handoffs

Never assume a handoff is safe to publish because it contains no source code.

Check for:

- home directories, usernames, hostnames, workspace and temporary paths;
- private repository, branch, organization, customer, product, or issue names;
- unreleased commit hashes, roadmap decisions, architecture, and security findings;
- credentials, tokens, environment variables, cookies, and signed URLs;
- command output, logs, stack traces, process IDs, terminal/session IDs, and CI URLs;
- proprietary test cases, performance figures, datasets, and customer-visible text;
- identities or links embedded in Git remotes and generated metadata.

For public examples:

1. start from `templates/MODEL_HANDOFF.md`, not a real packet;
2. invent repository names, paths, metrics, and commit placeholders;
3. retain the structure and decision shape, not the original facts;
4. run `python3 scripts/validate.py`;
5. review the final diff manually before push.
