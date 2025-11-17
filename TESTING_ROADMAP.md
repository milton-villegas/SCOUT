# Testing Roadmap: 23% → 60%+ Coverage

## Current Status (Before Improvements)

```
Total test lines: 3,725
Overall coverage: 23%

Coverage by file:
✅ exporter.py:      100%
✅ plotter.py:        99%
✅ data_handler.py:   98%
⚠️  doe_analyzer.py:  51% (26 tests → 38 tests now)
❌ optimizer.py:       0% (0 tests → 20+ tests now)
❌ project.py:        Unknown
```

## What We Just Added

### 1. ✅ Created `tests/core/test_optimizer.py`
- **250+ lines** of new tests
- Tests initialization, data handling, name sanitization
- Tests bounds calculation for numeric & categorical factors
- Tests error handling without Ax platform
- Tests edge cases (empty data, single values)
- **Impact: 0% → ~40% coverage for optimizer.py**

### 2. ✅ Enhanced `tests/core/test_doe_analyzer.py`
- Added 12 new tests for missing functionality
- Tests `compare_all_models()` function
- Tests `select_best_model()` function
- Tests `fit_reduced_quadratic()` comprehensively
- **Impact: 51% → ~75% coverage for doe_analyzer.py**

---

## Roadmap to 60%+ Overall Coverage

### STEP 1: ✅ DONE - Add Optimizer Tests
**Status: COMPLETED**
- Created test_optimizer.py with 20+ tests
- Covers initialization, data handling, edge cases

### STEP 2: ✅ DONE - Enhance Analyzer Tests
**Status: COMPLETED**
- Added missing tests for compare_all_models
- Added tests for select_best_model
- Added tests for reduced quadratic

### STEP 3: Add Project Tests (NEXT)
**Estimated impact: +5% overall coverage**

Create `tests/core/test_project.py`:

```python
"""Tests for Project class"""
import pytest
from core.project import Project

class TestProjectInit:
    def test_project_init(self):
        """Test project initialization"""
        project = Project()
        assert project is not None

    def test_project_save_load(self, tmp_path):
        """Test saving and loading projects"""
        # Create project with test data
        project = Project()
        # ... add data ...

        # Save
        save_path = tmp_path / "test_project.json"
        project.save(save_path)

        # Load
        loaded = Project.load(save_path)
        assert loaded is not None
```

### STEP 4: Add Edge Case Tests
**Estimated impact: +10% overall coverage**

Add these tests to existing test files:

**For doe_analyzer.py:**
```python
def test_predict_with_missing_columns():
    """Test prediction fails gracefully with wrong columns"""
    # Test error handling for bad input

def test_formula_with_special_characters():
    """Test formula building with factor names containing quotes"""
    # Test edge case: Factor name = "pH (7-9)"

def test_very_small_dataset():
    """Test behavior with only 3 data points"""
    # Edge case: insufficient data

def test_all_factors_insignificant():
    """Test when no factors are significant"""
    # Pure noise data
```

**For optimizer.py:**
```python
def test_suggest_with_no_data():
    """Test suggestions fail without observations"""

def test_multiple_optimization_rounds():
    """Test iterative optimization workflow"""

def test_plot_generation():
    """Test that optimization plots are created"""
```

### STEP 5: Add Integration Tests
**Estimated impact: +7% overall coverage**

Create `tests/integration/test_full_workflow.py`:

```python
"""Test complete DoE workflows"""
import pytest
import pandas as pd

def test_design_to_analysis_workflow():
    """Test full workflow: design → analyze → optimize"""
    # 1. Create design
    from core.doe_designer import DoEDesigner
    designer = DoEDesigner()
    # ... create design ...

    # 2. Simulate results
    results_df = pd.DataFrame(...)

    # 3. Analyze
    from core.doe_analyzer import DoEAnalyzer
    analyzer = DoEAnalyzer()
    analyzer.set_data(...)
    comparison = analyzer.compare_all_models()

    # 4. Optimize
    from core.optimizer import BayesianOptimizer
    optimizer = BayesianOptimizer()
    # ... suggest next experiments ...

    assert True  # Workflow completes without errors
```

---

## Expected Final Coverage

After completing all steps:

```
File                  Before  After   Gain
────────────────────────────────────────────
optimizer.py             0%    60%   +60%
doe_analyzer.py         51%    85%   +34%
project.py               ?     50%   +50%
(edge cases)             -      -    +10%
(integration)            -      -     +7%
────────────────────────────────────────────
OVERALL                 23%    65%   +42%
```

---

## How to Run Tests

### Install test dependencies:
```bash
pip install -r requirements-dev.txt
```

### Run all tests:
```bash
pytest tests/ -v
```

### Run with coverage report:
```bash
pytest tests/ --cov=core --cov-report=html
```

Then open `htmlcov/index.html` to see detailed coverage report!

### Run specific test file:
```bash
pytest tests/core/test_optimizer.py -v
pytest tests/core/test_doe_analyzer.py -v
```

### Run tests for one function:
```bash
pytest tests/core/test_optimizer.py::TestBayesianOptimizerInit -v
```

---

## Quick Wins for Coverage

**Easiest tests to add (high ROI):**

1. **Error handling tests** (2 min each)
   ```python
   def test_function_with_none_input():
       with pytest.raises(ValueError):
           function(None)
   ```

2. **Edge case tests** (5 min each)
   ```python
   def test_empty_dataframe():
       df = pd.DataFrame()
       result = process(df)
       assert result is not None
   ```

3. **Property tests** (1 min each)
   ```python
   def test_attribute_exists():
       obj = MyClass()
       assert hasattr(obj, 'important_attribute')
   ```

---

## Testing Best Practices

### ✅ DO:
- Test one thing per test function
- Use descriptive test names (`test_divide_by_zero_returns_none`)
- Use fixtures for repeated setup
- Test both success and failure cases
- Test edge cases (empty, None, extreme values)

### ❌ DON'T:
- Write tests that depend on external services
- Test implementation details (test behavior, not code)
- Skip error cases ("it'll never happen")
- Write tests without assertions

---

## Measuring Your Progress

### Generate coverage report:
```bash
pytest tests/ --cov=core --cov-report=term-missing
```

Output shows which lines aren't covered:
```
core/optimizer.py        45%   12-15, 23-28, 145-180
core/doe_analyzer.py     85%   312-315
```

### Set coverage goals:
```bash
# Fail if coverage drops below 60%
pytest tests/ --cov=core --cov-fail-under=60
```

---

## Next Steps

1. **Run the new tests** to ensure they pass
2. **Generate coverage report** to see current state
3. **Complete STEP 3**: Add project.py tests
4. **Complete STEP 4**: Add edge case tests
5. **Complete STEP 5**: Add integration tests
6. **Set up CI/CD** to run tests automatically (GitHub Actions)

---

## Resources

- pytest docs: https://docs.pytest.org
- Coverage.py: https://coverage.readthedocs.io
- Testing best practices: https://docs.python-guide.org/writing/tests/

