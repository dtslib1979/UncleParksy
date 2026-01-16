#!/usr/bin/env python3
"""
PARKSY Publisher Platform - Media Pipeline
텍스트 → 글 → 영상 → 스토리 자동화 파이프라인

사용법:
    python scripts/media_pipeline.py --input content.md --persona Philosopher-Parksy
    python scripts/media_pipeline.py --batch /path/to/content/
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
import hashlib

# === 설정 ===

DATA_DIR = Path(__file__).parent.parent / "data"
PUB_DIR = DATA_DIR / "publications"
API_DIR = Path(__file__).parent.parent / "api" / "v1"

PERSONAS = [
    "Philosopher-Parksy",
    "Technician-Parksy",
    "Visualizer-Parksy",
    "Musician-Parksy",
    "Protocol-Parksy",
    "Blogger-Parksy",
    "Orbit-Log",
    "Tester-Parksy",
]

PUBLICATION_TYPES = [
    "article",
    "essay",
    "tutorial",
    "review",
    "series-chapter",
    "listening-guide",
]


class MediaPipeline:
    """미디어 파이프라인 처리기"""

    def __init__(self):
        self.ensure_directories()

    def ensure_directories(self):
        """필수 디렉토리 확인"""
        PUB_DIR.mkdir(parents=True, exist_ok=True)
        API_DIR.mkdir(parents=True, exist_ok=True)

    def generate_id(self, title: str) -> str:
        """고유 ID 생성"""
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower())[:30].strip("-")
        short_hash = hashlib.md5(f"{title}{datetime.utcnow().isoformat()}".encode()).hexdigest()[:6]
        return f"pub-{date_str}-{slug}-{short_hash}"

    def parse_markdown(self, content: str) -> Dict:
        """마크다운 콘텐츠 파싱"""
        lines = content.strip().split("\n")
        metadata = {}
        body_lines = []
        in_frontmatter = False
        frontmatter_done = False

        for line in lines:
            if line.strip() == "---":
                if not frontmatter_done:
                    in_frontmatter = not in_frontmatter
                    if not in_frontmatter:
                        frontmatter_done = True
                    continue

            if in_frontmatter:
                if ":" in line:
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip().strip('"').strip("'")
            else:
                body_lines.append(line)

        body = "\n".join(body_lines).strip()

        # 제목 추출 (첫 번째 # 헤딩)
        title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        if title_match and "title" not in metadata:
            metadata["title"] = title_match.group(1)
            body = body.replace(title_match.group(0), "", 1).strip()

        return {
            "metadata": metadata,
            "body": body,
        }

    def extract_media_links(self, content: str) -> Dict:
        """콘텐츠에서 미디어 링크 추출"""
        youtube_videos = []
        spotify_links = []
        images = []

        # YouTube 링크
        yt_patterns = [
            r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([A-Za-z0-9_-]{11})",
            r"(?:https?://)?(?:www\.)?youtu\.be/([A-Za-z0-9_-]{11})",
            r"(?:https?://)?(?:www\.)?youtube\.com/embed/([A-Za-z0-9_-]{11})",
        ]

        for pattern in yt_patterns:
            for match in re.finditer(pattern, content):
                video_id = match.group(1)
                if video_id not in [v["videoId"] for v in youtube_videos]:
                    youtube_videos.append({
                        "videoId": video_id,
                        "role": "main" if not youtube_videos else "supplement",
                    })

        # Spotify 링크
        sp_patterns = [
            r"(?:https?://)?open\.spotify\.com/(track|album|playlist|artist)/([A-Za-z0-9]+)",
            r"spotify:(track|album|playlist|artist):([A-Za-z0-9]+)",
        ]

        for pattern in sp_patterns:
            for match in re.finditer(pattern, content):
                sp_type = match.group(1)
                sp_id = match.group(2)
                if sp_id not in [s["spotifyId"] for s in spotify_links]:
                    spotify_links.append({
                        "spotifyId": sp_id,
                        "type": sp_type,
                        "role": "main" if not spotify_links else "background",
                    })

        # 이미지 링크
        img_pattern = r"!\[.*?\]\((.+?)\)"
        for match in re.finditer(img_pattern, content):
            img_url = match.group(1)
            if img_url not in images:
                images.append(img_url)

        return {
            "youtube": youtube_videos,
            "spotify": spotify_links,
            "images": images,
        }

    def create_publication(
        self,
        content: str,
        persona: Optional[str] = None,
        pub_type: str = "article",
        status: str = "draft",
        series_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Dict:
        """출판물 생성"""
        parsed = self.parse_markdown(content)
        metadata = parsed["metadata"]
        body = parsed["body"]

        # 미디어 링크 추출
        media = self.extract_media_links(content)

        # 메타데이터에서 값 가져오기 (우선순위)
        title = metadata.get("title", "Untitled")
        subtitle = metadata.get("subtitle", "")
        persona = metadata.get("persona", persona)
        pub_type = metadata.get("type", pub_type)
        tags = metadata.get("tags", "").split(",") if metadata.get("tags") else (tags or [])
        tags = [t.strip() for t in tags if t.strip()]

        # ID 생성
        pub_id = self.generate_id(title)

        # 발췌문 생성
        excerpt = body[:300].rsplit(" ", 1)[0] + "..." if len(body) > 300 else body

        # 출판물 객체 생성
        now = datetime.utcnow().isoformat() + "Z"

        publication = {
            "id": pub_id,
            "title": title,
            "subtitle": subtitle,
            "type": pub_type,
            "status": status,
            "persona": persona,
            "content": {
                "body": body,
                "format": "markdown",
                "excerpt": excerpt,
            },
            "media": media,
            "series": {"id": series_id} if series_id else None,
            "tags": tags,
            "createdAt": now,
            "updatedAt": now,
            "publishedAt": now if status == "published" else None,
        }

        return publication

    def save_publication(self, publication: Dict) -> Path:
        """출판물 저장"""
        pub_file = PUB_DIR / f"{publication['id']}.json"

        with open(pub_file, "w", encoding="utf-8") as f:
            json.dump(publication, f, indent=2, ensure_ascii=False)

        print(f"[OK] 출판물 저장: {pub_file.name}")
        return pub_file

    def update_index(self) -> None:
        """출판물 인덱스 업데이트"""
        publications = []

        for f in PUB_DIR.glob("pub-*.json"):
            try:
                with open(f, "r", encoding="utf-8") as fp:
                    pub = json.load(fp)
                    publications.append(pub)
            except json.JSONDecodeError as e:
                print(f"[WARN] JSON 파싱 실패: {f.name} - {e}")
                continue

        # 날짜순 정렬
        publications.sort(key=lambda x: x.get("createdAt", ""), reverse=True)

        # 인덱스 저장
        index_data = {
            "$schema": "../config/schemas.json#/schemas/publication",
            "collection": "publications",
            "version": "1.0.0",
            "count": len(publications),
            "lastUpdated": datetime.utcnow().isoformat() + "Z",
            "items": publications,
        }

        index_file = PUB_DIR / "index.json"
        with open(index_file, "w", encoding="utf-8") as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)

        # API 엔드포인트 업데이트
        published = [p for p in publications if p.get("status") == "published"]
        api_data = {
            "success": True,
            "data": {
                "publications": published[:20],
                "total": len(published),
                "page": 1,
                "perPage": 20,
            },
            "meta": {
                "generatedAt": datetime.utcnow().isoformat() + "Z",
                "source": "/data/publications/index.json",
            },
        }

        api_file = API_DIR / "publications.json"
        with open(api_file, "w", encoding="utf-8") as f:
            json.dump(api_data, f, indent=2, ensure_ascii=False)

        print(f"[OK] 인덱스 업데이트: {len(publications)}개 출판물")

    def process_file(self, file_path: Path, **kwargs) -> Optional[Dict]:
        """파일 처리"""
        if not file_path.exists():
            print(f"[ERROR] 파일 없음: {file_path}")
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        publication = self.create_publication(content, **kwargs)
        self.save_publication(publication)
        return publication

    def process_batch(self, directory: Path, **kwargs) -> List[Dict]:
        """디렉토리 내 모든 마크다운 파일 처리"""
        publications = []

        for file_path in sorted(directory.glob("*.md")):
            print(f"\n처리 중: {file_path.name}")
            pub = self.process_file(file_path, **kwargs)
            if pub:
                publications.append(pub)

        self.update_index()
        return publications


def main():
    parser = argparse.ArgumentParser(description="PARKSY Media Pipeline")
    parser.add_argument("--input", "-i", type=Path, help="입력 마크다운 파일")
    parser.add_argument("--batch", "-b", type=Path, help="배치 처리할 디렉토리")
    parser.add_argument("--persona", "-p", choices=PERSONAS, help="페르소나 지정")
    parser.add_argument("--type", "-t", choices=PUBLICATION_TYPES, default="article", help="출판물 타입")
    parser.add_argument("--status", "-s", choices=["draft", "published"], default="draft", help="상태")
    parser.add_argument("--series", help="시리즈 ID")
    parser.add_argument("--tags", help="태그 (쉼표로 구분)")

    args = parser.parse_args()

    if not args.input and not args.batch:
        parser.print_help()
        print("\n[ERROR] --input 또는 --batch 옵션이 필요합니다.")
        sys.exit(1)

    pipeline = MediaPipeline()

    kwargs = {
        "persona": args.persona,
        "pub_type": args.type,
        "status": args.status,
        "series_id": args.series,
        "tags": args.tags.split(",") if args.tags else None,
    }

    print("=" * 60)
    print("PARKSY Media Pipeline")
    print("=" * 60)

    if args.batch:
        print(f"배치 모드: {args.batch}")
        publications = pipeline.process_batch(args.batch, **kwargs)
        print(f"\n총 {len(publications)}개 출판물 처리 완료")
    else:
        print(f"단일 파일: {args.input}")
        publication = pipeline.process_file(args.input, **kwargs)
        if publication:
            pipeline.update_index()
            print(f"\n출판물 ID: {publication['id']}")

    print("=" * 60)


if __name__ == "__main__":
    main()
