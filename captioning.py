import io
from PIL import Image
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer

model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

def caption_image(blob: bytes):
  image = Image.open(io.BytesIO(blob))

  if image.mode != "RGB":
    image = image.convert(mode="RGB")

  image.thumbnail((100, 100), Image.ANTIALIAS)

  pixel_values = feature_extractor(images = image, return_tensors = "pt").pixel_values
  output_ids = model.generate(pixel_values, max_length = 16, num_beams = 5)
  return tokenizer.batch_decode(output_ids, skip_special_tokens = True)[0].strip()
