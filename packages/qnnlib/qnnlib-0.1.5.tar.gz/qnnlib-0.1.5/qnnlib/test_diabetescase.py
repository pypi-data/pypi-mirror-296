from qnnlib import qnnlib
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

qnn = qnnlib(nqubits=8, device_name="lightning.qubit")
qnn.run_experiment(
    data_path='diabetes.csv', 
    target='Outcome', 
    test_size=0.3,
    model_output_path='qnn_model2.h5', 
    csv_output_path='training_progress_batch30_diabetes_lightning_rep256_learning0_001.csv',
    loss_plot_file='loss.png',
    accuracy_plot_file='acc.png',
    batch_size=30,
    epochs=100,
    reps=10,
    scaler=MinMaxScaler(),
    optimizer=tf.keras.optimizers.legacy.Adam(learning_rate=0.001),
    seed=1234
)


