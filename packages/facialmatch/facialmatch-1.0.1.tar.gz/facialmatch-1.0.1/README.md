# facialmatch

**facialmatch** is a Python package that provides easy-to-use functions for comparing faces in images and extracting facial regions from a given image.

## Features

- 🧑‍🤝‍🧑 **Compare Faces:** Compare two images and check if they match with a given similarity threshold.
- 🖼️ **Extract Face:** Extract and return the facial region from an image.

## Installation

You can install the package via pip:

```bash
pip install facialmatch
```

## Usage

**match.py**
```bash
from facialmatch import compare_faces

# Compare two faces
result = compare_faces("path/to/image1.jpg", "path/to/image2.jpg")

# Custom similarity threshold
custom_result = compare_faces("path/to/image1.jpg", "path/to/image2.jpg", minimum_similarity=0.80)
```
**output**
```bash
{
  "similarity": 0.86,
  "match": "true"
}

```
##
**ExtractFace.py**
```bash
from facialmatch import get_face_from_image
import matplotlib.pyplot as plt

# Extract a face from an image
face_image = get_face_from_image("path/to/image")

# Display the extracted face using matplotlib
plt.imshow(face_image)
plt.axis('off')  # Turn off the axis
plt.show()
```
