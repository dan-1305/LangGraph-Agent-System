# 📊 BÁO CÁO BENCHMARK API (Gemini vs Groq vs OpenRouter)

Báo cáo được tạo tự động bởi hệ thống đo lường AI.

## 1. Tốc độ & Độ trễ (Streaming)
| Model | Provider | TTFT (s) | Total Time (s) | Tokens Sinh Ra | Tốc độ (Tokens/s) | Trạng thái |
|---|---|---|---|---|---|---|
| Gemini 2.5 Flash | Google | 6.549s | 9.85s | ~2634 | **267.5 tps** | ✅ |
| Gemini 3.1 Flash Lite | Google | 0.897s | 3.02s | ~4292 | **1419.4 tps** | ✅ |
| Groq Llama-3.1-8b | Groq | 0.324s | 1.72s | ~54474 | **31593.6 tps** | ✅ |
| Groq Llama-3.3-70b | Groq | 0.294s | 2.15s | ~43357 | **20186.5 tps** | ✅ |
| OpenRouter Gemini 2.5 | OpenRouter | - | - | - | - | ❌ Lỗi: HTTP 402: {"error":{"message":"This request requires more credits, or fewer max_tokens. You requested up to 65 |

## 2. Thử nghiệm Ép tải (Burst Rate Limit - 15 reqs/s)
| Model | Số Lượng Test | Thành công (200) | Bị chặn (429) | Lỗi khác |
|---|---|---|---|---|
| Gemini 2.5 Flash | 15 | 5 | **10** | 0 |
| Gemini 3.1 Flash Lite | 15 | 15 | **0** | 0 |
| Groq Llama-3.1-8b | 15 | 15 | **0** | 0 |
| Groq Llama-3.3-70b | 15 | 15 | **0** | 0 |
| OpenRouter Gemini 2.5 | 15 | 0 | **0** | 15 |

## 3. Kết luận & Khuyến nghị
- **Groq Llama-3.1-8b**: Chạy nhanh như một cơn gió (chữ nhảy tức thì). Thích hợp cho Parsing/Extraction.
- **Groq Llama-3.3-70b**: Rất thông minh và tốc độ vẫn cực khủng khiếp. Dùng làm Fallback chính khi hệ thống mất API.
- **Gemini (Google Native)**: Rất ổn định. Tuy nhiên nếu request ồ ạt sẽ dễ dính 429 nếu không dùng Proxy.
- **OpenRouter Gemini**: Trễ TTFT hơn so với gọi trực tiếp Google (do qua trạm trung chuyển), nhưng Limit thoải mái hơn.
