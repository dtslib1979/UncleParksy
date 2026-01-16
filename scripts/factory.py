#!/usr/bin/env python3
"""
DTSLIB Publisher Core - Factory Engine
콘텐츠 공장의 핵심 엔진

사용법:
    python scripts/factory.py throw "오늘 생각한 것..."     # 던지기
    python scripts/factory.py throw --voice recording.m4a  # 음성 던지기
    python scripts/factory.py process                       # 처리하기
    python scripts/factory.py status                        # 상태 보기
    python scripts/factory.py publish src-20250116-001      # 출판하기
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
import hashlib
import re

# === 경로 설정 ===
ROOT = Path(__file__).parent.parent
INBOX = ROOT / "inbox"
PROCESS = ROOT / "process"
OUTPUT = ROOT / "output"
PIPELINES = ROOT / "pipelines"

# === 라우팅 키워드 ===
PARKSY_KEYWORDS = ["일상", "오늘", "생각", "느낌", "실험", "로그", "나는", "감정", "힘들", "좋아", "싫어"]
EAE_KEYWORDS = ["이론", "방법", "체계", "구조", "프레임워크", "모델", "설계", "시스템", "원칙", "정의"]
DTSLIB_KEYWORDS = ["출판", "책", "강좌", "판매", "웹툰", "시리즈", "상품", "강의", "교육", "완성"]


class Factory:
    """콘텐츠 공장"""

    def __init__(self):
        self._ensure_dirs()

    def _ensure_dirs(self):
        """디렉토리 확인"""
        for subdir in ["voice", "text", "visual", "mixed"]:
            (INBOX / subdir).mkdir(parents=True, exist_ok=True)
        for subdir in ["queue", "working", "done"]:
            (PROCESS / subdir).mkdir(parents=True, exist_ok=True)
        for domain in ["parksy", "eae", "dtslib"]:
            (OUTPUT / domain).mkdir(parents=True, exist_ok=True)

    def _generate_id(self) -> str:
        """원석 ID 생성"""
        date = datetime.now().strftime("%Y%m%d")
        # 오늘 생성된 원석 개수 확인
        existing = list(INBOX.rglob(f"src-{date}-*.json"))
        existing += list(PROCESS.rglob(f"src-{date}-*.json"))
        seq = len(existing) + 1
        return f"src-{date}-{seq:03d}"

    def _detect_domain(self, text: str, hint: Optional[str] = None) -> tuple:
        """도메인 감지"""
        if hint and hint in ["parksy", "eae", "dtslib"]:
            return hint, 1.0, f"사용자 지정: {hint}"

        text_lower = text.lower()
        scores = {
            "parksy": sum(1 for kw in PARKSY_KEYWORDS if kw in text_lower),
            "eae": sum(1 for kw in EAE_KEYWORDS if kw in text_lower),
            "dtslib": sum(1 for kw in DTSLIB_KEYWORDS if kw in text_lower)
        }

        total = sum(scores.values())
        if total == 0:
            return "parksy", 0.5, "기본값: 샘에서 시작"

        best = max(scores, key=scores.get)
        confidence = scores[best] / max(total, 1)

        reasons = {
            "parksy": "감정적/개인적 콘텐츠",
            "eae": "구조화/이론화 필요",
            "dtslib": "상품화 가능"
        }

        return best, confidence, reasons[best]

    def _extract_keywords(self, text: str) -> List[str]:
        """키워드 추출 (간단한 버전)"""
        # 한글 명사 추출 (단순화)
        words = re.findall(r'[가-힣]{2,}', text)
        # 빈도 계산
        freq = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
        # 상위 10개
        sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [w for w, _ in sorted_words[:10]]

    def throw(
        self,
        content: str,
        input_type: str = "text",
        mood: Optional[str] = None,
        hint_domain: Optional[str] = None,
        hint_format: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict:
        """원석 던지기"""
        source_id = self._generate_id()

        source = {
            "id": source_id,
            "createdAt": datetime.utcnow().isoformat() + "Z",
            "input": {
                "type": input_type,
                "raw": content,
                "attachments": []
            },
            "emotion": {
                "mood": mood
            } if mood else None,
            "hint": {
                "intendedDomain": hint_domain,
                "intendedFormat": hint_format,
                "tags": tags or [],
                "note": None
            },
            "processing": {
                "status": "inbox"
            },
            "history": [
                {
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "action": "thrown",
                    "details": "원석이 공장에 던져짐"
                }
            ]
        }

        # 저장
        target_dir = INBOX / input_type
        output_file = target_dir / f"{source_id}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(source, f, indent=2, ensure_ascii=False)

        print(f"✨ 원석 던져짐: {source_id}")
        print(f"   위치: {output_file.relative_to(ROOT)}")

        return source

    def process_one(self, source_id: str) -> Dict:
        """단일 원석 처리"""
        # 원석 찾기
        source_file = None
        for pattern in [INBOX, PROCESS / "queue"]:
            for f in pattern.rglob(f"{source_id}.json"):
                source_file = f
                break

        if not source_file:
            raise FileNotFoundError(f"원석을 찾을 수 없음: {source_id}")

        with open(source_file, "r", encoding="utf-8") as f:
            source = json.load(f)

        # 분석
        content = source["input"]["raw"]
        hint_domain = source.get("hint", {}).get("intendedDomain")

        domain, confidence, reason = self._detect_domain(content, hint_domain)
        keywords = self._extract_keywords(content)
        word_count = len(content.split())

        # 제목 추출
        lines = content.strip().split('\n')
        suggested_title = None
        for line in lines[:3]:
            line = line.strip()
            if line.startswith('#'):
                suggested_title = line.lstrip('#').strip()
                break
            elif 5 < len(line) < 80:
                suggested_title = line[:50]
                break

        # 처리 결과 저장
        source["processing"] = {
            "status": "routed",
            "analysis": {
                "detectedLanguage": "ko",
                "wordCount": word_count,
                "keywords": keywords,
                "suggestedTitle": suggested_title
            },
            "routing": {
                "domain": domain,
                "confidence": confidence,
                "reason": reason,
                "suggestedFormats": self._suggest_formats(domain, word_count)
            },
            "processedAt": datetime.utcnow().isoformat() + "Z",
            "processedBy": "factory-engine-v1"
        }

        source["history"].append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": "processed",
            "details": f"라우팅됨 → {domain} (신뢰도: {confidence:.2f})"
        })

        # done 폴더로 이동
        done_file = PROCESS / "done" / f"{source_id}.json"
        with open(done_file, "w", encoding="utf-8") as f:
            json.dump(source, f, indent=2, ensure_ascii=False)

        # 원본 삭제
        source_file.unlink()

        print(f"⚙️  처리 완료: {source_id}")
        print(f"   → 도메인: {domain}")
        print(f"   → 신뢰도: {confidence:.2f}")
        print(f"   → 이유: {reason}")
        print(f"   → 키워드: {', '.join(keywords[:5])}")

        return source

    def _suggest_formats(self, domain: str, word_count: int) -> List[str]:
        """도메인과 길이에 따른 포맷 제안"""
        if domain == "parksy":
            if word_count < 200:
                return ["log", "thought"]
            else:
                return ["essay", "log"]
        elif domain == "eae":
            if word_count < 500:
                return ["note", "definition"]
            else:
                return ["theory", "framework"]
        else:  # dtslib
            if word_count < 1000:
                return ["article", "tutorial"]
            else:
                return ["ebook-chapter", "course-script"]

    def process_all(self) -> List[Dict]:
        """인박스의 모든 원석 처리"""
        results = []
        for input_type in ["text", "voice", "visual", "mixed"]:
            inbox_dir = INBOX / input_type
            for f in inbox_dir.glob("src-*.json"):
                source_id = f.stem
                try:
                    result = self.process_one(source_id)
                    results.append(result)
                except Exception as e:
                    print(f"❌ 처리 실패: {source_id} - {e}")
        return results

    def status(self) -> Dict:
        """공장 상태"""
        inbox_count = sum(len(list((INBOX / t).glob("*.json"))) for t in ["text", "voice", "visual", "mixed"])
        queue_count = len(list((PROCESS / "queue").glob("*.json")))
        done_count = len(list((PROCESS / "done").glob("*.json")))

        domain_counts = {}
        for domain in ["parksy", "eae", "dtslib"]:
            domain_counts[domain] = len(list((OUTPUT / domain).glob("*"))) - 1  # TEMPLATE.md 제외

        # 라우팅 통계
        routing_stats = {"parksy": 0, "eae": 0, "dtslib": 0}
        for f in (PROCESS / "done").glob("*.json"):
            with open(f, "r", encoding="utf-8") as fp:
                data = json.load(fp)
                domain = data.get("processing", {}).get("routing", {}).get("domain")
                if domain in routing_stats:
                    routing_stats[domain] += 1

        return {
            "inbox": inbox_count,
            "queue": queue_count,
            "processed": done_count,
            "output": domain_counts,
            "routing": routing_stats,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    def publish(self, source_id: str) -> Dict:
        """원석을 출판물로 변환"""
        # 처리된 원석 찾기
        source_file = PROCESS / "done" / f"{source_id}.json"
        if not source_file.exists():
            raise FileNotFoundError(f"처리된 원석을 찾을 수 없음: {source_id}")

        with open(source_file, "r", encoding="utf-8") as f:
            source = json.load(f)

        domain = source["processing"]["routing"]["domain"]
        suggested_title = source["processing"]["analysis"].get("suggestedTitle", "제목 없음")
        content = source["input"]["raw"]

        # 출력 파일 생성
        date_str = datetime.now().strftime("%Y-%m-%d")
        slug = re.sub(r'[^가-힣a-z0-9]+', '-', suggested_title.lower())[:30]
        output_filename = f"{date_str}-{slug}.md"
        output_path = OUTPUT / domain / output_filename

        # 템플릿 적용
        if domain == "parksy":
            output_content = f"""---
