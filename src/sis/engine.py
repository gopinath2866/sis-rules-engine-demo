"""Deterministic rule engine for SIS."""
import re
import json
from typing import Dict, List, Any, Optional
from enum import Enum

class RuleType(str, Enum):
    IDENTITY_BINDING = "IRREVERSIBLE_IDENTITY_BINDING"
    DECISION = "IRREVERSIBLE_DECISION"
    ADMIN_OVERRIDE = "ADMIN_OVERRIDE_DEPENDENCY"

class MatchLogic(str, Enum):
    ALL = "ALL"
    ANY = "ANY"

class Operator(str, Enum):
    EQUALS = "EQUALS"
    EXISTS = "EXISTS"
    CONTAINS = "CONTAINS"
    REGEX = "REGEX"
    GREATER_THAN = "GREATER_THAN"

class Condition:
    def __init__(self, path: str, operator: Operator, value: Any):
        self.path = path
        self.operator = operator
        self.value = value
    
    def evaluate(self, resource: Dict) -> bool:
        """Evaluate condition against resource."""
        current = resource
        parts = self.path.split('.')
        
        for part in parts[:-1]:
            if not isinstance(current, dict) or part not in current:
                return False
            current = current[part]
        
        last_part = parts[-1]
        
        if not isinstance(current, dict) or last_part not in current:
            return False
        
        target = current[last_part]
        
        if self.operator == Operator.EXISTS:
            return True
        elif self.operator == Operator.EQUALS:
            return target == self.value
        elif self.operator == Operator.CONTAINS:
            return isinstance(target, str) and self.value in target
        elif self.operator == Operator.REGEX:
            return bool(re.match(self.value, str(target)))
        elif self.operator == Operator.GREATER_THAN:
            return float(target) > float(self.value)
        return False

class Rule:
    def __init__(self, rule_id: str, rule_type: RuleType, 
                 applies_to: Dict, detection: Dict, message: str):
        self.rule_id = rule_id
        self.rule_type = rule_type
        self.file_types = applies_to.get("file_types", [])
        self.resource_kinds = applies_to.get("resource_kinds", [])
        self.match_logic = MatchLogic(detection.get("match_logic", "ALL"))
        self.conditions = [
            Condition(
                cond["path"],
                Operator(cond["operator"]),
                cond.get("value")
            ) for cond in detection.get("conditions", [])
        ]
        self.message = message
    
    def matches_file_type(self, file_type: str) -> bool:
        return file_type in self.file_types
    
    def matches_resource_kind(self, resource_kind: str) -> bool:
        if "*" in self.resource_kinds:
            return True
        return resource_kind in self.resource_kinds
    
    def evaluate(self, resource: Dict) -> bool:
        """Evaluate rule against resource."""
        if not self.conditions:
            return False
        
        if self.match_logic == MatchLogic.ALL:
            return all(cond.evaluate(resource) for cond in self.conditions)
        else:
            return any(cond.evaluate(resource) for cond in self.conditions)

class RuleEngine:
    def __init__(self, rules_file: str = "rules/canonical.json"):
        self.rules = self._load_rules(rules_file)
        self.rules_by_id = {r.rule_id: r for r in self.rules}
    
    def _load_rules(self, rules_file: str) -> List[Rule]:
        with open(rules_file, 'r') as f:
            data = json.load(f)
        
        return [
            Rule(
                rule["rule_id"],
                RuleType(rule["rule_type"]),
                rule["applies_to"],
                rule["detection"],
                rule["message"]
            ) for rule in data.get("rules", [])
        ]
    
    def scan_resource(self, file_type: str, resource_kind: str, 
                     resource: Dict) -> List[Dict]:
        """Scan single resource for matching rules."""
        findings = []
        
        for rule in self.rules:
            if (rule.matches_file_type(file_type) and 
                rule.matches_resource_kind(resource_kind)):
                if rule.evaluate(resource):
                    findings.append({
                        "rule_id": rule.rule_id,
                        "rule_type": rule.rule_type.value,
                        "message": rule.message,
                        "resource_kind": resource_kind,
                        "resource_name": resource.get("name", "")
                    })
        
        return findings