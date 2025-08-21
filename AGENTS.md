# Instructions for AI Agents

## Communication Guidelines

- **Language**: Communicate with users in Russian language (русский язык). All responses, suggestions, and explanations should be provided in Russian.

## Project Overview

The `gigachat-adapter` project is an adapter for the GigaChat API that provides an interface compatible with the OpenAI API. This allows integration of GigaChat into applications originally designed for OpenAI with minimal code changes.

## Project Structure

- `src/` - application source code
  - `core/` - application core (settings, logging, patches)
  - `endpoints/` - API endpoints
  - `models/` - data models (Pydantic)
  - `gigachat_service.py` - service for working with GigaChat API
  - `main.py` - main FastAPI application file
- `tests/` - tests
- `templates/` - templates
- `Dockerfile` - file for building Docker image

## Development Guidelines

1. **Maintain Project Structure**: All new features should follow the current directory structure.

2. **Use Type Annotations**: All code should use Python type annotations.

3. **Maintain API Compatibility**: New endpoints should conform to the OpenAI API specification.

4. **Testing**: Every new feature should have tests written in the `tests/` directory.

5. **Documentation**: Any new parameters should be documented in README.md.

6. **Error Handling**: Use exception handlers from `main.py` to unify error responses.

## Technical Stack

- **Python**: Version 3.12+
- **FastAPI**: Main framework for API
- **Pydantic**: For data validation and settings
- **HTTPX**: HTTP client for asynchronous requests
- **GigaChat SDK**: Official library for interacting with GigaChat

## Important Features

1. Application configuration is done through environment variables (`.env` file).

2. Testing uses `pytest` with HTTP request mocking via `pytest-httpx`.

3. The project supports Docker for deployment.

## Code Style

- Use `ruff` for code style checking
- Use `mypy` for static type analysis
- Follow the import structure: standard libraries first, then third-party libraries, then local imports

## Modern Python Coding Practices

1. **Async/Await**: Use asynchronous programming for I/O-bound operations. Ensure that blocking operations run in separate threads with `run_in_threadpool`.

2. **Dependency Injection**: Utilize FastAPI's dependency injection system for reusable components, validation, and database connections.

3. **Pydantic Models**: Define separate models for requests, responses, and database entities. Use field validators for complex validation logic.

4. **Error Handling**: Raise specific exceptions and handle them consistently through exception handlers.

5. **Type Annotations**: Use comprehensive type hints including generics and unions for better code readability and IDE support.

6. **Domain-Driven Structure**: Organize code by domains or features rather than by technical layers.

7. **Small Functions**: Write small, focused functions that do one thing well and have clear input/output contracts.

8. **Testing**: Implement both unit tests and integration tests. Mock external dependencies to focus on testing specific functionality.

9. **Documentation**: Use descriptive docstrings with clear examples. Document API endpoints with response models and status codes.

10. **Configuration Management**: Separate configuration from code using environment variables and Pydantic's BaseSettings.

11. **Explicit over Implicit**: Prefer explicit, clear code over clever tricks. Write code that is easy to understand and maintain.

12. **Security Best Practices**: Validate all inputs, use proper authentication mechanisms, and protect against common vulnerabilities.
