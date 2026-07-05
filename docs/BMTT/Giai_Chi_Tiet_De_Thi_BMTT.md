# GIẢI CHI TIẾT ĐỀ ÔN TẬP AN TOÀN BẢO MẬT THÔNG TIN

*(Tài liệu này được biên soạn dựa trên giáo trình nội bộ. Phù hợp làm tài liệu cho sinh viên ôn tập và Giảng viên làm Bareme chấm điểm.)*

---

## 🟢 PHẦN 1: BÀI TẬP TÍNH TOÁN

**Quy ước chung:** Mọi bài toán mã hóa chữ cái tiếng Anh được ánh xạ sang tập $Z_{26} = \{0, 1, ..., 25\}$ với:
`A=0, B=1, C=2, D=3, E=4, F=5, G=6, H=7, I=8, J=9, K=10, L=11, M=12, N=13, O=14, P=15, Q=16, R=17, S=18, T=19, U=20, V=21, W=22, X=23, Y=24, Z=25`.

---

### Câu 1: Sử dụng Mã Affine giải mã bản mã sau: "rmpjvpwtwtmhgmpwtgfwgkzn" với từ khóa a = 19, b = 23

**1. Cơ sở lý thuyết và công thức giải mã:**
*   Hàm mã hóa Affine: $C = E(P) = (a \cdot P + b) \pmod{26}$
*   Hàm giải mã Affine: $P = D(C) = a^{-1} \cdot (C - b) \pmod{26}$
*   Với: $a = 19, b = 23$.

**2. Tìm phần tử nghịch đảo $a^{-1} \pmod{26}$:**
*   Ta cần tìm $a^{-1}$ sao cho $19 \cdot a^{-1} \equiv 1 \pmod{26}$.
*   Sử dụng thuật toán Euclide mở rộng hoặc thử chọn: $19 \cdot 11 = 209 = 26 \cdot 8 + 1 \Rightarrow 19 \cdot 11 \equiv 1 \pmod{26}$.
*   Vậy $a^{-1} = 11$.

**3. Thiết lập công thức giải mã cụ thể:**
*   $P = 11 \cdot (C - 23) \pmod{26}$
*   Do $-23 \equiv 3 \pmod{26}$, công thức có thể viết gọn thành:
    $$P = 11 \cdot (C + 3) \pmod{26}$$

**4. Áp dụng giải mã cho chuỗi "rmpjvpwtwtmhgmpwtgfwgkzn":**
*(Chuyển các chữ thường sang giá trị số tương ứng)*

| Ký tự (C) | Số (C) | $C+3$ | $11 \cdot (C+3)$ | $P \pmod{26}$ | Giải mã (P) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| r | 17 | 20 | 220 | 12 | M |
| m | 12 | 15 | 165 | 9 | J |
| p | 15 | 18 | 198 | 16 | Q |
| j | 9 | 12 | 132 | 2 | C |
| v | 21 | 24 | 264 | 4 | E |
| p | 15 | 18 | 198 | 16 | Q |
| w | 22 | 25 | 275 | 15 | P |
| t | 19 | 22 | 242 | 8 | I |
| w | 22 | 25 | 275 | 15 | P |
| t | 19 | 22 | 242 | 8 | I |
| m | 12 | 15 | 165 | 9 | J |
| h | 7 | 10 | 110 | 6 | G |
| g | 6 | 9 | 99 | 21 | V |
| m | 12 | 15 | 165 | 9 | J |
| p | 15 | 18 | 198 | 16 | Q |
| w | 22 | 25 | 275 | 15 | P |
| t | 19 | 22 | 242 | 8 | I |
| g | 6 | 9 | 99 | 21 | V |
| f | 5 | 8 | 88 | 10 | K |
| w | 22 | 25 | 275 | 15 | P |
| g | 6 | 9 | 99 | 21 | V |
| k | 10 | 13 | 143 | 13 | N |
| z | 25 | 28 | 308 | 22 | W |
| n | 13 | 16 | 176 | 20 | U |

