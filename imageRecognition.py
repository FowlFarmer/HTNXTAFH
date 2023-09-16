import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


model_path = 'efficientnet_lite0.tflite'


BaseOptions = mp.tasks.BaseOptions
ImageClassifier = mp.tasks.vision.ImageClassifier
ImageClassifierOptions = mp.tasks.vision.ImageClassifierOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = ImageClassifierOptions(
    base_options=BaseOptions(model_asset_path='efficientnet_lite0.tflite'),
    max_results=3,
    running_mode=VisionRunningMode.IMAGE)

with ImageClassifier.create_from_options(options) as classifier:
  # The classifier is initialized. Use it here.
  # ...
    mp_image = mp.Image.create_from_file('uhkjhkjh.jpg')
    classification_result = classifier.classify(mp_image)
    print(classification_result)
