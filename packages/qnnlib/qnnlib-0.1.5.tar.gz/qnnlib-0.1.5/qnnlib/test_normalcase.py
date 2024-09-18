from qnnlib import qnnlib
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

qnn = qnnlib(nqubits=4, device_name="qiskit.aer")
qnn.run_experiment(
    data_path='diabetes.csv', 
    target='Outcome', 
    test_size=0.3,
    model_output_path='qnn_model_diabetes_reps_1.h5', 
    csv_output_path='training_progress_batch20_rep1_diabetes_lightning.csv',
    loss_plot_file='loss.png',
    accuracy_plot_file='acc.png',
    batch_size=20,
    epochs=500, 
    reps=10,
    scaler=MinMaxScaler(),
    optimizer=tf.keras.optimizers.legacy.Adam(learning_rate=0.001),
    seed=1234
)