> **Lưu ý chấm điểm:** Giảng viên chú ý việc quy đổi công thức $(C-23)$ thành $(C+3)$ là một bước tối ưu tính toán hợp lệ của sinh viên. Bản rõ (Plaintext) có thể không phải là một từ có nghĩa trong tiếng Anh.

---

### Câu 2: Sử dụng mật mã Hill mã hóa bản rõ "doikhongnhulamo" rồi giải mã lại kết quả. Với khóa $K = \begin{pmatrix} 7 & 3 \\ 8 & 7 \end{pmatrix}$

**1. Chuẩn bị (Mã hóa):**
*   Bản rõ: `doikhongnhulamo` (15 ký tự).
*   Do khóa K là ma trận $2 \times 2$, ta cần chia bản rõ thành các block 2 ký tự. Bản rõ lẻ (15), ta thêm ký tự đệm `x` vào cuối: `do ik ho ng nh ul am ox`.
*   Quy đổi sang số: `d=3, o=14, i=8, k=10, h=7, o=14, n=13, g=6, n=13, h=7, u=20, l=11, a=0, m=12, o=14, x=23`.

**2. Thực hiện mã hóa $C = P \times K \pmod{26}$:**

*   Block 1: (do) = $(3, 14)$
    $C_1 = (3 \times 7 + 14 \times 8) \pmod{26} = (21 + 112) \pmod{26} = 133 \pmod{26} = 3 \rightarrow \text{D}$
    $C_2 = (3 \times 3 + 14 \times 7) \pmod{26} = (9 + 98) \pmod{26} = 107 \pmod{26} = 3 \rightarrow \text{D}$
    *(Lưu ý: Cách tính trên là nhân ma trận cột. Tuy nhiên, theo quy ước Hill phổ biến trong nhiều giáo trình (bao gồm cả bài mẫu), ta nhân vector dòng $1 \times 2$ với ma trận $2 \times 2$)*.
    **Nhân theo vector dòng $1 \times 2$:**
    $$[C_1, C_2] = [P_1, P_2] \times \begin{pmatrix} 7 & 3 \\ 8 & 7 \end{pmatrix} \pmod{26}$$
    
    *   `do` = $[3, 14] \times K = [3 \times 7 + 14 \times 8, 3 \times 3 + 14 \times 7] = [133, 107] \equiv [3, 3] \pmod{26} \rightarrow \textbf{DD}$ (Có vẻ lời giải tham khảo trước đó tính sai block đầu tiên ra LS, đúng phải là DD).
    *   `ik` = $[8, 10] \times K = [8 \times 7 + 10 \times 8, 8 \times 3 + 10 \times 7] = [136, 94] \equiv [6, 16] \pmod{26} \rightarrow \textbf{GQ}$
    *   `ho` = $[7, 14] \times K = [7 \times 7 + 14 \times 8, 7 \times 3 + 14 \times 7] = [161, 119] \equiv [5, 15] \pmod{26} \rightarrow \textbf{FP}$
    *   `ng` = $[13, 6] \times K = [13 \times 7 + 6 \times 8, 13 \times 3 + 6 \times 7] = [139, 81] \equiv [9, 3] \pmod{26} \rightarrow \textbf{JD}$
    *   `nh` = $[13, 7] \times K = [13 \times 7 + 7 \times 8, 13 \times 3 + 7 \times 7] = [147, 88] \equiv [17, 10] \pmod{26} \rightarrow \textbf{RK}$
    *   `ul` = $[20, 11] \times K = [20 \times 7 + 11 \times 8, 20 \times 3 + 11 \times 7] = [228, 137] \equiv [20, 7] \pmod{26} \rightarrow \textbf{UH}$
    *   `am` = $[0, 12] \times K = [0 \times 7 + 12 \times 8, 0 \times 3 + 12 \times 7] = [96, 84] \equiv [18, 6] \pmod{26} \rightarrow \textbf{SG}$
    *   `ox` = $[14, 23] \times K = [14 \times 7 + 23 \times 8, 14 \times 3 + 23 \times 7] = [282, 203] \equiv [22, 21] \pmod{26} \rightarrow \textbf{WV}$
    
    > **Kết quả bản mã:** `DD GQ FP JD RK UH SG WV`

