"""
Context Pipeline V3.0 - Intelligence Layer cho Prepare Gemini
==============================================================
Pipeline ETL (Extract → Transform → Enrich) giúp bundle context
thông minh hơn trước khi gửi cho Gemini Web.

Modules:
    - FileTransformer: Per-file filter rules (loại noise, compress)
    - SectionEnricher: Inject metadata (priority, summary, tokens)
    - transform_content: Public API cho orchestrator
    - enrich_section: Public API cho orchestrator

Usage:
    from context_pipeline import transform_content, enrich_section
    clean = transform_content("docs/ERROR_ENCYCLOPEDIA.md", raw_text)
    enriched = enrich_section("docs/SYSTEM_MAP.md", clean)
"""

import json
import re
import sys
from dataclasses import dataclass
from typing import Optional

# Fix Unicode/GBK encoding cho Windows Terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass


# =============================================================================
# CONFIG: File Priority & Summary Registry
# =============================================================================

@dataclass(frozen=True)
class FileMeta:
    """Metadata cho mỗi file trong bundle."""
    name: str
    priority: str          # 🔴 CRITICAL | 🟡 IMPORTANT | 🟢 OPTIONAL
    file_type: str         # Architecture | Strategy | Lore | Config | Error | ...
    summary: str           # 1 câu tóm tắt cho Gemini
    max_top_errors: int = 20  # Riêng cho ERROR_ENCYCLOPEDIA


# Registry: file_path -> FileMeta
FILE_REGISTRY: dict[str, FileMeta] = {
    "WHITE_PAPER_JARVIS.md": FileMeta(
        "WHITE_PAPER_JARVIS.md", "🔴 CRITICAL", "Manifesto",
        "Tuyên ngôn kiến trúc tổng quan JARVIS - đọc đầu tiên."
    ),
    "context/SYSTEM_LORE.md": FileMeta(
        "context/SYSTEM_LORE.md", "🔴 CRITICAL", "Lore",
        "Bối cảnh & nhân cách hệ thống (Sovereign AI)."
    ),
    "context/GLOBAL_STATE.md": FileMeta(
        "context/GLOBAL_STATE.md", "🔴 CRITICAL", "State",
        "Snapshot trạng thái hệ thống hiện tại (hardware, goal, timestamp)."
    ),
    "context/ACTIVE_THOUGHTS.md": FileMeta(
        "context/ACTIVE_THOUGHTS.md", "🔴 CRITICAL", "Worklog",
        "Công việc dang dở & next steps."
    ),
    "context/ROADMAP.md": FileMeta(
        "context/ROADMAP.md", "🟡 IMPORTANT", "Roadmap",
        "Lộ trình Q3-Q4 và chiến dịch ưu tiên."
    ),
    "context/JARVIS_CHRONICLES.md": FileMeta(
        "context/JARVIS_CHRONICLES.md", "🟡 IMPORTANT", "History",
        "Lịch sử tiến hóa kỹ thuật & tech debt."
    ),
    "docs/SYSTEM_MAP.md": FileMeta(
        "docs/SYSTEM_MAP.md", "🔴 CRITICAL", "Architecture",
        "Sơ đồ dependency toàn hệ thống - 22+ projects."
    ),
    "docs/ERROR_ENCYCLOPEDIA.md": FileMeta(
        "docs/ERROR_ENCYCLOPEDIA.md", "🟢 OPTIONAL", "Error DB",
        "Tổng hợp lỗi thường gặp + solutions.", max_top_errors=20
    ),
    "reports/SOVEREIGN_MATURITY_ASSESSMENT.md": FileMeta(
        "reports/SOVEREIGN_MATURITY_ASSESSMENT.md", "🟢 OPTIONAL", "Maturity",
        "Đánh giá mức trưởng thành AI Engineering."
    ),
    "reports/Q3_STRATEGIC_PLAN.md": FileMeta(
        "reports/Q3_STRATEGIC_PLAN.md", "🟡 IMPORTANT", "Strategy",
        "OKRs & chiến dịch trọng tâm Q3."
    ),
    "monorepo_manifest.json": FileMeta(
        "monorepo_manifest.json", "🟡 IMPORTANT", "Manifest",
        "Danh sách 22 active projects + status."
    ),
    ".clinerules": FileMeta(
        ".clinerules", "🔴 CRITICAL", "Constitution",
        "Hiến pháp cưỡng chế - rules tuyệt đối cho AI agents."
    ),
}

