# Hunter Skill Migration Guide

## Overview

This guide walks through the process of migrating skill files from the legacy format to the standardized schema v1.0.0.

## Prerequisites

### Required Packages
```bash
pip install jsonschema
```

### Files Needed
- `SKILL_SCHEMA.json` - The canonical schema definition
- `SKILL_STANDARD.md` - Standard documentation
- `scripts/validate_skills.py` - Validation tool
- `scripts/migrate_skills.py` - Migration tool

## Migration Process

### Phase 1: Validation (Pre-Migration Check)

Before migrating, validate current files against the new schema to identify issues.

#### Dry Run Validation
```bash
# Validate all skills in the directory
python3 scripts/validate_skills.py skills/

# Validate specific directory
python3 scripts/validate_skills.py skills/

# Validate specific file
python3 scripts/validate_skills.py skills/account_takeover-8be4bd2d2663.json
```

#### Detailed Report
```bash
# Generate validation report
python3 scripts/validate_skills.py skills/ --report validation_report.json

# View report
cat validation_report.json | jq '.'
```

### Phase 2: Dry Run Migration

Always perform a dry run first to preview changes without modifying files.

```bash
# Preview migration of entire directory
python3 scripts/migrate_skills.py skills/ --dry-run

# Preview migration of specific category
python3 scripts/migrate_skills.py skills/ --dry-run --category "CVE Exploits"

# Preview single file migration
python3 scripts/migrate_skills.py skills/account_takeover-8be4bd2d2663.json --dry-run
```

### Phase 3: Actual Migration

Once the dry run looks good, proceed with actual migration.

#### Full Directory Migration
```bash
# Migrate all skills
python3 scripts/migrate_skills.py skills/

# Migrate specific category
python3 scripts/migrate_skills.py skills/ --category "CVE Exploits"

# Migrate all directories
for dir in skills skills skills; do
    python3 scripts/migrate_skills.py "$dir"
done
```

#### Single File Migration
```bash
python3 scripts/migrate_skills.py skills/account_takeover-8be4bd2d2663.json
```

### Phase 4: Post-Migration Validation

Validate all migrated files to ensure they conform to the schema.

```bash
# Validate migrated files
python3 scripts/validate_skills.py skills/

# Generate compliance report
python3 scripts/validate_skills.py skills/ --report migration_compliance.json

# Check compliance rate
cat migration_compliance.json | jq '.summary'
```

## Backup & Recovery

### Automatic Backups
The migration tool automatically creates backups in `skills_backup/` directory.

### Restore from Backup
```bash
# Restore specific file
cp skills_backup/account_takeover-8be4bd2d2663.json skills/

# Restore entire directory
cp -r skills_backup/* skills/
```

## What Changed

### Old Format
```json
{
  "id": "category-hash123",
  "category": "Category Name",
  "title": "Skill Title",
  "description": "...",
  "payloads": [...],
  "source": "Source",
  "references": [...]
}
```

### New Format
```json
{
  "version": "1.0.0",
  "metadata": {
    "id": "semantic-id",
    "schema_version": "1.0.0",
    "created_at": "2025-01-15T10:00:00Z",
    "updated_at": "2025-02-06T14:30:00Z",
    "status": "active"
  },
  "classification": {
    "category": "Category Name",
    "tags": ["tag1", "tag2"],
    "difficulty": "intermediate"
  },
  "content": {
    "title": "Skill Title",
    "summary": "Brief summary",
    "description": "...",
    "payloads": [...]
  },
  "context": {
    "source": "Source",
    "references": [...]
  }
}
```

### Key Changes

1. **ID Format**: Now semantic (e.g., `log4shell-cve-2021-44228`)
2. **Metadata**: Added timestamps, schema version, status
3. **Classification**: Structured with tags, difficulty, attack types
4. **Content**: Separated into title, summary, description, payloads
5. **Context**: Restructured references with type information

## Troubleshooting

### Migration Failures

If migration fails for specific files:

1. **Check JSON Syntax**
   ```bash
   python3 -m json.tool skills/filename.json
   ```

2. **Validate File Format**
   ```bash
   python3 scripts/validate_skills.py skills/filename.json
   ```

3. **Manual Review**
   - Open file in editor
   - Compare with schema
   - Fix issues manually

### Schema Validation Errors

**Error**: `"id" missing from required fields`
- **Fix**: Ensure `metadata.id` exists in new format

**Error**: `"category" is not valid`
- **Fix**: Check category is in standard format (title case)

**Error**: `"format" constraint violation`
- **Fix**: Ensure timestamps are ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)

### Reference Issues

**Error**: `Invalid URL format in references`
- **Fix**: Ensure all reference URLs start with `http://`, `https://`, or `/`

## Post-Migration Tasks

### 1. Update Applications
Update any code that reads skill files to handle new structure:

```python
# Old way
skill_id = skill['id']
category = skill['category']

# New way
skill_id = skill['metadata']['id']
category = skill['classification']['category']
```

### 2. Update Documentation
- Update README files with new structure
- Update API documentation
- Document backward compatibility rules

### 3. Testing
- Test all applications with migrated files
- Verify search/filtering functionality
- Check export/import processes

### 4. Deployment
- Back up production data
- Deploy migrated files
- Monitor for issues
- Rollback plan ready

## Rollback Plan

If issues are discovered post-migration:

```bash
# Stop using new files
# Restore from backup
cp -r skills_backup/* skills/

# Diagnose issues
python3 scripts/validate_skills.py skills/

# Fix issues
# Re-run migration with fixes
```

## Continuous Integration

### GitHub Actions Example
```yaml
name: Skill Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install jsonschema
      - run: python3 scripts/validate_skills.py skills/
      - run: python3 scripts/validate_skills.py skills/
      - run: python3 scripts/validate_skills.py skills/
```

## Performance Considerations

### File Size Impact
- Schema adds ~100-200 bytes per file
- Payloads array maintained for compatibility
- Overall impact: < 5% size increase

### Processing Time
- Validation: ~100-200ms per file
- Migration: ~50-100ms per file
- Batch operations: 5-10 seconds per 100 files

## Support & FAQ

### Q: Can I migrate incrementally?
**A**: Yes! You can migrate by category or directory. Both old and new format files can coexist.

### Q: Will this break existing tools?
**A**: Check the migration guide for your specific tool. New structure requires code updates.

### Q: How do I validate after migration?
**A**: Use `python3 scripts/validate_skills.py` to validate all files.

### Q: Can I revert?
**A**: Yes, backups are automatically created in `skills_backup/` directory.

### Q: What about custom fields?
**A**: Additional fields are allowed in current schema. Plan for v1.1 to formalize custom extensions.

## Resources

- [SKILL_STANDARD.md](./SKILL_STANDARD.md) - Complete standard documentation
- [SKILL_SCHEMA.json](./SKILL_SCHEMA.json) - JSON Schema definition
- [validate_skills.py](./scripts/validate_skills.py) - Validation tool
- [migrate_skills.py](./scripts/migrate_skills.py) - Migration tool

## Timeline

- **Week 1**: Planning & tool preparation ✓
- **Week 2**: Validation & testing
- **Week 3**: Pilot migration (small category)
- **Week 4**: Full migration & verification
- **Week 5**: Production deployment & monitoring

---

**Last Updated**: 2025-02-06
**Version**: 1.0.0
