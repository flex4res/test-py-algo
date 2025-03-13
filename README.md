
---

This repository provides a modular template for building algorithms that run in a **Compute-to-Data (CtD)** environment on Pontus‑X. The template separates the static, CtD-specific code from the user-defined algorithm logic, making it easy for developers to adapt the solution to their own use cases.

# Compute-to-Data (CtD) Algorithm Guide

This guide explains how to:
1. **Set up and understand the CtD algorithm code.**
2. **Build and push a Docker image** to Docker Hub.
3. **Publish the algorithm** on Pontus‑X (Flex4Res), including which fields to fill out and why.


## Overview

The core code (e.g., `my_algorithm.py`) is designed to run in a **Compute-to-Data** environment. Key points:

- **Reads input data** from `/data/inputs`.
- **Parses** that data as JSON.
- **Applies** a simple filtering algorithm (or your custom logic).
- **Writes** results to `/data/outputs/results.json`.
- Optionally, reads **custom parameters** from `/data/inputs/algoCustomData.json` (like a `threshold`).
- 
In a CtD environment:
- Data assets are mounted to `/data/inputs`.
- Results must be written to `/data/outputs`.

## File Structure

- **my_algorithm.py**:  
  The main Python script. It is divided into several modular functions:
  - `read_custom_params()`: Loads optional configuration (e.g., a threshold).
  - `find_input_file()`: Locates the first input file from `/data/inputs` (ignoring `algoCustomData.json`).
  - `parse_json_file(file_path)`: Parses a file as JSON.
  - `user_algorithm(data, threshold)`: Contains the user-specific data processing logic (default example filters records based on a threshold).
  - `write_results(data)`: Writes the processed results to `/data/outputs/results.json`.
  - `main()`: Ties all steps together.
- **Dockerfile**:  
  A sample Dockerfile to build your Docker image. It copies `my_algorithm.py` into the image and sets the entrypoint.

**Key Directories in CtD**:

- `/data/inputs`: Where the dataset is mounted.  
- `/data/outputs`: Where your code must place results.  
- `/data/inputs/algoCustomData.json`: Optional file for custom parameters (e.g., `threshold`).

---

## How to Use the Template

### 1. Customize Your Algorithm

- **User Logic**:  
  Open `my_algorithm.py` and locate the `user_algorithm(data, threshold)` function. Replace or extend the default filtering logic with your custom algorithm.  
  *Example (default logic):*
  ```python
  def user_algorithm(data, threshold):
      if not isinstance(data, list):
          raise ValueError("Expected input data to be a list of records.")
      filtered = [item for item in data if item.get("value", 0) >= threshold]
      return filtered
  
- **Static CtD Components**:  
  The remaining functions handle CtD-specific tasks (reading parameters, finding input files, writing outputs). You typically won't need to change these unless your environment differs.


## Building and Pushing the Docker Image to Docker Hub

Below is a step-by-step guide for **Docker**:

### Dockerfile

A minimal `Dockerfile` might look like:

```dockerfile
FROM python:3.8-slim

WORKDIR /app
COPY my_algorithm.py .

ENTRYPOINT ["python", "/app/my_algorithm.py"]
```

- **FROM python:3.8-slim**: Uses Python 3.8 in a slim environment.  
- **WORKDIR /app**: Sets the working directory.  
- **COPY my_algorithm.py .**: Copies your algorithm code into the container.  
- **ENTRYPOINT**: Ensures that running the container executes `my_algorithm.py`.

### Build the Image

In your project folder (where the Dockerfile resides), run:

```bash
docker build -t salihkz/pontusx-example:v6 .
```

- **`-t salihkz/pontusx-example:v6`**: Names the image and applies a versioned tag (`v6`).

### Push to Docker Hub

1. **Log in** to Docker Hub (if needed):
   ```bash
   docker login
   ```
2. **Push** the image:
   ```bash
   docker push salihkz/pontusx-example:v6
   ```

This uploads your image to Docker Hub under `salihkz/pontusx-example:v6`.  

---

## Publishing the Algorithm on Pontus-X

### Creating a New Algorithm Asset

1. **[Flex4Res Pontus Portal](https://flex4res.pontus-x.eu/publish/1)**  
2. **Click “Publish”**  
3. **Choose “Algorithm”** as the Asset Type.

### Metadata

- **Title**: e.g., `Test-algo-v6`.  
- **Description**: e.g. “For testing only.”

### Docker Image Settings

1. **Docker Image**: Select **“Custom”** (rather than `node:latest` or `python:latest`).  
2. **Custom Docker Image**: `salihkz/pontusx-example:v6`  
3. **Docker Image Checksum**: If your image is public pressing pressing `use` on the `Custom Docker Image` will automatically generate and fill the `Checksum`.
    In case you image is private you need to generate the checksum either:
   - **Using the Docker CLI**
   After building your image (e.g., `salihkz/pontusx-example:v4`), run:

```bash
docker images --digests salihkz/pontusx-example:v4
```

This command lists your images along with their digests (a SHA256 hash). The digest will look something like:

```
salihkz/pontusx-example   v4   sha256:dfdd75866b9fbbc99c7011d508ed27e392899ff0e51332cb2dfb22b77f56fcc9   123MB
```
   - **Alternatively, you can find it on Docker Hub**  Once you push your image to Docker Hub, the repository page usually displays the digest under the "Tags" section. You can copy the digest from there as well.
4. **Docker Image Entrypoint**: `python /app/my_algorithm.py` or empty if your Dockerfile already sets it.


## Using the Algorithm with a Dataset

To actually **run** the algorithm:

1. **Publish or find a dataset** on Pontus‑X.  
2. **Enable Compute** for that dataset.  
3. **Allowlist** your algorithm (Test-algo-v6).  
4. **Start a Compute job** on that dataset, selecting your algorithm.  
5. The logs and results (e.g. `results.json`) will be available once the job finishes.

---

## Example

- **Building Docker**: “Docker build -t salihkz/pontusx-example:v6 .”  
- **Pushing Docker**: “Docker push salihkz/pontusx-example:v6.”  
- **Pontus-X**: “Custom Docker Image” = `salihkz/pontusx-example:v6`, “Docker Image Entrypoint” = `python /app/my_algorithm.py`.  
- **Dataset & Algorithm**: Show how to allowlist or run a compute job.

---

## Troubleshooting & Tips

1. **File Not Found**: If your code expects `/data/inputs/data.json` but Pontus-X saves it as `/data/inputs/<did>/0`, consider searching recursively (as in the sample code).
2. **No Output**: Ensure you write results to `/data/outputs`; otherwise, the platform can’t retrieve them.
3. **Large Data**: Avoid printing file contents in logs for big or sensitive data.

---

## Conclusion

By following this guide, you can:

1. **Write or adapt** the CtD Python code.  
2. **Build & push** a Docker image to Docker Hub.  
3. **Publish** the algorithm on Pontus-X, specifying crucial fields like Docker image name, entrypoint, and optional checksum.  
4. **Run** a compute job on any dataset that’s allowlisted for your algorithm.

**Happy computing!**

---
