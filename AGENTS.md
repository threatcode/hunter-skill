# AGENTS.md - Autonomous Agents Guide

## Overview

This document provides guidance for autonomous agents and AI systems working on the Hunter Skill standardization project.

---

## Project Context for Agents

### Objective
Standardize ~250+ skill files from 3 directories (skills/, skills_h4cker/, skills_hacktricks/) to conform with SKILL_SCHEMA.json v1.0.0.

### Key Resources
- **Schema**: [SKILL_SCHEMA.json](./SKILL_SCHEMA.json)
- **Standard**: [SKILL_STANDARD.md](./SKILL_STANDARD.md)
- **Migration Guide**: [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md)
- **Validation Tool**: `scripts/validate_skills.py`
- **Migration Tool**: `scripts/migrate_skills.py`

---

## Autonomous Tasks

### ✅ Tasks Suitable for Autonomous Agents

#### 1. **Validation & Auditing**
```
Task: Validate all skill files against schema
Command: python3 scripts/validate_skills.py skills/ --report report.json
Agent Role: Run validation, analyze results, generate reports
Output: Compliance reports, error lists, audit trails
Timeline: 30-60 minutes for full validation
```

#### 2. **Migration Execution**
```
Task: Migrate files from old to new format
Command: python3 scripts/migrate_skills.py [directory]
Agent Role: Execute phased migration, backups, validation
Process: Dry-run → Execute → Validate → Report
Timeline: 1-2 hours per directory with 50+ files
```

#### 3. **Category Standardization**
```
Task: Ensure consistent category naming
Agent Role: Check all files for category consistency
Priority: High - directly affects searchability
Reference: SKILL_STANDARD.md (Categories section)
```

#### 4. **Tag Generation**
```
Task: Extract and validate tags from skill files
Agent Role: Analyze titles/descriptions, extract keywords
Constraints: Max 20 tags per skill, searchable format
Reference: QUICK_START.md (Tag Guidelines section)
```

#### 5. **ID Standardization**
```
Task: Generate semantic IDs for skills
Agent Role: Convert hash-based IDs to semantic format
Rules: lowercase, hyphens, meaningful (log4shell-cve-2021-44228)
Reference: SKILL_STANDARD.md (ID Format section)
```

#### 6. **Metadata Population**
```
Task: Add/update metadata fields
Agent Role: Generate timestamps, set status, add schema version
Requirements: ISO 8601 UTC timestamps, valid status values
Reference: SKILL_SCHEMA.json (metadata section)
```

#### 7. **Reference Structure**
```
Task: Convert reference strings to structured format
Agent Role: Parse references, add type/title/url fields
Types: github, blog, documentation, tool, pdf, video, academic, other
Reference: QUICK_START.md (Reference Types section)
```

#### 8. **Data Quality Checks**
```
Task: Validate data integrity post-migration
Agent Role: Check for data loss, corruption, missing fields
Verification: Compare original vs migrated files
Success Metric: 100% data preservation
```

---

## Agent Workflow

### Phase 1: Preparation (Day 1)
```
1. Read SKILL_STANDARD.md (understand current/target format)
2. Review SKILL_SCHEMA.json (validation rules)
3. Install dependencies: pip install jsonschema
4. Run: python3 scripts/validate_skills.py --help
5. Generate baseline report: python3 scripts/validate_skills.py skills/ --report baseline.json
```

### Phase 2: Pilot (Days 2-3)
```
1. Select single category for pilot
2. Run dry-run: python3 scripts/migrate_skills.py skills/ --dry-run --category "CVE Exploits"
3. Review output for errors
4. Execute: python3 scripts/migrate_skills.py skills/ --category "CVE Exploits"
5. Validate: python3 scripts/validate_skills.py skills/ --category "CVE Exploits"
6. Report results
```

### Phase 3: Full Migration (Days 4-5)
```
1. Migrate skills_h4cker/: python3 scripts/migrate_skills.py skills_h4cker/
2. Validate: python3 scripts/validate_skills.py skills_h4cker/
3. Migrate skills_hacktricks/: python3 scripts/migrate_skills.py skills_hacktricks/
4. Validate: python3 scripts/validate_skills.py skills_hacktricks/
5. Generate final report
```

### Phase 4: Quality Assurance (Day 6)
```
1. Verify 100% compliance: check all validation reports
2. Confirm zero data loss: sample check migrated vs original
3. Check file integrity: all JSON valid, no corruption
4. Generate compliance summary
5. Document any issues/resolutions
```

---

## Agent Guidelines

### ✅ DO

