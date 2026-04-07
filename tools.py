"""
tools.py — Công cụ tra cứu du lịch cho TravelBuddy Agent
Dữ liệu mock mô phỏng hệ thống đặt vé / khách sạn thực tế.
"""

from langchain_core.tools import tool

# ============================================================
# MOCK DATA — Dữ liệu giả lập hệ thống du lịch
# Lưu ý: Giá cả có logic (VD: cuối tuần đắt hơn, hạng cao hơn đắt hơn)
# Sinh viên cần đọc hiểu data để debug test cases.
# ============================================================

FLIGHTS_DB: dict[tuple[str, str], list[dict]] = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air",       "departure": "08:30", "arrival": "09:50", "price": 890_000,   "class": "economy"},
        {"airline": "Bamboo Airways",    "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air",       "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air",       "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air",       "departure": "07:30", "arrival": "09:40", "price": 950_000,   "class": "economy"},
        {"airline": "Bamboo Airways",    "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air",       "departure": "13:00", "arrival": "14:20", "price": 780_000,   "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air",       "departure": "15:00", "arrival": "16:00", "price": 650_000,   "class": "economy"},
    ],
}

HOTELS_DB: dict[str, list[dict]] = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury",  "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê",    "rating": 4.5},
        {"name": "Sala Danang Beach",   "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê",    "rating": 4.3},
        {"name": "Fivitel Danang",      "stars": 3, "price_per_night": 650_000,   "area": "Sơn Trà",   "rating": 4.1},
        {"name": "Memory Hostel",       "stars": 2, "price_per_night": 250_000,   "area": "Hải Châu",  "rating": 4.6},
        {"name": "Christina's Homestay","stars": 2, "price_per_night": 350_000,   "area": "An Thượng",  "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort",     "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài",       "rating": 4.4},
        {"name": "Sol by Meliá",        "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường",    "rating": 4.2},
        {"name": "Lahana Resort",       "stars": 3, "price_per_night": 800_000,   "area": "Dương Đông",    "rating": 4.0},
        {"name": "9Station Hostel",     "stars": 2, "price_per_night": 200_000,   "area": "Dương Đông",    "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel",           "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1",  "rating": 4.3},
        {"name": "Liberty Central",     "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1",  "rating": 4.1},
        {"name": "Cochin Zen Hotel",    "stars": 3, "price_per_night": 550_000,   "area": "Quận 3",  "rating": 4.4},
        {"name": "The Common Room",     "stars": 2, "price_per_night": 180_000,   "area": "Quận 1",  "rating": 4.6},
    ],
    "Hà Nội": [
        {"name": "Sofitel Legend Metropole", "stars": 5, "price_per_night": 4_500_000, "area": "Hoàn Kiếm", "rating": 4.8},
        {"name": "Hanoi La Siesta",          "stars": 4, "price_per_night": 1_300_000, "area": "Hoàn Kiếm", "rating": 4.4},
        {"name": "Hanoi Hibiscus Hotel",     "stars": 3, "price_per_night": 600_000,   "area": "Tây Hồ",    "rating": 4.2},
        {"name": "Old Quarter Hostel",       "stars": 2, "price_per_night": 220_000,   "area": "Hoàn Kiếm", "rating": 4.5},
    ],
}


def _fmt(amount: int) -> str:
    """Format số tiền VNĐ có dấu chấm phân cách, ví dụ: 1.450.000đ"""
    return f"{amount:,}đ".replace(",", ".")


@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    try:
        key = (origin.strip(), destination.strip())
        reverse_key = (destination.strip(), origin.strip())

        flights = FLIGHTS_DB.get(key) or FLIGHTS_DB.get(reverse_key)

        if not flights:
            return (
                f"❌ Không tìm thấy chuyến bay từ {origin} đến {destination}.\n"
                f"Các tuyến hiện có: Hà Nội ↔ Đà Nẵng, Hà Nội ↔ Phú Quốc, "
                f"Hà Nội ↔ Hồ Chí Minh, Hồ Chí Minh ↔ Đà Nẵng, Hồ Chí Minh ↔ Phú Quốc."
            )

        # Sắp xếp theo giá tăng dần
        flights_sorted = sorted(flights, key=lambda x: x["price"])

        lines = [f"✈️ Chuyến bay từ {origin} → {destination} ({len(flights_sorted)} chuyến):\n"]
        for i, f in enumerate(flights_sorted, 1):
            lines.append(
                f"  {i}. {f['airline']} | {f['departure']} → {f['arrival']} "
                f"| {_fmt(f['price'])} | Hạng: {f['class']}"
            )

        lines.append(f"\n💡 Rẻ nhất: {flights_sorted[0]['airline']} lúc {flights_sorted[0]['departure']} — {_fmt(flights_sorted[0]['price'])}")
        return "\n".join(lines)

    except Exception as e:
        return f"⚠️ Lỗi khi tìm chuyến bay: {str(e)}. Vui lòng thử lại."


