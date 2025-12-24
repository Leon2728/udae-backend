# Versioning Policy

## Semantic Versioning
UDAE Backend follows **Semantic Versioning 2.0.0** (semver.org):

- **MAJOR**: Breaking changes in core evaluation logic or contracts
- **MINOR**: New features, new normative rules, backward-compatible
- **PATCH**: Bug fixes, clarifications, performance improvements

## Version Format
`MAJOR.MINOR.PATCH` (e.g., `1.3.2`)

## Backward Compatibility Guarantee
- Audit results produced by version X.Y.Z must be verifiable by any version X.*.*
- Normative rules are versioned independently
- Snapshot format changes require MAJOR bump

## Deprecation Policy
- Deprecated features: announced 2 MINOR versions before removal
- Core contracts: never removed without MAJOR version change

## Status
Policy active from v0.1.0 onwards.