- **Read documentation first**: SKILL_STANDARD.md and QUICK_START.md
- **Always use --dry-run first**: Before executing any migration
- **Create backups**: Automatically handled by tools, verify they exist
- **Generate reports**: Validation reports are critical for verification
- **Test incrementally**: Pilot with small category first
- **Document decisions**: log what was done and why
- **Communicate status**: Regular status updates on progress
- **Handle errors gracefully**: Log errors, don't fail silently
- **Preserve original data**: Backups are automatic, but verify

### ❌ DON'T

- **Skip validation**: Always validate before and after
- **Migrate without backup**: Tools do this automatically, but verify
- **Ignore errors**: Report all validation failures
- **Modify schema**: SKILL_SCHEMA.json is canonical
- **Skip documentation**: Update CHANGELOG if making decisions
- **Rush through phases**: Each phase builds on previous
- **Assume format consistency**: Validate before trusting data
- **Leave incomplete tasks**: Mark status clearly (in-progress/done)
- **Override existing decisions**: Check existing standards first

---

## Error Handling

### Common Issues & Resolution

#### Issue: Validation Fails on Old Format
```
Symptom: python3 scripts/validate_skills.py shows many errors
Expected: Old format won't pass schema validation
Action: Run migrate_skills.py first, then validate
Resolution Type: Normal - expected behavior
```

#### Issue: Migration Fails on Specific File
```
Symptom: migrate_skills.py errors on some files
Expected: Some files may have encoding or JSON issues
Action: 
  1. Check file with: python3 -m json.tool filename.json
  2. Fix JSON syntax
  3. Re-run migration
  4. Report the issue
Resolution Type: Data quality issue
```

#### Issue: Backup Not Created
```
Symptom: skills_backup/ directory missing
Expected: Should be created automatically
Action:
  1. Check directory exists: ls -la skills_backup/
  2. If missing, create manually: mkdir -p skills_backup
  3. Copy files: cp skills/*.json skills_backup/
  4. Verify: ls skills_backup/ | wc -l
Resolution Type: Manual intervention
```

---

## Agent Capabilities & Limitations

### ✅ What Agents Can Do

- Run Python scripts: `python3 scripts/validate_skills.py`
- Read & analyze documentation files
- Generate validation reports
- Execute migrations with tools
- Compare before/after files
- Generate compliance reports
- Create summary documents
- Organize work in phases
- Track progress & status

### ⚠️ Limitations

- **Cannot modify schema**: SKILL_SCHEMA.json is read-only (canonical)
- **Cannot add new fields**: Only defined in schema
- **Cannot create custom tools**: Use provided scripts only
- **Cannot ignore validation**: Must achieve 100% compliance
- **Cannot skip phases**: Must follow 4-6 week timeline
- **Cannot make architectural decisions**: Follow SKILL_STANDARD.md
- **Cannot change standard**: SKILL_STANDARD.md is baseline

---

## Success Criteria for Agents

### Quantitative Metrics
- [ ] All 250+ files processed
- [ ] 100% schema compliance
- [ ] 0 data loss incidents
- [ ] < 5% file size increase
- [ ] < 1 hour total migration time (all files)

### Qualitative Metrics
- [ ] Clear documentation of process
- [ ] Detailed error logs created
- [ ] Backup verification complete
- [ ] Validation reports generated
- [ ] Status updates provided regularly

### Deliverables
- [ ] Migrated files (all converted to new format)
- [ ] Validation reports (compliance proof)
- [ ] Migration logs (audit trail)
- [ ] Backup verification (safety confirmation)
- [ ] Summary report (final status)

---

## Agent Communication Protocol

### Status Updates
Report progress at key milestones:
```
Phase 1 Complete: Validation done, X issues found
Phase 2 Complete: Pilot migration successful, Y% data migrated
Phase 3 Complete: Full migration done, 100% compliance achieved
Phase 4 Complete: QA passed, all systems verified
```

### Issue Reporting
Format:
```
Issue: [Brief title]
Severity: [Critical/High/Medium/Low]
Details: [Description]
Files Affected: [List specific files]
Recommended Action: [What to do]
```

### Decision Logging
```
Decision: [What was decided]
Reason: [Why]
Reference: [Link to docs]
Impact: [What changes]
Approval: [From whom/what authority]
```

---

## Integration with Humans

### When to Escalate to Human
- ❌ Schema modification requests
- ❌ Architectural changes needed
- ❌ Approval decisions required
- ❌ Data integrity issues beyond repair
- ❌ Unexpected errors (not in this guide)

### When Agent Can Decide
- ✅ Validation & reporting
- ✅ Following standardization rules
- ✅ Running approved tools
- ✅ Following established workflow
- ✅ Documented error recovery