**3. Quá trình Giải mã:**
*   **Tính định thức:** $\det(K) = 7 \times 7 - 3 \times 8 = 49 - 24 = 25$.
*   **Tìm nghịch đảo định thức $\det(K)^{-1} \pmod{26}$:** $25 \times (-1) = -25 \equiv 1 \pmod{26}$. Vậy $\det(K)^{-1} \equiv -1 \equiv 25 \pmod{26}$.
*   **Tìm ma trận phụ hợp (Adjugate Matrix):** Đổi chỗ phần tử đường chéo chính, đổi dấu đường chéo phụ:
    $Adj(K) = \begin{pmatrix} 7 & -3 \\ -8 & 7 \end{pmatrix} \equiv \begin{pmatrix} 7 & 23 \\ 18 & 7 \end{pmatrix} \pmod{26}$
*   **Tính ma trận nghịch đảo $K^{-1}$:**
    $$K^{-1} = 25 \times \begin{pmatrix} 7 & 23 \\ 18 & 7 \end{pmatrix} \pmod{26} = \begin{pmatrix} 175 & 575 \\ 450 & 175 \end{pmatrix} \pmod{26} = \begin{pmatrix} 19 & 3 \\ 8 & 19 \end{pmatrix}$$
*   **Thực hiện giải mã $P = C \times K^{-1} \pmod{26}$:**
    *   `DD` = $[3, 3] \times K^{-1} = [3 \times 19 + 3 \times 8, 3 \times 3 + 3 \times 19] = [81, 66] \equiv [3, 14] \pmod{26} \rightarrow \textbf{do}$
    *   *Tiếp tục nhân tương tự cho các block còn lại, ta sẽ thu được bản rõ ban đầu.*

---

### Câu 3: Sử dụng Mã Hill mã hóa nội dung "khoacongnghekythuat" với khóa $K = \begin{pmatrix} 5 & 8 & 9 \\ 3 & 7 & 5 \\ 6 & 3 & 9 \end{pmatrix}$, sau đó giải mã.

**1. Chuẩn bị:**
*   Bản rõ: `kho a co ngn ghe kyt hua tx` (đã thêm `x` ở cuối để chuỗi dài 21 ký tự, chia hết cho 3).
*   Quy đổi sang số: `k=10, h=7, o=14, a=0, c=2, o=14, n=13, g=6, n=13...`

**2. Mã hóa $C = P \times K \pmod{26}$:** (Theo vector dòng)
*   `kho` = $[10, 7, 14] \times \begin{pmatrix} 5 & 8 & 9 \\ 3 & 7 & 5 \\ 6 & 3 & 9 \end{pmatrix} = [10 \times 5 + 7 \times 3 + 14 \times 6, 10 \times 8 + 7 \times 7 + 14 \times 3, 10 \times 9 + 7 \times 5 + 14 \times 9]$
    $= [50+21+84, 80+49+42, 90+35+126] = [155, 171, 251] \equiv [25, 15, 17] \pmod{26} \rightarrow \textbf{ZPR}$
*   `aco` = $[0, 2, 14] \times K = [0+6+84, 0+14+42, 0+10+126] = [90, 56, 136] \equiv [12, 4, 6] \pmod{26} \rightarrow \textbf{MEG}$
*(Sinh viên tự thực hiện nốt quá trình nhân ma trận để hoàn thành việc mã hóa).*

**3. Giải mã $P = C \times K^{-1} \pmod{26}$:**
*   Tính định thức bằng quy tắc Sarrus:
    $\det(K) = 5(7 \times 9 - 5 \times 3) - 8(3 \times 9 - 5 \times 6) + 9(3 \times 3 - 7 \times 6)$
    $= 5(48) - 8(-3) + 9(-33) = 240 + 24 - 297 = -33 \equiv 19 \pmod{26}$.