domain: parksy
type: log
source: {source_id}
created: {source['createdAt']}
published: {datetime.utcnow().isoformat()}Z
mood: {source.get('emotion', {}).get('mood', 'unknown')}
tags: {source['processing']['analysis']['keywords'][:5]}
---

# {suggested_title}

{content}

---

> 이 글은 parksy.kr에서 태어났습니다.
> 날것 그대로, 오늘의 나.
"""
        elif domain == "eae":
            output_content = f"""---
domain: eae
type: note
source: {source_id}
created: {source['createdAt']}
published: {datetime.utcnow().isoformat()}Z
framework: EduArt
tags: {source['processing']['analysis']['keywords'][:5]}
reusable: true
---

# {suggested_title}

## 개요

{content[:500]}...

## 구조

(구조화 필요)

## 적용

(적용 방안)

---

> EduArt Engineer Framework
> Beyond AI — 설명 가능한 형태로.
"""
        else:  # dtslib
            output_content = f"""---
domain: dtslib
type: draft
source: {source_id}
created: {source['createdAt']}
published: {datetime.utcnow().isoformat()}Z
product_id: null
status: draft
---

# {suggested_title}

## 소개

{content}

## 구매/이용

(상품화 준비 중)

---

© DTSLIB Publishing
"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output_content)

        # 원석 업데이트
        source["output"] = {
            "domain": domain,
            "format": "markdown",
            "path": str(output_path.relative_to(ROOT)),
            "publishedAt": datetime.utcnow().isoformat() + "Z"
        }
        source["processing"]["status"] = "published"
        source["history"].append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": "published",
            "details": f"출판됨 → {domain}/{output_filename}"
        })

        with open(source_file, "w", encoding="utf-8") as f:
            json.dump(source, f, indent=2, ensure_ascii=False)

        print(f"📚 출판 완료: {source_id}")
        print(f"   → 도메인: {domain}")
        print(f"   → 파일: {output_path.relative_to(ROOT)}")

        return source


