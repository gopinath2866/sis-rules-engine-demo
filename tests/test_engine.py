"""Test rule engine."""
import json
import pytest
from sis.engine import RuleEngine, Rule, RuleType, Condition, Operator

def test_rule_loading():
    """Test that all 25 rules load correctly."""
    engine = RuleEngine("rules/canonical.json")
    assert len(engine.rules) == 25
    
    rule_types = {r.rule_type for r in engine.rules}
    assert RuleType.IDENTITY_BINDING in rule_types
    assert RuleType.DECISION in rule_types
    assert RuleType.ADMIN_OVERRIDE in rule_types

def test_condition_evaluation():
    """Test condition evaluation logic."""
    cond = Condition("deletion_protection", Operator.EQUALS, True)
    
    resource = {"deletion_protection": True}
    assert cond.evaluate(resource)
    
    resource = {"deletion_protection": False}
    assert not cond.evaluate(resource)

def test_rule_evaluation():
    """Test full rule evaluation."""
    rule = Rule(
        rule_id="TEST-01",
        rule_type=RuleType.DECISION,
        applies_to={"file_types": ["terraform"], "resource_kinds": ["*"]},
        detection={
            "match_logic": "ALL",
            "conditions": [
                {"path": "lifecycle.prevent_destroy", "operator": "EQUALS", "value": True}
            ]
        },
        message="Test rule"
    )
    
    resource = {"lifecycle": {"prevent_destroy": True}}
    assert rule.evaluate(resource)
    
    resource = {"lifecycle": {"prevent_destroy": False}}
    assert not rule.evaluate(resource)

# Additional tests for each rule...