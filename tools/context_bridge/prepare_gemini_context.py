"""
Prepare Gemini Context V3.0 - Sovereign Context Pipeline
============================================================
Bản nâng cấp từ V2.0, tích hợp Context Pipeline ETL:
- EXTRACT: Đọc raw files
- TRANSFORM: Per-file filter rules (qua context_pipeline.FileTransformer)
- ENRICH: Inject metadata header (priority, summary, tokens)
- ASSEMBLE: Build bundle với ToC, validation prompt

Files output: context_for_gemini.txt (+ clipboard)

CLI Flags:
    --mode full|arch|strategy    Chế độ bundle (default: full)
"""

import argparse
import hashlib
import os
import sys
import pyperclip
from datetime import datetime
from pathlib import Path

# Fix Unicode/GBK encoding cho Windows Terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Thêm đường dẫn gốc vào sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Import Pipeline V3.0
from context_pipeline import (
    FileTransformer,
    SectionEnricher,
    transform_content,
    enrich_section,
    get_file_meta,
    FILE_REGISTRY,
)


# =============================================================================
# CONFIG V3.0
# =============================================================================

# Full bundle (default): toàn bộ 12 file cốt lõi
CORE_FILES_FULL = [
    "WHITE_PAPER_JARVIS.md",
    "context/SYSTEM_LORE.md",
    "context/GLOBAL_STATE.md",
    "context/ACTIVE_THOUGHTS.md",
    "context/ROADMAP.md",
    "context/JARVIS_CHRONICLES.md",
    "docs/SYSTEM_MAP.md",
    "docs/ERROR_ENCYCLOPEDIA.md",
    "reports/SOVEREIGN_MATURITY_ASSESSMENT.md",
    "reports/Q3_STRATEGIC_PLAN.md",
    "monorepo_manifest.json",
    ".clinerules",
]

# Architecture mode: chỉ file kiến trúc
CORE_FILES_ARCH = [
    "docs/SYSTEM_MAP.md",
    "monorepo_manifest.json",
    ".clinerules",
    "WHITE_PAPER_JARVIS.md",
]

# Strategy mode: chỉ file chiến lược
CORE_FILES_STRATEGY = [
    "context/ROADMAP.md",
    "context/ACTIVE_THOUGHTS.md",
    "context/JARVIS_CHRONICLES.md",
    "reports/Q3_STRATEGIC_PLAN.md",
    "reports/SOVEREIGN_MATURITY_ASSESSMENT.md",
]

# Map mode -> file list
MODE_MAP = {
    "full": CORE_FILES_FULL,
    "arch": CORE_FILES_ARCH,
    "strategy": CORE_FILES_STRATEGY,
}

# Thư mục chứa ý tưởng thô của User
ANALYSIS_DIR = ROOT_DIR / "analysis_user"

# Giới hạn dung lượng (ký tự)
MAX_CHARS_PER_FILE = 30000       # Mỗi file tối đa 30k ký tự
MAX_USER_INPUT_LINES = 500       # Chỉ lấy 500 dòng cuối của user input
MAX_USER_INPUT_FILES = 3         # Lấy tối đa 3 file mới nhất
MAX_TOTAL_BUNDLE = 200000        # Tổng bundle < 200k (fit Gemini 1M, không loãng)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def truncate_content(content: str, max_chars: int = MAX_CHARS_PER_FILE, file_name: str = "") -> str:
    """Cắt nội dung nếu vượt quá giới hạn ký tự, thêm thông báo."""
    if len(content) <= max_chars:
        return content
    truncated = content[:max_chars]
    return f"{truncated}\n\n[...FILE BỊ CẮT NGẮN: {len(content)} -> {max_chars} ký tự để tiết kiệm context Gemini...]"


def read_file_safe(file_path: Path, max_chars: int = MAX_CHARS_PER_FILE) -> tuple[str, int]:
    """Đọc file an toàn, trả về (nội dung, số ký tự gốc)."""
    if not file_path.exists():
        return f"[FILE KHÔNG TỒN TẠI: {file_path.name}]", 0
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read().strip()
        original_len = len(content)
        return truncate_content(content, max_chars, file_path.name), original_len
    except Exception as e:
        return f"[LỖI ĐỌC FILE {file_path.name}]: {str(e)}", 0


