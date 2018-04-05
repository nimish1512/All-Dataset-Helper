import tensorflow as tf
import os

class CKLoader:

	def __init__(self):
		try:
			target_class = os.listdir("sorted_set")
			self.images = {}
			self.classes = len(target_class)
			temp = list()
			self.min_samples_count = 5
			self.min_samples_class=None
			flag=1
			for cl in target_class:
				for _, _, files in os.walk("sorted_set/"+str(cl)+"/"):
					temp.append(["sorted_set/{0}/".format(cl) + x for x in files])
					if flag:
						self.min_samples_count=len(files)
						min_samples_class=cl
						flag=0
					if len(files)<self.min_samples_count:
						self.min_samples_count=len(files)
						self.min_samples_class=cl
				self.images.update({cl:temp[0]})
				del temp[:]
			del flag
		except Exception as e:
			print(e)

	def format_data(self,train_test_split=0.8, normalized_test_split=False, shuffle=False, channels=1, img_dims=(32,32)):
		try:
			train_images = list()
			train_labels = list()
			test_images = list()
			test_labels = list()		
			if normalized_test_split:
				if int(self.min_samples_count*train_test_split)<=5:
					raise Exception("Cannot split dataset. Test-data too small {0} test samples for class {1}".format(int(self.min_samples_count*train_test_split),self.min_samples_class))
				else:
					test_count = int(self.min_samples_count*float(1.0 -train_test_split))+1
					if shuffle:
						print("shuffle")
					else:
						for k,v in self.images.items():
							train_count = len(v)-test_count
							for i in range(train_count):
								train_images.append(v[i])
								train_labels.append(k)
							for i in range(len(v)-test_count,len(v)):
								test_images.append(v[i])
								test_labels.append(k)
			else:
				for k,v in self.images.items():
					train_count = int(len(v)*train_test_split)
					for i in range(train_count):
						train_images.append(v[i])
						train_labels.append(k)
					for i in range(len(v)-train_count,len(v)):
						test_images.append(v[i])
						test_labels.append(k)
			training_data = tf.data.Dataset.from_tensor_slices((train_images,train_labels))
			test_data = tf.data.Dataset.from_tensor_slices((test_images, test_labels))
			print(training_data.output_types)
			training_data = training_data.map(load_images)
			test_data = test_data.map(load_images)
			iter1 = tf.data.Iterator.from_structure(training_data.output_types, training_data.output_shapes)
			self.train_next_batch = iter1.get_next()
		except Exception as e:
			print(e)
				

def load_images(img_path, label):
	one_hot = tf.one_hot(label, 8)
	img = tf.read_file(img_path)
	img = tf.image.decode_image(img, channels=1)
	return (img,one_hot)



x = CKLoader()
print(x.min_samples_class, x.min_samples_count)
x.format_data()

'''
images_list = []
for i in range(6):
    image = tf.read_file("{0}.jpg".format(i))
    image_tensor = tf.image.decode_jpeg(image, channels=3)
    image_tensor = tf.image.rgb_to_grayscale(image_tensor)
    image_tensor = tf.image.resize_images(image_tensor, [28, 28])
    image_tensor = tf.expand_dims(image_tensor, 0)
    images_list.append(image_tensor)

with tf.Session() as sess:
	sess.run(tf.global_variables_initializer())	
	batches = tf.train.batch(images_list, batch_size=3, enqueue_many=True, capacity=6)
'''