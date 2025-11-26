# Test Generation Features

## Overview

The GenAI Requirements Automation platform now includes comprehensive test generation capabilities, extending beyond basic TDD test cases to include:

- **Test Plans**: Strategic testing documentation
- **Unit Tests**: Component-level automated tests
- **System Tests**: End-to-end integration tests

## New Artifact Types

### 1. Test Plan (`test_plan`)
**Purpose**: Generate comprehensive test planning documentation

**Generated Content**:
- Test objectives and scope
- Test strategy and approach
- Test levels (unit, integration, system, UAT)
- Test environment requirements
- Test schedule and milestones
- Risk assessment and mitigation
- Entry and exit criteria
- Test deliverables and reports

**Example Usage**:
```json
{
  "artifact_types": ["test_plan"],
  "spec_file_path": "data/spec/requirements.pdf"
}
```

### 2. Unit Tests (`unit_tests`)
**Purpose**: Generate automated unit test code

**Generated Content**:
- Test class structure
- Test methods for each component/function
- Mock object setup
- Test data preparation
- Assertions and validations
- Edge case coverage
- Framework-specific code (JUnit, pytest, etc.)

**Example Output**:
```python
import pytest
from unittest.mock import Mock, patch
from myapp.services import UserService

class TestUserService:
    def setup_method(self):
        self.user_service = UserService()
    
    def test_create_user_success(self):
        # Test user creation with valid data
        user_data = {"name": "John Doe", "email": "john@example.com"}
        result = self.user_service.create_user(user_data)
        assert result.status == "success"
        assert result.user_id is not None
```

### 3. System Tests (`system_tests`)
**Purpose**: Generate end-to-end system test scenarios

**Generated Content**:
- End-to-end test scenarios
- Integration test cases
- Performance test cases
- Security test scenarios
- User acceptance test cases
- Test data requirements
- Expected system behavior
- Cross-system validation

**Example Scenarios**:
- Complete user registration flow
- Payment processing integration
- Data synchronization between systems
- Load testing scenarios
- Security penetration tests

## API Integration

### Updated Generate Endpoint

```http
POST /api/v1/generate
```

**Request Body**:
```json
{
  "spec_file_path": "data/spec/requirements.pdf",
  "artifact_types": [
    "epic", 
    "stories", 
    "use_cases", 
    "tdd", 
    "data_model",
    "test_plan",
    "unit_tests", 
    "system_tests"
  ],
  "output_format": "docx"
}
```

**Response**:
```json
{
  "message": "Successfully generated 8 artifacts",
  "artifacts": {
    "test_plan": "# Test Plan\n## Objectives...",
    "unit_tests": "import pytest\nclass TestUserService...",
    "system_tests": "# System Test Cases\n## End-to-End Scenarios..."
  },
  "file_paths": {
    "test_plan": "data/generated/test_plan_abc123.docx",
    "unit_tests": "data/generated/unit_tests_def456.docx",
    "system_tests": "data/generated/system_tests_ghi789.docx"
  }
}
```

## LLM Prompts for Test Generation

### Test Plan Generation
```python
system_prompt = """You are a test manager. Generate a comprehensive test plan based on the functional specification.
Include: test objectives, scope, test strategy, test levels (unit, integration, system, UAT), 
test environment requirements, test schedule, risk assessment, entry/exit criteria, and deliverables."""
```

### Unit Test Generation
```python
system_prompt = """You are a software developer. Generate unit test cases based on the functional specification.
Include: test class structure, test methods for each function/component, mock objects, test data setup, 
assertions, and edge cases. Format as code with appropriate testing framework (JUnit, pytest, etc.)."""
```

### System Test Generation
```python
system_prompt = """You are a system test engineer. Generate system test cases based on the functional specification.
Include: end-to-end test scenarios, integration test cases, performance test cases, security test cases, 
user acceptance test scenarios, test data requirements, and expected system behavior."""
```

## Usage Examples

### Generate All Test Artifacts
```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "spec_file_path": "data/spec/banking_system.pdf",
    "artifact_types": ["test_plan", "unit_tests", "system_tests"],
    "output_format": "docx"
  }'
```

### Generate Specific Test Type
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/generate",
    json={
        "spec_text": "The system should handle user authentication...",
        "artifact_types": ["unit_tests"],
        "output_format": "docx"
    }
)
```

## Test Generation Benefits

### 1. Comprehensive Coverage
- **Strategic Level**: Test plans provide overall testing strategy
- **Component Level**: Unit tests ensure individual component quality
- **System Level**: System tests validate end-to-end functionality

### 2. Framework Agnostic
- Generates tests for multiple frameworks (pytest, JUnit, NUnit, etc.)
- Adapts to different programming languages
- Includes appropriate imports and setup code

### 3. Quality Assurance
- Covers positive and negative test cases
- Includes edge cases and boundary conditions
- Provides mock object setup for isolated testing

### 4. Documentation Integration
- Test plans align with requirements
- Test cases trace back to specifications
- Maintains consistency across artifacts

## File Generation

All test artifacts are generated as both DOCX and PDF formats:

- **Test Plans**: Formatted as professional documents with sections and tables
- **Unit Tests**: Code-formatted with syntax highlighting preservation
- **System Tests**: Structured test case documentation with scenarios

## Azure DevOps Integration

Test artifacts can be pushed to Azure DevOps as:
- **Test Plans**: As Test Plan work items
- **Unit Tests**: As Test Case work items
- **System Tests**: As Test Suite work items

## Future Enhancements

### Planned Features
- **Test Data Generation**: Automatic test data creation
- **Test Automation Scripts**: Selenium/Playwright script generation
- **Performance Test Scripts**: JMeter/LoadRunner configuration
- **API Test Cases**: Postman/REST Assured test generation
- **Test Execution Reports**: Automated test result analysis

### Integration Possibilities
- **CI/CD Pipeline**: Integrate generated tests into build pipelines
- **Test Management Tools**: Export to TestRail, Zephyr, etc.
- **Code Coverage**: Link with coverage analysis tools
- **Defect Tracking**: Connect test results with bug tracking systems