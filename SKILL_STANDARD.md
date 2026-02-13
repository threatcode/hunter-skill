# Hunter Skill Standard Format & Structure

## Project Overview

The Hunter Skill project is a comprehensive collection of cybersecurity skills and knowledge, organized into JSON files across three main sources:

- **skills/** - PayloadsAllTheThings collection
- **skills/** - h4cker collection
- **skills/** - HackTricks collection

### Project Statistics
- Multiple skill files organized by categories
- JSON-based format for easy parsing and consumption
- Skills sourced from well-known security resources

---

## Current Format (As-Is)

### Current JSON Structure
```json
{
  "id": "category_name-hash_identifier",
  "category": "Category Name",
  "title": "Skill Title",
  "description": "Brief description of the skill...",
  "payloads": [
    "Array of content lines",
    "Line 2",
    "Line 3"
  ],
  "source": "SourceName",
  "references": [
    "Path/to/original/file.md"
  ]
}
```

### Current Issues Identified

1. **Inconsistent Category Naming**
   - Some use spaces: "Account Takeover"
   - Some use hyphens: "generic-hacking"
   - Some use underscores: "programming-and-scripting-for-cybersecurity"
   - Inconsistent capitalization

2. **Missing Metadata**
   - No timestamps (created_at, updated_at)
   - No version information
   - No difficulty levels
   - No tags/keywords for discoverability
   - No author information
   - No status/lifecycle information

3. **ID Generation**
   - Not consistently formatted
   - Hash identifiers are 12-16 characters
   - No semantic meaning beyond uniqueness

4. **Description Handling**
   - Descriptions are often truncated
   - May contain Markdown formatting mixed with content

5. **Payloads Array**
   - Stored as array of strings (good for line-based storage)
   - Can be reassembled into content by joining with newlines

6. **Missing Validation**
   - No schema validation
   - No required field checks
   - No format specification

---

## Standard Format (To-Be)

### Canonical JSON Schema

```json
{
  "version": "1.0.0",
  
  "metadata": {
    "id": "unique-identifier",
    "schema_version": "1.0.0",
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z",
    "status": "active"
  },
  
  "classification": {
    "category": "Category Name",
    "subcategory": "Optional Subcategory",
    "tags": ["tag1", "tag2"],
    "difficulty": "beginner|intermediate|advanced",
    "attack_type": "exploitation|reconnaissance|post-exploitation",
    "cves": ["CVE-2021-44228"]
  },
  
  "content": {
    "title": "Skill Title",
    "description": "Comprehensive description",
    "summary": "Brief one-line summary",
    "payloads": ["Array of content lines"]
  },
  
  "context": {
    "source": "Source Name",
    "references": [
      {
        "title": "Reference Title",
        "url": "https://example.com",
        "type": "github|blog|documentation|tool"
      }
    ],
    "author": "Original Author",
    "license": "License Information"
  }
}
```

### Key Improvements

#### 1. **Version Control**
- Explicit schema version for migrations
- Metadata tracking for audit trails

#### 2. **Standardized Categorization**
```
Format: "Category Name" (title case with spaces)
Examples:
  - "Account Takeover"
  - "API Key Leaks"
  - "CVE Exploits"
  - "Methodology and Resources"
```

#### 3. **Metadata Fields**
- `id`: Semantic identifier (e.g., "log4shell-cve-2021-44228")
- `created_at/updated_at`: ISO 8601 timestamps
- `status`: active|deprecated|retired|draft
- `version`: Skill version number

#### 4. **Enhanced Classification**
- `category`: Primary classification
- `subcategory`: Optional deeper classification
- `tags`: Array of searchable keywords
- `difficulty`: Standardized skill difficulty
- `attack_type`: Type of attack/technique
- `cves`: Associated CVE identifiers

#### 5. **Structured References**
- Moving from string paths to structured objects
- Include reference type and title
- Support multiple reference types

#### 6. **Content Structure**
- `title`: Clear, concise skill name
- `summary`: One-line description
- `description`: Full description
- `payloads`: Content array maintained for compatibility

---

## Migration Strategy

### Phase 1: Schema Definition & Validation
1. ✓ Define canonical schema (this document)
2. Create JSON Schema (.schema.json)
3. Create validation tools/scripts

### Phase 2: Gradual Migration
1. Start with new skills using new format
2. Migrate high-priority skills
3. Create migration tooling for bulk updates

### Phase 3: Backward Compatibility
1. Support both v1.0 and new format
2. Provide conversion utilities
3. Document deprecation timeline

### Phase 4: Full Implementation
1. Migrate all remaining skills
2. Retire old format support
3. Update all tooling and documentation

---

## Standards & Best Practices

### ID Format
- **Pattern**: `[skill-name]-[identifier]`
- **Example**: `log4shell-cve-2021-44228` or `sql-injection-blind`
- **Guidelines**:
  - Use lowercase with hyphens
  - Be semantic and meaningful
  - Include CVE if applicable
  - Use UUID or hash for uniqueness suffix if needed

### Category Standardization
- Use title case
- Single-word or hyphenated multi-word (in JSON use spaces)
- Standard categories:
  - Account Takeover
  - API Key Leaks
  - CVE Exploits
  - Encoding Transformations
  - File Inclusion
  - Insecure Deserialization
  - LDAP Injection
  - Methodology and Resources
  - Learning and Socials
  - [Custom categories as needed]

### Difficulty Levels
- `beginner`: Basic concepts, common exploits
- `intermediate`: Requires some knowledge, nuanced techniques
- `advanced`: Advanced exploitation, sophisticated techniques

### Attack Types
- `reconnaissance`: Information gathering
- `exploitation`: Actual compromise/vulnerability exploitation
- `post-exploitation`: Post-compromise activities
- `evasion`: Evading security controls
- `social-engineering`: Human-focused attacks

### Timestamps
- Format: ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)
- Timezone: Always UTC
- Example: `2025-01-15T14:30:00Z`

### References Structure
```json
{
  "title": "Reference Title",
  "url": "https://example.com/reference",
  "type": "github|blog|documentation|tool|pdf|video",
  "author": "Author Name (optional)",
  "date": "2025-01-15 (optional)"
}
```

### Tags Guidelines
- Use lowercase
- Use hyphens for multi-word tags
- Include: technique, impact, affected-software, etc.
- Examples: `mfa-bypass`, `log4j`, `authentication`, `web`

---

## File Organization

### Directory Structure
```
/hunter-skill/
  ├── skills/                          # PayloadsAllTheThings
  │   ├── [skill-files].json
  │   └── ...
  ├── skills/                   # h4cker collection
  │   ├── [skill-files].json
  │   └── ...
  ├── skills/               # HackTricks collection
  │   ├── [skill-files].json
  │   └── ...
  ├── SKILL_STANDARD.md               # This document
  ├── SKILL_SCHEMA.json               # JSON Schema definition
  ├── scripts/
  │   ├── validate_skills.py          # Validation script
  │   ├── migrate_skills.py           # Migration script
  │   └── generate_skills.py          # Generation script
  └── docs/
      └── MIGRATION_GUIDE.md          # Migration step-by-step
```

---

## Implementation Checklist

- [ ] Create JSON Schema definition (.schema.json)
- [ ] Implement validation script
- [ ] Create migration tooling
- [ ] Validate existing skills against new schema
- [ ] Generate compliance reports
- [ ] Create audit trail
- [ ] Update documentation
- [ ] Add CI/CD validation
- [ ] Gradual migration of files
- [ ] Full compliance verification

---

## Tools & Utilities

### Validation
```bash
# Validate against schema
python3 scripts/validate_skills.py --schema SKILL_SCHEMA.json

# Validate specific directory
python3 scripts/validate_skills.py skills/ --schema SKILL_SCHEMA.json

# Generate compliance report
python3 scripts/validate_skills.py --report compliance.json
```

### Migration
```bash
# Dry run migration
python3 scripts/migrate_skills.py --dry-run

# Migrate specific category
python3 scripts/migrate_skills.py --category "CVE Exploits"

# Full migration
python3 scripts/migrate_skills.py --all
```

---

## Questions & Clarifications Needed

1. Should all existing skills be migrated or only new ones?
2. What is the priority order for migration?
3. Should backward compatibility be maintained?
4. Are there specific naming conventions already in use that should be preserved?
5. Should skills have explicit owners/maintainers?
6. What is the target timeline for full compliance?

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-02-06 | Initial standard document and schema definition |

---

*Last Updated: 2025-02-06*
