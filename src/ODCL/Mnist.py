#code from https://www.tensorflow.org/datasets/keras_example
#documentation by our team

print("importing tensorflow...")
import tensorflow as tf
print("importing tensorflow_datasets...")
import tensorflow_datasets as tfds
print("imports complete")

print()
print("Loading dataset...")
print("-----------------------------------------------")

#loads dataset and splits into 2 subsets, one for training and the other for testing
(train, test), info = tfds.load(
    'mnist', #name of the dataset
    split=['train', 'test'], #type of split
    shuffle_files=True, #randomizes order of files to prevent overfitting*
    as_supervised=True, #stores each image as (image, label) instead of {"img" : img, "label" : label}
    with_info=True, #gives verbose console output
)
# *the mnist dataset is stored all in one file, so this doesn't matter, but it's a good practice
print("-----------------------------------------------")
print("Dataset loading complete")

"""
the value of each pixel in tensorflow datasets is stored as an unsigned 8 bit integer
(an integer from 0-255)

whereas the dataset expects a 32 bit float 
(a decimal value, in this case from 0 to 1)

This code block remaps every image from integer to float and fits the values between 0 and 1

num_parallel_calls sets how many threads to use at the same time
tf.data.AUTOTUNE will optimize this to the best of its ability
"""
def normalize_img(image, label):
    """Normalizes images: `uint8` -> `float32`."""
    return (tf.cast(image, tf.float32) / 255., label)

train = train.map(normalize_img, num_parallel_calls=tf.data.AUTOTUNE)
test = test.map(normalize_img, num_parallel_calls=tf.data.AUTOTUNE)


#loads the training dataset into memory
train = train.cache()

#shuffles the training dataset again for more randomness
train = train.shuffle(min(info.splits['train'].num_examples, 1000))

#splits training dataset into batches of size 128 to give the net new batches each epoch
train = train.batch(128)

#fetches whatever the tensorflow optimizer deems fit for performance
train = train.prefetch(tf.data.AUTOTUNE)

#batching occurs before caching now because we don't care if batches are unique between epochs
test = test.batch(128)
test = test.cache()
test = test.prefetch(tf.data.AUTOTUNE)

"""
creates a keras neural net
input layer flattens out the 28x28 image into a set of 28^2 input nodes
first hidden layer sends thes inputs through 128 nodes
second hidden layer takes the outputs from the first hidden layer and sends them through 10 nodes
these 10 second layer nodes will then be used to compute the output

an activation function is used to prevent diminishing returns while hill climbing
ReLU, because of its linearity, is very fast to compute in comaprison to altertnatives like sigmoid
"""
model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(10)
])

"""
the Adam optimizer is used to adjust the net between epochs
a more complex, efficient variation of gradient descent

Using legacy Adam instead of current Adam because we're on MacOS with an ARM chip
WARNING:absl:At this time, the v2.11+ optimizer `tf.keras.optimizers.Adam` 
runs slowly on M1/M2 Macs, please use the legacy Keras optimizer instead, 
located at `tf.keras.optimizers.legacy.Adam`.

the value 0.001 is a step size, or learning rate
if the model never converges, lower the rate
if the model keeps converging on tiny local minimums or takes too long to train, raise the rate

the Sparse Categorical Cross-Entropy loss function is used here
this is to compute how far off the expected and actual results are for each image
https://machinelearningmastery.com/cross-entropy-for-machine-learning/
https://stats.stackexchange.com/questions/326065/cross-entropy-vs-sparse-cross-entropy-when-to-use-one-over-the-other
"""
model.compile(
    optimizer=tf.keras.optimizers.legacy.Adam(0.001),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
)

#finally runs the dataset
model.fit(
    train,
    epochs=7,
    validation_data=test,
)
print()
model.summary()

model.save("./src/ODCL/Trained/Mnist/model1.h5")