# Validation Tools - Developer Guide

This directory contains Python validation scripts for Home Assistant configuration management.

## Tool Overview

### `run_tests.py` - Main Test Suite
**Purpose**: Orchestrates all validation tests
**Usage**: `source ../venv/bin/activate && python run_tests.py`
**What it runs**:
- YAML syntax validation
- Entity reference validation
- Device trigger validation
- Official HA validation

### `yaml_validator.py` - YAML Syntax Validation
**Purpose**: Validates YAML syntax with HA-specific tags
**Key features**:
- Supports `!include`, `!secret`, `!input` tags
- UTF-8 encoding validation
- Line-by-line error reporting
**Usage**: `python yaml_validator.py [file_path]`

### `reference_validator.py` - Entity Reference Validation
**Purpose**: Verifies all entity/device references exist
**Key features**:
- Parses entity registry from `.storage/core.entity_registry`
- Extracts entities from Jinja2 templates
- Detects disabled entities
- Reports missing references with file/line context
**Usage**: `python reference_validator.py`

### `device_validator.py` - Device Trigger Validation
**Purpose**: Validates device triggers in automations
**Key features**:
- Parses device registry from `.storage/core.device_registry`
- Validates all device_id references in automation triggers
- Prevents false positives from local validation without physical devices
- Ready for MCP integration for live device verification
**Usage**: `python device_validator.py`

**Why this validator exists**:
Device triggers (like Hue dimmer switches, ZHA remotes) reference devices by device_id. When validating locally without physical devices connected, Home Assistant's official validator reports false errors like "Device has no config entry from domain 'hue'". This validator checks the device registry directly and confirms devices exist, preventing these false positives.

### `ha_official_validator.py` - Official HA Validation
**Purpose**: Uses Home Assistant's own validation tools
**Key features**:
- Most comprehensive validation
- Integration-specific checks
- Platform compatibility verification
- Filters device trigger errors (false positives) to warnings
**Usage**: `python ha_official_validator.py`

**Enhanced in v2**: Now detects device trigger validation errors and converts them to warnings instead of failures, since these are expected when validating locally. Actual device validation is handled by `device_validator.py`.

### `entity_explorer.py` - Entity Discovery Tool
**Purpose**: Search and explore available HA entities
**Key features**:
- Search by domain, area, or keyword
- Full details or summary view
- Device class filtering
**Usage**:
```bash
python entity_explorer.py --search motion
python entity_explorer.py --domain climate
python entity_explorer.py --area kitchen --full
```

## Development Guidelines

### Adding New Validators

When creating a new validator tool:

1. **Follow existing patterns**:
   - Return 0 on success, non-zero on failure
   - Use clear error messages with file paths and line numbers
   - Support both file-specific and directory-wide validation

2. **Error reporting format**:
   ```python
   print(f"ERROR: {file_path}:{line_num} - {error_message}")
   ```

3. **Integration with run_tests.py**:
   - Add your validator to the test suite
   - Ensure it can be called programmatically
   - Return proper exit codes

4. **Testing requirements**:
   - Write unit tests in `../tests/test_your_validator.py`
   - Use pytest framework
   - Avoid mocking entity registry - use fixtures
   - Test edge cases:
     - Valid configurations (should pass)
     - Invalid configurations (should fail with clear messages)
     - Missing files (should handle gracefully)
     - Malformed YAML (should report syntax errors)

### Test-Driven Development Workflow

**Example: Adding entity validation for scripts**

1. **Write test first** (tests/test_script_validator.py):
   ```python
   def test_script_entity_validation():
       """Test that script validator catches invalid entities"""
       result = validate_script("config/scripts.yaml")
       assert "entity_id 'light.nonexistent' not found" in result.errors
   ```

2. **Run test - verify it fails**:
   ```bash
   source ../venv/bin/activate
   pytest tests/test_script_validator.py -v
   # Should fail: validator doesn't exist yet
   ```

3. **Implement validator**:
   - Create `script_validator.py`
   - Implement entity checking logic
   - Follow existing patterns from `reference_validator.py`

4. **Iterate until tests pass**:
   ```bash
   pytest tests/test_script_validator.py -v
   # Keep refining until green
   ```

5. **Add to test suite**:
   - Update `run_tests.py` to call new validator
   - Test full suite: `python run_tests.py`

## Code Quality Standards

All Python code in this directory must:

