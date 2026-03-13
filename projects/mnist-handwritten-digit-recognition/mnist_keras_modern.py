"""
Modern Keras implementation of MNIST handwritten digit recognition.
Replaces the deprecated TensorFlow 1.x logic.
"""
import tensorflow as tf
from tensorflow.keras import layers, models # type: ignore

def main() -> None:
    # 1. Load data natively from Keras
    print("Loading MNIST data...")
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

    # 2. Preprocess data (Normalize pixels to 0-1)
    x_train = x_train.reshape(-1, 784).astype("float32") / 255.0
    x_test = x_test.reshape(-1, 784).astype("float32") / 255.0
    
    # 3. Build the Sequential Model (Softmax Regression equivalent)
    model = models.Sequential([
        layers.Dense(10, activation='softmax', input_shape=(784,))
    ])

    # 4. Compile the model
    model.compile(
        optimizer=tf.keras.optimizers.SGD(learning_rate=0.5),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    # 5. Train the model
    print("Starting training...")
    model.fit(x_train, y_train, epochs=10, batch_size=100, validation_split=0.1)

    # 6. Evaluate
    print("Evaluating on test set...")
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
    print(f"Test Accuracy: {test_acc:.4f}")

if __name__ == '__main__':
    main()
