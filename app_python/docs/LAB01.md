I'm choosing FastAPI because it is the most [popular, most widely adopted, and most well-supported framework]((https://www.reddit.com/r/Backend/comments/1qj8z6o/is_fastapi_still_a_good_choice_in_2026_for_web/)) for building Python APIs in 2026.

This document outlines the best practices followed in this project, inspired by this [repo](https://github.com/zhanymkanov/fastapi-best-practices). It also explains why the official FastAPI documentation, while excellent for getting started, may not always suffice for large-scale industrial projects.

---

## Why FastAPI Best Practices Repository?

The repository [fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices) by **Zhanymkanov** is an excellent resource for implementing FastAPI in industrial-grade projects. Here’s why it was chosen as a reference:

1. **Real-World Experience**:
   - The repository is based on real-world industrial projects, ensuring that the practices are battle-tested and scalable.
   - It addresses common challenges faced in production environments, such as dependency management, testing, and deployment.

2. **Beyond Official Documentation**:
   - While the official FastAPI documentation is great for beginners, it often focuses on simplicity and may not cover advanced use cases or scalability concerns.
   - This repository fills the gap by providing patterns and practices that are essential for large-scale applications.

3. **Community-Driven**:
   - The repository is widely recognized in the FastAPI community and has been reviewed and improved by multiple contributors.

---

## Best Practices Implemented in My Project

### 1. **Project Structure**

- The project follows a modular structure.
  - This structure separates application logic, tests, and configuration, making the project easier to maintain and scale.

### 2. **PEP 8 Compliance**

- The code adheres to **PEP 8** standards for readability and consistency:
  - Use of `snake_case`, docstrings, spacing and other popular standards.

### 3. **Dependency Management**

- Dependencies are listed in `requirements.txt` for easy installation:
  - A virtual environment is used to isolate dependencies and avoid conflicts.

### 4. **Logging**

- Logging is used to track application behavior and errors. Implemented as a middleware that writes logs in terminal.

### 5. **Code Formatting**

- Use the `black` module to ensure consistent style during development.
     To run styler formater run the following command in root directory:

     ```bash
     pip install black
     black .
     ```

### 6. **Documentation**

- A comprehensive `README.md` file is provided to guide users through setup, usage, and testing.
  - Docstrings are added to functions for better code documentation.

--- 

## API examples

Check [README.md](/app_python/README.md)

## Testing evidence

![01-main-endpoint.png](/app_python/docs/screenshots/01-main-endpoint.png)
![02-health-check.png](/app_python/docs/screenshots/02-health-check.png)
![03-formatted-output.png](/app_python/docs/screenshots/03-formatted-output.png)

## GitHub Community section (why stars/follows matter)

| Activity | Purpose | Benefit |
|----------|---------|---------|
| **Starring** | Bookmark interesting projects | Personal library of resources |
| **Starring** | Show appreciation | Encourages maintainers |
| **Starring** | Increase project visibility | Helps projects grow |
| **Following** | See others' work | Discover new projects |
| **Following** | Learn from examples | Improve coding skills |
| **Following** | Build network | Career opportunities |

