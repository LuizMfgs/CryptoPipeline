from app.Load import remove_old_data

tests = [0, -1, -7]

for days in tests:
    try:
        remove_old_data(days)
        print(f"❌ FAIL: {days} deveria ter gerado ValueError")
    except ValueError as e:
        print(f"✅ PASS: {days} -> {e}")