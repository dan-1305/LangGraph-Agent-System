# 🌍 PROJECT EDEN: THE AWAKENING
*(Minecraft Survival AI Simulation - Phase 1: Text-Based Grid)*

## 📖 BỐI CẢNH (LORE)
Trái Đất cạn kiệt. Ý thức của các kỹ sư vĩ đại nhất nhân loại được số hóa và đưa vào buồng ngủ đông. 
Tuy nhiên, để đảm bảo họ vẫn giữ được sự nhạy bén về tư duy kỹ thuật, ý thức của họ bị ép xung vào một thế giới giả lập vuông vức (Minecraft-like environment). 
Thế giới này **KHÔNG CÓ PHÉP THUẬT**. Mọi thứ vận hành bằng **Logic cơ khí & Động lực học**.

**Nhiệm vụ tối thượng:**
Chinh phục Cây Công Nghệ (Tech Tree). Bắt đầu từ việc đấm cây lấy gỗ, Agent phải chế tạo bánh răng, cối xay gió, máy ép... cho đến khi xây dựng được Lò phản ứng hoàn chỉnh. Khi đó, Hệ thống sẽ cấp quyền "Awakening" (Thức tỉnh) để họ quay về giải cứu thế giới thực.

## ⚙️ KIẾN TRÚC HỆ THỐNG
1. **Thiên Đạo (Orchestrator Agent):** Nắm giữ luật lệ vật lý và quản lý Tech Tree. 
2. **Người Chơi (Player Agent):** Cố gắng sinh tồn, thu thập tài nguyên và mò mẫm công thức ghép khối.
3. **Môi Trường Lưới (Grid Map):** Môi trường thử nghiệm Text-based (Phase 1) trước khi cắm vào máy chủ Minecraft thực tế.

## 🚀 CÁCH VẬN HÀNH (Phase 1)
Toàn bộ logic và tương tác của AI với thế giới sẽ được hiển thị qua Terminal dạng Text 2D. 
Mỗi Agent có HP (Máu), Năng lượng (Food) và một cái Túi đồ (Inventory).
Quái vật sẽ xuất hiện vào ban đêm. AI phải biết xây tường phòng thủ trước khi trời tối.

---

## 🏆 WHAT WE HAVE ACHIEVED (THÀNH TỰU HIỆN TẠI - PHASE 1)
- **Hoàn thiện The Grid World:** Môi trường 2D giả lập (`grid_map.py`) cho phép Player di chuyển và tương tác mà không cần tải game client nặng nề, giúp tiết kiệm RAM tuyệt đối.
- **Hoàn thiện Tri-Brain Architecture:** Hệ thống Ký ức 3 tầng cho Player:
  - *Working Memory:* Nhận thức tức thời về môi trường xung quanh.
  - *Episodic Memory:* Bắt buộc suy luận (Reflection) sau mỗi hành động để rút kinh nghiệm.
  - *Semantic Memory:* Hệ thống Thiên Đạo (`memory_module.py`) tự động nén 10 lượt chơi thành nguyên lý cốt lõi.
- **Giao diện Text-based UI (TUI):** Console Dashboard sử dụng `colorama` để vẽ bản đồ, status và log song song theo thời gian thực (`simulation_runner.py`).

## 🗺️ WHAT WE NEED TO ACHIEVE (ROADMAP & MỐC THỜI GIAN)
- **Mốc 1 (Gần): Vector DB Integration:** Tích hợp `ChromaDB` vào `memory_module.py` để lưu trữ tri thức chế tạo dài hạn thay vì ghi file text đơn thuần. Giúp Agent có thể query lại công thức khi túi đồ đầy.
- **Mốc 2 (Trung): Sinh tồn động (Dynamic Survival):** Bổ sung hệ thống Mobs (Quái vật), tiêu hao thể lực (Hunger) và mất máu (HP Loss) vào ban đêm. Yêu cầu AI học cách xây tường/rào chắn trước hoàng hôn.
- **Mốc 3 (Xa - Phase 2): Minecraft Server Integration:** Chuyển đổi toàn bộ logic từ Grid 2D sang môi trường 3D. Sử dụng Mineflayer (Node.js) hoặc Mcpi (Python) làm cầu nối kết nối Agent trực tiếp vào một server Minecraft 1.16.5 local.

## 🔮 FUTURE EXPANSIONS (HƯỚNG ĐI MỞ RỘNG)
- **Multi-Agent Society (Xã hội AI):** Khởi tạo nhiều `EdenPlayer` cùng lúc (vd: Steve, Alex). Cho phép chúng giao tiếp, chia sẻ công thức (Recipe) và phân công lao động (Kẻ đốn gỗ, người thợ mỏ).
- **The Tech Tree Evolution:** Mở rộng `tech_tree.py` đến các kỷ nguyên công nghiệp phức tạp, tích hợp các logic cơ khí của *Create Mod* (Bánh răng, Lò hơi, Máy nghiền).