- ✅ **Pass Black formatting**: `black tools/`
- ✅ **Pass isort sorting**: `isort tools/`
- ✅ **Pass flake8 linting**: `flake8 tools/`
- ✅ **Have type hints** (mypy): Function signatures should be typed
- ✅ **Include docstrings**: Module, class, and function level
- ✅ **Have tests**: Minimum 80% coverage

### Pre-commit Hooks

Hooks automatically run on commit:
- YAML formatting
- Python code formatting (Black + isort)
- Linting (flake8)
- Type checking (mypy)
- Tests (pytest)

**To run manually**:
```bash
source ../venv/bin/activate
make -f ../Makefile.dev dev-workflow
```

## Common Patterns

### Reading Entity Registry
```python
import json

def load_entity_registry():
    """Load and parse entity registry"""
    registry_path = "config/.storage/core.entity_registry"
    with open(registry_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return {entry['entity_id']: entry for entry in data['data']['entities']}
```

### YAML Parsing with HA Tags
```python
import yaml
from homeassistant.util.yaml import loader as ha_loader

def load_yaml_file(file_path):
    """Load YAML with HA-specific tags"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return ha_loader.yaml.load(f, Loader=ha_loader.SafeLineLoader)
```

### Extracting Entities from Templates
```python
import re

def extract_entities_from_template(template):
    """Extract entity_ids from Jinja2 templates"""
    patterns = [
        r'states\.([\w]+)\.([\w]+)',  # states.light.kitchen
        r'state_attr\(["\']?([\w.]+)["\']?',  # state_attr('light.kitchen')
        r'is_state\(["\']?([\w.]+)["\']?',  # is_state('light.kitchen')
    ]
    entities = []
    for pattern in patterns:
        matches = re.findall(pattern, str(template))
        entities.extend(matches)
    return entities
```

## Debugging Validators

### Enable Verbose Output
Most validators support `-v` or `--verbose` flags:
```bash
python reference_validator.py --verbose
```

### Test Single File
```bash
python yaml_validator.py config/automations.yaml
```

### Check Specific Entity
```bash
python entity_explorer.py --search "binary_sensor.home_basement_motion"
```

## Integration with Claude Code

These tools integrate with Claude Code via:

1. **Hooks**: `.claude-code/hooks/posttooluse-ha-validation.sh` runs after edits
2. **Slash Commands**: `/validate-config` runs full suite
3. **Make Commands**: `make validate` from project root

When developing validators, Claude should:
- ✅ Run validators after making changes
- ✅ Parse error output to identify specific issues
- ✅ Suggest fixes based on error messages
- ✅ Validate fixes before considering task complete

## Performance Considerations

- **Entity registry caching**: Load once, reuse for multiple validations
- **Parallel validation**: Independent validators can run concurrently
- **Incremental validation**: Validate only changed files when possible
- **Target**: Full validation suite should complete in <5 seconds

## Dependencies

Core dependencies (in `../pyproject.toml`):
- `homeassistant` - HA validation tools and YAML loaders
- `voluptuous` - Schema validation
- `pyyaml` - YAML parsing

Dev dependencies:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `black` - Code formatting
- `isort` - Import sorting
- `flake8` - Linting
- `mypy` - Type checking

## Examples

### Adding Temperature Range Validation

**Scenario**: Validate that climate entities don't set unrealistic temperatures

**tests/test_climate_validator.py**:
```python
def test_climate_temperature_range():
    """Test that climate configs have reasonable temperature ranges"""
    config = {
        'climate': {
            'platform': 'generic_thermostat',
            'target_temp': 150  # Too high!
        }
    }
    errors = validate_climate_config(config)
    assert 'temperature out of range' in errors[0].lower()
```

**Implementation in `climate_validator.py`**:
```python
def validate_climate_config(config):
    """Validate climate entity configurations"""
    errors = []
    for entity, settings in config.get('climate', {}).items():
        temp = settings.get('target_temp')
        if temp and (temp < 45 or temp > 95):
            errors.append(
                f"Temperature {temp}°F out of range (45-95°F) for {entity}"
            )
    return errors
```

## Troubleshooting

**Import errors**:
```bash
# Ensure venv is activated
source ../venv/bin/activate
# Reinstall dependencies
pip install -e ..
```

**Entity registry not found**:
```bash
# Pull latest config first
make pull
# Verify file exists
ls -la config/.storage/core.entity_registry
```

**Tests failing**:
```bash
# Run with verbose output
pytest -vv tests/test_your_validator.py
# Check coverage
pytest --cov=tools --cov-report=html
open htmlcov/index.html
```