*   Tìm $\det(K)^{-1} \pmod{26}$: $19 \times 11 = 209 \equiv 1 \pmod{26} \Rightarrow \det(K)^{-1} = 11$.
*   Lập ma trận phụ hợp $Adj(K)$ và tính $K^{-1}$:
    $$K^{-1} = 11 \cdot Adj(K) \pmod{26}$$ *(Giảng viên chấm bước thiết lập định thức và phương pháp lập ma trận phụ hợp).*

---

### Câu 4: Sử dụng thuật toán RSA mã hóa "chuccacbanthitotnhe" với $p=11, q=13$.

*(RSA thường không mã hóa trực tiếp nguyên chuỗi mà chia theo block hoặc mã số thứ tự chữ cái, do bảng $Z_{26}$ chỉ tới 25 mà $n=143$, ta có thể mã hóa từng chữ cái một).*

**1. Khởi tạo Khóa RSA:**
*   $n = p \times q = 11 \times 13 = 143$.
*   $\phi(n) = (p-1)(q-1) = 10 \times 12 = 120$.
*   Chọn $e$ nguyên tố cùng nhau với $120$. Chọn ngẫu nhiên $e = 7$.
*   Khóa công khai $PU = (e, n) = (7, 143)$.
*   Tính khóa bí mật $d \equiv e^{-1} \pmod{120} \Rightarrow d \equiv 7^{-1} \pmod{120}$. Ta có $7 \times 103 = 721 = 6 \times 120 + 1$, vậy $d = 103$. Khóa bí mật $PR = (103, 143)$.

**2. Quá trình mã hóa $C = M^e \pmod{n}$:**
*   Bản rõ "c" = 2. $C_1 = 2^7 \pmod{143} = 128 \pmod{143} = 128$.
*   Bản rõ "h" = 7. $C_2 = 7^7 \pmod{143} = 823543 \pmod{143} = 6$.
*   Bản rõ "u" = 20. $C_3 = 20^7 \pmod{143} \equiv (20^2)^3 \cdot 20 \pmod{143} = 400^3 \cdot 20 \equiv 114^3 \cdot 20 \equiv 125 \pmod{143}$.
*   *(Sinh viên áp dụng quy tắc bình phương và nhân để xử lý các số mũ lớn).*

---

### Câu 6 & 7: Mã hóa "ho và tên" bằng thuật toán Playfair (ví dụ Khóa "bainaylamroi").

Giả sử sinh viên tên: **LE VAN AN**.
**1. Lập ma trận 5x5:**
*   Khóa "bainaylamroi" sau khi bỏ ký tự trùng lặp: `b a i n y l m r o`. (Quy ước chữ J gộp vào chữ I).
*   Điền nốt bảng chữ cái còn lại:
```text
B A I N Y
L M R O C
D E F G H
K P Q S T
U V W X Z
```

**2. Mã hóa "LE VAN AN":**
*   Chia cặp: `LE VA NA Nx` (Thêm X vào cuối để đủ cặp).
*   `LE`: L nằm ở $(1,0)$, E nằm ở $(2,1)$. Hình chữ nhật $\rightarrow$ **MD**.
*   `VA`: V nằm ở $(4,1)$, A nằm ở $(0,1)$. Cùng cột $\rightarrow$ **AV**.
*   `NA`: N nằm ở $(0,3)$, A nằm ở $(0,1)$. Cùng hàng $\rightarrow$ **YI**.
*   `NX`: N nằm ở $(0,3)$, X nằm ở $(4,3)$. Cùng cột $\rightarrow$ **OS**.
*   $\rightarrow$ Bản mã: `MD AV YI OS`.

---

## 🔵 PHẦN 2: LÝ THUYẾT

