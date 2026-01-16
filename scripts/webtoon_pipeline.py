#!/usr/bin/env python3
"""
DTSLIB Media Empire - Webtoon AI Generation Pipeline
AI 이미지 생성 기반 웹툰 제작 자동화

사용법:
    python scripts/webtoon_pipeline.py new --title "제목" --genre fantasy
    python scripts/webtoon_pipeline.py script --webtoon-id webtoon-xxx --episode 1
    python scripts/webtoon_pipeline.py generate --webtoon-id webtoon-xxx --episode 1
    python scripts/webtoon_pipeline.py status --webtoon-id webtoon-xxx
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

# === 설정 ===

DATA_DIR = Path(__file__).parent.parent / "data"
WEBTOON_DIR = DATA_DIR / "webtoons"
ASSETS_DIR = Path(__file__).parent.parent / "assets" / "webtoons"

# AI 이미지 생성 프롬프트 템플릿
PROMPT_TEMPLATES = {
    "character_sheet": """
Character reference sheet for webtoon:
Name: {name}
Description: {description}
Style: {style}
--
Multiple angles, full body, face close-up, expressions (happy, sad, angry, surprised)
Consistent design, clean lines, webtoon art style
High quality, detailed, white background
    """.strip(),

    "background": """
Webtoon background art:
Setting: {setting}
Mood: {mood}
Time: {time_of_day}
Style: {style}
--
No characters, detailed environment, {perspective} perspective
Webtoon style, clean lines, vibrant colors
{additional_details}
    """.strip(),

    "panel": """
Webtoon panel:
Scene: {scene_description}
Characters: {characters}
Action: {action}
Emotion: {emotion}
Camera: {camera_angle}
Style: {style}
--
Single panel composition, speech bubble space reserved
Dynamic pose, expressive, webtoon art style
High quality, detailed
    """.strip(),

    "cover": """