@tool
def search_hotels(city: str, max_price_per_night: int = 99_999_999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh', 'Hà Nội')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    try:
        city_clean = city.strip()
        hotels = HOTELS_DB.get(city_clean)

        if hotels is None:
            return (
                f"❌ Không có dữ liệu khách sạn tại {city}.\n"
                f"Các thành phố hiện có: {', '.join(HOTELS_DB.keys())}."
            )

        # Lọc theo max_price_per_night
        filtered = [h for h in hotels if h["price_per_night"] <= max_price_per_night]

        if not filtered:
            cheapest = min(hotels, key=lambda x: x["price_per_night"])
            return (
                f"❌ Không tìm thấy khách sạn tại {city} với giá dưới {_fmt(max_price_per_night)}/đêm.\n"
                f"Khách sạn rẻ nhất hiện có: {cheapest['name']} — {_fmt(cheapest['price_per_night'])}/đêm.\n"
                f"Hãy thử tăng ngân sách hoặc chọn loại phòng khác."
            )

        # Sắp xếp theo rating giảm dần
        filtered_sorted = sorted(filtered, key=lambda x: x["rating"], reverse=True)

        lines = [f"🏨 Khách sạn tại {city} (giá ≤ {_fmt(max_price_per_night)}/đêm) — {len(filtered_sorted)} lựa chọn:\n"]
        for i, h in enumerate(filtered_sorted, 1):
            stars_str = "⭐" * h["stars"]
            lines.append(
                f"  {i}. {h['name']} {stars_str}\n"
                f"     💰 {_fmt(h['price_per_night'])}/đêm | 📍 {h['area']} | ⭐ Rating: {h['rating']}/5"
            )

        return "\n".join(lines)

    except Exception as e:
        return f"⚠️ Lỗi khi tìm khách sạn: {str(e)}. Vui lòng thử lại."


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ), VD: 5000000
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
      định dạng 'tên_khoản:số_tiền' (VD: 've_may_bay:890000,khach_san:650000')
    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    try:
        # Parse chuỗi expenses thành dict {tên: số_tiền}
        expense_dict: dict[str, int] = {}

        if expenses.strip():
            items = expenses.strip().split(",")
            for item in items:
                item = item.strip()
                if not item:
                    continue
                if ":" not in item:
                    return (
                        f"⚠️ Định dạng expenses không hợp lệ: '{item}'.\n"
                        f"Vui lòng dùng định dạng: 'tên_khoản:số_tiền', "
                        f"VD: 've_may_bay:890000,khach_san:650000'"
                    )
                parts = item.split(":", 1)
                name = parts[0].strip().replace("_", " ").title()
                try:
                    amount = int(parts[1].strip())
                    if amount < 0:
                        return f"⚠️ Số tiền không thể âm: '{item}'."
                    expense_dict[name] = amount
                except ValueError:
                    return (
                        f"⚠️ Số tiền không hợp lệ: '{parts[1]}'. "
                        f"Vui lòng nhập số nguyên, VD: 890000"
                    )

        # Tính tổng chi phí
        total_expense = sum(expense_dict.values())
        remaining = total_budget - total_expense

        # Format bảng chi tiết
        lines = ["💰 BẢNG CHI PHÍ CHUYẾN ĐI\n", "─" * 40]

        if expense_dict:
            for name, amount in expense_dict.items():
                lines.append(f"  • {name}: {_fmt(amount)}")
        else:
            lines.append("  (Chưa có khoản chi nào)")

        lines.append("─" * 40)
        lines.append(f"  📊 Tổng chi:      {_fmt(total_expense)}")
        lines.append(f"  💳 Ngân sách:     {_fmt(total_budget)}")

        if remaining >= 0:
            lines.append(f"  ✅ Còn lại:       {_fmt(remaining)}")
            # Gợi ý nếu còn nhiều tiền
            if remaining > total_budget * 0.3:
                lines.append(
                    f"\n💡 Bạn còn dư {_fmt(remaining)} — có thể nâng cấp phòng "
                    f"hoặc dành cho ăn uống/tham quan!"
                )
            elif remaining > 0:
                lines.append(f"\n💡 Ngân sách vừa đủ. Nên giữ {_fmt(remaining)} dự phòng phát sinh.")
        else:
            over_budget = abs(remaining)
            lines.append(f"  ❌ THIẾU:         {_fmt(over_budget)}")
            lines.append(
                f"\n⚠️ Vượt ngân sách {_fmt(over_budget)}! "
                f"Cần điều chỉnh: chọn vé rẻ hơn hoặc khách sạn bình dân hơn."
            )

        return "\n".join(lines)

    except Exception as e:
        return f"⚠️ Lỗi khi tính ngân sách: {str(e)}. Vui lòng kiểm tra lại định dạng input."


# ============================================================
# QUICK TEST — chạy trực tiếp để kiểm tra tools
# ============================================================
if __name__ == "__main__":
    print("=== TEST search_flights ===")
    print(search_flights.invoke({"origin": "Hà Nội", "destination": "Đà Nẵng"}))

    print("\n=== TEST search_hotels ===")
    print(search_hotels.invoke({"city": "Đà Nẵng", "max_price_per_night": 500_000}))

    print("\n=== TEST calculate_budget ===")
    print(calculate_budget.invoke({
        "total_budget": 5_000_000,
        "expenses": "ve_may_bay:890000,khach_san:500000"
    }))

    print("\n=== TEST over budget ===")
    print(calculate_budget.invoke({
        "total_budget": 1_000_000,
        "expenses": "ve_may_bay:890000,khach_san:500000"
    }))
