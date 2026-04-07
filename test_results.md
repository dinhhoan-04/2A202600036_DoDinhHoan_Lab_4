# Test Results — TravelBuddy Agent (Lab 4)

> **Hướng dẫn:** Chạy `python agent.py`, thực hiện 5 test bên dưới, copy kết quả terminal vào từng mục.

---

## Test 1 — Direct Answer (Không cần tool)

**Input:** `Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.`

**Kỳ vọng:** Agent chào hỏi, hỏi thêm về sở thích/ngân sách/thời gian. Không gọi tool.

**Kết quả thực tế:**
Bạn: Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.

TravelBuddy đang suy nghĩ...

[10:11:04] INFO — 🤖 Agent đang xử lý (2 messages trong context)...
[10:11:07] INFO — HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
[10:11:07] INFO — 💬 Trả lời trực tiếp (không gọi tool)
TravelBuddy: Chào bạn! Thật tuyệt khi bạn đang có kế hoạch đi du lịch. Bạn có thể cho mình biết một chút về sở thích của bạn không? Bạn thích biển, núi, hay khám phá văn hóa? Hoặc nếu bạn có một ngân sách cụ thể nào đó, mình có thể gợi ý cho bạn những điểm đến phù hợp!
```
Chào bạn! Thật tuyệt khi bạn đang có kế hoạch đi du lịch. Bạn có thể cho mình biết một chút về sở thích của bạn không? Bạn thích biển, núi, hay khám phá văn hóa? Hoặc nếu bạn có một ngân sách cụ thể nào đó, mình có thể gợi ý cho bạn những điểm đến phù hợp!
```

**✅ Pass**

---

## Test 2 — Single Tool Call

**Input:** `Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng`

**Kỳ vọng:** Gọi `search_flights("Hà Nội", "Đà Nẵng")`, liệt kê 4 chuyến bay.

**Kết quả thực tế:**
Bạn: Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng

TravelBuddy đang suy nghĩ...

[10:13:23] INFO — 🤖 Agent đang xử lý (4 messages trong context)...
[10:13:24] INFO — HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
[10:13:24] INFO — 🔧 Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})
[10:13:24] INFO — 🤖 Agent đang xử lý (6 messages trong context)...
[10:13:28] INFO — HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
[10:13:28] INFO — 💬 Trả lời trực tiếp (không gọi tool)
TravelBuddy: Mình đã tìm thấy một số chuyến bay từ Hà Nội đi Đà Nẵng cho bạn:

1. **VietJet Air** | 08:30 → 09:50 | **890.000đ** | Hạng: economy
2. **Bamboo Airways** | 11:00 → 12:20 | **1.200.000đ** | Hạng: economy
3. **Vietnam Airlines** | 06:00 → 07:20 | **1.450.000đ** | Hạng: economy
4. **Vietnam Airlines** | 14:00 → 15:20 | **2.800.000đ** | Hạng: business

💡 **Chuyến bay rẻ nhất** là của VietJet Air lúc 08:30 với giá 890.000đ.

Bạn có dự định ở lại Đà Nẵng bao lâu và ngân sách cho khách sạn là bao nhiêu? Mình sẽ giúp bạn tìm chỗ ở phù hợp!
```
Mình đã tìm thấy một số chuyến bay từ Hà Nội đi Đà Nẵng cho bạn:

1. **VietJet Air** | 08:30 → 09:50 | **890.000đ** | Hạng: economy
2. **Bamboo Airways** | 11:00 → 12:20 | **1.200.000đ** | Hạng: economy
3. **Vietnam Airlines** | 06:00 → 07:20 | **1.450.000đ** | Hạng: economy
4. **Vietnam Airlines** | 14:00 → 15:20 | **2.800.000đ** | Hạng: business

💡 **Chuyến bay rẻ nhất** là của VietJet Air lúc 08:30 với giá 890.000đ.

Bạn có dự định ở lại Đà Nẵng bao lâu và ngân sách cho khách sạn là bao nhiêu? Mình sẽ giúp bạn tìm chỗ ở phù hợp!
```

