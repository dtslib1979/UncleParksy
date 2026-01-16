#!/usr/bin/env python3
"""
DTSLIB Media Empire - AI Processing Pipeline
콘텐츠 자동 처리 및 라우팅 시스템

사용법:
    python scripts/ai_pipeline.py process --input inbox/
    python scripts/ai_pipeline.py route --content-id src-xxx
    python scripts/ai_pipeline.py status
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import hashlib

# === 설정 ===

DATA_DIR = Path(__file__).parent.parent / "data"
INBOX_DIR = DATA_DIR / "inbox"
PROCESSED_DIR = DATA_DIR / "processed"
CONFIG_DIR = DATA_DIR / "config"

# 도메인 라우팅 키워드
ROUTING_KEYWORDS = {
    "parksy.kr": [
        "일상", "실험", "개인", "로그", "일기", "생각", "감상",
        "daily", "personal", "experiment", "log", "thought"
    ],
    "eae.kr": [
        "이론", "철학", "모델", "체계", "선언", "교육", "프레임워크",
        "theory", "philosophy", "model", "manifesto", "framework"
    ],
    "dtslib.kr": [
        "출판", "책", "강좌", "웹툰", "시리즈", "튜토리얼", "리뷰",
        "publish", "book", "course", "webtoon", "series", "tutorial"
    ],
    "dtslib.com": [
        "비즈니스", "포트폴리오", "서비스", "클라이언트", "문의",
        "business", "portfolio", "service", "client", "contact"
    ]
}

# 콘텐츠 타입 키워드
CONTENT_TYPE_KEYWORDS = {
    "ebook": ["책", "전자책", "ebook", "book", "chapter", "챕터"],
    "webtoon": ["웹툰", "만화", "그림", "패널", "webtoon", "comic", "panel"],
    "audiobook": ["오디오북", "낭독", "audiobook", "narration"],
    "video-course": ["강좌", "강의", "튜토리얼", "course", "lecture", "tutorial"],
    "web-novel": ["웹소설", "소설", "novel", "fiction", "연재"],
    "blog-post": ["블로그", "포스트", "글", "blog", "post", "article"],
    "vlog": ["브이로그", "일상", "vlog", "daily"]
}


class AIProcessingPipeline:
    """AI 콘텐츠 처리 파이프라인"""

    def __init__(self):
        self.ensure_directories()
        self.universe_config = self.load_universe_config()

    def ensure_directories(self):
        """필수 디렉토리 생성"""
        for subdir in ["text", "voice", "visual"]:
            (INBOX_DIR / subdir).mkdir(parents=True, exist_ok=True)
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    def load_universe_config(self) -> Dict:
        """유니버스 설정 로드"""
        config_file = CONFIG_DIR / "universe.json"
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def generate_id(self, prefix: str = "src") -> str:
        """고유 ID 생성"""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        random_part = hashlib.md5(str(datetime.utcnow().timestamp()).encode()).hexdigest()[:6]
        return f"{prefix}-{timestamp}-{random_part}"

    def detect_content_type(self, text: str) -> Tuple[str, float]:
        """콘텐츠 타입 감지"""
        text_lower = text.lower()
        scores = {}

        for content_type, keywords in CONTENT_TYPE_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[content_type] = score

        if not scores:
            return "blog-post", 0.5  # 기본값

        best_type = max(scores, key=scores.get)
        confidence = min(scores[best_type] / 5, 1.0)
        return best_type, confidence

    def detect_domain(self, text: str, content_type: str) -> Tuple[str, float]:
        """라우팅 도메인 감지"""
        text_lower = text.lower()
        scores = {}

        for domain, keywords in ROUTING_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            scores[domain] = score

        # 콘텐츠 타입에 따른 가중치
        type_domain_weights = {
            "ebook": {"dtslib.kr": 3},
            "webtoon": {"dtslib.kr": 3},
            "audiobook": {"dtslib.kr": 3},
            "video-course": {"dtslib.kr": 3},
            "web-novel": {"dtslib.kr": 2},
            "blog-post": {"parksy.kr": 2},
            "vlog": {"parksy.kr": 3},
        }

        if content_type in type_domain_weights:
            for domain, weight in type_domain_weights[content_type].items():
                scores[domain] = scores.get(domain, 0) + weight

        if not any(scores.values()):
            return "parksy.kr", 0.5  # 기본값

        best_domain = max(scores, key=scores.get)
        total = sum(scores.values())
        confidence = scores[best_domain] / total if total > 0 else 0.5
        return best_domain, confidence

    def extract_metadata(self, text: str) -> Dict:
        """텍스트에서 메타데이터 추출"""
        word_count = len(text.split())

        # 언어 감지 (간단한 휴리스틱)
        korean_chars = len(re.findall(r'[가-힣]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        language = "ko" if korean_chars > english_chars else "en"

        # 태그 추출 (해시태그)
        tags = re.findall(r'#(\w+)', text)

        # 제목 추출 (첫 줄 또는 # 헤딩)
        lines = text.strip().split('\n')
        title = None
        for line in lines[:5]:
            line = line.strip()
            if line.startswith('# '):
                title = line[2:].strip()
                break
            elif len(line) > 5 and len(line) < 100:
                title = line
                break

        return {
            "wordCount": word_count,
            "language": language,
            "tags": tags,
            "suggestedTitle": title,
            "estimatedReadTime": word_count // 200  # 분
        }

    def process_text_content(self, file_path: Path) -> Dict:
        """텍스트 콘텐츠 처리"""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        content_id = self.generate_id("src")
        metadata = self.extract_metadata(content)
        content_type, type_confidence = self.detect_content_type(content)
        domain, domain_confidence = self.detect_domain(content, content_type)

        result = {
            "id": content_id,
            "type": "text",
            "origin": "manual",
            "sourcePath": str(file_path),
            "rawContent": content,
            "metadata": metadata,
            "aiProcessing": {
                "transcribed": False,
                "summarized": False,
                "categorized": True,
                "processedAt": datetime.utcnow().isoformat() + "Z",
                "model": "rule-based"
            },
            "contentAnalysis": {
                "detectedType": content_type,
                "typeConfidence": type_confidence
            },
            "routing": {
                "suggestedDomain": domain,
                "suggestedFormat": content_type,
                "confidence": domain_confidence
            },
            "createdAt": datetime.utcnow().isoformat() + "Z",
            "status": "processed"
        }

        return result

    def save_processed(self, data: Dict) -> Path:
        """처리된 데이터 저장"""
        output_file = PROCESSED_DIR / f"{data['id']}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return output_file

    def process_inbox(self) -> List[Dict]:
        """인박스의 모든 파일 처리"""
        results = []

        # 텍스트 파일 처리
        text_dir = INBOX_DIR / "text"
        for file_path in text_dir.glob("*.txt"):
            print(f"처리 중: {file_path.name}")
            try:
                result = self.process_text_content(file_path)
                self.save_processed(result)
                results.append(result)

                # 처리 완료 후 파일 이동
                processed_inbox = INBOX_DIR / "processed"
                processed_inbox.mkdir(exist_ok=True)
                file_path.rename(processed_inbox / file_path.name)

                print(f"  → 타입: {result['contentAnalysis']['detectedType']}")
                print(f"  → 도메인: {result['routing']['suggestedDomain']}")
            except Exception as e:
                print(f"  → 오류: {e}")

        # 마크다운 파일 처리
        for file_path in text_dir.glob("*.md"):
            print(f"처리 중: {file_path.name}")
            try:
                result = self.process_text_content(file_path)
                self.save_processed(result)
                results.append(result)

                processed_inbox = INBOX_DIR / "processed"
                processed_inbox.mkdir(exist_ok=True)
                file_path.rename(processed_inbox / file_path.name)

                print(f"  → 타입: {result['contentAnalysis']['detectedType']}")
                print(f"  → 도메인: {result['routing']['suggestedDomain']}")
            except Exception as e:
                print(f"  → 오류: {e}")

        return results

    def get_status(self) -> Dict:
        """파이프라인 상태 조회"""
        inbox_count = {
            "text": len(list((INBOX_DIR / "text").glob("*.*"))),
            "voice": len(list((INBOX_DIR / "voice").glob("*.*"))),
            "visual": len(list((INBOX_DIR / "visual").glob("*.*")))
        }

        processed_count = len(list(PROCESSED_DIR.glob("*.json")))

        # 도메인별 라우팅 현황
        domain_counts = {"parksy.kr": 0, "eae.kr": 0, "dtslib.kr": 0, "dtslib.com": 0}
        for f in PROCESSED_DIR.glob("*.json"):
            try:
                with open(f, "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                    domain = data.get("routing", {}).get("suggestedDomain", "unknown")
                    if domain in domain_counts:
                        domain_counts[domain] += 1
            except:
                pass

        return {
            "inbox": inbox_count,
            "processed": processed_count,
            "byDomain": domain_counts,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }


def main():
    parser = argparse.ArgumentParser(description="DTSLIB AI Processing Pipeline")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # process 명령
    process_parser = subparsers.add_parser("process", help="인박스 콘텐츠 처리")
    process_parser.add_argument("--input", "-i", type=Path, help="입력 디렉토리")

    # route 명령
    route_parser = subparsers.add_parser("route", help="콘텐츠 라우팅")
    route_parser.add_argument("--content-id", "-c", help="콘텐츠 ID")

    # status 명령
    subparsers.add_parser("status", help="파이프라인 상태 조회")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    pipeline = AIProcessingPipeline()

    print("=" * 60)
    print("DTSLIB AI Processing Pipeline")
    print("=" * 60)
    print()

    if args.command == "process":
        results = pipeline.process_inbox()
        print()
        print(f"처리 완료: {len(results)}개 콘텐츠")

    elif args.command == "status":
        status = pipeline.get_status()
        print("인박스 현황:")
        for key, count in status["inbox"].items():
            print(f"  {key}: {count}개")
        print()
        print(f"처리됨: {status['processed']}개")
        print()
        print("도메인별 라우팅:")
        for domain, count in status["byDomain"].items():
            print(f"  {domain}: {count}개")

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
