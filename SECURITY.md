# Security Policy

## Reporting a Vulnerability

If you believe you have found a security vulnerability in this repository or in the content
pipeline it describes, please report it privately rather than opening a public issue.

Email details to **karsten@tensormesh.ai**. Include enough to reproduce the problem —
steps, screenshots, or a minimal example. We will investigate every report and do our best
to fix the problem quickly.

Vulnerabilities in **LMCache itself** belong upstream: see
[LMCache's security policy](https://github.com/LMCache/LMCache/blob/dev/SECURITY.md).

## Credentials and unpublished content

Two classes of mistake are worth reporting here even though they are not vulnerabilities in
code:

- **A credential, token, or API key committed to this repo.** Report it privately and it
  gets rotated, not just deleted from the history.
- **Embargoed or unpublished content, or a customer name, that reached a public surface.**
  The skeleton's `Notes for the editor` section exists to keep this material out of drafts;
  if something got through, say so privately so it can be pulled before it spreads.
