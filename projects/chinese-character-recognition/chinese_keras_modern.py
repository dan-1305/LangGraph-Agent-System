"""
Modern Keras implementation of Chinese Character Recognition with CNN and Batch Normalization.
Replaces the deprecated tf.contrib.slim and tf.Session logic.
"""
import os
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks # type: ignore

# Hyperparameters
IMAGE_SIZE = 64
CHARSET_SIZE = 3755
BATCH_SIZE = 128
EPOCHS = 10

def build_model() -> tf.keras.Model:
    """Builds a modern CNN model equivalent to the original TF1 slim model."""
    model = models.Sequential()
    
    # Input layer
    model.add(layers.InputLayer(input_shape=(IMAGE_SIZE, IMAGE_SIZE, 1)))

    # Block 1
    model.add(layers.Conv2D(64, (3, 3), padding='same', use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D((2, 2), padding='same'))

    # Block 2
    model.add(layers.Conv2D(128, (3, 3), padding='same', use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D((2, 2), padding='same'))

    # Block 3
    model.add(layers.Conv2D(256, (3, 3), padding='same', use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D((2, 2), padding='same'))

    # Block 4
    model.add(layers.Conv2D(512, (3, 3), padding='same', use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.Activation('relu'))
    
    # Block 5
    model.add(layers.Conv2D(512, (3, 3), padding='same', use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.Activation('relu'))
    model.add(layers.MaxPooling2D((2, 2), padding='same'))

    # Fully Connected layers
    model.add(layers.Flatten())
    model.add(layers.Dropout(0.2)) # keep_prob=0.8 means dropout rate=0.2
    model.add(layers.Dense(1024, use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.Activation('relu'))
    
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(CHARSET_SIZE, activation='softmax'))

    return model

def create_dataset_pipeline(data_dir: str, augment: bool = False) -> tf.data.Dataset:
    """Uses modern tf.data API instead of old QueueRunners."""
    if not os.path.exists(data_dir):
        print(f"Warning: Directory {data_dir} does not exist. Please download the dataset.")
        # Returning a dummy dataset for demonstration purposes if real data is missing
        return tf.data.Dataset.from_tensors((tf.zeros((BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, 1)), tf.zeros((BATCH_SIZE,))))

    dataset = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        labels='inferred',
        label_mode='int',
        color_mode='grayscale',
        batch_size=BATCH_SIZE,
        image_size=(IMAGE_SIZE, IMAGE_SIZE),
        shuffle=True
    )
    
    # Normalize images
    normalization_layer = layers.Rescaling(1./255)
    dataset = dataset.map(lambda x, y: (normalization_layer(x), y), num_parallel_calls=tf.data.AUTOTUNE)
    
    if augment:
        data_augmentation = tf.keras.Sequential([
            layers.RandomFlip("horizontal_and_vertical"),
            layers.RandomContrast(0.2),
            layers.RandomBrightness(0.2)
        ])
        dataset = dataset.map(lambda x, y: (data_augmentation(x, training=True), y), num_parallel_calls=tf.data.AUTOTUNE)

    return dataset.prefetch(buffer_size=tf.data.AUTOTUNE)

def main() -> None:
    print("Building modern Keras model...")
    model = build_model()
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), # Standard Adam
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.SparseTopKCategoricalAccuracy(k=3, name='top_3_acc')]
    )
    
    model.summary()

    # Load datasets using modern tf.data API
    train_dataset = create_dataset_pipeline('./data/train/', augment=True)
    val_dataset = create_dataset_pipeline('./data/test/', augment=False)

    # Callbacks
    checkpoint_cb = callbacks.ModelCheckpoint(
        filepath='./checkpoint/modern_model.keras',
        save_best_only=True,
        monitor='val_accuracy'
    )
    tensorboard_cb = callbacks.TensorBoard(log_dir='./logs_modern')

    print("Starting training with modern fit() loop...")
    # Uncomment to actually train (requires data)
    # model.fit(train_dataset, validation_data=val_dataset, epochs=EPOCHS, callbacks=[checkpoint_cb, tensorboard_cb])

if __name__ == '__main__':
    main()
