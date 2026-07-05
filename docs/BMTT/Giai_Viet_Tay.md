# HƯỚNG DẪN TRÌNH BÀY GIẤY THI - AN TOÀN VÀ BẢO MẬT THÔNG TIN
*(Chép y nguyên theo từng bước dưới đây vào giấy)*

---
## CÂU 1: GIẢI MÁ AFFINE
**Đề bài:** Giải mã "rmpjvpwtwtmhgmpwtgfwgkzn" với a=19, b=23.

**Giải:**
**Bước 1:** Xác định công thức giải mã:
- Hệ mã Affine trên $Z_{26}$.
- Công thức giải mã: $P = a^{-1} \cdot (C - b) \pmod{26}$

**Bước 2:** Tìm phần tử nghịch đảo của $a=19$:
- Ta cần tìm $a^{-1}$ sao cho $19 \cdot a^{-1} \equiv 1 \pmod{26}$
- Dùng thuật toán Euclide hoặc nhẩm: $19 \cdot 11 = 209 = 8 \cdot 26 + 1$
- Suy ra $a^{-1} = 11$.

**Bước 3:** Lập công thức giải mã cụ thể:
- $P = 11 \cdot (C - 23) \pmod{26}$
- Do $-23 \equiv 3 \pmod{26}$ nên $P = 11 \cdot (C + 3) \pmod{26}$

**Bước 4:** Lập bảng giải mã:
*(Lưu ý: Bạn kẻ bảng này vào giấy, không cần nháp quá chi tiết từng phép tính nhân)*

| Bản mã (C) | Số (C) | $C+3$ | $11 \cdot (C+3)$ | Số (P) mod 26 | Bản rõ (P) |
|---|---|---|---|---|---|
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

*Vậy bản rõ là:* MJQCEQPIPIJGVJQPIVKVWNU

---

## CÂU 2: MÃ HILL (MA TRẬN 2x2)
**Đề bài:** Mã hóa "doikhongnhulamo" với khóa $K = \begin{pmatrix} 7 & 3 \\ 8 & 7 \end{pmatrix}$. Giải mã lại.

### A. MÃ HÓA
**Bước 1:** Chuẩn bị bản rõ
- Bản rõ: `do ik ho ng nh ul am ox` *(thêm 'x' ở cuối để chẵn)*
- Đổi sang số: `(3,14), (8,10), (7,14), (13,6), (13,7), (20,11), (0,12), (14,23)`

**Bước 2:** Mã hóa $C = P \times K \pmod{26}$
- Block 1 (do): $[3, 14] \times \begin{pmatrix} 7 & 3 \\ 8 & 7 \end{pmatrix} = [3\cdot7 + 14\cdot8, 3\cdot3 + 14\cdot7] = [133, 107] \equiv [3, 3] \pmod{26} \Rightarrow$ **DD**
- Block 2 (ik): $[8, 10] \times \begin{pmatrix} 7 & 3 \\ 8 & 7 \end{pmatrix} = [8\cdot7 + 10\cdot8, 8\cdot3 + 10\cdot7] = [136, 94] \equiv [6, 16] \pmod{26} \Rightarrow$ **GQ**
- Block 3 (ho): $[7, 14] \times K = [161, 119] \equiv [5, 15] \pmod{26} \Rightarrow$ **FP**
- Block 4 (ng): $[13, 6] \times K = [139, 81] \equiv [9, 3] \pmod{26} \Rightarrow$ **JD**
- Block 5 (nh): $[13, 7] \times K = [147, 88] \equiv [17, 10] \pmod{26} \Rightarrow$ **RK**
- Block 6 (ul): $[20, 11] \times K = [228, 137] \equiv [20, 7] \pmod{26} \Rightarrow$ **UH**
- Block 7 (am): $[0, 12] \times K = [96, 84] \equiv [18, 6] \pmod{26} \Rightarrow$ **SG**
- Block 8 (ox): $[14, 23] \times K = [282, 203] \equiv [22, 21] \pmod{26} \Rightarrow$ **WV**
*Bản mã thu được:* **DD GQ FP JD RK UH SG WV**

### B. GIẢI MÁ
**Bước 1:** Tính định thức $\det(K)$
- $\det(K) = 7\cdot7 - 3\cdot8 = 49 - 24 = 25 \equiv 25 \pmod{26}$

**Bước 2:** Tìm $\det(K)^{-1}$
- Vì $25 \equiv -1 \pmod{26}$, nên $(-1) \cdot (-1) = 1 \Rightarrow \det(K)^{-1} = -1 \equiv 25 \pmod{26}$

**Bước 3:** Tính ma trận nghịch đảo $K^{-1}$
- Đổi vị trí chéo chính, đổi dấu chéo phụ: $Adj(K) = \begin{pmatrix} 7 & -3 \\ -8 & 7 \end{pmatrix} \equiv \begin{pmatrix} 7 & 23 \\ 18 & 7 \end{pmatrix} \pmod{26}$
- $K^{-1} = 25 \cdot \begin{pmatrix} 7 & 23 \\ 18 & 7 \end{pmatrix} = \begin{pmatrix} 175 & 575 \\ 450 & 175 \end{pmatrix} \equiv \begin{pmatrix} 19 & 3 \\ 8 & 19 \end{pmatrix} \pmod{26}$

