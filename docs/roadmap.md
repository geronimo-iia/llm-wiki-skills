# Roadmap

## Planned Skills

- `custom-type` — guide for creating custom page types with schemas
- `ci-cd` — set up CI/CD validation and deployment

## Skill Registry

Transform `llm-wiki-skills` into a llm-wiki itself — indexable,
searchable, with knowledge pages about the engine's design.

- Add wiki structure (`wiki.toml`, `schemas/`)
- Verify all skills pass `wiki_schema validate`
- Index and test search/graph
- Add knowledge pages (epistemic model, DKR, type system)
- Backward compatibility with Claude plugin

## Future

- Skill composition (`extends` field)
- Skill versioning (track which engine version a skill targets)
- Automated skill testing
