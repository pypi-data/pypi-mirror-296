# Similarix: Semantic and Multimodal Search Client

![PyPI version](https://img.shields.io/pypi/v/similarix.svg)
![Python versions](https://img.shields.io/pypi/pyversions/similarix.svg)
![License](https://img.shields.io/github/license/s-emanuilov/similarix-client.svg)

Similarix is a powerful Python client for interacting with the [Similarix API](https://similarix.com/docs/), enabling semantic and multimodal search capabilities for both images and text.

## 🌐 [Visit Similarix website](https://similarix.com)

## 🚀 Features

- 🔍 Semantic text search
- 🖼️ Image-based search
- 🔀 Multimodal search capabilities
- 📁 Collection management
- 🔄 Synchronization controls
- ☁️ Managed cloud storage integration

## 🛠️ Installation

Install Similarix using pip:

```bash
pip install similarix
```

## 🏁 Quick Start
```python
from similarix import Similarix
```

### Initialize the client
```python
client = Similarix('your_api_token')
```

### Perform a text search
```python
results = client.text_search('cute puppies')
print(results)
```

### Perform an image search
```python
with open('path/to/image.jpg', 'rb') as img:
    results = client.image_search(img)
print(results)
```

## 📚 Usage
### Text search
```python
results = client.text_search('landscape photography')
```

### Image search
```python
with open('mountain.jpg', 'rb') as img:
    results = client.image_search(img)
```

### Managing collections
```python
# List all collections
collections = client.list_collections()

# Get details of a specific collection
collection = client.get_collection('collection_uuid')

# Trigger a sync for a collection
client.trigger_sync('collection_uuid')

# Check sync status
status = client.check_sync_status('collection_uuid')
```
### Uploading to managed collection (Similarix cloud)
```python
with open('new_image.jpg', 'rb') as img:
    result = client.upload_to_managed_collection('collection_uuid', img)
```
## 🌟 Why Similarix?
- Powerful Semantic Search: Go beyond keyword matching with our advanced semantic understanding.
- Multimodal Capabilities: Seamlessly search across text and images.
- Easy Integration: Simple API designed for quick integration and rapid development.
- Scalable: Built to handle large datasets and high-volume requests.
- Flexible: Suitable for a wide range of applications, from e-commerce to content management.

## 🤝 Contributing
We welcome contributions! 

## 📄 License
Similarix is released under the MIT License. See the LICENSE file for more details.

## 📬 Contact
For support or queries, please open an issue or contact us at support@similarix.com.

<p align="center">
  Made with ❤️ by the Similarix
</p>
