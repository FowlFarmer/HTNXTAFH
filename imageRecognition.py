import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

model_path = 'efficientdet_lite0.tflite'

BaseOptions = mp.tasks.BaseOptions
ObjectDetector = mp.tasks.vision.ObjectDetector
ObjectDetectorOptions = mp.tasks.vision.ObjectDetectorOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = ObjectDetectorOptions(
    base_options=BaseOptions(model_asset_path='efficientdet_lite0.tflite'),
    max_results=10,
    running_mode=VisionRunningMode.IMAGE)

with ObjectDetector.create_from_options(options) as detector:
    mp_image = mp.Image.create_from_file('Garden_strawberry_(Fragaria_×_ananassa)_single2.jpg')

    detection_result = detector.detect(mp_image)

    print(detection_result)
    


# # STEP 1: Import the necessary modules.
# import numpy as np
# import mediapipe as mp
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision

# # STEP 2: Create an ObjectDetector object.
# base_options = python.BaseOptions(model_asset_path='efficientdet.tflite')
# options = vision.ObjectDetectorOptions(base_options=base_options,
#                                        score_threshold=0.5)
# detector = vision.ObjectDetector.create_from_options(options)

# # STEP 3: Load the input image.
# image = mp.Image.create_from_file("Garden_strawberry_(Fragaria_×_ananassa)_single2.jpg")

# # STEP 4: Detect objects in the input image.
# detection_result = detector.detect(image)

# # STEP 5: Process the detection result. In this case, visualize it.
# image_copy = np.copy(image.numpy_view())
# annotated_image = visualize(image_copy, detection_result)
# rgb_annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
# cv2_imshow(rgb_annotated_image)