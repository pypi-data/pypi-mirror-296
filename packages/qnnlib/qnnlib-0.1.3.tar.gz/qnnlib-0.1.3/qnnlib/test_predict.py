from qnnlib import qnnlib
import numpy as np

qnn = qnnlib(nqubits=8, device_name="lightning.qubit")
qnn.load_pretrained_qnn(model_file="qnn_model2.h5", nqubits=8, reps=30 )

sample_input = np.array([[10, 1, 4, 3, 5,6,1,2]])

result = qnn.predict(sample_input)

print (result)

