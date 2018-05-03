

# Helper for CKPlus (ck+) Dataset
A base class for using ColorFeret dataset for emotion detection and recognition from images
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for training and testing purposes. Notes for Tensorflow serving would be added in the future. 

### Prerequisites
```
Python3
Numpy
Tensorflow v1.0 or higher
```

## Restructuring dataset for training
*  Download the CKPlus Dataset from [here](http://www.consortium.ri.cmu.edu/ckagree/) and put it at the root of CKPlus folder
*  Create two folders ```source_images``` and ```source_emotion``` at the root of project.
*  Copy all images to ```source_images``` and all ```.txt``` files to ```source_emotion``` folder 
### Setting task for dataset
This dataset can be used for the following task:
* Emotion Recognition


Execute the following file. The structured dataset would be in the ```dataset``` folder. 
```
python3 dataset_organizer.py
```
### Using dataset for training
To consume batches of images while training, add following lines to your file.
``` 
from dataset_organizer import CKPlusOrganizer
from helper import CKLoader
```
Once that is done, create a ```CKLoader``` object inside your session loop. 
Make a call  to```format_data()``` with a list of parameters. Below is the currently supported parameters:

| Parameter     | Default_value |
| ------------- | ------------- |
| train_test_split   | 80/20 resp  |
| normalzed_test_split  | False  |
| shuffle  | False  |
| channels  | 1  |
| img_dims  | [32,32]  |
| batch_size  | 128  |
| preprocess  | None |

The preprocess parameter takes a list of supported preprocessing techniques explained below:

| Task name     | Encoded task name |
| ------------- | ------------- |
| Randomly flip images vertically   | random_flip_vertical  |
| Randomly flip images horizontally  | random_flip_horizontal  |
| RGB to Grayscale  | RGB2GRAY  |
| Grayscale to RGB  | GRAY2RGB  |
| Adjust image brightness  | Adjust_brightness  |

### Example 

Simply copy-paste this snippet and add other stuff to this as per needed.
```
with tf.Session() as sess:
  x = CKLoader()
  x.format_data(preprocess=['random_flip_vertical','random_flip_horizontal' ,'RGB2GRAY', 'GRAY2RGB', ,'Adjust_brightness']])
  while True:
    batch_x = sess.run(x.train_next_batch())
    x,y = batch_x
    result = sess.run(trainer, feed_dict={X:x,Y:y})
```
## Built With

* [Tensorflow](https://github.com/tensorflow/tensorflow) - Deep Learning framework
* [Python 3](https://github.com/python) - Programming Language
* [Numpy](https://github.com/numpy/numpy) - Data processing Library

## Authors
* **Nimish Ronghe** (https://github.com/nimish1512)

