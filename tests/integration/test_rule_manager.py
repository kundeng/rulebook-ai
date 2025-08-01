"""Integration tests for the rulebook_ai.core module."""

import os
import tempfile
import shutil
from pathlib import Path
import pytest

# Import RuleManager using standard import - no need for tools_symlink here
from rulebook_ai.core import RuleManager


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def rule_manager(temp_dir):
    """Create a RuleManager instance for testing."""
    # Create a mock project structure in the temp directory
    project_root = Path(temp_dir)
    
    # Create source directories
    rule_sets_dir = project_root / "rule_sets"
    rule_sets_dir.mkdir()
    
    test_rule_set = rule_sets_dir / "test-set"
    test_rule_set.mkdir()
    
    # Create a test rule file
    with open(test_rule_set / "01-test-rule.md", "w") as f:
        f.write("# Test Rule\n\nThis is a test rule.")
    
    memory_dir = project_root / "memory_starters"
    memory_dir.mkdir()
    with open(memory_dir / "test-memory.md", "w") as f:
        f.write("# Test Memory\n\nThis is a test memory.")
    
    tools_dir = project_root / "tool_starters"
    tools_dir.mkdir()
    with open(tools_dir / "test-tool.md", "w") as f:
        f.write("# Test Tool\n\nThis is a test tool.")
    
    # Create a test env.example file
    with open(project_root / ".env.example", "w") as f:
        f.write("API_KEY=your-api-key-here")
    
    # Initialize RuleManager with the test project root
    manager = RuleManager(project_root=project_root)
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


def test_install(rule_manager, temp_dir):
    """Test the install method."""
    project_root = Path(temp_dir)
    target_dir = project_root / "target"
    target_dir.mkdir()
    
    result = rule_manager.install(
        rule_set="test-set", 
        project_dir=str(target_dir),
        include_copilot=True
    )
    
    assert result == 0
    assert (target_dir / "project_rules").exists()
    assert (target_dir / "memory").exists()
    assert (target_dir / "tools").exists()
    assert (target_dir / ".github" / "copilot-instructions.md").exists()