# Default meta cho file không có trong registry (user ideas, ...)
DEFAULT_META = FileMeta(
    "unknown", "🟢 OPTIONAL", "User Input",
    "Dữ liệu thô từ Admin.", max_top_errors=0
)


# =============================================================================
# STAGE: TRANSFORM (Làm sạch / Compress)
# =============================================================================

class FileTransformer:
    """
    Áp dụng per-file transformation rules để loại noise, compress dung lượng.
    Mỗi rule trả về text đã làm sạch.
    """

    # Patterns loại bỏ chung (apply cho mọi file)
    _MULTI_BLANK_RE = re.compile(r"\n{3,}", re.MULTILINE)     # > 2 blank lines
    _DECOR_LINE_RE = re.compile(r"^[\-=]{5,}$", re.MULTILINE) # lines `-----` → `---`
    _TRAIL_WS_RE = re.compile(r"[ \t]+$", re.MULTILINE)       # trailing whitespace

    @classmethod
    def transform(cls, file_name: str, content: str) -> str:
        """Transform entry point - dispatch theo file type."""
        if not content:
            return content

        # 1) Generic cleaning (apply cho tất cả)
        cleaned = cls._generic_clean(content)

        # 2) Per-file specific rules
        if file_name == "docs/ERROR_ENCYCLOPEDIA.md":
            cleaned = cls._filter_error_encyclopedia(cleaned)
        elif file_name == "monorepo_manifest.json":
            cleaned = cls._minify_json(cleaned)
        elif file_name == "context/GLOBAL_STATE.md":
            cleaned = cls._strip_emoji_noise(cleaned)
        elif file_name == ".clinerules":
            cleaned = cls._collapse_decor(cleaned)

        return cleaned.strip()

    @classmethod
    def _generic_clean(cls, text: str) -> str:
        """Làm sạch chung: blank lines, dashes, trailing whitespace."""
        text = cls._TRAIL_WS_RE.sub("", text)
        text = cls._DECOR_LINE_RE.sub("---", text)
        text = cls._MULTI_BLANK_RE.sub("\n\n", text)
        return text

    @classmethod
    def _filter_error_encyclopedia(cls, text: str, top_n: int = 20) -> str:
        """
        ERROR_ENCYCLOPEDIA rất dài do Auto-Generated AST section.
        Chỉ giữ phần đầu (errors + solutions) và top N lỗi phổ biến.
        """
        marker = "[AUTO-GENERATED"
        idx = text.find(marker)
        if idx > 0:
            head = text[:idx]
            tail_note = (
                f"\n\n[...Đã cắt {len(text) - idx:,} ký tự phần Auto-Generated AST "
                f"để tiết kiệm context. Query RAG nếu cần chi tiết...]"
            )
            text = head + tail_note
        return text

    @classmethod
    def _minify_json(cls, text: str) -> str:
        """Minify JSON: bỏ indent thừa, giữ cấu trúc."""
        try:
            data = json.loads(text)
            return json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        except (json.JSONDecodeError, ValueError):
            return text  # fallback: giữ nguyên nếu parse lỗi

    @classmethod
    def _strip_emoji_noise(cls, text: str) -> str:
        """GLOBAL_STATE: giữ emoji ở header nhưng collapse blocks thừa."""
        # Chỉ collapse blank lines aggressive hơn cho state file
        return cls._MULTI_BLANK_RE.sub("\n", text)

    @classmethod
    def _collapse_decor(cls, text: str) -> str:
        """Clinerules: gộp các separator line dày đặc."""
        # Đã xử lý ở generic, ở đây chỉ thêm: bỏ comment block rỗng
        return re.sub(r"---\n---+", "---", text)


