# Dabarqus SDK Documentation

## Table of Contents
1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [API Reference](#api-reference)
   - [Health and Admin](#health-and-admin)
   - [Models and Downloads](#models-and-downloads)
   - [Inference](#inference)
   - [Hardware](#hardware)
   - [Silk (Memory) Operations](#silk-memory-operations)
   - [Shutdown](#shutdown)
   - [Logging](#logging)
   - [Embedding](#embedding)
4. [Examples](#examples)

## Installation

### Dabarqus Service
**Important**: This SDK requires [Dabarqus](dabarqus.com) to be installed and running on your machine.
Before using this SDK, please ensure that you have:

- Downloaded and installed [Dabarqus](dabarqus.com)
- Started the Dabarqus service on your machine

The SDK communicates with the Dabarqus service via its API, so having Dabarqus running is essential for the SDK to function correctly.  
Once Dabarqus is set up and running, you can proceed with using this SDK.
For more information on how to start and manage the Dabarqus service, please refer to the Dabarqus documentation.

### SDK
To install the Dabarqus SDK, you can use pip:

```bash
pip install dabarqus
```

## Getting Started

To start using the Dabarqus SDK, import it and create an instance:

```python
from dabarqus import barq

# Create an instance of the SDK
sdk = barq("http://localhost:6568")  # Replace with your Dabarqus server URL
```

## API Reference

### Health and Admin

#### `check_health()`
Check the health status of the Dabarqus service.

```python
health_status = sdk.check_health()
print(health_status)
```

### Models and Downloads

#### `get_models()`
Retrieve available AI models.

```python
models = sdk.get_models()
print(models)
```

#### `get_model_metadata(model_repo: str, file_path: Optional[str] = None)`
Get metadata for a specific model.

```python
metadata = sdk.get_model_metadata("model_repo_name", "path/to/model")
print(metadata)
```

#### `get_downloads(model_repo: Optional[str] = None, file_path: Optional[str] = None)`
Get information about downloaded items.

```python
downloads = sdk.get_downloads("model_repo_name")
print(downloads)
```

#### `enqueue_download(model_repo: str, file_path: str)`
Enqueue a new download.

```python
result = sdk.enqueue_download("model_repo_name", "path/to/model")
print(result)
```

#### `cancel_download(model_repo: str, file_path: str)`
Cancel a download.

```python
result = sdk.cancel_download("model_repo_name", "path/to/model")
print(result)
```

#### `remove_download(model_repo: str, file_path: str)`
Remove a downloaded item.

```python
result = sdk.remove_download("model_repo_name", "path/to/model")
print(result)
```

### Inference

#### `get_inference_info(alias: Optional[str] = None)`
Get information about inference items.

```python
info = sdk.get_inference_info("my_inference")
print(info)
```

#### `start_inference(alias: str, model_repo: str, file_path: str, ...)`
Start an inference.

```python
result = sdk.start_inference("my_inference", "model_repo", "path/to/model")
print(result)
```

#### `stop_inference(alias: str)`
Stop an inference.

```python
result = sdk.stop_inference("my_inference")
print(result)
```

#### `get_inference_status(alias: Optional[str] = None)`
Get the status of an inference.

```python
status = sdk.get_inference_status("my_inference")
print(status)
```

#### `reset_inference(alias: str)`
Reset an inference.

```python
result = sdk.reset_inference("my_inference")
print(result)
```

#### `restart_inference()`
Restart the current inference.

```python
result = sdk.restart_inference()
print(result)
```

### Hardware

#### `get_hardware_info()`
Get hardware information.

```python
hardware_info = sdk.get_hardware_info()
print(hardware_info)
```

### Silk (Memory) Operations

#### `get_memory_status()`
Get memory status.

```python
status = sdk.get_memory_status()
print(status)
```

#### `enable_memories()`
Enable memories.

```python
result = sdk.enable_memories()
print(result)
```

#### `disable_memories()`
Disable memories.

```python
result = sdk.disable_memories()
print(result)
```

#### `get_memory_banks()`
Get memory banks information.

```python
banks = sdk.get_memory_banks()
print(banks)
```

#### `activate_memory_bank(bank: str)`
Activate a memory bank.

```python
result = sdk.activate_memory_bank("my_bank")
print(result)
```

#### `deactivate_memory_bank(bank: str)`
Deactivate a memory bank.

```python
result = sdk.deactivate_memory_bank("my_bank")
print(result)
```

#### `query_semantic_search(query: str, limit: Optional[int] = None, memory_bank: Optional[str] = None)`
Perform a semantic query.

```python
results = sdk.query_semantic_search("What is Dabarqus?", limit=5, memory_bank="my_bank")
print(results)
```

#### `check_silk_health()`
Check the health of the Silk retriever.

```python
health = sdk.check_silk_health()
print(health)
```

#### `get_silk_model_metadata()`
Get model metadata from the Silk retriever.

```python
metadata = sdk.get_silk_model_metadata()
print(metadata)
```

#### `check_silk_store_health()`
Check the health of the Silk store.

```python
health = sdk.check_silk_store_health()
print(health)
```

#### `enqueue_ingestion(memory_bank_name: str, input_path: str, ...)`
Enqueue a new ingestion item.

```python
result = sdk.enqueue_ingestion("my_bank", "/path/to/documents")
print(result)
```

#### `cancel_ingestion(bank: str)`
Cancel an ingestion.

```python
result = sdk.cancel_ingestion("my_bank")
print(result)
```

#### `get_ingestions(bank: Optional[str] = None)`
Get information about ingestion items.

```python
ingestions = sdk.get_ingestions("my_bank")
print(ingestions)
```

### Shutdown

#### `shutdown_server()`
Initiate server shutdown.

```python
result = sdk.shutdown_server()
print(result)
```

### Logging

#### `write_to_log(log_data: Dict[str, Any])`
Write to log.

```python
log_result = sdk.write_to_log({"message": "Test log entry", "level": "INFO"})
print(log_result)
```

### Embedding

#### `get_embedding(input_text: str)`
Get an embedding from the Silk retriever.

```python
embedding = sdk.get_embedding("Hello, world!")
print(embedding)
```

## Examples

Here's a more comprehensive example that demonstrates using multiple SDK functions:

```python
from dabarqus import barq

# Initialize the SDK
sdk = barq("http://localhost:6568")

# Check the health of the service
health = sdk.check_health()
print(f"Service health: {health}")

# Get available memory banks
banks = sdk.get_memory_banks()
print(f"Available memory banks: {banks}")

# Activate a memory bank
sdk.activate_memory_bank("my_documents")

# Enqueue an ingestion
ingestion_result = sdk.enqueue_ingestion("my_documents", "/path/to/documents")
print(f"Ingestion result: {ingestion_result}")

# Perform a semantic search
search_results = sdk.query_semantic_search("What is Dabarqus?", limit=5, memory_bank="my_documents")
print("Search results:")
for result in search_results:
    print(f"- {result}")

# Get an embedding
embedding = sdk.get_embedding("Dabarqus is a powerful RAG solution")
print(f"Embedding (first 5 elements): {embedding[:5]}")

# Get hardware info
hardware_info = sdk.get_hardware_info()
print(f"Hardware info: {hardware_info}")
```

This documentation provides a comprehensive guide to using the Dabarqus SDK. Users can refer to this documentation to understand how to use each method in the SDK, along with examples of how to use them in their code.