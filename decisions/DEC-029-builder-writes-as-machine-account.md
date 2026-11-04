# DEC-029 — Gli agenti scrivono su GitHub come `QN-Builder`, account macchina dichiarato

Status: DECIDED (4 November 2026, owner in the builder session, on the question put by the builder)
Supersedes in part: DEC-013, in the suspension of the identity separation for the builder's
writes. DEC-013 is unchanged and not reopened; it gains a pointer under its `Status:` line.
Integrates: DEC-028, point 1, without changing it. The Claude GitHub App stays installed on
QN, and the organization is still evaluated after a week without restrictions.
Blocks: nothing.

Question: DEC-028 left open whether the Claude GitHub App would make the builder's writes
appear as an app. Claude Code's documentation says it does not. Replies written by
Claude «are posted using your GitHub account, so they appear under your username, but each
reply is labeled as coming from Claude Code». GitHub attributes activity to an app only
when the app authenticates as itself, which Codex does and Claude does not.

GitHub's Terms of Service (B.3) say what is admitted instead: «A machine account is an
Account set up by an individual human who accepts the Terms on behalf of the Account» and
is «used exclusively for performing automated tasks»; «You may maintain no more than one
free machine account in addition to your free Personal Account»; «the owner of the Account
is ultimately responsible for the machine's actions».

Who writes on GitHub for the agents?

Context (audit of 30 October and the check of 4 November):
- **Commits.** Of the commits on the open pull-request branches, 363 are authored by
  «Claude», 48 were created through the API by the weekly watch job as the owner, and 10
  are the owner's own.
- **Comments and replies.** Almost all are machine-generated, often seconds apart, in a
  dialogue with the Codex bot.
- **Several automated clients on one personal account.** Claude cloud sessions, the
  ChatGPT/Codex connector of the watch job, and the owner from their own machine and the
  website.
- **Volumes.** The volumes never approached the official limits.

Hypothesis, not proven: a personal account that behaves like a bot is what the anti-abuse
classification reads as anomalous. It fits the record better than volume does. Only GitHub
support can confirm it.

Options:
A. The owner's account, with the protocol of DEC-028 and a profile that declares the use of
   AI assistants.
B. **CHOSEN.** `QN-Builder`, the account created in September and stopped by DEC-013,
   becomes the declared machine account through which every agent write goes.
C. B, but from the next day.

Claude recommendation: B.

Owner's words, 4 November 2026: «QN-Builder come account macchina».

## Rule

1. **Who writes.** The GitHub connection of Claude (claude.ai) is `QN-Builder`. Pushes,
   pull requests, comments and replies of the builder appear as `QN-Builder`. The owner's
   account carries no agent write.
2. **Declared.** `QN-Builder`'s profile states that it is a machine account of the owner for
   Quartieri News, operated by AI assistants, and names the owner as responsible.
3. **Scoped.** `QN-Builder` is a collaborator with the Write role on QN only. It has no
   admin role and is not in any ruleset bypass list. It never merges: that stays a process
   rule (DEC-012, DEC-013), and this entry does not enforce it.
4. **The owner's account stays human.**
   - It does the merges, the decisions and the settings.
   - It also posts the `@codex review` requests that the review integration does not accept
     from `QN-Builder`, because the integration authorises per requesting account
     (DEC-013).
   - The first review of a pull request starts on its own when the pull request is opened
     for review.
5. **Verified, not assumed.** On the first pull request after the switch the builder checks
   that the author and the pushes are `QN-Builder`. It records what the check shows and what
   it does not in `docs/autonomy/IDENTITY_AND_PERMISSIONS.md`.
6. **Not decided here.** The approval gate becomes possible again, because the owner can
   approve a pull request opened by `QN-Builder`. Turning it on is a ruleset setting the
   owner decides on separately.

Impact:
- **Owner steps.**
  - Install the Claude GitHub App on QN only.
  - Invite `QN-Builder` with the Write role.
  - On `QN-Builder`: profile, two-factor authentication, accept the invitation.
  - Connect Claude's GitHub on claude.ai while signed in as `QN-Builder`.
- **Repository.**
  - `CLAUDE.md`: the re-review rule says who asks.
  - `docs/github/PROTOCOLLO.md`, section 4.
  - `docs/autonomy/IDENTITY_AND_PERMISSIONS.md`, after the check.
  - The pointer in DEC-013.
- No change to pipeline, gazetteer, prompts, n8n, lane gate, CI or ruleset.

Decided by: owner · Date: 4 November 2026 · Affected components: GitHub accounts and
repository collaborators, Claude's GitHub connection, `CLAUDE.md`,
`docs/github/PROTOCOLLO.md`, `docs/autonomy/IDENTITY_AND_PERMISSIONS.md`, DEC-010, DEC-013,
DEC-028.
