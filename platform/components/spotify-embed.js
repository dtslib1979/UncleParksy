/**
 * PARKSY Spotify Embed Component
 * 웹에서 합법적으로 음악을 감상하기 위한 Spotify 임베드 컴포넌트
 */

class ParksySpotifyEmbed {
    constructor(container, options = {}) {
        this.container = typeof container === 'string'
            ? document.querySelector(container)
            : container;

        this.options = {
            theme: 'dark', // 'dark' or 'light'
            compact: false,
            width: '100%',
            height: options.compact ? 80 : 352,
            ...options
        };

        this.currentTrack = null;
    }

    /**
     * Spotify URI 파싱
     * @param {string} input - Spotify URL 또는 URI
     * @returns {object} - { type, id }
     */
    parseSpotifyUri(input) {
        // URL 형식: https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh
        const urlMatch = input.match(/open\.spotify\.com\/(track|album|playlist|artist|episode|show)\/([A-Za-z0-9]+)/);
        if (urlMatch) {
            return { type: urlMatch[1], id: urlMatch[2] };
        }

        // URI 형식: spotify:track:4iV5W9uYEdYUVa79Axb7Rh
        const uriMatch = input.match(/spotify:(track|album|playlist|artist|episode|show):([A-Za-z0-9]+)/);
        if (uriMatch) {
            return { type: uriMatch[1], id: uriMatch[2] };
        }

        // 그냥 ID만 있는 경우 (기본값 track)
        if (/^[A-Za-z0-9]{22}$/.test(input)) {
            return { type: 'track', id: input };
        }

        return null;
    }

    /**
     * 임베드 URL 생성
     * @param {string} type - track, album, playlist, artist, episode, show
     * @param {string} id - Spotify ID
     * @returns {string} - 임베드 URL
     */
    getEmbedUrl(type, id) {
        const theme = this.options.theme === 'dark' ? '0' : '1';
        return `https://open.spotify.com/embed/${type}/${id}?utm_source=generator&theme=${theme}`;
    }

    /**
     * 트랙/플레이리스트 임베드
     * @param {string} input - Spotify URL, URI, 또는 ID
     * @param {string} [type] - 타입 (ID만 제공시 필요)
     */
    embed(input, type = null) {
        const parsed = this.parseSpotifyUri(input);
        if (!parsed && !type) {
            console.error('Invalid Spotify input:', input);
            return;
        }

        const spotifyType = parsed?.type || type;
        const spotifyId = parsed?.id || input;

        const embedUrl = this.getEmbedUrl(spotifyType, spotifyId);
        const height = this.options.compact ? 80 :
            (spotifyType === 'track' ? 152 : 352);

        const iframe = document.createElement('iframe');
        iframe.src = embedUrl;
        iframe.width = this.options.width;
        iframe.height = height;
        iframe.frameBorder = '0';
        iframe.allow = 'autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture';
        iframe.loading = 'lazy';
        iframe.style.borderRadius = '12px';

        this.container.innerHTML = '';
        this.container.appendChild(iframe);

        this.currentTrack = { type: spotifyType, id: spotifyId };
    }

    /**
     * 플레이리스트 임베드 (편의 메서드)
     */
    playlist(playlistId) {
        this.embed(playlistId, 'playlist');
    }

    /**
     * 트랙 임베드 (편의 메서드)
     */
    track(trackId) {
        this.embed(trackId, 'track');
    }

    /**
     * 앨범 임베드 (편의 메서드)
     */
    album(albumId) {
        this.embed(albumId, 'album');
    }

    /**
     * 아티스트 임베드 (편의 메서드)
     */
    artist(artistId) {
        this.embed(artistId, 'artist');
    }
}

/**
 * PARKSY YouTube Embed Component
 * YouTube 영상 임베드 컴포넌트
 */

class ParksyYouTubeEmbed {
    constructor(container, options = {}) {
        this.container = typeof container === 'string'
            ? document.querySelector(container)
            : container;

        this.options = {
            width: '100%',
            aspectRatio: '16/9',
            autoplay: false,
            controls: true,
            ...options
        };
    }

    /**
     * YouTube Video ID 추출
     */
    parseVideoId(input) {
        // 표준 URL
        let match = input.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([A-Za-z0-9_-]{11})/);
        if (match) return match[1];

        // 그냥 ID
        if (/^[A-Za-z0-9_-]{11}$/.test(input)) return input;

        return null;
    }

    /**
     * 영상 임베드
     */
    embed(input, options = {}) {
        const videoId = this.parseVideoId(input);
        if (!videoId) {
            console.error('Invalid YouTube input:', input);
            return;
        }

        const mergedOptions = { ...this.options, ...options };
        const params = new URLSearchParams();

        if (mergedOptions.autoplay) params.set('autoplay', '1');
        if (!mergedOptions.controls) params.set('controls', '0');
        if (mergedOptions.start) params.set('start', mergedOptions.start);
        if (mergedOptions.end) params.set('end', mergedOptions.end);

        const iframe = document.createElement('iframe');
        iframe.src = `https://www.youtube.com/embed/${videoId}?${params.toString()}`;
        iframe.width = mergedOptions.width;
        iframe.style.aspectRatio = mergedOptions.aspectRatio;
        iframe.style.height = 'auto';
        iframe.frameBorder = '0';
        iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
        iframe.allowFullscreen = true;
        iframe.loading = 'lazy';
        iframe.style.borderRadius = '12px';

        this.container.innerHTML = '';
        this.container.appendChild(iframe);
    }
}

// 전역 네임스페이스에 등록
window.PARKSY = window.PARKSY || {};
window.PARKSY.SpotifyEmbed = ParksySpotifyEmbed;
window.PARKSY.YouTubeEmbed = ParksyYouTubeEmbed;

// 사용 예시
// const spotify = new PARKSY.SpotifyEmbed('#player');
// spotify.playlist('37i9dQZF1DXcBWIGoYBM5M');
//
// const youtube = new PARKSY.YouTubeEmbed('#video');
// youtube.embed('dQw4w9WgXcQ');
