from app.ocr.mali_ocr import ocr_mali_french

# Put a Mali license image in backend/ and name it sample_mali.jpg
res = ocr_mali_french("sample_mali.jpg")

print(res.meta)
print(res.text[:1500])
