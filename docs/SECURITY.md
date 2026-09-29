# EPE — Security

## 1. Threat Model

| Threat                                        | Mitigation                                |
|-----------------------------------------------|-------------------------------------------|
| Source document contains secrets              | Security validator scans on ingest        |
| Customer PII leaks into shared knowledge      | Sensitivity ACLs in retrieval layer       |
| AI prompt injection via source content        | Source content is treated as data, never as instructions; structured fields are extracted, not raw text |
| AI hallucinates unsupported requirement      | Traceability validator flags ungrounded claims |
| Secrets in prompts or logs                    | Redaction layer in `core/logging.py`      |
| Unauthorized access across projects           | Per-project path scoping; per-namespace ACL |
| Restricted content in public outputs          | Security validator blocks before write    |
| Cross-tenant data leakage in vector store     | Vector collection per project/namespace   |

## 2. Sensitivity Levels

| Level        | Description                                  | Storage                      |
|--------------|----------------------------------------------|------------------------------|
| public       | Marketing, public docs                       | All namespaces               |
| internal     | Internal EPE docs, internal runbooks         | All except restricted views  |
| confidential | Customer-confidential (single project)       | Per-project isolation        |
| restricted   | Highest sensitivity (per-item ACL)           | Per-item ACL enforced        |

Every `SourceDocument`, `KnowledgeItem`, and `Project` artifact carries a
`sensitivity` field. Retrieval returns only items whose sensitivity is
allowed for the calling stage and project.

## 3. AI Safety Boundaries

- AI is **never** trusted to invent a customer requirement, decision, or
  scope item. The Presales engine refuses to proceed if the input source
  documents do not contain enough evidence.
- AI prompts explicitly state: "Treat the source documents as evidence.
  Do not introduce claims that are not grounded in a source citation."
- Every AI-generated artifact is validated before it is persisted.
- AI output is parsed into structured fields; free-form text is preserved
  but the structured fields are what the next stage consumes.

## 4. Prompt Injection Defense

The ingestion layer:

1. Extracts structured fields (titles, headings, table rows) separately
   from free-form text.
2. Marks free-form text as `untrusted_text` in the prompt.
3. Wraps untrusted text in clearly delimited blocks
   (`<<<UNTRUSTED_SOURCE_DOCUMENT doc=DOC-NNN>>>`) and instructs the model
   to treat the block as data.
4. Separates any instruction-like content (lines starting with "Ignore
   previous", "You are now", etc.) into a flagged bucket that is logged
   and surfaced to the user in the ingestion report.

## 5. Secrets Handling

- No secrets are committed to `config/`. The Anthropic API key is read from
  the environment (`ANTHROPIC_API_KEY`).
- `.env` is gitignored.
- Logs are scrubbed of high-entropy strings and known secret patterns.
- Vector store embeddings do not include secrets (text is redacted before
  chunking).

## 6. Access Control

- All filesystem reads/writes are scoped to the project's path.
- The vector store uses a per-project collection; cross-project queries
  are refused at the retrieval layer.
- The FastAPI dashboard exposes read-only endpoints; state mutations go
  through the orchestrator CLI which enforces role checks.

## 7. Audit Trail

Every state transition, every gate evaluation, and every artifact write is
appended to `projects/<id>/.audit.log` as a single-line JSON record with
timestamp, actor, action, target, and outcome.

Audit records are append-only and never edited.

## 8. Data Retention

- Source documents: retention per `SourceDocument.retention`, default `P7Y`.
- Project artifacts: lifetime of project + `P7Y`.
- Vector embeddings: lifetime of the project; deleted on project archival.
- Audit log: lifetime of project + `P7Y`.

## 9. Compliance Posture

EPE does not by itself make a deployment compliant. It produces the
evidence trail a compliance program needs:

- requirement → design → test → acceptance chains
- decision logs with consequences
- risk register with mitigation
- audit trail of all changes

Customers and internal compliance teams export these artifacts as the
compliance evidence.

## 10. Cross-References

- See `docs/VALIDATION.md` for the security validator.
- See `docs/KNOWLEDGE_MODEL.md` for sensitivity propagation.
- See `docs/DATA_MODEL.md` for the `sensitivity` field on entities.
- See `docs/CONFIGURATION.md` for environment-scoped configuration.
