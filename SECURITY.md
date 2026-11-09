# Security and verification boundaries

External submissions are untrusted data and code. Review source before local
execution. Public pull-request checks receive no secrets and have read-only
repository permissions. Do not use privileged pull_request_target execution
of contributor code. Do not expose an operator's workstation or persistent
self-hosted runner to arbitrary submissions.

The exact-certificate CLI accepts bounded JSON and executes no submitted
commands. The elementary Lean workflow checks the reviewed pilot with a
pinned compiler. It is not a hardened proof marketplace for arbitrary Lean
metaprograms. See [formal scope](formal/README.md).

The scheduled research-cycle workflow runs trusted main-branch source. Its
write permission is used only to preserve generated public practice evidence
under research/cycles. It has no provider keys or private-library credential.
The separate agent research task may propose work through pull requests;
changing the verifier or acceptance policy requires human review.

Keep credentials, personal membership data, confidential journal materials
and proprietary research out of this public repository. Report a suspected
exposure privately to the repository owner using GitHub's available private
reporting/contact route; do not repeat secrets in a public issue.
