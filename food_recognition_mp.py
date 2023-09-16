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
    max_results=1,
    running_mode=VisionRunningMode.IMAGE)

def recognise_food(imagePath):
  with ImageClassifier.create_from_options(options) as classifier:
    # The classifier is initialized. Use it here.
      mp_image = mp.Image.create_from_file(imagePath)
      classification_result = classifier.classify(mp_image)
      # the first 0 is since we are only doing one classificaiton at a time, and the second is to get the first result
      top_answer = classification_result.classifications[0].categories[0].category_name
      return top_answer

if __name__ == "__main__":
   print(recognise_food("test.jpg"))