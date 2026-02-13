#!/usr/bin/env python3
"""
Hunter Skill Migration Tool
Converts skill files from old format to standard schema v1.0.0
"""

import json
import os
import sys
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import shutil


class SkillMigrator:
    def __init__(self, dry_run: bool = False):
        """Initialize migrator"""
        self.dry_run = dry_run
        self.migration_count = 0
        self.failed_count = 0
        self.backup_dir = Path("skills_backup")
        
        # Standardized category mappings
        self.category_mappings = {
            # Convert underscores and hyphens to proper title case with spaces
            "account_takeover": "Account Takeover",
            "account-takeover": "Account Takeover",
            "api_key_leaks": "API Key Leaks",
            "api-key-leaks": "API Key Leaks",
            "cve_exploits": "CVE Exploits",
            "cve-exploits": "CVE Exploits",
            "dns_rebinding": "DNS Rebinding",
            "dns-rebinding": "DNS Rebinding",
            "encoding_transformations": "Encoding Transformations",
            "encoding-transformations": "Encoding Transformations",
            "file_inclusion": "File Inclusion",
            "file-inclusion": "File Inclusion",
            "insecure_deserialization": "Insecure Deserialization",
            "insecure-deserialization": "Insecure Deserialization",
            "insecure_management_interface": "Insecure Management Interface",
            "insecure-management-interface": "Insecure Management Interface",
            "insecure_source_code_management": "Insecure Source Code Management",
            "insecure-source-code-management": "Insecure Source Code Management",
            "ldap_injection": "LDAP Injection",
            "ldap-injection": "LDAP Injection",
            "mass_assignment": "Mass Assignment",
            "mass-assignment": "Mass Assignment",
            "methodology_and_resources": "Methodology and Resources",
            "methodology-and-resources": "Methodology and Resources",
            "_learning_and_socials": "Learning and Socials",
            "_LEARNING_AND_SOCIALS": "Learning and Socials",
            "learning_and_socials": "Learning and Socials",
            "learning-and-socials": "Learning and Socials",
            "_template_vuln": "Template Vulnerability",
            "_TEMPLATE_VULN": "Template Vulnerability",
            "template_vuln": "Template Vulnerability",
            "generic_hacking": "Generic Hacking",
            "generic-hacking": "Generic Hacking",
            "pentesting_web": "Pentesting Web",
            "pentesting-web": "Pentesting Web",
            "linux_hardening": "Linux Hardening",
            "linux-hardening": "Linux Hardening",
            "windows_hardening": "Windows Hardening",
            "windows-hardening": "Windows Hardening",
            "network_services_pentesting": "Network Services Pentesting",
            "network-services-pentesting": "Network Services Pentesting",
            "mobile_pentesting": "Mobile Pentesting",
            "mobile-pentesting": "Mobile Pentesting",
            "ai": "AI",
            "binary_exploitation": "Binary Exploitation",
            "binary-exploitation": "Binary Exploitation",
            "macos_hardening": "macOS Hardening",
            "macos-hardening": "macOS Hardening",
            "programming_and_scripting_for_cybersecurity": "Programming and Scripting for Cybersecurity",
            "programming-and-scripting-for-cybersecurity": "Programming and Scripting for Cybersecurity",
            "docker_and_k8s_security": "Docker and Kubernetes Security",
            "docker-and-k8s-security": "Docker and Kubernetes Security",
        }

    def migrate_skill(self, file_path: str) -> bool:
        """Migrate a single skill file to new format"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                old_skill = json.load(f)
            
            # Create new skill structure
            new_skill = self._convert_format(old_skill)
            
            if not self.dry_run:
                # Backup original file
                self._backup_file(file_path)
                
                # Write new file
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(new_skill, f, indent=2, ensure_ascii=False)
                    f.write('\n')  # Add trailing newline
            
            self.migration_count += 1
            print(f"✓ Migrated: {Path(file_path).name}")
            return True
            
        except Exception as e:
            self.failed_count += 1
            print(f"✗ Failed to migrate {Path(file_path).name}: {str(e)}")
            return False

    def _convert_format(self, old_skill: Dict[str, Any]) -> Dict[str, Any]:
        """Convert old format to new format"""
        
        # Extract old fields
        skill_id = old_skill.get('id', '')
        category = old_skill.get('category', 'Uncategorized')
        title = old_skill.get('title', '')
        description = old_skill.get('description', '')
        payloads = old_skill.get('payloads', [])
        source = old_skill.get('source', 'Unknown')
        references = old_skill.get('references', [])
        
        # Normalize category
        normalized_category = self._normalize_category(category)
        
        # Generate semantic ID from old ID or title
        semantic_id = self._generate_semantic_id(skill_id, title)
        
        # Create new structure
        new_skill = {
            "version": "1.0.0",
            "metadata": {
                "id": semantic_id,
                "schema_version": "1.0.0",
                "created_at": datetime.utcnow().isoformat() + "Z",
                "updated_at": datetime.utcnow().isoformat() + "Z",
                "status": "active"
            },
            "classification": {
                "category": normalized_category,
                "tags": self._extract_tags(title, description),
                "difficulty": "intermediate"
            },
            "content": {
                "title": title,
                "summary": self._extract_summary(description),
                "description": description,
                "payloads": payloads if isinstance(payloads, list) else [payloads]
            },
            "context": {
                "source": source,
                "references": self._convert_references(references)
            }
        }
        
        return new_skill

    def _normalize_category(self, category: str) -> str:
        """Convert category to standard format"""
        # Try direct mapping first
        if category.lower() in self.category_mappings:
            return self.category_mappings[category.lower()]
        
        # Try replacing underscores with spaces and title casing
        normalized = category.replace('_', ' ').replace('-', ' ')
        # Title case each word
        normalized = ' '.join(word.title() for word in normalized.split())
        return normalized

    def _generate_semantic_id(self, old_id: str, title: str) -> str:
        """Generate semantic ID from old ID and title"""
        # If old ID already has semantic meaning, try to extract it
        if old_id:
            parts = old_id.split('-')
            # Remove hash suffix (usually last part)
            if len(parts) > 1 and len(parts[-1]) >= 10:
                semantic_part = '-'.join(parts[:-1])
                if semantic_part:
                    return semantic_part.lower().replace('_', '-')
        
        # Generate from title
        if title:
            semantic = title.lower().replace(' ', '-').replace('_', '-')
            # Remove special characters
            semantic = ''.join(c if c.isalnum() or c == '-' else '' for c in semantic)
            # Remove multiple hyphens
            while '--' in semantic:
                semantic = semantic.replace('--', '-')
            return semantic.strip('-')
        
        return old_id.lower().replace('_', '-')

    def _extract_summary(self, description: str) -> str:
        """Extract first line as summary"""
        if not description:
            return "No summary available"
        
        lines = description.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('>'):
                # Limit to 500 chars
                return line[:500]
        
        return description[:500]

    def _extract_tags(self, title: str, description: str) -> List[str]:
        """Extract tags from title and description"""
        tags = set()
        
        # Add technology/tool names as tags
        tech_keywords = [
            'log4j', 'log4shell', 'sql', 'injection', 'xss', 'csrf', 'lfi', 'rfi',
            'rce', 'deserialization', 'mfa', 'authentication', 'ldap', 'dns',
            'json', 'xml', 'web', 'api', 'java', 'python', 'php', 'node', 'golang',
            'docker', 'kubernetes', 'cloud', 'aws', 'azure', 'gcp', 'windows',
            'linux', 'macos', 'exploitation', 'reconnaissance', 'evasion'
        ]
        
        combined_text = (title + ' ' + description).lower()
        for keyword in tech_keywords:
            if keyword in combined_text:
                tags.add(keyword)
        
        # Limit tags to 20
        return sorted(list(tags))[:20]

    def _convert_references(self, old_references: List[str]) -> List[Dict[str, str]]:
        """Convert old reference strings to structured format"""
        new_references = []
        
        for ref in old_references:
            if isinstance(ref, str):
                new_ref = {
                    "title": ref,
                    "url": "/" + ref if not ref.startswith('http') else ref,
                    "type": "documentation" if ref.endswith('.md') else "other"
                }
                new_references.append(new_ref)
        
        return new_references

    def _backup_file(self, file_path: str):
        """Create backup of original file"""
        if not self.backup_dir.exists():
            self.backup_dir.mkdir(parents=True)
        
        backup_path = self.backup_dir / Path(file_path).name
        shutil.copy2(file_path, backup_path)

    def migrate_directory(self, directory: str, category: str = None) -> Dict[str, Any]:
        """Migrate all skills in a directory"""
        results = {
            "directory": directory,
            "total": 0,
            "migrated": 0,
            "failed": 0,
            "dry_run": self.dry_run
        }
        
        dir_path = Path(directory)
        if not dir_path.exists():
            print(f"Error: Directory not found: {directory}")
            return results
        
        json_files = list(dir_path.glob("*.json"))
        
        # Filter by category if specified
        if category:
            json_files = [
                f for f in json_files
                if category.lower() in f.name.lower()
            ]
        
        print(f"Found {len(json_files)} skill files in {directory}")
        if self.dry_run:
            print("(DRY RUN - no files will be modified)")
        
        for file_path in sorted(json_files):
            results["total"] += 1
            if self.migrate_skill(str(file_path)):
                results["migrated"] += 1
            else:
                results["failed"] += 1
        
        return results


def main():
    parser = argparse.ArgumentParser(
        description="Migrate skill files to standard schema v1.0.0"
    )
    parser.add_argument(
        "target",
        nargs="?",
        default="skills/",
        help="Directory or file to migrate (default: skills/)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be migrated without making changes"
    )
    parser.add_argument(
        "--category",
        help="Only migrate files matching this category"
    )
    
    args = parser.parse_args()
    
    migrator = SkillMigrator(dry_run=args.dry_run)
    
    target_path = Path(args.target)
    
    if target_path.is_dir():
        results = migrator.migrate_directory(
            str(target_path),
            category=args.category
        )
        print(f"\n{'='*60}")
        print(f"Migration Summary")
        print(f"{'='*60}")
        print(f"Total files: {results['total']}")
        print(f"Migrated: {results['migrated']}")
        print(f"Failed: {results['failed']}")
        if results['dry_run']:
            print("(DRY RUN - no changes were made)")
    else:
        migrator.migrate_skill(str(target_path))
        print(f"\n{'='*60}")
        print(f"Migration Summary")
        print(f"{'='*60}")
        print(f"Migrated: {migrator.migration_count}")
        print(f"Failed: {migrator.failed_count}")
    
    sys.exit(0 if migrator.failed_count == 0 else 1)


if __name__ == "__main__":
    main()
