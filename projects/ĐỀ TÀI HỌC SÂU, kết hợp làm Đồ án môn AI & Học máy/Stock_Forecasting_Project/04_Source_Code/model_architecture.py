import tensorflow as tf
from tensorflow.keras import layers, Model

class TimeAttentionLayer(layers.Layer):
    def __init__(self, **kwargs):
        super(TimeAttentionLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        self.W = self.add_weight(name="att_weight",
                                 shape=(input_shape[-1], 1),
                                 initializer="normal")
        self.b = self.add_weight(name="att_bias",
                                 shape=(input_shape[1], 1),
                                 initializer="zeros")
        super(TimeAttentionLayer, self).build(input_shape)

    def call(self, x):
        e = tf.tanh(tf.tensordot(x, self.W, axes=1) + self.b)
        a = tf.nn.softmax(e, axis=1)
        output = x * a
        return tf.reduce_sum(output, axis=1)

    def get_config(self):
        config = super(TimeAttentionLayer, self).get_config()
        return config

class DataFusionModel:
    def __init__(self, sequence_length=30, n_features=3, nlp_dim=3, forecast_horizon=3):
        self.sequence_length = sequence_length
        self.n_features = n_features
        self.nlp_dim = nlp_dim
        self.forecast_horizon = forecast_horizon

    def build_model(self):
        ts_input = layers.Input(shape=(self.sequence_length, self.n_features), name="ts_input")
        x_ts = layers.LSTM(128, return_sequences=True)(ts_input)
        x_ts = layers.Dropout(0.3)(x_ts)
        x_ts = layers.LSTM(64, return_sequences=True)(x_ts)
        ts_attended = TimeAttentionLayer(name="time_attention")(x_ts)

        nlp_input = layers.Input(shape=(self.nlp_dim,), name="nlp_input")
        x_nlp = layers.Dense(32, activation='relu')(nlp_input)
        x_nlp = layers.BatchNormalization()(x_nlp)

        combined = layers.Concatenate()([ts_attended, x_nlp])
        x = layers.Dense(64, activation='relu')(combined)
        x = layers.Dropout(0.4)(x)
        
        output = layers.Dense(self.forecast_horizon, activation='linear', name="price_prediction")(x)

        model = Model(inputs=[ts_input, nlp_input], outputs=output)
        model.compile(optimizer='adam', loss=tf.keras.losses.Huber(), metrics=['mae'])
        return model