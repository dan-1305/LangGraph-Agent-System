import pydantic
from typing import List, Dict, Any, Optional

# --- CẤU TRÚC LOREBOOK (CHARACTER BOOK) THEO CHUẨN SILLYTAVERN ---

class LoreBookExtension(pydantic.BaseModel):
    """Phần mở rộng của 1 entry trong Lorebook"""
    position: int = 0
    exclude_recursion: bool = True
    display_index: int = 0
    probability: int = 100
    useProbability: bool = True
    depth: int = 4
    selectiveLogic: int = 0
    outlet_name: str = ""
    group: str = ""
    group_override: bool = False
    group_weight: int = 100
    prevent_recursion: bool = True
    delay_until_recursion: bool = False
    match_whole_words: Optional[bool] = None
    use_group_scoring: bool = False
    case_sensitive: Optional[bool] = None
    automation_id: str = ""
    role: int = 0
    vectorized: bool = False
    sticky: int = 0
    cooldown: int = 0
    delay: int = 0
    match_persona_description: bool = False
    match_character_description: bool = False
    match_character_personality: bool = False
    match_character_depth_prompt: bool = False
    match_scenario: bool = False
    match_creator_notes: bool = False
    triggers: list = []
    ignore_budget: bool = False

class LoreBookEntry(pydantic.BaseModel):
    """Đại diện cho 1 Mục (Entry) trong Lorebook"""
    id: int
    keys: List[str]
    secondary_keys: List[str] = []
    comment: str  # Tên hiển thị của thẻ
    content: str  # Nội dung chính
    constant: bool = False
    selective: bool = True
    insertion_order: int = 100
    enabled: bool = True
    position: str = "before_char"
    use_regex: bool = True
    extensions: LoreBookExtension = pydantic.Field(default_factory=LoreBookExtension)

class CharacterBook(pydantic.BaseModel):
    """Bọc danh sách các entries"""
    name: str = "Thế Giới"
    description: str = ""
    scan_depth: int = 50
    token_budget: int = 500
    recursive_scanning: bool = False
    extensions: Dict = {}
    entries: List[LoreBookEntry] = []

# --- CẤU TRÚC REGEX SCRIPTS & EXTENSIONS ---
# Ghi chú: SillyTavern cho phép JSON linh hoạt đối với Extension, 
# nên thay vì dùng Model cứng, ta dùng kiểu List[Dict[str, Any]] 
# để tránh lỗi Pydantic ValidationError.

class CharacterExtensions(pydantic.BaseModel):
    """Phần Extensions bọc regex và các tính năng phụ của character"""
    talkativeness: str = "0.5"
    fav: bool = False
    world: str = ""
    depth_prompt: Dict[str, Any] = {
        "prompt": "",
        "depth": 4,
        "role": "system"
    }
    regex_scripts: List[Dict[str, Any]] = []

# --- CẤU TRÚC GỐC WORLD CARD (V3) ---

class CharacterData(pydantic.BaseModel):
    """Phần Data chứa chi tiết Character/World Card"""
    name: str
    description: str  # Đây chính là System Prompt
    personality: str = ""
    scenario: str = ""
    first_mes: str    # Đây chính là Lời chào đầu
    mes_example: str = ""
    creator_notes: str = ""
    system_prompt: str = ""
    post_history_instructions: str = ""
    tags: List[str] = []
    creator: str = "AI Agent"
    character_version: str = "1.0"
    alternate_greetings: List[str] = []
    extensions: CharacterExtensions = pydantic.Field(default_factory=CharacterExtensions)
    character_book: Optional[CharacterBook] = None

class WorldCardV3(pydantic.BaseModel):
    """
    Cấu trúc bao bọc lớp ngoài cùng của file JSON chuẩn V3.
    Giống hệt file mẫu Cơ Nương.
    """
    name: str
    description: str  
    personality: str = ""
    scenario: str = ""
    first_mes: str
    mes_example: str = ""
    creatorcomment: str = ""
    avatar: str = "none"
    talkativeness: str = "0.5"
    fav: bool = False
    tags: List[str] = []
    spec: str = "chara_card_v3"
    spec_version: str = "3.0"
    data: CharacterData
    
    def to_json(self) -> str:
        """Xuất ra chuỗi JSON đẹp mắt."""
        # Dùng model_dump thay cho dict() ở bản Pydantic V2
        return self.model_dump_json(indent=2, exclude_none=True)

class UserIdeaInput(pydantic.BaseModel):
    """Input từ người dùng để AI sinh ra thẻ."""
    theme: str
    features: List[str] = []
    style: str = "Epic"
    details: str = ""
    template_reference: str = "Không" # File mẫu để AI học lỏm
    auto_balance: bool = False # Bật cân bằng chỉ số RPG
    dynamic_quest: bool = False # Sinh nhiệm vụ động
    image_prompt: bool = False # Tích hợp sinh câu lệnh ảnh