Webtoon series cover art:
Title: {title}
Genre: {genre}
Main characters: {characters}
Mood: {mood}
--
Vertical format, eye-catching composition
Title space at top, dramatic lighting
Professional webtoon cover quality
    """.strip()
}

# 장르별 기본 스타일
GENRE_STYLES = {
    "fantasy": "epic fantasy webtoon style, magical, detailed backgrounds, vibrant colors",
    "romance": "soft romance manhwa style, warm colors, emotional expressions, beautiful characters",
    "action": "dynamic action webtoon style, bold lines, intense expressions, motion effects",
    "comedy": "expressive comedy manhwa style, exaggerated expressions, bright colors",
    "drama": "realistic drama webtoon style, subtle emotions, cinematic compositions",
    "slice-of-life": "warm slice-of-life manhwa style, cozy atmosphere, soft lighting",
    "educational": "clean educational webtoon style, clear visuals, friendly characters"
}


class WebtoonPipeline:
    """웹툰 AI 생성 파이프라인"""

    def __init__(self):
        self.ensure_directories()

    def ensure_directories(self):
        """필수 디렉토리 생성"""
        WEBTOON_DIR.mkdir(parents=True, exist_ok=True)
        ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    def generate_id(self) -> str:
        """웹툰 ID 생성"""
        timestamp = datetime.utcnow().strftime("%Y%m%d")
        random_part = hashlib.md5(str(datetime.utcnow().timestamp()).encode()).hexdigest()[:6]
        return f"webtoon-{timestamp}-{random_part}"

    def create_webtoon(
        self,
        title: str,
        genre: str,
        synopsis: str = "",
        target_audience: str = "all-ages"
    ) -> Dict:
        """새 웹툰 프로젝트 생성"""
        webtoon_id = self.generate_id()
        style = GENRE_STYLES.get(genre, GENRE_STYLES["drama"])

        webtoon = {
            "id": webtoon_id,
            "title": title,
            "subtitle": "",
            "genre": genre,
            "synopsis": synopsis,
            "targetAudience": target_audience,
            "characters": [],
            "episodes": [],
            "style": {
                "artStyle": style,
                "colorPalette": [],
                "aiModel": "midjourney",
                "basePrompt": f"{style}, consistent character design"
            },
            "publishing": {
                "platforms": [],
                "schedule": "weekly"
            },
            "status": "planning",
            "createdAt": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        }

        # 웹툰 디렉토리 생성
        webtoon_path = WEBTOON_DIR / webtoon_id
        webtoon_path.mkdir(exist_ok=True)
        (webtoon_path / "characters").mkdir(exist_ok=True)
        (webtoon_path / "backgrounds").mkdir(exist_ok=True)
        (webtoon_path / "episodes").mkdir(exist_ok=True)

        # 메타데이터 저장
        self.save_webtoon(webtoon)

        return webtoon

    def save_webtoon(self, webtoon: Dict) -> Path:
        """웹툰 메타데이터 저장"""
        webtoon["updatedAt"] = datetime.utcnow().isoformat() + "Z"
        webtoon_path = WEBTOON_DIR / webtoon["id"]
        meta_file = webtoon_path / "metadata.json"

        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(webtoon, f, indent=2, ensure_ascii=False)

        return meta_file

    def load_webtoon(self, webtoon_id: str) -> Optional[Dict]:
        """웹툰 메타데이터 로드"""
        meta_file = WEBTOON_DIR / webtoon_id / "metadata.json"
        if not meta_file.exists():
            return None

        with open(meta_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def add_character(
        self,
        webtoon_id: str,
        name: str,
        description: str,
        role: str = "supporting"
    ) -> Dict:
        """캐릭터 추가"""
        webtoon = self.load_webtoon(webtoon_id)
        if not webtoon:
            raise ValueError(f"웹툰을 찾을 수 없습니다: {webtoon_id}")

        char_id = f"char-{hashlib.md5(name.encode()).hexdigest()[:8]}"

        character = {
            "id": char_id,
            "name": name,
            "description": description,
            "role": role,
            "visualPrompt": self.generate_character_prompt(name, description, webtoon["style"]["artStyle"]),
            "referenceImages": [],
            "status": "pending"
        }

        webtoon["characters"].append(character)
        self.save_webtoon(webtoon)

        return character

    def generate_character_prompt(self, name: str, description: str, style: str) -> str:
        """캐릭터 시트 프롬프트 생성"""
        return PROMPT_TEMPLATES["character_sheet"].format(
            name=name,
            description=description,
            style=style
        )

    def create_episode(
        self,
        webtoon_id: str,
        episode_number: int,
        title: str,
        script: str = ""
    ) -> Dict:
        """에피소드 생성"""
        webtoon = self.load_webtoon(webtoon_id)
        if not webtoon:
            raise ValueError(f"웹툰을 찾을 수 없습니다: {webtoon_id}")

        episode = {
            "number": episode_number,
            "title": title,
            "script": script,
            "panels": [],
            "status": "script" if script else "planning",
            "createdAt": datetime.utcnow().isoformat() + "Z"
        }

        # 기존 에피소드 업데이트 또는 추가
        existing_idx = next(
            (i for i, ep in enumerate(webtoon["episodes"]) if ep["number"] == episode_number),
            None
        )

        if existing_idx is not None:
            webtoon["episodes"][existing_idx] = episode
        else:
            webtoon["episodes"].append(episode)
            webtoon["episodes"].sort(key=lambda x: x["number"])

        # 에피소드 디렉토리 생성
        ep_dir = WEBTOON_DIR / webtoon_id / "episodes" / f"ep{episode_number:03d}"
        ep_dir.mkdir(exist_ok=True)

        self.save_webtoon(webtoon)
        return episode

    def parse_script_to_panels(self, script: str) -> List[Dict]:
        """스크립트를 패널로 파싱"""
        panels = []
        current_panel = None

        # 간단한 스크립트 형식:
        # [패널 1]
        # 장면: 거리, 낮
        # 캐릭터: 주인공
        # 대사: "안녕하세요!"
        # 행동: 손을 흔든다

        lines = script.strip().split('\n')
        panel_pattern = re.compile(r'\[패널\s*(\d+)\]|\[Panel\s*(\d+)\]', re.IGNORECASE)

        for line in lines:
            line = line.strip()
            if not line:
                continue

            panel_match = panel_pattern.match(line)
            if panel_match:
                if current_panel:
                    panels.append(current_panel)

                panel_num = panel_match.group(1) or panel_match.group(2)
                current_panel = {
                    "order": int(panel_num),
                    "description": "",
                    "dialogue": [],
                    "characters": "",
                    "action": "",
                    "emotion": "",
                    "cameraAngle": "medium shot",
                    "imagePath": None,
                    "aiPrompt": None,
                    "generated": False
                }
            elif current_panel:
                if line.startswith("장면:") or line.startswith("Scene:"):
                    current_panel["description"] = line.split(":", 1)[1].strip()
                elif line.startswith("캐릭터:") or line.startswith("Characters:"):
                    current_panel["characters"] = line.split(":", 1)[1].strip()
                elif line.startswith("대사:") or line.startswith("Dialogue:"):
                    dialogue = line.split(":", 1)[1].strip().strip('"')
                    current_panel["dialogue"].append(dialogue)
                elif line.startswith("행동:") or line.startswith("Action:"):
                    current_panel["action"] = line.split(":", 1)[1].strip()
                elif line.startswith("감정:") or line.startswith("Emotion:"):
                    current_panel["emotion"] = line.split(":", 1)[1].strip()
                elif line.startswith("카메라:") or line.startswith("Camera:"):
                    current_panel["cameraAngle"] = line.split(":", 1)[1].strip()

        if current_panel:
            panels.append(current_panel)

        return panels

    def generate_panel_prompts(self, webtoon_id: str, episode_number: int) -> List[Dict]:
        """에피소드의 모든 패널에 대한 AI 프롬프트 생성"""
        webtoon = self.load_webtoon(webtoon_id)
        if not webtoon:
            raise ValueError(f"웹툰을 찾을 수 없습니다: {webtoon_id}")

        episode = next(
            (ep for ep in webtoon["episodes"] if ep["number"] == episode_number),
            None
        )
        if not episode:
            raise ValueError(f"에피소드를 찾을 수 없습니다: {episode_number}")

        style = webtoon["style"]["artStyle"]

        for panel in episode["panels"]:
            prompt = PROMPT_TEMPLATES["panel"].format(
                scene_description=panel.get("description", ""),
                characters=panel.get("characters", ""),
                action=panel.get("action", "standing"),
                emotion=panel.get("emotion", "neutral"),
                camera_angle=panel.get("cameraAngle", "medium shot"),
                style=style
            )
            panel["aiPrompt"] = prompt

        self.save_webtoon(webtoon)
        return episode["panels"]

    def export_prompts(self, webtoon_id: str, episode_number: int) -> Path:
        """프롬프트를 텍스트 파일로 내보내기 (Midjourney 등에서 사용)"""
        webtoon = self.load_webtoon(webtoon_id)
        if not webtoon:
            raise ValueError(f"웹툰을 찾을 수 없습니다: {webtoon_id}")

        episode = next(
            (ep for ep in webtoon["episodes"] if ep["number"] == episode_number),
            None
        )
        if not episode:
            raise ValueError(f"에피소드를 찾을 수 없습니다: {episode_number}")

        output_file = WEBTOON_DIR / webtoon_id / "episodes" / f"ep{episode_number:03d}" / "prompts.txt"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# {webtoon['title']} - Episode {episode_number}: {episode['title']}\n")
            f.write(f"# Generated: {datetime.utcnow().isoformat()}\n\n")

            for panel in episode["panels"]:
                f.write(f"## Panel {panel['order']}\n")
                f.write(f"Description: {panel.get('description', '')}\n")
                f.write(f"Characters: {panel.get('characters', '')}\n")
                f.write(f"Dialogue: {', '.join(panel.get('dialogue', []))}\n\n")
                f.write("### AI Prompt:\n")
                f.write(f"{panel.get('aiPrompt', 'No prompt generated')}\n")
                f.write("\n" + "="*60 + "\n\n")

        return output_file

    def get_status(self, webtoon_id: str) -> Dict:
        """웹툰 상태 조회"""
        webtoon = self.load_webtoon(webtoon_id)
        if not webtoon:
            return {"error": "웹툰을 찾을 수 없습니다"}

        total_panels = sum(len(ep.get("panels", [])) for ep in webtoon["episodes"])
        generated_panels = sum(
            len([p for p in ep.get("panels", []) if p.get("generated")])
            for ep in webtoon["episodes"]
        )

        return {
            "id": webtoon["id"],
            "title": webtoon["title"],
            "status": webtoon["status"],
            "episodes": len(webtoon["episodes"]),
            "characters": len(webtoon["characters"]),
            "totalPanels": total_panels,
            "generatedPanels": generated_panels,
            "progress": f"{generated_panels}/{total_panels}" if total_panels > 0 else "0/0"
        }

    def list_webtoons(self) -> List[Dict]:
        """모든 웹툰 목록"""
        webtoons = []
        for webtoon_dir in WEBTOON_DIR.iterdir():
            if webtoon_dir.is_dir():
                meta_file = webtoon_dir / "metadata.json"
                if meta_file.exists():
                    webtoon = self.load_webtoon(webtoon_dir.name)
                    if webtoon:
                        webtoons.append({
                            "id": webtoon["id"],
                            "title": webtoon["title"],
                            "genre": webtoon["genre"],
                            "status": webtoon["status"],
                            "episodes": len(webtoon["episodes"])
                        })
        return webtoons


def main():
    parser = argparse.ArgumentParser(description="DTSLIB Webtoon AI Pipeline")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # new 명령
    new_parser = subparsers.add_parser("new", help="새 웹툰 프로젝트 생성")
    new_parser.add_argument("--title", "-t", required=True, help="웹툰 제목")
    new_parser.add_argument("--genre", "-g", required=True,
        choices=["fantasy", "romance", "action", "comedy", "drama", "slice-of-life", "educational"])
    new_parser.add_argument("--synopsis", "-s", default="", help="시놉시스")

    # character 명령
    char_parser = subparsers.add_parser("character", help="캐릭터 추가")
    char_parser.add_argument("--webtoon-id", "-w", required=True)
    char_parser.add_argument("--name", "-n", required=True)
    char_parser.add_argument("--description", "-d", required=True)
    char_parser.add_argument("--role", "-r", default="supporting",
        choices=["protagonist", "antagonist", "supporting", "extra"])

    # episode 명령
    ep_parser = subparsers.add_parser("episode", help="에피소드 생성")
    ep_parser.add_argument("--webtoon-id", "-w", required=True)
    ep_parser.add_argument("--number", "-n", type=int, required=True)
    ep_parser.add_argument("--title", "-t", required=True)
    ep_parser.add_argument("--script-file", "-s", type=Path, help="스크립트 파일")

    # generate 명령
    gen_parser = subparsers.add_parser("generate", help="AI 프롬프트 생성")
    gen_parser.add_argument("--webtoon-id", "-w", required=True)
    gen_parser.add_argument("--episode", "-e", type=int, required=True)

    # status 명령
    status_parser = subparsers.add_parser("status", help="상태 조회")
    status_parser.add_argument("--webtoon-id", "-w", help="특정 웹툰 ID")

    # list 명령
    subparsers.add_parser("list", help="웹툰 목록")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    pipeline = WebtoonPipeline()

    print("=" * 60)
    print("DTSLIB Webtoon AI Pipeline")
    print("=" * 60)
    print()

    if args.command == "new":
        webtoon = pipeline.create_webtoon(
            title=args.title,
            genre=args.genre,
            synopsis=args.synopsis
        )
        print(f"웹툰 생성됨: {webtoon['id']}")
        print(f"  제목: {webtoon['title']}")
        print(f"  장르: {webtoon['genre']}")
        print(f"  스타일: {webtoon['style']['artStyle'][:50]}...")

    elif args.command == "character":
        char = pipeline.add_character(
            webtoon_id=args.webtoon_id,
            name=args.name,
            description=args.description,
            role=args.role
        )
        print(f"캐릭터 추가됨: {char['name']}")
        print(f"  역할: {char['role']}")
        print()
        print("캐릭터 시트 프롬프트:")
        print(char['visualPrompt'])

    elif args.command == "episode":
        script = ""
        if args.script_file and args.script_file.exists():
            with open(args.script_file, "r", encoding="utf-8") as f:
                script = f.read()

        episode = pipeline.create_episode(
            webtoon_id=args.webtoon_id,
            episode_number=args.number,
            title=args.title,
            script=script
        )

        if script:
            # 스크립트 파싱
            webtoon = pipeline.load_webtoon(args.webtoon_id)
            ep_idx = next(i for i, ep in enumerate(webtoon["episodes"]) if ep["number"] == args.number)
            webtoon["episodes"][ep_idx]["panels"] = pipeline.parse_script_to_panels(script)
            pipeline.save_webtoon(webtoon)

        print(f"에피소드 생성됨: #{episode['number']} - {episode['title']}")
        print(f"  상태: {episode['status']}")
        if script:
            webtoon = pipeline.load_webtoon(args.webtoon_id)
            ep = next(ep for ep in webtoon["episodes"] if ep["number"] == args.number)
            print(f"  패널 수: {len(ep['panels'])}")

    elif args.command == "generate":
        panels = pipeline.generate_panel_prompts(args.webtoon_id, args.episode)
        output = pipeline.export_prompts(args.webtoon_id, args.episode)
        print(f"프롬프트 생성됨: {len(panels)}개 패널")
        print(f"내보내기: {output}")

    elif args.command == "status":
        if args.webtoon_id:
            status = pipeline.get_status(args.webtoon_id)
            if "error" in status:
                print(status["error"])
            else:
                print(f"웹툰: {status['title']}")
                print(f"  상태: {status['status']}")
                print(f"  에피소드: {status['episodes']}개")
                print(f"  캐릭터: {status['characters']}개")
                print(f"  진행률: {status['progress']} 패널")
        else:
            webtoons = pipeline.list_webtoons()
            print(f"총 {len(webtoons)}개 웹툰")
            for wt in webtoons:
                print(f"  - {wt['id']}: {wt['title']} ({wt['genre']}) - {wt['status']}")

    elif args.command == "list":
        webtoons = pipeline.list_webtoons()
        if not webtoons:
            print("등록된 웹툰이 없습니다.")
        else:
            print(f"총 {len(webtoons)}개 웹툰:")
            for wt in webtoons:
                print(f"  [{wt['status']:10}] {wt['id']}")
                print(f"              {wt['title']} ({wt['genre']}) - {wt['episodes']}화")

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
