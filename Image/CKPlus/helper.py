import tensorflow as tf
import os

class CKLoader:

	def __init__(self):
		try:
			target_class = os.listdir("sorted_set")
			self.images = {}
			self.encoded_classes = {}
			for i in range(len(target_class)):
				self.encoded_classes.update({target_class[i]:i})
			#print(self.encoded_classes)
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
			del temp
		except Exception as e:
			print(e)

	def format_data(self,train_test_split=0.8, normalized_test_split=False, shuffle=False, channels=1, img_dims=[32,32], preprocess=[None], batch_size=128):
		try:
			train_images = list()
			train_labels = list()
			test_images = list()
			test_labels = list()
			self.img_size= img_dims
			self.channels = channels
			self.preprocess = preprocess	
			if normalized_test_split:
				if int(self.min_samples_count*train_test_split)<=5:
					raise Exception("Cannot split dataset. Test-data too small {0} test samples for class {1}".format(int(self.min_samples_count*train_test_split),self.min_samples_class))
				else:
					test_count = int(self.min_samples_count*float(1.0 -train_test_split))+1
					for k,v in self.images.items():
						train_count = len(v)-test_count
						for i in range(train_count):
							train_images.append(v[i])
							train_labels.append(self.encoded_classes[k])
						for i in range(len(v)-test_count,len(v)):
							test_images.append(v[i])
							test_labels.append(self.encoded_classes[k])
			else:
				for k,v in self.images.items():
					train_count = int(len(v)*train_test_split)
					for i in range(train_count):
						train_images.append(v[i])
						train_labels.append(self.encoded_classes[k])
					for i in range(len(v)-train_count,len(v)):
						test_images.append(v[i])
						test_labels.append(self.encoded_classes[k])
			if shuffle: 
				no_imgs_train = len(train_images)
				no_imgs_test = len(test_images)
			train_images = tf.constant(train_images)
			train_labels = tf.constant(train_labels)
			train_labels = tf.cast(train_labels, tf.int32)
			test_images = tf.constant(test_images)
			test_labels = tf.constant(test_labels)
			test_labels = tf.cast(test_labels, tf.int32)
			training_data = tf.data.Dataset.from_tensor_slices((train_images,train_labels))
			test_data = tf.data.Dataset.from_tensor_slices((test_images, test_labels))
			if shuffle:
				print("Shuffling Training Images")
				training_data = training_data.shuffle(buffer_size=no_imgs_train)
				test_data = test_data.shuffle(buffer_size=no_imgs_test)
				print("Shuffling Validation Images")			
			training_data = training_data.map(self.load_images)
			test_data = test_data.map(self.load_images)
			training_data = training_data.batch(batch_size)
			iter1 = training_data.make_one_shot_iterator()
			self.train_next_batch = iter1.get_next()
			iter2 = test_data.make_one_shot_iterator()
			self.test_data = iter2.get_next()
		except Exception as e:
			print(e)
				

	def load_images(self, img_path, label):
		one_hot = tf.one_hot(label, len(self.encoded_classes))
		img = tf.read_file(img_path)
		img = tf.image.decode_image(img, self.channels)
		img.set_shape([None, None, None])
		img = tf.image.resize_images(img, self.img_size)
		if self.preprocess!=[None]:

		return img,one_hot

with tf.Session() as sess:
	x = CKLoader()
	x.format_data(batch_size=64, shuffle=True, normalized_test_split=True, channels=3, img_dims=[28,28])
	i=1
	while True:
		try:
			elem = sess.run(x.train_next_batch)
			print(type(elem))
			print("Batch {0} ------------------------------------------------------->".format(i))
			i+=1
		except:
			break
