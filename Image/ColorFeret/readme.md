
# Helper for ColorFeret Dataset
A base class for using ColorFeret dataset for facial recognition, gender classification, etc
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for training and testing purposes. Notes for Tensorflow serving would be added in the future. 

### Prerequisites
```
Python3
Numpy
Tensorflow v1.0 or higher
```

## Restructuring dataset for training
Download the ColorFeret Dataset from [here](https://www.nist.gov/itl/iad/image-group/color-feret-database) and put it at the root of ColorFeret folder
### Setting task for dataset
This dataset can be used for several purposes. Supported tasks can be selected using their names shown below:
* Gender Classification
* Age Prediction (Scope of prediction : Years)
* Facial features detection (mouth, nose, eyes, facial hair)
* Sunglasses Detection

| Task name     | Encoded task name |
| ------------- | ------------- |
| Gender Classification  | gender  |
| Age Prediction  | age  |
| Facial features  | face-features  |
| Sunglass Detection  | sunglass  |

Execute the following file and replace ```encoded_task_name``` with your desired task from the table above. The structured dataset would be in the ```dataset``` folder. 
```
python3 dataset_organizer.py --task encoded_task_name
```
You can also simply do ```--help``` to learn about currently supported tasks

```python3 dataset_organizer.py --help```

## Built With

* [Tensorflow](https://github.com/tensorflow/tensorflow) - Deep Learning framework
* [Python 3](https://github.com/python) - Programming Language
* [Numpy](https://github.com/numpy/numpy) - Data processing Library

## Authors
* **Nimish Ronghe** (https://github.com/nimish1512)

