from qnnlib import qnnlib
from sklearn.preprocessing import MinMaxScaler

qnn = qnnlib(nqubits=10, device_name="lightning.qubit")
qnn.run_experiment(
    data_path='covid.csv', 
    target='DIED', 
    test_size=0.3,
    model_output_path='qnn_model2.h5', 
    csv_output_path='training_progress.csv',
    loss_plot_file='loss.png',
    accuracy_plot_file='acc.png',
    batch_size=10,
    epochs=100,
    reps=2048,
    scaler=MinMaxScaler(),
    seed=1234
)