**Bước 4:** Giải mã $P = C \times K^{-1} \pmod{26}$
- Block 1 (DD): $[3, 3] \times \begin{pmatrix} 19 & 3 \\ 8 & 19 \end{pmatrix} = [3\cdot19 + 3\cdot8, 3\cdot3 + 3\cdot19] = [81, 66] \equiv [3, 14] \pmod{26} \Rightarrow$ **do**
*(Chỉ cần ghi 1 dòng mẫu thế này là đủ chứng minh hiểu bài, sau đó ghi câu "Thực hiện tương tự cho các block tiếp theo ta thu lại được bản rõ ban đầu: doikhongnhulamo" là qua).*

---

## CÂU 4: MÃ HÓA RSA
**Đề bài:** Mã hóa "chuccacbanthitotnhe" với $p=11, q=13$

**Giải:**
**Bước 1:** Khởi tạo thông số RSA
- $n = p \times q = 11 \times 13 = 143$
- $\phi(n) = (p-1)(q-1) = 10 \times 12 = 120$

**Bước 2:** Chọn $e$ và tính khóa bí mật $d$
- Chọn ngẫu nhiên $e = 7$ (vì $\gcd(7, 120) = 1$). Khóa công khai $PU = (7, 143)$.
- Tính $d \equiv e^{-1} \pmod{120} \Rightarrow d \equiv 7^{-1} \pmod{120}$. 
- Thử chọn $k$: $7 \cdot 103 = 721 = 120 \cdot 6 + 1 \Rightarrow d = 103$. Khóa bí mật $PR = (103, 143)$.

**Bước 3:** Mã hóa $C = M^e \pmod{143}$
- Chữ 'c' = 2 $\rightarrow C_1 = 2^7 \pmod{143} = 128$
- Chữ 'h' = 7 $\rightarrow C_2 = 7^7 \pmod{143} = 823543 \pmod{143} = 6$
- Chữ 'u' = 20 $\rightarrow C_3 = 20^7 \pmod{143} \equiv 125 \pmod{143}$
*(Tương tự cho các ký tự còn lại...)*

---

## CÂU 6: MÃ HÓA PLAYFAIR
**Đề bài:** Mã hóa tên bạn (Ví dụ: LE VAN AN) với khóa "bainaylamroi".

**Giải:**
**Bước 1:** Lập bảng Playfair 5x5
- Từ khóa loại bỏ chữ trùng, gộp I/J: B, A, I, N, Y, L, M, R, O.
- Bảng 5x5 (điền nốt các chữ cái còn lại):
B  A  I  N  Y
L  M  R  O  C
D  E  F  G  H
K  P  Q  S  T
U  V  W  X  Z

**Bước 2:** Mã hóa
- Chia cặp: LE - VA - NA - NX (thêm X ở cuối)
- LE: L ở (1,0), E ở (2,1) $\rightarrow$ Góc hình chữ nhật $\rightarrow$ **MD**
- VA: V ở (4,1), A ở (0,1) $\rightarrow$ Cùng cột $\rightarrow$ **AV**
- NA: N ở (0,3), A ở (0,1) $\rightarrow$ Cùng hàng $\rightarrow$ **YI**
- NX: N ở (0,3), X ở (4,3) $\rightarrow$ Cùng cột $\rightarrow$ **OS**
*Bản mã: MD AV YI OS*

---

## LÝ THUYẾT (HỌC THUỘC)

### Câu 5 & 8: IDS và IPS
*   **IDS (Phát hiện xâm nhập):** Thụ động. Đứng ngoài quan sát lưu lượng mạng. Giống "camera giám sát" - phát hiện thấy dấu hiệu khả nghi thì gửi báo động (Alert), không trực tiếp chặn.
*   **IPS (Ngăn ngừa xâm nhập):** Chủ động. Nằm trực tiếp trên luồng mạng (Inline). Giống "bảo vệ" - phát hiện thấy bất thường sẽ cắt kết nối (Drop/Block) gói tin ngay lập tức.
*   *Cơ chế phát hiện (dùng chung):* Dựa trên chữ ký (Signature) hoặc dựa trên sự bất thường (Anomaly).

### Câu 9: Vai trò SSL/TLS
1.  **Mã hóa (Encryption):** Tránh bị nghe trộm, biến dữ liệu thành bản mã khó đọc.
2.  **Xác thực (Authentication):** Đảm bảo kết nối đúng máy chủ hợp pháp thông qua chứng chỉ số (Certificate).
3.  **Toàn vẹn (Integrity):** Đảm bảo dữ liệu không bị kẻ gian sửa đổi giữa đường.

### Câu 10: Chữ ký số
*   **Ký (Người gửi):** Dùng hàm Băm (Hash) để tạo tóm tắt nội dung tài liệu. Dùng Khóa bí mật (Private Key) để mã hóa bản tóm tắt đó $\rightarrow$ thành Chữ ký số đính kèm vào file.
*   **Kiểm tra (Người nhận):** Dùng Khóa công khai (Public Key) của người gửi để giải mã Chữ ký số. Nếu giải mã được và giống với bản băm mới, chứng tỏ tài liệu an toàn.
*   *Vai trò:* Chống giả mạo, chống chối bỏ (người gửi không thể chối là mình không gửi) và đảm bảo tính toàn vẹn.

---
*(Hết tài liệu viết tay)*