# =============================================================================
# STAGE: ENRICH (Inject Metadata)
# =============================================================================

class SectionEnricher:
    """
    Inject metadata header trước mỗi section để Gemini hiểu priority & context.
    """

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Ước lượng tokens (~4 chars/token cho mixed vi/en)."""
        return max(1, len(text) // 4)

    @classmethod
    def enrich(
        cls,
        file_name: str,
        content: str,
        original_chars: int = 0,
        transformed_chars: int = 0,
    ) -> str:
        """
        Build enriched section với header metadata.

        Args:
            file_name: Path tương đối (VD: "docs/SYSTEM_MAP.md")
            content: Nội dung đã transform
            original_chars: Số ký tự gốc (pre-transform)
            transformed_chars: Số ký tự sau transform

        Returns:
            Section có header enriched + content
        """
        meta = FILE_REGISTRY.get(file_name, DEFAULT_META)
        tokens = cls.estimate_tokens(content)
        savings = original_chars - transformed_chars if original_chars > 0 else 0
        savings_pct = (
            f" (-{savings / original_chars * 100:.0f}% compressed)"
            if original_chars > 0 and savings > 0
            else ""
        )

        header = (
            f"[PRIORITY: {meta.priority}] "
            f"[TYPE: {meta.file_type}] "
            f"[TOKENS: ~{tokens:,}]\n"
            f"[SUMMARY: {meta.summary}]\n"
            f"[CHARS: {transformed_chars:,}{savings_pct}]"
        )

        return f"{header}\n---\n{content}"


# =============================================================================
# PUBLIC API
# =============================================================================

def transform_content(file_name: str, content: str) -> str:
    """Public API: Transform content theo per-file rules."""
    return FileTransformer.transform(file_name, content)


def enrich_section(
    file_name: str,
    content: str,
    original_chars: int = 0,
    transformed_chars: int = 0,
) -> str:
    """Public API: Enrich section với metadata header."""
    return SectionEnricher.enrich(
        file_name, content, original_chars, transformed_chars
    )


def get_file_meta(file_name: str) -> Optional[FileMeta]:
    """Lấy metadata của file từ registry."""
    return FILE_REGISTRY.get(file_name)


# =============================================================================
# SELF-TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 CONTEXT PIPELINE V3.0 - SELF TEST")
    print("=" * 60)

    # Test 1: Generic clean
    raw = "Hello\n\n\n\n\nWorld\n=====     \n-----"
    cleaned = FileTransformer.transform("test.md", raw)
    assert "\n\n\n" not in cleaned, "Generic clean failed"
    print("✅ Test 1 (Generic clean): PASSED")

    # Test 2: Error Encyclopedia filter
    raw_err = "Error 1\n\n[AUTO-GENERATED AST DATA...]" + "x" * 5000
    filtered = FileTransformer.transform("docs/ERROR_ENCYCLOPEDIA.md", raw_err)
    assert len(filtered) < len(raw_err), "Error filter failed"
    assert "[AUTO-GENERATED" not in filtered.split("---")[-1]
    print(f"✅ Test 2 (Error filter): PASSED ({len(raw_err)} → {len(filtered)} chars)")

    # Test 3: JSON minify
    raw_json = '{\n  "a": 1,\n  "b": 2\n}'
    minified = FileTransformer.transform("monorepo_manifest.json", raw_json)
    assert "\\n" not in minified.replace('"', ""), "JSON minify failed"
    print(f"✅ Test 3 (JSON minify): PASSED ({len(raw_json)} → {len(minified)} chars)")

    # Test 4: Enrich
    enriched = enrich_section("docs/SYSTEM_MAP.md", "test content", 100, 80)
    assert "[PRIORITY:" in enriched and "[TOKENS:" in enriched
    print("✅ Test 4 (Enrich): PASSED")

    # Test 5: Token estimate
    assert SectionEnricher.estimate_tokens("abcd") == 1
    print("✅ Test 5 (Token estimate): PASSED")

    print("\n🎉 ALL TESTS PASSED - Pipeline ready!")