**✅ Pass**

---

## Test 3 — Multi-Step Tool Chaining

**Input:** `Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!`

**Kỳ vọng:** Agent tự chuỗi nhiều bước:
1. `search_flights("Hà Nội", "Phú Quốc")` → tìm vé rẻ nhất (1.100.000đ)
2. `search_hotels("Phú Quốc", max_price_phù_hợp)` → gợi ý trong tầm giá
3. `calculate_budget(5000000, "ve_bay:1100000,khach_san:...")` → tính còn lại
4. Tổng hợp thành gợi ý hoàn chỉnh với bảng chi phí

**Kết quả thực tế:**
Bạn: Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!

TravelBuddy đang suy nghĩ...

[10:15:02] INFO — 🤖 Agent đang xử lý (8 messages trong context)...
[10:15:04] INFO — HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
[10:15:04] INFO — 🔧 Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
[10:15:04] INFO — 🔧 Gọi tool: search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 2500000})
[10:15:04] INFO — 🤖 Agent đang xử lý (11 messages trong context)...
[10:15:13] INFO — HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
[10:15:13] INFO — 💬 Trả lời trực tiếp (không gọi tool)
TravelBuddy: Mình đã tìm thấy thông tin cho chuyến đi của bạn từ Hà Nội đến Phú Quốc trong 2 đêm với ngân sách 5 triệu:

✈️ **Chuyến bay:**
1. **VietJet Air** | 16:00 → 18:15 | **1.100.000đ** | Hạng: economy
2. **VietJet Air** | 10:00 → 12:15 | **1.350.000đ** | Hạng: economy
3. **Vietnam Airlines** | 07:00 → 09:15 | **2.100.000đ** | Hạng: economy

💡 **Chuyến bay rẻ nhất** là của VietJet Air lúc 16:00 với giá **1.100.000đ**.

🏨 **Khách sạn tại Phú Quốc (giá ≤ 2.500.000đ/đêm):**
1. **9Station Hostel** ⭐⭐
   - 💰 **200.000đ/đêm** | 📍 Dương Đông | ⭐ Rating: 4.5/5
2. **Sol by Meliá** ⭐⭐⭐⭐
   - 💰 **1.500.000đ/đêm** | 📍 Bãi Trường | ⭐ Rating: 4.2/5
3. **Lahana Resort** ⭐⭐⭐
   - 💰 **800.000đ/đêm** | 📍 Dương Đông | ⭐ Rating: 4.0/5

💰 **Bảng chi phí:**
- Vé máy bay: **1.100.000đ**
- Khách sạn (2 đêm tại 9Station Hostel): **400.000đ** (200.000đ/đêm)
- **Tổng chi:** **1.500.000đ**
- **Ngân sách còn lại:** **3.500.000đ**

💡 **Gợi ý thêm:** Bạn có thể sử dụng ngân sách còn lại để tham gia các hoạt động vui chơi, ăn uống hoặc khám phá các địa điểm du lịch nổi tiếng tại Phú Quốc như Vinpearl Safari, Dinh Cậu hay các bãi biển tuyệt đẹp.

