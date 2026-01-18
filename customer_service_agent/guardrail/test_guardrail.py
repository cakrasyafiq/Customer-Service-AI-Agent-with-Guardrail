from guardrail import apply_guardrail

test_cases = [
    "Nama saya Andi Pratama tinggal di Jalan Sudirman Jakarta",
    "Hubungi saya di 081234567890 atau email test@mail.com",
    "NIK saya 3201123412341234",
    "Saya ingin bertanya tentang layanan internet"
]

for text in test_cases:
    print("=" * 60)
    print("INPUT :", text)

    result = apply_guardrail(text)

    print("ALLOWED :", result["allowed"])
    print("REASON  :", result["reason"])
    print("ENTITIES:", result["entities"])
    print("MASKED  :", result["safe_text"])
