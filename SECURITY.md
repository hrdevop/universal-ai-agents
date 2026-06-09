# Security Policy

## Reporting a vulnerability

Please report security issues **privately** — do not open a public issue for a
vulnerability.

- Use GitHub's **[Report a vulnerability](https://github.com/hrdevop/universal-ai-agents/security/advisories/new)**
  (Security → Advisories) to open a private advisory, **or**
- Contact the maintainer privately via GitHub ([@hrdevop](https://github.com/hrdevop)).

Please include what you found, how to reproduce it, and the potential impact. We aim to
acknowledge reports within a few days and will keep you updated on the fix.

## Scope

This repository contains **configuration- and prompt-driven agents** (Markdown + YAML),
not a running service. The most relevant concerns are therefore:

- **Prompt-injection / unsafe-instruction issues** — e.g. a job listing or web page that
  tries to make an agent fabricate information, bypass the confirmation gate, exfiltrate
  data, or auto-submit. Reports that demonstrate a bypass of the safety rules below are
  in scope and valued.
- **Accidental exposure of personal data** — e.g. a path or example that would cause a
  user's real profile or generated output to be committed. (CI already fails the build if
  tracked files include a real `config.yaml`, a non-example profile, or anything under
  `output/<user>/`.)

## Safety model (what agents must never do)

These rules are enforced in every agent's `AGENTS.md` and should hold regardless of any
configuration:

- Never fabricate information — materials use only the user's real, profile-provided data.
- Never submit an application or other outward-facing action without the user's explicit
  confirmation.
- Never bypass captchas or login walls, and never auto-solve hiring assessments — pause
  and ask the user.

## Please do not include secrets

When filing any report or issue, **redact personal data** — real resumes, emails, API
keys, tokens. This repo is designed so none of that is ever needed to reproduce a problem.
