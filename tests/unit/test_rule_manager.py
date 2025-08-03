"""Unit tests for the rulebook_ai.core.RuleManager class."""

import pytest
from pathlib import Path

# Import RuleManager using standard import - testing installed package
from rulebook_ai.core import RuleManager


@pytest.fixture
def rule_manager(mock_rule_manager_env):
    """Create a RuleManager instance for testing."""
    # Initialize RuleManager with the test project root
    manager = RuleManager(project_root=mock_rule_manager_env)
    return manager


def test_list_rules(rule_manager):
    """Test the list_rules method."""
    rule_sets = rule_manager.list_rules()
    assert "test-set" in rule_sets


def test_get_ordered_source_files(rule_manager, temp_dir):
    """Test the get_ordered_source_files method."""
    project_root = Path(temp_dir)
    test_dir = project_root / "test_dir"
    test_dir.mkdir()
    
    # Create some test files
    with open(test_dir / "01-first.md", "w") as f:
        f.write("First file")
    with open(test_dir / "02-second.md", "w") as f:
        f.write("Second file")
    
    files = rule_manager.get_ordered_source_files(test_dir)
    assert len(files) == 2
    assert "first" in str(files[0])
    assert "second" in str(files[1])


def test_copy_file(rule_manager, temp_dir):
    """Test the copy_file method."""
    project_root = Path(temp_dir)
    source_file = project_root / "source.txt"
    dest_file = project_root / "subdir" / "dest.txt"
    
    with open(source_file, "w") as f:
        f.write("Test content")
    
    result = rule_manager.copy_file(source_file, dest_file)
    assert result is True
    assert dest_file.exists()
    assert dest_file.read_text() == "Test content"
