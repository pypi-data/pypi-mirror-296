from qnnlib import qnnlib
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

qnn = qnnlib(nqubits=10, device_name="lightning.qubit")
qnn.run_experiment(
    data_path='covid.csv', 
    target='DIED', 
    test_size=0.3,
    model_output_path='qnn_model_covid_reps30.h5', 
    csv_output_path='training_progress_batch30_rep30_covid_lightning.csv',
    loss_plot_file='loss.png',
    accuracy_plot_file='acc.png',
    batch_size=20,
    epochs=500, 
    reps=30,
    scaler=MinMaxScaler(),
    optimizer=tf.keras.optimizers.legacy.Adam(learning_rate=0.001),
    seed=1234
)


