import matplotlib.pylab as plt
import numpy as np
from _230104_utils import *  # most of the functionality is here


if __name__ == "__main__":
	## New model every iteration
	reference_iteration = 1
	reference_checkpoint = 1


	train_ds, val_ds = prepare_datasets_from_dir("./Rice_Image_Dataset")
	class_names = train_ds.class_names

	model = prepare_new_model( IMAGE_SIZE, len(class_names) )

	model.load_weights(f'training_checkpoints_{reference_iteration}/ckpt_{reference_checkpoint}')

	model.evaluate(val_ds.data)


	# Which grains of rice are NOT being identified correctly?
	found_transgressor = False
	val_ds_iterator = iter(val_ds.data)

	while not found_transgressor:  # Find the first incorrect inference and break
		x, y = next(val_ds_iterator)
		image = x[0, :, :, :]

		# Expand validation image dimensions to (1, 224, 224, 3) before predicting the label
		prediction_scores = model.predict(np.expand_dims(image, axis=0))
		predicted_index = np.argmax(prediction_scores)
		true_index = np.argmax(y[0])
		
		if class_names[true_index] == class_names[predicted_index]:
			continue
		
		print("True label: " + class_names[true_index])
		print("Predicted label: " + class_names[predicted_index])
		
		plt.imshow(image)
		plt.axis('off')
		plt.savefig('./the_transgressor.png')
		plt.show()
		
		break

