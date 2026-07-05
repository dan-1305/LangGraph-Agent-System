# 🪂 Báo Cáo Kiến Trúc & Khả Năng Mở Rộng: Airdrop Guerrilla

**Thời gian xuất báo cáo:** Mới nhất
**Mục tiêu:** Phân tích cấu trúc hệ thống tự động hóa săn Airdrop, quản lý ví và khả năng mở rộng lên các mạng lưới On-chain Testnet mới (Monad, Soneium, Inco).

---

## 1. Cơ chế Quản lý & Giải mã Ví (WalletManager)

Hệ thống quản lý ví của Airdrop Guerrilla đang làm rất tốt vai trò bảo mật và chống tấn công mạo danh (Anti-Sybil). Cụ thể tại `src/automation/wallet_manager.py`:

*   **Bảo mật cấp độ cao (AES-128 Encryption):** 
    Sử dụng thư viện `cryptography.fernet.Fernet`. Tất cả thông tin nhạy cảm bao gồm Private Key (PK), Token xác thực Twitter (X), và Token Discord đều được mã hóa trước khi ghi xuống file cơ sở dữ liệu `secure_wallets.json`.
*   **Quản lý Master Key:** 
    Khóa giải mã (`WALLET_MASTER_KEY`) được lưu trữ ngoài luồng mã nguồn (thông qua `.env`), ngăn chặn nguy cơ rò rỉ khi đẩy code lên Git. Nếu không tìm thấy, hệ thống sẽ yêu cầu người dùng nhập tay hoặc tự sinh key mới.
*   **Stealth User-Agent (Anti-Sybil tĩnh):**
    Đây là một điểm sáng giá. Hàm `generate_static_user_agent()` băm địa chỉ ví bằng MD5 để làm hạt giống (seed) cho bộ sinh số ngẫu nhiên (`random.seed`). Cơ chế này đảm bảo mỗi ví luôn gắn liền với một "vân tay trình duyệt" (User-Agent) cố định từ lúc tạo đến vĩnh viễn, đánh lừa hệ thống của Twitter và Galxe rằng đây là một người dùng thật luôn xài một thiết bị.

---

## 2. Cấu trúc hàm thực thi Playwright (Executor)

Hàm thực thi Playwright hiện tại (`src/automation/executor.py`) là trái tim của luồng làm nhiệm vụ mạng xã hội:

*   **Cơ chế Action Plan:** Bot hoạt động dựa trên file JSON kế hoạch (`action_plan`), linh hoạt duyệt qua từng nhiệm vụ của từng nền tảng (Twitter, Discord, Faucet).
*   **Session Persistence (Duy trì phiên đăng nhập):** 
    Tránh tình trạng đăng nhập đi đăng nhập lại dễ bị checkpoint. Hệ thống nạp thẳng Cookie/Local Storage từ file session (hoặc tiêm Token thông qua `SessionManager` ở lần chạy đầu tiên).
*   **Xử lý Ngoại lệ & Cảnh báo Timeout:** 
    Vì Playwright dễ bị nghẽn (do mạng hoặc do bị Cloudflare chặn), khi gặp `PlaywrightTimeoutError`, hệ thống sẽ đóng ngay trình duyệt để giải phóng RAM cho CPU (i3) và lập tức gửi thông báo khẩn cấp (Alert) qua Telegram (`TelegramNotifier`) báo tên ví và bước bị kẹt.
*   **Captcha Solver:** Có tích hợp API từ dịch vụ trung gian (2Captcha) để giải các rào cản reCAPTCHA truyền thống trên Faucet.

---

## 3. Đánh giá Kiến trúc mới: Mở rộng sang On-chain thuần RPC

Việc bổ sung luồng tương tác on-chain thuần RPC (không dùng Playwright) cho 3 mạng Testnet: **Monad**, **Soneium**, và **Inco** là một bước tiến vượt bậc, giảm tải cho phần cứng và mở ra hai trường phái rõ ràng.

### Sự Phân tách Luồng (Execution Modes)
Tại thư mục `src/modes/`, dự án đã được chia làm 2 chiến lược:
1.  **Luồng `full_auto_cli.py` (On-chain Bot):**
    *   *Cơ chế:* Chạy ngầm 100% bằng giao diện dòng lệnh thông qua `web3.py`.
    *   *Hiệu suất:* Tốc độ ánh sáng, tốn cực ít RAM vì không phải load nhân Chromium. Thích hợp để cày cuốc số lượng Transaction và Volume lớn mỗi ngày một cách âm thầm.
2.  **Luồng `semi_auto_ui.py` (Human-in-the-loop):**
    *   *Cơ chế:* Mở trình duyệt có giao diện (`headless=False`) để giải quyết các hệ thống Anti-bot mạnh (Zealy, Galxe, hoặc Cloudflare Turnstile). Khi bị kẹt, bot sẽ phát âm thanh báo động (Beep) và chờ Admin (người thật) vào bấm xác thực trước khi tự động chạy tiếp.

### Lớp nền tảng On-chain (`src/networks/`)
Hệ thống sử dụng Kế thừa Hướng đối tượng (OOP) cực kỳ gọn gàng:
*   **Class `EVMBase` (`evm_base.py`):** Xử lý mọi thao tác chung của Web3 như nối RPC (có inject PoA middleware), lấy số dư, tính toán Gas fee, gửi giao dịch (gửi Native Token) và đặc biệt là **Tự động Deploy Smart Contract** rỗng (Dummy Contract). Tính năng Deploy này giúp ví được gắn mác "Developer Wallet" cực kỳ uy tín cho các kỳ Airdrop.
*   **Tích hợp Testnet Mục tiêu:**
    1.  `monad.py` (Chain ID 10143): Hỗ trợ farm trên Monad - Layer 1 EVM song song.
    2.  `soneium.py` (Chain ID 1946): Hỗ trợ farm Soneium Minato Testnet (Layer 2 của Sony).
    3.  `inco.py` (Chain ID 9090): Hỗ trợ farm trên nền tảng Fully Homomorphic Encryption (FHE) của Inco Network.

### Đánh giá khả năng Mở rộng (Scalability)
**Điểm 10/10.** Với cấu trúc `EVMBase` hiện tại, nếu tương lai có thêm một Testnet mới (ví dụ: *Berachain* hay *Linea*), kỹ sư chỉ cần tạo một file Python mới kế thừa `EVMBase`, đổi 2 biến số là `rpc_url` và `chain_id` là có thể farm ngay lập tức mà không cần viết lại logic gửi giao dịch hay Deploy Contract.

---
*Báo cáo được khởi tạo tự động bởi Hệ thống LangGraph Agent System V2.*