import keras
import tensorflow as tf


def train_model(
        model: keras.Model,
        train_ds: tf.data.Dataset,
        epochs: int,
        verbose=0,
) -> keras.Model:
    model.compile(
        optimizer=keras.optimizers.Adam(),
        loss={
            "figure": keras.losses.SparseCategoricalCrossentropy(),
            "direction": keras.losses.SparseCategoricalCrossentropy(),
        },
        metrics={
            "figure": ["accuracy"],
            "direction": ["accuracy"],
        }
    )

    model.fit(
        train_ds,
        epochs=epochs,
        verbose=verbose,
    )

    return model
