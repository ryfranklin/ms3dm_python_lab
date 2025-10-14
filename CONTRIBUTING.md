# Contributing to Python Learning Lab

Thank you for your interest in contributing! This document provides guidelines for adding new labs or improving existing ones.

## 🎯 Philosophy

Each lab should be:

- **Educational**: Clear learning objectives and teaching angle
- **Production-Ready**: Well-structured, tested, and documented code
- **Self-Contained**: Independent of other labs (though they can build on concepts)
- **Thoroughly Tested**: Comprehensive test coverage with pytest

## 📝 Adding a New Lab

### 1. Choose a Lab Number

Labs are numbered sequentially with 4-digit zero-padding: `lab_0001`, `lab_0002`, etc.

Find the next available number and create your directory:

```bash
mkdir -p lessons/lab_XXXX_topic_name
```

### 2. Directory Structure

Each lab should follow this structure:

```text
lessons/lab_XXXX_topic_name/
├── __init__.py                    # Package initialization
├── README.md                      # Lab documentation
├── topic_name/                    # Implementation package
│   ├── __init__.py
│   ├── module1.py
│   └── module2.py
└── tests/                         # Test suite
    ├── __init__.py
    ├── test_module1.py
    └── test_module2.py
```

### 3. README Requirements

Every lab README should include:

- **Status Badge**: ✅ Complete or 🚧 In Progress
- **Difficulty Level**: Beginner, Intermediate, or Advanced
- **Key Concepts**: List of topics covered
- **Learning Objectives**: What students will learn
- **Quick Start**: Basic usage examples
- **Documentation**: Detailed explanation of concepts
- **Tests**: How to run the test suite
- **Exercises**: Challenges for deeper learning
- **Real-World Applications**: Where this is used
- **Further Reading**: Links to external resources

See `lessons/lab_0001_event_bus/README.md` as a reference.

### 4. Code Quality Standards

All code must follow these standards:

#### Style and Formatting

```bash
# Format with Black
black lessons/lab_XXXX_topic_name/

# Lint with Ruff
ruff check lessons/lab_XXXX_topic_name/
```

#### Documentation

- **Docstrings**: Every module, class, and public function must have docstrings
- **Type Hints**: Use type hints for all function signatures
- **Examples**: Include examples in docstrings
- **Comments**: Explain *why*, not *what*

#### Defensive Programming

Use assertions to validate:

- Input parameters (types, ranges, non-null)
- State invariants
- Postconditions

Example:

```python
def subscribe(self, event: str, handler: Callable) -> str:
    assert isinstance(event, str), "Event must be a string"
    assert len(event) > 0, "Event name cannot be empty"
    assert callable(handler), "Handler must be callable"
    # ... implementation ...
```

### 5. Testing Requirements

Every lab must have comprehensive tests:

#### Minimum Coverage

- **Unit Tests**: Test all public methods and functions
- **Edge Cases**: Empty inputs, None values, boundary conditions
- **Error Cases**: Invalid inputs, assertion failures
- **Integration**: Test components working together

#### Test Organization

```python
class TestBasicFunctionality:
    """Test basic feature operations."""

    def test_initialization(self):
        """Test that component initializes correctly."""
        pass

    def test_basic_operation(self):
        """Test primary use case."""
        pass


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    pass


class TestValidation:
    """Test input validation and assertions."""
    pass
```

#### Running Tests

```bash
# Run tests for your lab
pytest lessons/lab_XXXX_topic_name/tests/ -v

# With coverage
pytest lessons/lab_XXXX_topic_name/tests/ --cov=lessons/lab_XXXX_topic_name --cov-report=term-missing

# Aim for >90% coverage
```

### 6. Examples and Notebooks

Add practical examples:

1. **Demo Script**: Create `examples/demo_topic_name.py`
   - Real-world scenarios
   - Multiple use cases
   - Well-commented code

2. **Jupyter Notebook**: Create `notebooks/Lab_XXXX_TopicName.ipynb`
   - Interactive exploration
   - Step-by-step examples
   - Exercises with cells for students

### 7. Update Main README

Add your lab to the main `README.md`:

```markdown
### Lab XXXX: Topic Name
**Status**: ✅ Complete
**Concepts**: Concept1, Concept2, Concept3
**Location**: `lessons/lab_XXXX_topic_name/`

Brief description of what the lab teaches.

[View Lab XXXX →](lessons/lab_XXXX_topic_name/README.md)
```

## 🔍 Pre-Commit Checklist

Before submitting your contribution:

- [ ] All tests pass: `pytest`
- [ ] Code is formatted: `black .`
- [ ] Linting passes: `ruff check .`
- [ ] Security scan passes: `bandit -r lessons/lab_XXXX_topic_name/`
- [ ] Documentation is complete
- [ ] Examples and notebooks work
- [ ] README is thorough and clear
- [ ] Main README is updated

## 🐛 Bug Reports

If you find a bug:

1. Check if it's already reported in Issues
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs. actual behavior
   - Python version and OS
   - Relevant code snippets

## 💡 Improvement Suggestions

Have an idea? Great!

1. Open an issue to discuss it first
2. Explain the educational value
3. Outline the implementation approach
4. Get feedback before starting work

## 📋 Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b lab/XXXX-topic-name`
3. **Commit** your changes with clear messages
4. **Push** to your fork
5. **Open** a pull request with:
   - Description of changes
   - Learning value
   - Test results
   - Screenshots/examples if applicable

## ✅ Review Criteria

Pull requests are evaluated on:

- **Educational Value**: Does it teach something valuable?
- **Code Quality**: Is it well-written and documented?
- **Test Coverage**: Are there comprehensive tests?
- **Documentation**: Is it clear and thorough?
- **Examples**: Are there practical demonstrations?
- **Consistency**: Does it follow the existing style?

## 🎓 Teaching Angle

Consider how your lab can be used:

- **Blog Post**: Can this be a tutorial article?
- **Video**: Would this work as a screencast?
- **Course Module**: Could this be part of a course?
- **Interview Prep**: Is this a common interview topic?

Add a "Teaching Notes" section to your README with suggestions.

## 🤝 Code of Conduct

- Be respectful and constructive
- Focus on education and learning
- Help others improve their contributions
- Celebrate all contributions, big and small

## 📬 Questions?

Open an issue with the `question` label, and we'll be happy to help!

---

Thank you for contributing to Python Learning Lab! Your work helps others learn and grow. 🚀