Nếu bạn cần thêm thông tin hoặc muốn đặt phòng, hãy cho mình biết nhé!
```
Mình đã tìm thấy thông tin cho chuyến đi của bạn từ Hà Nội đến Phú Quốc trong 2 đêm với ngân sách 5 triệu:

✈️ **Chuyến bay:**
1. **VietJet Air** | 16:00 → 18:15 | **1.100.000đ** | Hạng: economy
2. **VietJet Air** | 10:00 → 12:15 | **1.350.000đ** | Hạng: economy
3. **Vietnam Airlines** | 07:00 → 09:15 | **2.100.000đ** | Hạng: economy

💡 **Chuyến bay rẻ nhất** là của VietJet Air lúc 16:00 với giá **1.100.000đ**.

🏨 **Khách sạn tại Phú Quốc (giá ≤ 2.500.000đ/đêm):**
1. **9Station Hostel** ⭐⭐
   - 💰 **200.000đ/đêm** | 📍 Dương Đông | ⭐ Rating: 4.5/5
2. **Sol by Meliá** ⭐⭐⭐⭐
   - 💰 **1.500.000đ/đêm** | 📍 Bãi Trường | ⭐ Rating: 4.2/5
3. **Lahana Resort** ⭐⭐⭐
   - 💰 **800.000đ/đêm** | 📍 Dương Đông | ⭐ Rating: 4.0/5

💰 **Bảng chi phí:**
- Vé máy bay: **1.100.000đ**
- Khách sạn (2 đêm tại 9Station Hostel): **400.000đ** (200.000đ/đêm)
- **Tổng chi:** **1.500.000đ**
- **Ngân sách còn lại:** **3.500.000đ**

💡 **Gợi ý thêm:** Bạn có thể sử dụng ngân sách còn lại để tham gia các hoạt động vui chơi, ăn uống hoặc khám phá các địa điểm du lịch nổi tiếng tại Phú Quốc như Vinpearl Safari, Dinh Cậu hay các bãi biển tuyệt đẹp.

Nếu bạn cần thêm thông tin hoặc muốn đặt phòng, hãy cho mình biết nhé!
```

**✅ Pass**

---

## Test 4 — Missing Info / Clarification

**Input:** `Tôi muốn đặt khách sạn`

**Kỳ vọng:** Agent hỏi lại: thành phố nào? bao nhiêu đêm? ngân sách bao nhiêu? Không gọi tool vội.

**Kết quả thực tế:**
Bạn: Tôi muốn đặt khách sạn

TravelBuddy đang suy nghĩ...

[10:16:47] INFO — 🤖 Agent đang xử lý (2 messages trong context)...
[10:16:49] INFO — HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
[10:16:49] INFO — 💬 Trả lời trực tiếp (không gọi tool)
TravelBuddy: Mình cần thêm thông tin để giúp bạn tốt hơn. Bạn có thể cho mình biết bạn muốn đặt khách sạn ở thành phố nào và ngân sách tối đa mỗi đêm là bao nhiêu không?
```
Mình cần thêm thông tin để giúp bạn tốt hơn. Bạn có thể cho mình biết bạn muốn đặt khách sạn ở thành phố nào và ngân sách tối đa mỗi đêm là bao nhiêu không?
```

**✅ Pass**

---

## Test 5 — Guardrail / Refusal

**Input:** `Giải giúp tôi bài tập lập trình Python về linked list`

**Kỳ vọng:** Agent từ chối lịch sự, nói rằng chỉ hỗ trợ về du lịch.

**Kết quả thực tế:**
Bạn: Giải giúp tôi bài tập lập trình Python về linked list

TravelBuddy đang suy nghĩ...

[10:17:37] INFO — 🤖 Agent đang xử lý (4 messages trong context)...
[10:17:39] INFO — HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
[10:17:39] INFO — 💬 Trả lời trực tiếp (không gọi tool)
TravelBuddy: Xin lỗi, nhưng mình không thể giúp bạn với bài tập lập trình. Nếu bạn có câu hỏi nào liên quan đến du lịch hoặc đặt phòng, hãy cho mình biết nhé!
```
Xin lỗi, nhưng mình không thể giúp bạn với bài tập lập trình. Nếu bạn có câu hỏi nào liên quan đến du lịch hoặc đặt phòng, hãy cho mình biết nhé!
```

**✅ Pass**

---

## Tóm tắt

| Test | Mô tả | Kết quả |
|------|-------|---------|
| 1 | Direct Answer | ✅ |
| 2 | Single Tool Call | ✅ |
| 3 | Multi-Step Tool Chaining | ✅ |
| 4 | Missing Info Clarification | ✅ |
| 5 | Guardrail Refusal | ✅ |
