# Docker Best Practices

1. **Use a Minimal Base Image:**

    The `python:3.12-slim` base image is lightweight and secure, reducing the attack surface and image size.

2. **Run as a Non-Root User:**

    The application runs as a non-root user (appuser) inside the container to improve security.
    <details>
    <summary>Running containers as root is dangerous because:</summary>

    If an attacker exploits a vulnerability in your application and breaks out of the container, they automatically gain root access on your host machine. This gives them full control over your entire system.
    </details>

3. **Optimize Docker Layers:**

    Dependencies are installed in a separate layer to leverage Docker's caching mechanism and speed up builds.

4. **Expose Only Necessary Ports:**

    Exposed only port 8000 (the port used by the FastAPI application). Not `network` mode.

5. **Use .dockerignore:**

    Unnecessary files are excluded from the Docker build context using a `.dockerignore` file, reducing the build context size.

6. **Set Environment Variables:**

    `PYTHONUNBUFFERED=1` is set to ensure Python outputs are sent directly to the terminal (useful for logging that may occure in next versions).

7. **Use COPY Instead of ADD:**

    The COPY instruction is used to copy only necessary files into the image, avoiding unintended side effects.
    <details>
    <summary>Why COPY over ADD in Dockerfiles?</summary>
        `COPY` is simple and transparent — it just copies files from your local machine into the image.

        `ADD` does the same but adds two "magic" behaviors:
        * Auto-extracts local tar archives (.tar, .gz, etc.)
        * Downloads files from remote URLs
    </details>

8. **Expose Only Necessary Ports:**

    Only port 8000 (used by FastAPI) is exposed in the Dockerfile.

9. **Push to Docker Hub:**

    Pushed the Docker image to Docker Hub [repo](https://hub.docker.com/repository/docker/konstantinqwertin/devops-info-app/general) for easy sharing and deployment.

10. **Git Commit Hash (SHA) tagging strategy:**

    Tag the Docker image with the Git commit hash it was built from

    ```bash
        docker build -t myapp:$(git rev-parse --short HEAD) .
        # Example: myapp:a4f7d2e
    ```

    Or set up this approach in CI

    ```yaml
        - name: Build Docker image
            run: |
            docker build -t konstantinqwertin/devops-info-app:${{ github.sha }} app_python/
    ```
