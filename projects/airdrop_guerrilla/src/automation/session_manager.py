class SessionManager:
    """
    Quản lý phiên đăng nhập (Session Persistence) cho các nền tảng mạng xã hội.
    Nạp trực tiếp Token/Cookie vào trình duyệt để vượt qua bước Login và 2FA.
    """
    @staticmethod
    def apply_twitter_session(context, auth_data: str):
        """
        Nạp auth_token của X (Twitter) hoặc một mảng JSON Cookie vào Browser Context.
        
        Args:
            context: Playwright Browser Context.
            auth_data (str): Giá trị auth_token hoặc chuỗi JSON chứa array các cookies.
        """
        if not auth_data:
            return
            
        import json
        try:
            # Thử parse JSON xem có phải là mảng Cookie được export từ extension không
            cookies_array = json.loads(auth_data)
            if isinstance(cookies_array, list):
                # Chuẩn hóa domain cho X (Bảo đảm có .twitter.com và .x.com)
                normalized_cookies = []
                for c in cookies_array:
                    # Bỏ các field không tương thích
                    if 'sameSite' in c and c['sameSite'] not in ['Strict', 'Lax', 'None']:
                        c['sameSite'] = 'None'
                    
                    # Fix một số trường hay gây lỗi
                    if 'hostOnly' in c:
                        del c['hostOnly']
                    if 'session' in c:
                        del c['session']
                    if 'storeId' in c:
                        del c['storeId']
                        
                    normalized_cookies.append(c)
                    
                    # Duplicate cookie cho domain x.com nếu nó là twitter.com
                    if 'twitter.com' in c.get('domain', ''):
                        c_x = c.copy()
                        c_x['domain'] = '.x.com'
                        normalized_cookies.append(c_x)
                        
                context.add_cookies(normalized_cookies)
                print("   🍪 Đã nạp thành công MẢNG Cookie JSON (Bypass cao cấp) vào Session.")
                return
        except json.JSONDecodeError:
            pass # Chuyển sang fallback nạp auth_token đơn giản
            
        # Fallback: Nếu chỉ truyền chuỗi auth_token
        cookies = [
            {'name': 'auth_token', 'value': auth_data, 'domain': '.twitter.com', 'path': '/', 'secure': True, 'httpOnly': True},
            {'name': 'auth_token', 'value': auth_data, 'domain': '.x.com', 'path': '/', 'secure': True, 'httpOnly': True}
        ]
        
        context.add_cookies(cookies)
        print("   🍪 Đã nạp thành công Twitter auth_token đơn giản vào Session.")

    @staticmethod
    def apply_discord_session(context, token: str):
        """
        Nạp Token của Discord vào Local Storage thông qua add_init_script.
        
        Args:
            context: Playwright Browser Context.
            token (str): Token đăng nhập của Discord.
        """
        if not token:
            return
            
        print("   🍪 Đang nạp Discord Token qua Init Script...")
        # Tiêm đúng chuẩn nháy kép bọc trong nháy đơn để Discord nhận diện
        script = f"window.localStorage.setItem('token', '\"{token}\"');"
        context.add_init_script(script=script)
        print("   🍪 Đã nạp thành công Discord token vào Context Init Script.")