def main():
    parser = argparse.ArgumentParser(
        description="DTSLIB Publisher Core - Factory Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  %(prog)s throw "오늘 느낀 것..."              # 텍스트 던지기
  %(prog)s throw -m excited "아이디어!"        # 감정과 함께 던지기
  %(prog)s throw -d eae "이론 정리..."         # 도메인 힌트와 함께
  %(prog)s process                              # 모든 인박스 처리
  %(prog)s status                               # 공장 상태 확인
  %(prog)s publish src-20250116-001             # 출판하기
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="명령")

    # throw
    throw_parser = subparsers.add_parser("throw", help="원석 던지기")
    throw_parser.add_argument("content", nargs="?", help="던질 내용")
    throw_parser.add_argument("-f", "--file", type=Path, help="파일에서 읽기")
    throw_parser.add_argument("-t", "--type", default="text",
        choices=["text", "voice", "visual", "mixed"], help="입력 타입")
    throw_parser.add_argument("-m", "--mood",
        choices=["excited", "calm", "frustrated", "curious", "urgent", "reflective"],
        help="감정 상태")
    throw_parser.add_argument("-d", "--domain",
        choices=["parksy", "eae", "dtslib"], help="도메인 힌트")
    throw_parser.add_argument("--tags", nargs="+", help="태그")

    # process
    process_parser = subparsers.add_parser("process", help="원석 처리하기")
    process_parser.add_argument("source_id", nargs="?", help="특정 원석 ID (없으면 전체)")

    # status
    subparsers.add_parser("status", help="공장 상태 확인")

    # publish
    publish_parser = subparsers.add_parser("publish", help="출판하기")
    publish_parser.add_argument("source_id", help="원석 ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    factory = Factory()

    print()
    print("═" * 50)
    print("  DTSLIB Publisher Core - Factory Engine")
    print("═" * 50)
    print()

    if args.command == "throw":
        content = args.content
        if args.file:
            with open(args.file, "r", encoding="utf-8") as f:
                content = f.read()

        if not content:
            print("❌ 던질 내용이 없습니다.")
            sys.exit(1)

        factory.throw(
            content=content,
            input_type=args.type,
            mood=args.mood,
            hint_domain=args.domain,
            tags=args.tags
        )

    elif args.command == "process":
        if args.source_id:
            factory.process_one(args.source_id)
        else:
            results = factory.process_all()
            print(f"\n총 {len(results)}개 원석 처리됨")

    elif args.command == "status":
        status = factory.status()
        print("📊 공장 상태")
        print()
        print(f"  인박스: {status['inbox']}개")
        print(f"  대기열: {status['queue']}개")
        print(f"  처리됨: {status['processed']}개")
        print()
        print("  라우팅 현황:")
        for domain, count in status['routing'].items():
            bar = "█" * count + "░" * (10 - min(count, 10))
            print(f"    {domain:8} [{bar}] {count}")
        print()
        print("  출판 현황:")
        for domain, count in status['output'].items():
            print(f"    {domain:8}: {count}개")

    elif args.command == "publish":
        factory.publish(args.source_id)

    print()
    print("═" * 50)


if __name__ == "__main__":
    main()
