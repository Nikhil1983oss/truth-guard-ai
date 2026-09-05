from PIL import Image
import torch
from transformers import AutoImageProcessor, SiglipForImageClassification


MODEL_NAME = "prithivMLmods/deepfake-detector-model-v1"

print("Loading TruthGuard image model...")

processor = AutoImageProcessor.from_pretrained(MODEL_NAME)

model = SiglipForImageClassification.from_pretrained(
    MODEL_NAME
)

model.eval()

print("TruthGuard image model loaded.")


def analyze_image(image_path: str):

    image = Image.open(image_path).convert("RGB")

    inputs = processor(
        images=image,
        return_tensors="pt"
    )

    with torch.no_grad():

        outputs = model(**inputs)

        probabilities = torch.softmax(
            outputs.logits,
            dim=1
        )[0]

    fake_score = float(probabilities[0])
    real_score = float(probabilities[1])

    if fake_score >= real_score:
        verdict = "LIKELY_MANIPULATED"
    else:
        verdict = "LIKELY_AUTHENTIC"

    return {
        "verdict": verdict,
        "fake_score": round(fake_score * 100, 2),
        "real_score": round(real_score * 100, 2),
        "model": MODEL_NAME
    }