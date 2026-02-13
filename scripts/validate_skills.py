#!/usr/bin/env python3
"""
Hunter Skill Validator
Validates skill files against the SKILL_SCHEMA.json schema
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any
import argparse

try:
    import jsonschema
    from jsonschema import validate, ValidationError
except ImportError:
    print("Error: jsonschema package required. Install with: pip install jsonschema")
    sys.exit(1)


class SkillValidator:
    def __init__(self, schema_path: str):
        """Initialize validator with schema file"""
        with open(schema_path, 'r') as f:
            self.schema = json.load(f)
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
        self.valid_count = 0
        self.invalid_count = 0

    def validate_file(self, file_path: str) -> Tuple[bool, List[str]]:
        """Validate a single skill file"""
        issues = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                skill_data = json.load(f)
            
            # Validate against schema
            validate(instance=skill_data, schema=self.schema)
            
            # Additional custom validations
            custom_issues = self._custom_validations(skill_data, file_path)
            if custom_issues:
                issues.extend(custom_issues)
                self.warnings.append({
                    "file": file_path,
                    "issues": custom_issues
                })
                return False, issues
            
            self.valid_count += 1
            return True, []
            
        except json.JSONDecodeError as e:
            msg = f"Invalid JSON: {e}"
            issues.append(msg)
            self.errors.append({
                "file": file_path,
                "error": msg
            })
            self.invalid_count += 1
            return False, issues
            
        except ValidationError as e:
            msg = f"Schema validation error: {e.message} at path: {'.'.join(str(p) for p in e.path)}"
            issues.append(msg)
            self.errors.append({
                "file": file_path,
                "error": msg,
                "path": list(e.path)
            })
            self.invalid_count += 1
            return False, issues
            
        except Exception as e:
            msg = f"Unexpected error: {str(e)}"
            issues.append(msg)
            self.errors.append({
                "file": file_path,
                "error": msg
            })
            self.invalid_count += 1
            return False, issues

    def _custom_validations(self, skill: Dict, file_path: str) -> List[str]:
        """Perform custom validations beyond schema"""
        issues = []
        
        # Check if payloads can form valid content
        if 'content' in skill and 'payloads' in skill['content']:
            if not skill['content']['payloads']:
                issues.append("Payloads array is empty")
        
        # Validate references have proper structure
        if 'context' in skill and 'references' in skill['context']:
            for ref in skill['context']['references']:
                if 'url' in ref and not ref['url'].startswith(('http://', 'https://', '/')):
                    issues.append(f"Invalid URL format: {ref.get('title', 'unknown')}")
        
        # Check for reasonable timestamp values
        if 'metadata' in skill:
            created = skill['metadata'].get('created_at')
            updated = skill['metadata'].get('updated_at')
            if created and updated:
                try:
                    created_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    updated_dt = datetime.fromisoformat(updated.replace('Z', '+00:00'))
                    if updated_dt < created_dt:
                        issues.append("updated_at is before created_at")
                except ValueError:
                    issues.append("Invalid timestamp format")
        
        return issues

    def validate_directory(self, directory: str, pattern: str = "*.json") -> Dict[str, Any]:
        """Validate all skill files in a directory"""
        results = {
            "directory": directory,
            "files_checked": 0,
            "valid": 0,
            "invalid": 0,
            "details": []
        }
        
        dir_path = Path(directory)
        if not dir_path.exists():
            print(f"Error: Directory not found: {directory}")
            return results
        
        json_files = list(dir_path.glob(pattern))
        print(f"Found {len(json_files)} skill files in {directory}")
        
        for file_path in sorted(json_files):
            is_valid, issues = self.validate_file(str(file_path))
            results["files_checked"] += 1
            
            if is_valid:
                results["valid"] += 1
                print(f"✓ {file_path.name}")
            else:
                results["invalid"] += 1
                print(f"✗ {file_path.name}")
                for issue in issues:
                    print(f"  - {issue}")
                results["details"].append({
                    "file": file_path.name,
                    "issues": issues
                })
        
        return results

    def generate_report(self, output_file: str = None) -> Dict[str, Any]:
        """Generate validation report"""
        report = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "summary": {
                "total": self.valid_count + self.invalid_count,
                "valid": self.valid_count,
                "invalid": self.invalid_count,
                "compliance_rate": (
                    f"{(self.valid_count / (self.valid_count + self.invalid_count) * 100):.1f}%"
                    if (self.valid_count + self.invalid_count) > 0
                    else "0%"
                )
            },
            "errors": self.errors,
            "warnings": self.warnings
        }
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\nReport saved to: {output_file}")
        
        return report


def main():
    parser = argparse.ArgumentParser(
        description="Validate Hunter Skill files against SKILL_SCHEMA.json"
    )
    parser.add_argument(
        "target",
        nargs="?",
        default="skills/",
        help="Directory or file to validate (default: skills/)"
    )
    parser.add_argument(
        "--schema",
        default="SKILL_SCHEMA.json",
        help="Path to schema file (default: SKILL_SCHEMA.json)"
    )
    parser.add_argument(
        "--report",
        help="Generate report file (JSON format)"
    )
    parser.add_argument(
        "--show-valid",
        action="store_true",
        help="Show valid files in output"
    )
    
    args = parser.parse_args()
    
    # Check if schema exists
    if not os.path.exists(args.schema):
        print(f"Error: Schema file not found: {args.schema}")
        sys.exit(1)
    
    # Initialize validator
    validator = SkillValidator(args.schema)
    
    # Validate target
    target_path = Path(args.target)
    
    if target_path.is_dir():
        results = validator.validate_directory(str(target_path))
        print(f"\n{'='*60}")
        print(f"Validation Results for {args.target}")
        print(f"{'='*60}")
        print(f"Files checked: {results['files_checked']}")
        print(f"Valid: {results['valid']}")
        print(f"Invalid: {results['invalid']}")
    else:
        is_valid, issues = validator.validate_file(str(target_path))
        print(f"\n{'='*60}")
        print(f"Validation Results for {args.target}")
        print(f"{'='*60}")
        if is_valid:
            print("✓ File is valid")
        else:
            print("✗ File has errors:")
            for issue in issues:
                print(f"  - {issue}")
    
    # Generate report if requested
    if args.report:
        validator.generate_report(args.report)
    
    # Exit with appropriate code
    sys.exit(0 if validator.invalid_count == 0 else 1)


if __name__ == "__main__":
    main()