### Communication Channels
- **Status**: Regular updates to project leads
- **Issues**: Detailed error logs with context
- **Decisions**: Document in CHANGELOG
- **Escalation**: Clear problem statement to human lead

---

## Tools Reference

### Validation Tool
```bash
python3 scripts/validate_skills.py [target] [options]

Options:
  --schema SCHEMA_FILE     Path to schema (default: SKILL_SCHEMA.json)
  --report REPORT_FILE     Generate JSON report
  --show-valid             Show valid files in output
```

### Migration Tool
```bash
python3 scripts/migrate_skills.py [target] [options]

Options:
  --dry-run               Preview changes without modifying
  --category CATEGORY     Migrate specific category only
```

### Helper Commands
```bash
# Check JSON validity
python3 -m json.tool filename.json

# Generate file list
find skills/ -name "*.json" | wc -l

# Check backups
ls -la skills_backup/ | wc -l

# Generate diff (before/after)
diff skills/file.json skills_backup/file.json
```

---

## Best Practices for Agents

1. **Always validate before claiming success**
   - Run validation after every operation
   - Check compliance rate in report

2. **Create audit trails**
   - Log all operations
   - Record timestamps
   - Document decisions

3. **Test on pilot first**
   - Don't migrate everything at once
   - Verify with small category
   - Build confidence progressively

4. **Preserve originals**
   - Backups are automatic (verify they exist)
   - Never overwrite without backup
   - Keep audit trail of changes

5. **Document extensively**
   - Why decisions were made
   - What issues were encountered
   - How they were resolved

6. **Communicate clearly**
   - Regular status updates
   - Clear error messages
   - Success metrics demonstrated

---

## Troubleshooting Guide for Agents

### Validation Shows Errors
```
Check: Are these from OLD or NEW format?
Old Format → Migration needed (expected)
New Format → Schema compliance issue (unexpected)
Action: Review error details, cross-check with schema
```

### Migration Tool Hangs
```
Check: File size (some very large?)
Check: Disk space available (backups take space)
Check: Python version (3.7+ required)
Action: Kill process, investigate, retry
```

### Backup Directory Missing
```
Check: Was --dry-run used? (--dry-run doesn't create backups)
Check: Disk permissions (can tool write?)
Check: Permission denied errors
Action: Create manually, copy files, continue
```

### Data Loss Suspected
```
Check: Compare with backup: diff -u backup/file.json file.json
Check: File sizes (should be similar)
Check: Content sampling (spot check)
Escalate: If confirmed data loss, this is critical
```

---

## Agent Checklist

Before Starting:
- [ ] Read SKILL_STANDARD.md completely
- [ ] Review SKILL_SCHEMA.json structure
- [ ] Understand current vs target format
- [ ] Install dependencies: `pip install jsonschema`
- [ ] Test tools: `python3 scripts/validate_skills.py --help`

During Execution:
- [ ] Follow workflow phases in order
- [ ] Always use --dry-run first
- [ ] Document all operations
- [ ] Generate validation reports
- [ ] Verify backups created
- [ ] Track compliance percentage
- [ ] Report progress regularly

After Completion:
- [ ] Verify 100% compliance
- [ ] Confirm zero data loss
- [ ] Document all issues resolved
- [ ] Generate final summary report
- [ ] Provide recommendations

---

## Success Example

**What a successful agent run looks like:**

```
Phase 1: Validation
├─ Generated baseline report: 47 files checked, 0 errors (old format)
├─ Identified 0 format issues (expected for old files)
└─ Ready for migration

Phase 2: Pilot
├─ Dry-run on "CVE Exploits": 8 files preview
├─ Executed migration: 8 files converted
├─ Validation result: 100% compliance (8/8 pass)
└─ Pilot successful, proceeding to full migration

Phase 3: Full Migration
├─ Migrated skills/: 100 files → 100/100 valid ✓
├─ Migrated skills_h4cker/: 50 files → 50/50 valid ✓
├─ Migrated skills_hacktricks/: 100 files → 100/100 valid ✓
└─ Total: 250+ files, 100% compliance

Phase 4: QA
├─ Data integrity verified: 0 loss detected
├─ Backup verification: All files backed up
├─ Schema compliance: 100% (250+ files)
└─ Project complete ✓

Final Status: ✅ SUCCESS
Compliance: 100% (250+/250+ files)
Data Loss: 0 incidents
Issues: 0 unresolved
Recommendation: Ready for production deployment
```

---

**Version**: 1.0.0  
**Last Updated**: February 6, 2025  
**Status**: Ready for Agent Deployment
