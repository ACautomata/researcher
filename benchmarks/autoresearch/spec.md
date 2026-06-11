# Autoresearch Wiki QA Benchmark

Tests wiki knowledge retrieval, cross-paper comparison, mechanism understanding, and cross-domain synthesis.

## Structure
- `wiki/` ¡ª Full wiki knowledge base
- `autoresearch-1/` through `autoresearch-10/` ¡ª 10 shards x 5 QAs = 50 total

## Scoring
All QAs use `judge: "agent"` ¡ª the judge agent evaluates answers against rubrics.

## Constraints
- No subagent delegation prompts in QA questions
- Main agent reads wiki files directly and answers
- Each shard is independent and runs in its own container
