# AGENTS.md

## Purpose
This project uses **Spec-Driven Development (SDD)** where no code is written until specifications are complete.

## Agent Instructions

### Core Rule
**No code may be written without a corresponding specification in specs/speckit.specify**

### Workflow
1. **Specify** → Write requirements in `specs/speckit.specify`
2. **Plan** → Create technical approach in `specs/speckit.plan`
3. **Tasks** → Break into actionable items in `specs/speckit.tasks`
4. **Implement** → Write code only after all above are complete

### When Generating Code
All code must:
- Reference the spec section it implements
- Include task ID in comments
- Follow constitution principles
- Include type hints and docstrings

### File Organization
- `specs/speckit.constitution` - Project principles and constraints
- `specs/speckit.specify` - What to build (requirements)
- `specs/speckit.plan` - How to build it (architecture)
- `specs/speckit.tasks` - Breakdown of work items
- `src/` - Implementation code

### Agent Behavior
When asked to implement a feature:
1. First check if specification exists
2. If not, request that specification be written first
3. Only generate code after spec is confirmed
4. Always reference spec section in code comments

## Technology Constraints
- Python 3.13+ only
- No external dependencies
- In-memory storage only
- Console-based interface
