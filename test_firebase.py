from firebase_client import upload_detection

print("=" * 50)
print("PRANSTHAMBH FIREBASE TEST")
print("=" * 50)

result = upload_detection(
    class_name="Leopard",
    confidence=0.947,
    pole_id="POLE_001",
    image_path="alerts/test.jpg"
)

if result:
    print()
    print("SUCCESS!")
    print("Data successfully sent to Firebase.")
else:
    print()
    print("FAILED!")
    print("Check Firebase configuration.")