def read_user_input_tail(file_path: Path, max_lines: int = MAX_USER_INPUT_LINES) -> tuple[str, int]:
    """Đọc user input nhưng chỉ lấy N dòng cuối (Smart Filter)."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        original_lines = len(lines)
        if original_lines <= max_lines:
            return "".join(lines).strip(), original_lines
        # Lấy tail
        tail_lines = lines[-max_lines:]
        header = f"[SMART FILTER: File có {original_lines} dòng, chỉ lấy {max_lines} dòng cuối để tránh loãng context]\n\n"
        return header + "".join(tail_lines).strip(), original_lines
    except Exception as e:
        return f"[LỖI: {str(e)}]", 0


# =============================================================================
# MAIN PIPELINE (Extract → Transform → Enrich → Assemble)
# =============================================================================

def gather_context(mode: str = "full") -> tuple[str, dict]:
    """
    Gom toàn bộ context qua pipeline ETL V3.0.

    Args:
        mode: "full" | "arch" | "strategy"

    Returns:
        (bundle_text, metadata)
    """
    core_files = MODE_MAP.get(mode, CORE_FILES_FULL)
    sections = []
    toc_entries = []
    metadata = {
        "files_included": [],
        "files_missing": [],
        "total_chars": 0,
        "total_original_chars": 0,
        "total_tokens": 0,
        "mode": mode,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # -------------------------------------------------------------------------
    # PIPELINE STAGE 1-3: EXTRACT + TRANSFORM + ENRICH cho CORE FILES
    # -------------------------------------------------------------------------
    for file_name in core_files:
        file_path = ROOT_DIR / file_name

        # STAGE 1: EXTRACT
        raw_content, orig_len = read_file_safe(file_path)
        if orig_len == 0:
            metadata["files_missing"].append(file_name)
            toc_entries.append(f"- ❌ {file_name} (MISSING)")
            continue

        # STAGE 2: TRANSFORM
        transformed = transform_content(file_name, raw_content)
        transformed_len = len(transformed)

        # STAGE 3: ENRICH
        enriched = enrich_section(
            file_name, transformed,
            original_chars=orig_len,
            transformed_chars=transformed_len,
        )

        meta = get_file_meta(file_name)
        tokens = SectionEnricher.estimate_tokens(transformed)

        section_header = f"\n{'=' * 60}\n📁 FILE: {file_name}\n{'=' * 60}\n"
        sections.append(f"{section_header}\n{enriched}")

        metadata["files_included"].append({
            "name": file_name,
            "orig_chars": orig_len,
            "transformed_chars": transformed_len,
            "tokens": tokens,
        })
        metadata["total_original_chars"] += orig_len
        metadata["total_chars"] += transformed_len
        metadata["total_tokens"] += tokens

        priority_tag = meta.priority if meta else "🟢 OPTIONAL"
        toc_entries.append(
            f"- {priority_tag} {file_name} "
            f"({transformed_len:,} ký tự, ~{tokens:,} tokens)"
        )

    # -------------------------------------------------------------------------
    # USER RAW IDEAS (chỉ ở mode "full")
    # -------------------------------------------------------------------------
    if mode == "full":
        user_section_header = f"\n{'=' * 60}\n🧠 USER RAW IDEAS (analysis_user/ - Smart Filter: {MAX_USER_INPUT_LINES} dòng/file)\n{'=' * 60}\n"
        user_parts = [user_section_header]

        if ANALYSIS_DIR.exists():
            md_files = sorted(
                list(ANALYSIS_DIR.glob("*.md")),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            if not md_files:
                user_parts.append("[Không tìm thấy file .md nào trong analysis_user/]")
                toc_entries.append(f"- 🧠 User Ideas: (Không có file)")
            else:
                for file_path in md_files[:MAX_USER_INPUT_FILES]:
                    content, orig_lines = read_user_input_tail(file_path)
                    file_header = f"\n--- 📝 {file_path.name} ({orig_lines} dòng gốc) ---\n"
                    user_parts.append(f"{file_header}\n{content}")
                    tokens = SectionEnricher.estimate_tokens(content)
                    metadata["files_included"].append({
                        "name": f"analysis_user/{file_path.name}",
                        "orig_chars": len(content),
                        "transformed_chars": len(content),
                        "tokens": tokens,
                    })
                    metadata["total_chars"] += len(content)
                    metadata["total_tokens"] += tokens
                    toc_entries.append(
                        f"- 🧠 {file_path.name} ({len(content):,} ký tự, ~{tokens:,} tokens)"
                    )
        else:
            user_parts.append("[Thư mục analysis_user/ không tồn tại]")
            toc_entries.append(f"- 🧠 User Ideas: (Thư mục không tồn tại)")

        sections.append("\n".join(user_parts))

    # -------------------------------------------------------------------------
    # PIPELINE STAGE 4: ASSEMBLE (Header + ToC + Body + Footer)
    # -------------------------------------------------------------------------
    bundle_hash = hashlib.md5(
        f"{metadata['total_chars']}{metadata['total_tokens']}".encode()
    ).hexdigest()[:8]

    compression_pct = 0
    if metadata["total_original_chars"] > 0:
        compression_pct = (
            (metadata["total_original_chars"] - metadata["total_chars"])
            / metadata["total_original_chars"] * 100
        )

    header = []
    header.append("=" * 60)
    header.append("🌟 SOVEREIGN CONTEXT BUNDLE V3.0 FOR GEMINI 🌟")
    header.append("(Powered by Context Pipeline ETL)")
    header.append("=" * 60)
    header.append("")
    header.append(f"⏰ Timestamp: {metadata['timestamp']}")
    header.append(f"🎯 Mode: {mode.upper()}")
    header.append(f"📦 Tổng ký tự: {metadata['total_chars']:,}")
    header.append(f"📊 Tổng tokens ước tính: ~{metadata['total_tokens']:,} "
                  f"(~{metadata['total_tokens'] / 1_000_000 * 100:.1f}% Gemini 1M window)")
    if compression_pct > 0:
        header.append(f"🗜️ Compression: -{compression_pct:.1f}% "
                      f"(raw {metadata['total_original_chars']:,} → {metadata['total_chars']:,})")
    header.append(f"🔍 Bundle Hash: {bundle_hash}")
    header.append(f"📄 Files included: {len(metadata['files_included'])}")
    header.append(f"❌ Files missing: {len(metadata['files_missing'])}")
    if metadata["files_missing"]:
        header.append(f"   Missing list: {', '.join(metadata['files_missing'])}")
    header.append("")
    header.append("📖 MỤC LỤC (TABLE OF CONTENTS):")
    header.append("\n".join(toc_entries))
    header.append("")
    header.append("-" * 60)
    header.append("HƯỚNG DẪN ĐỌC:")
    header.append("  1. Ưu tiên file [🔴 CRITICAL] trước, rồi [🟡 IMPORTANT], cuối cùng [🟢 OPTIONAL].")
    header.append("  2. Mỗi section có [SUMMARY] và [TOKENS] để định hướng đọc.")
    header.append("  3. Khi đề xuất code, hãy trích dẫn file/section liên quan.")
    header.append("-" * 60)

    full_bundle = "\n".join(header) + "\n" + "\n".join(sections)
    metadata["bundle_hash"] = bundle_hash
    metadata["final_chars"] = len(full_bundle)
    metadata["compression_pct"] = compression_pct

    return full_bundle, metadata


# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    """Hàm main - parse CLI args, chạy pipeline và copy vào clipboard."""
    parser = argparse.ArgumentParser(
        description="Sovereign Context Bundle V3.0 - Gemini Pipeline"
    )
    parser.add_argument(
        "--mode", choices=["full", "arch", "strategy"], default="full",
        help="Chế độ bundle: full (12 file), arch (kiến trúc), strategy (chiến lược)"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("🌟 PREPARE GEMINI CONTEXT V3.0 - PIPELINE ETL 🌟")
    print("=" * 60)
    print(f"⏰ Bắt đầu: {datetime.now().strftime('%H:%M:%S')}")
    print(f"🎯 Mode: {args.mode.upper()}")
    print()

    print("🔄 Pipeline: EXTRACT → TRANSFORM → ENRICH → ASSEMBLE...")
    full_context, metadata = gather_context(mode=args.mode)

    print(f"✅ Pipeline hoàn tất!")
    print(f"   📦 Tổng ký tự: {metadata['total_chars']:,}")
    print(f"   📊 Tokens ước tính: ~{metadata['total_tokens']:,} "
          f"({metadata['total_tokens'] / 1_000_000 * 100:.2f}% Gemini 1M)")
    print(f"   🗜️ Compression: -{metadata['compression_pct']:.1f}%")
    print(f"   📄 Files OK: {len(metadata['files_included'])}")
    print(f"   ❌ Files Missing: {len(metadata['files_missing'])}")
    if metadata["files_missing"]:
        print(f"   ⚠️ Missing: {', '.join(metadata['files_missing'])}")
    print(f"   🔍 Hash: {metadata['bundle_hash']}")
    print()

    # Kiểm tra giới hạn tổng bundle
    if metadata["final_chars"] > MAX_TOTAL_BUNDLE:
        print(f"⚠️ CẢNH BÁO: Bundle ({metadata['final_chars']:,}) vượt giới hạn {MAX_TOTAL_BUNDLE:,} ký tự!")
        print(f"   Gemini vẫn nhận được nhưng có thể bị loãng. Khuyên giảm MAX_CHARS_PER_FILE.")
    else:
        print(f"✅ Bundle nằm trong giới hạn an toàn (< {MAX_TOTAL_BUNDLE:,} ký tự)")
    print()

    # Ghi ra file
    output_file = ROOT_DIR / "context_for_gemini.txt"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(full_context)
        print(f"✅ Đã ghi file: {output_file.name} ({len(full_context):,} ký tự)")
    except Exception as e:
        print(f"❌ Lỗi ghi file: {str(e)}")
        return

    # Copy vào clipboard
    print()
    print("📋 Đang copy vào clipboard...")
    try:
        pyperclip.copy(full_context)
        print("✅ ĐÃ SAO CHÉP VÀO CLIPBOARD THÀNH CÔNG!")
        print("   Hãy mở Gemini Web -> Ctrl+V để paste.")
    except pyperclip.PyperclipException:
        print("⚠️ Lỗi Clipboard: Không thể tự động copy.")
        print(f"   Vui lòng mở file '{output_file.name}' để copy thủ công.")
    except Exception as e:
        print(f"⚠️ Lỗi pyperclip: {str(e)}")
        print(f"   Vui lòng mở file '{output_file.name}' để copy thủ công.")

    print()
    print("=" * 60)
    print(f"🎉 HOÀN TẤT V3.0 - {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)


if __name__ == "__main__":
    main()