### Câu 5 & 8: Hệ thống IPS và IDS - Khái niệm & So sánh

**1. Khái niệm IDS (Intrusion Detection System):**
*   Hệ thống phát hiện xâm nhập mạng. Có vai trò như một camera giám sát, **thụ động (Passive)** quan sát lưu lượng mạng để tìm kiếm các dấu hiệu độc hại hoặc vi phạm chính sách.
*   **Hành động:** Khi phát hiện, chỉ ghi log và gửi cảnh báo (Alert) cho quản trị viên, không can thiệp vào luồng dữ liệu.

**2. Khái niệm IPS (Intrusion Prevention System):**
*   Hệ thống ngăn ngừa xâm nhập. Có vai trò như nhân viên bảo vệ, **chủ động (Active/Inline)** đứng trực tiếp giữa luồng dữ liệu (traffic).
*   **Hành động:** Có khả năng chặn đứng, ngắt kết nối (Drop/Block) cuộc tấn công ngay tại thời điểm phát hiện.

**3. Cơ chế chung:**
Cả 2 đều dùng 2 cơ chế chính để phát hiện:
*   *Signature-based (Dựa trên chữ ký)*: So sánh với cơ sở dữ liệu mẫu mã độc đã biết.
*   *Anomaly-based (Dựa trên sự bất thường)*: Học hành vi bình thường của mạng và báo động khi có dấu hiệu lạ.

### Câu 9: Vai trò của SSL/TLS trong bảo mật website

Giao thức SSL (Secure Sockets Layer) / TLS (Transport Layer Security) là xương sống của HTTPS, với 3 vai trò cốt lõi:
1.  **Mã hóa dữ liệu (Encryption):** Chuyển đổi dữ liệu trao đổi giữa Client và Server thành bản mã (ciphertext), ngăn chặn tin tặc bắt gói tin (sniffing/man-in-the-middle) đọc trộm thông tin nhạy cảm như thẻ tín dụng, mật khẩu.
2.  **Xác thực (Authentication):** Đảm bảo người dùng đang giao tiếp đúng với máy chủ thực (thông qua chứng chỉ số Digital Certificate do CA cấp), ngăn chặn các cuộc tấn công lừa đảo (Phishing/Spoofing).
3.  **Tính toàn vẹn (Data Integrity):** Sử dụng các mã MAC (Message Authentication Code) để đảm bảo dữ liệu không bị chỉnh sửa, thay đổi trên đường truyền.

### Câu 10: Cơ chế hoạt động của Chữ ký số (Digital Signature)

Chữ ký số sử dụng hệ thống Mật mã Khóa công khai (Asymmetric Cryptography) để xác thực tính toàn vẹn và chống chối bỏ của tài liệu số.

**Cơ chế gồm 2 quá trình:**
1.  **Quá trình Ký (Bên gửi):**
    *   Bên gửi chạy hàm băm (Hash Function) trên toàn bộ thông điệp $M$ để tạo ra một chuỗi tóm tắt $h = Hash(M)$.
    *   Bên gửi dùng **Khóa bí mật (Private Key)** của chính mình để mã hóa chuỗi $h$, tạo thành chữ ký số $S = Encrypt(h, PR)$.
    *   Gửi thông điệp $M$ kèm theo chữ ký $S$ cho người nhận.
2.  **Quá trình Kiểm tra (Bên nhận):**
    *   Bên nhận dùng **Khóa công khai (Public Key)** của người gửi để giải mã chữ ký $S$, thu lại chuỗi tóm tắt ban đầu $h = Decrypt(S, PU)$.
    *   Đồng thời, bên nhận cũng chạy hàm băm trên thông điệp $M$ nhận được để tạo ra một bản tóm tắt mới $h' = Hash(M)$.
    *   So sánh $h$ và $h'$. Nếu khớp nhau, chứng tỏ thông điệp nguyên vẹn, không bị sửa đổi và thực sự do người có Private Key ký.

---
*(Hết tài liệu)*