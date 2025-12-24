# Adapters

Ports & Adapters layer for external integrations.

## Responsibility
Translate external world (APIs, files, UI) into core domain models and vice versa.

## Principles
- **No business logic here**
- Thin translation layer
- Core remains independent

## Submodules
- `api/` - REST/GraphQL endpoints
- `word/` - Microsoft Word integration
- `gdocs/` - Google Docs integration
- `web/` - Web UI adapter

## Status
Architecture defined. Implementation pending.