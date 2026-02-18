### Why Pytest?

* Simple assertions - Uses plain Python `assert` statements without complex syntax
* Powerful fixtures - Built-in test client for FastAPI
* Mocking support - Uses @patch.dict for environment variable testing
* Clear failure messages - Provides detailed output when tests fail
* Class-based organization - Groups related tests into classes (TestRootEndpoint, TestHealthEndpoint)


### Test structure

Class Organization

* `TestRootEndpoint` - Tests for the main API endpoint
* `TestHealthEndpoint` - Tests for health check functionality
* `TestConfiguration` - Tests for configuration handling
