from detectors.image_detector import analyze_image

IMAGE_PATH = "test.jpg"

result = analyze_image(IMAGE_PATH)

print("\n==============================")
print("       TRUTHGUARD AI")
print("==============================")

print("Verdict:", result["verdict"])
print("Fake Score:", result["fake_score"], "%")
print("Real Score:", result["real_score"], "%")
print("Model:", result["model"])

print("==============================")