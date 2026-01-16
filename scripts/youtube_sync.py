#!/usr/bin/env python3
"""
PARKSY Publisher Platform - YouTube Auto-Sync
YouTube 채널 자동 동기화 및 출판물 생성

사용법:
    python scripts/youtube_sync.py --channel-id UC... [--api-key YOUR_KEY]

환경 변수:
    YOUTUBE_API_KEY: YouTube Data API v3 키
    YOUTUBE_CHANNEL_ID: 채널 ID (옵션)
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

# === 설정 ===

DATA_DIR = Path(__file__).parent.parent / "data"
YOUTUBE_DIR = DATA_DIR / "youtube"
API_DIR = Path(__file__).parent.parent / "api" / "v1"

YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"


def fetch_channel_videos(channel_id: str, api_key: str, max_results: int = 50) -> list:
    """YouTube 채널의 최신 영상 목록 가져오기"""
    videos = []

    # 1. 채널의 uploads 플레이리스트 ID 가져오기
    channel_url = (
        f"{YOUTUBE_API_BASE}/channels?"
        f"part=contentDetails&id={channel_id}&key={api_key}"
    )

    try:
        req = Request(channel_url, headers={"User-Agent": "PARKSY-Publisher/2.0"})
        with urlopen(req, timeout=30) as response:
            channel_data = json.loads(response.read().decode())

        if not channel_data.get("items"):
            print(f"[ERROR] 채널을 찾을 수 없습니다: {channel_id}")
            return []

        uploads_playlist = channel_data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    except (HTTPError, URLError) as e:
        print(f"[ERROR] 채널 정보 가져오기 실패: {e}")
        return []

    # 2. 플레이리스트에서 영상 목록 가져오기
    playlist_url = (
        f"{YOUTUBE_API_BASE}/playlistItems?"
        f"part=snippet,contentDetails&maxResults={max_results}"
        f"&playlistId={uploads_playlist}&key={api_key}"
    )

    try:
        req = Request(playlist_url, headers={"User-Agent": "PARKSY-Publisher/2.0"})
        with urlopen(req, timeout=30) as response:
            playlist_data = json.loads(response.read().decode())

        for item in playlist_data.get("items", []):
            snippet = item.get("snippet", {})
            video = {
                "videoId": snippet.get("resourceId", {}).get("videoId"),
                "title": snippet.get("title"),
                "description": snippet.get("description", "")[:500],  # 처음 500자만
                "channelId": channel_id,
                "channelTitle": snippet.get("channelTitle"),
                "thumbnails": {
                    "default": snippet.get("thumbnails", {}).get("default", {}).get("url"),
                    "medium": snippet.get("thumbnails", {}).get("medium", {}).get("url"),
                    "high": snippet.get("thumbnails", {}).get("high", {}).get("url"),
                },
                "publishedAt": snippet.get("publishedAt"),
                "syncedAt": datetime.utcnow().isoformat() + "Z",
            }
            if video["videoId"]:
                videos.append(video)

    except (HTTPError, URLError) as e:
        print(f"[ERROR] 영상 목록 가져오기 실패: {e}")
        return []

    return videos


def fetch_video_details(video_ids: list, api_key: str) -> dict:
    """영상 상세 정보 가져오기 (duration, tags 등)"""
    if not video_ids:
        return {}

    details = {}
    # API는 최대 50개씩 처리
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        ids_str = ",".join(batch)

        url = (
            f"{YOUTUBE_API_BASE}/videos?"
            f"part=contentDetails,statistics&id={ids_str}&key={api_key}"
        )

        try:
            req = Request(url, headers={"User-Agent": "PARKSY-Publisher/2.0"})
            with urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode())

            for item in data.get("items", []):
                video_id = item["id"]
                details[video_id] = {
                    "duration": item.get("contentDetails", {}).get("duration"),
                    "viewCount": item.get("statistics", {}).get("viewCount"),
                    "likeCount": item.get("statistics", {}).get("likeCount"),
                }

        except (HTTPError, URLError) as e:
            print(f"[WARN] 영상 상세 정보 가져오기 실패: {e}")

    return details


def update_youtube_index(videos: list, channel_id: str) -> None:
    """YouTube 인덱스 파일 업데이트"""
    YOUTUBE_DIR.mkdir(parents=True, exist_ok=True)

    index_file = YOUTUBE_DIR / "index.json"

    # 기존 데이터 로드
    existing_videos = {}
    if index_file.exists():
        try:
            with open(index_file, "r", encoding="utf-8") as f:
                existing = json.load(f)
                for v in existing.get("items", []):
                    existing_videos[v["videoId"]] = v
        except json.JSONDecodeError:
            pass

    # 새 영상 병합 (기존 데이터 유지하면서 업데이트)
    for video in videos:
        video_id = video["videoId"]
        if video_id in existing_videos:
            # 기존 linked publications 유지
            video["linkedPublications"] = existing_videos[video_id].get("linkedPublications", [])
        else:
            video["linkedPublications"] = []
        existing_videos[video_id] = video

    # 날짜순 정렬
    sorted_videos = sorted(
        existing_videos.values(),
        key=lambda x: x.get("publishedAt", ""),
        reverse=True
    )

    # 인덱스 파일 저장
    index_data = {
        "$schema": "../config/schemas.json#/schemas/youtubeVideo",
        "collection": "youtube",
        "version": "1.0.0",
        "channelId": channel_id,
        "lastSynced": datetime.utcnow().isoformat() + "Z",
        "count": len(sorted_videos),
        "items": sorted_videos
    }

    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)

    print(f"[OK] YouTube 인덱스 업데이트 완료: {len(sorted_videos)}개 영상")


def update_api_endpoint(videos: list, channel_id: str) -> None:
    """API 엔드포인트 업데이트"""
    API_DIR.mkdir(parents=True, exist_ok=True)

    api_file = API_DIR / "youtube.json"

    api_data = {
        "success": True,
        "data": {
            "videos": videos[:20],  # 최신 20개만 API에 노출
            "total": len(videos),
            "channelId": channel_id,
            "lastSynced": datetime.utcnow().isoformat() + "Z"
        },
        "meta": {
            "generatedAt": datetime.utcnow().isoformat() + "Z",
            "source": "/data/youtube/index.json"
        }
    }

    with open(api_file, "w", encoding="utf-8") as f:
        json.dump(api_data, f, indent=2, ensure_ascii=False)

    print(f"[OK] API 엔드포인트 업데이트 완료")


def create_publication_drafts(videos: list) -> int:
    """새 영상에 대한 출판물 초안 생성"""
    PUB_DIR = DATA_DIR / "publications"
    PUB_DIR.mkdir(parents=True, exist_ok=True)

    # 기존 출판물 확인
    pub_index_file = PUB_DIR / "index.json"
    existing_video_ids = set()

    if pub_index_file.exists():
        try:
            with open(pub_index_file, "r", encoding="utf-8") as f:
                pub_data = json.load(f)
                for pub in pub_data.get("items", []):
                    for yt in pub.get("media", {}).get("youtube", []):
                        existing_video_ids.add(yt.get("videoId"))
        except json.JSONDecodeError:
            pass

    # 새 영상에 대한 출판물 초안 생성
    created = 0
    for video in videos:
        if video["videoId"] in existing_video_ids:
            continue

        pub_id = f"pub-{video['publishedAt'][:10]}-{video['videoId'][:8]}"
        publication = {
            "id": pub_id,
            "title": video["title"],
            "subtitle": "",
            "type": "article",
            "status": "draft",
            "persona": None,  # 콘솔에서 지정
            "content": {
                "body": video["description"],
                "format": "plain",
                "excerpt": video["description"][:200] if video["description"] else ""
            },
            "media": {
                "youtube": [{
                    "videoId": video["videoId"],
                    "title": video["title"],
                    "role": "main"
                }],
                "spotify": [],
                "images": [video["thumbnails"].get("high") or video["thumbnails"].get("medium")]
            },
            "series": None,
            "tags": [],
            "createdAt": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z",
            "sourceVideo": video["videoId"]
        }

        # 개별 출판물 파일 저장
        pub_file = PUB_DIR / f"{pub_id}.json"
        with open(pub_file, "w", encoding="utf-8") as f:
            json.dump(publication, f, indent=2, ensure_ascii=False)

        created += 1

    if created > 0:
        print(f"[OK] 출판물 초안 {created}개 생성됨")

    return created


def update_publications_index() -> None:
    """출판물 인덱스 업데이트"""
    PUB_DIR = DATA_DIR / "publications"
    pub_index_file = PUB_DIR / "index.json"

    publications = []
    for f in PUB_DIR.glob("pub-*.json"):
        try:
            with open(f, "r", encoding="utf-8") as fp:
                pub = json.load(fp)
                publications.append(pub)
        except json.JSONDecodeError:
            continue

    # 날짜순 정렬
    publications.sort(key=lambda x: x.get("createdAt", ""), reverse=True)

    index_data = {
        "$schema": "../config/schemas.json#/schemas/publication",
        "collection": "publications",
        "version": "1.0.0",
        "count": len(publications),
        "lastUpdated": datetime.utcnow().isoformat() + "Z",
        "items": publications
    }

    with open(pub_index_file, "w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)

    # API 엔드포인트도 업데이트
    api_file = API_DIR / "publications.json"
    api_data = {
        "success": True,
        "data": {
            "publications": [p for p in publications if p.get("status") == "published"][:20],
            "total": len([p for p in publications if p.get("status") == "published"]),
            "page": 1,
            "perPage": 20
        },
        "meta": {
            "generatedAt": datetime.utcnow().isoformat() + "Z",
            "source": "/data/publications/index.json"
        }
    }

    with open(api_file, "w", encoding="utf-8") as f:
        json.dump(api_data, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="PARKSY YouTube Auto-Sync")
    parser.add_argument("--channel-id", help="YouTube 채널 ID")
    parser.add_argument("--api-key", help="YouTube API 키 (또는 YOUTUBE_API_KEY 환경변수)")
    parser.add_argument("--max-results", type=int, default=50, help="가져올 최대 영상 수")
    parser.add_argument("--dry-run", action="store_true", help="실제 저장 없이 테스트")
    args = parser.parse_args()

    # API 키 확인
    api_key = args.api_key or os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        print("[ERROR] YouTube API 키가 필요합니다.")
        print("  --api-key 옵션 또는 YOUTUBE_API_KEY 환경변수를 설정하세요.")
        sys.exit(1)

    # 채널 ID 확인
    channel_id = args.channel_id or os.environ.get("YOUTUBE_CHANNEL_ID")
    if not channel_id:
        print("[ERROR] YouTube 채널 ID가 필요합니다.")
        print("  --channel-id 옵션 또는 YOUTUBE_CHANNEL_ID 환경변수를 설정하세요.")
        sys.exit(1)

    print("=" * 60)
    print("PARKSY YouTube Auto-Sync")
    print("=" * 60)
    print(f"채널 ID: {channel_id}")
    print(f"최대 결과: {args.max_results}")
    print()

    # 1. 영상 목록 가져오기
    print("[1/5] YouTube 채널 영상 가져오는 중...")
    videos = fetch_channel_videos(channel_id, api_key, args.max_results)

    if not videos:
        print("[WARN] 가져온 영상이 없습니다.")
        sys.exit(0)

    print(f"      {len(videos)}개 영상 발견")

    # 2. 영상 상세 정보 가져오기
    print("[2/5] 영상 상세 정보 가져오는 중...")
    video_ids = [v["videoId"] for v in videos]
    details = fetch_video_details(video_ids, api_key)

    for video in videos:
        vid = video["videoId"]
        if vid in details:
            video.update(details[vid])

    if args.dry_run:
        print("\n[DRY-RUN] 실제 저장 건너뜀")
        print(f"  가져온 영상: {len(videos)}개")
        for v in videos[:5]:
            print(f"    - {v['title'][:50]}...")
        sys.exit(0)

    # 3. YouTube 인덱스 업데이트
    print("[3/5] YouTube 인덱스 업데이트 중...")
    update_youtube_index(videos, channel_id)

    # 4. API 엔드포인트 업데이트
    print("[4/5] API 엔드포인트 업데이트 중...")
    update_api_endpoint(videos, channel_id)

    # 5. 출판물 초안 생성
    print("[5/5] 출판물 초안 생성 중...")
    created = create_publication_drafts(videos)
    if created > 0:
        update_publications_index()

    print()
    print("=" * 60)
    print("YouTube Auto-Sync 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()
