#!/usr/bin/env python3
"""
parksy.kr Single-File Codex Guard
루트 화이트리스트 / PWA 금지 / pycache 차단 / 공백 파일명 차단
"""

import os
import sys
from pathlib import Path

# === 설정 ===

ROOT_WHITELIST = {
    "index.html",
    "README.md",
    "CNAME",
    ".nojekyll",
    ".gitignore",
    "favicon.ico",
    "favicon.svg",
    "robots.txt",
    "sitemap.xml",
    "feed.xml",
}

ALLOWED_DIRS = {
    "assets",
    "archive",
    "category",
    "docs",
    "backup",
    "scripts",
    ".github",
}

PWA_FORBIDDEN = {
    "sw.js",
    "service-worker.js",
    "manifest.json",
    "manifest.webmanifest",
}

FORBIDDEN_DIRS = {
    "__pycache__",
    "node_modules",
    "build",
    "dist",
    ".cache",
}

# === 검사 함수 ===

def check_root_whitelist(root: Path) -> list[str]:
    """루트 화이트리스트 검사"""
    errors = []
    for item in root.iterdir():
        name = item.name
        if item.is_file():
            if name not in ROOT_WHITELIST:
                # workbox 패턴
                if name.startswith("workbox-"):
                    errors.append(f"❌ PWA 금지 위반: {name}")
                else:
                    errors.append(f"❌ 루트 화이트리스트 위반: {name}")
        elif item.is_dir():
            if name not in ALLOWED_DIRS and not name.startswith("."):
                errors.append(f"❌ 허용되지 않은 루트 폴더: {name}/")
    return errors


def check_pwa_forbidden(root: Path) -> list[str]:
    """PWA 금지 파일 검사"""
    errors = []
    for fname in PWA_FORBIDDEN:
        if (root / fname).exists():
            errors.append(f"❌ PWA 금지 위반: {fname}")
    # workbox 패턴
    for f in root.glob("workbox-*.js"):
        errors.append(f"❌ PWA 금지 위반: {f.name}")
    return errors


def check_forbidden_dirs(root: Path) -> list[str]:
    """금지된 디렉토리 검사 (재귀)"""
    errors = []
    for dname in FORBIDDEN_DIRS:
        found = list(root.rglob(dname))
        for d in found:
            if d.is_dir():
                errors.append(f"❌ 금지 디렉토리: {d.relative_to(root)}/")
    return errors


def check_pyc_files(root: Path) -> list[str]:
    """*.pyc 파일 검사"""
    errors = []
    for f in root.rglob("*.pyc"):
        errors.append(f"❌ .pyc 파일 발견: {f.relative_to(root)}")
    return errors


def check_space_in_filename(root: Path) -> list[str]:
    """루트에 공백 포함 파일명 검사"""
    errors = []
    for item in root.iterdir():
        if " " in item.name:
            errors.append(f"❌ 공백 포함 파일명: {item.name}")
    return errors


# === 메인 ===

def main():
    root = Path(".")
    all_errors = []

    print("=" * 60)
    print("🛡️  parksy.kr Single-File Codex Guard")
    print("=" * 60)
    print()

    # 1. 루트 화이트리스트
    print("[1/5] 루트 화이트리스트 검사...")
    errs = check_root_whitelist(root)
    all_errors.extend(errs)
    print(f"      {'✅ PASS' if not errs else f'❌ {len(errs)} 위반'}")

    # 2. PWA 금지
    print("[2/5] PWA 금지 파일 검사...")
    errs = check_pwa_forbidden(root)
    all_errors.extend(errs)
    print(f"      {'✅ PASS' if not errs else f'❌ {len(errs)} 위반'}")

    # 3. 금지 디렉토리
    print("[3/5] 금지 디렉토리 검사...")
    errs = check_forbidden_dirs(root)
    all_errors.extend(errs)
    print(f"      {'✅ PASS' if not errs else f'❌ {len(errs)} 위반'}")

    # 4. .pyc 파일
    print("[4/5] .pyc 파일 검사...")
    errs = check_pyc_files(root)
    all_errors.extend(errs)
    print(f"      {'✅ PASS' if not errs else f'❌ {len(errs)} 위반'}")

    # 5. 공백 파일명
    print("[5/5] 공백 파일명 검사...")
    errs = check_space_in_filename(root)
    all_errors.extend(errs)
    print(f"      {'✅ PASS' if not errs else f'❌ {len(errs)} 위반'}")

    print()
    print("=" * 60)

    if all_errors:
        print("❌ FAILED - 위반 사항:")
        print()
        for e in all_errors:
            print(f"  {e}")
        print()
        print("위 파일들을 정리한 후 다시 실행하세요.")
        print("=" * 60)
        sys.exit(1)
    else:
        print("✅ ALL PASSED - Single-File Codex 규칙 준수")
        print("=" * 60)
        sys.exit(0)


if __name__ == "__main__":
    main()
