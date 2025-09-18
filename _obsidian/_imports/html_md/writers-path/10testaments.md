# 📱 Mobile Production Platform

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --primary: #1a1a2e;
            --secondary: #16213e;
            --accent: #7c78ff;
            --accent-light: #a29bff;
            --text-primary: #ffffff;
            --text-secondary: #b8b8d1;
            --success: #4ade80;
            --warning: #fbbf24;
            --glass: rgba(255, 255, 255, 0.1);
            --gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --gradient-2: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --gradient-3: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }
        
        body {
            font-family: 'Noto Sans KR', sans-serif;
            background: var(--primary);
            color: var(--text-primary);
            overflow-x: hidden;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        /* Header */
        .header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: rgba(26, 26, 46, 0.95);
            backdrop-filter: blur(20px);
            z-index: 1000;
            padding: 15px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 24px;
            font-weight: 900;
            background: var(--gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .nav-menu {
            display: flex;
            gap: 30px;
            list-style: none;
        }
        
        .nav-item a {
            color: var(--text-secondary);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
            padding: 8px 16px;
            border-radius: 20px;
        }
        
        .nav-item a:hover {
            color: var(--text-primary);
            background: var(--glass);
        }
        
        /* Hero Section */
        .hero {
            min-height: 100vh;
            display: flex;
            align-items: center;
            position: relative;
            overflow: hidden;
        }
        
        .hero::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 30% 20%, rgba(124, 120, 255, 0.3) 0%, transparent 50%),
                        radial-gradient(circle at 70% 80%, rgba(162, 155, 255, 0.2) 0%, transparent 50%);
            z-index: -1;
        }
        
        .hero-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            align-items: center;
            padding-top: 100px;
        }
        
        .hero-text h1 {
            font-size: clamp(2.5rem, 5vw, 4rem);
            font-weight: 900;
            margin-bottom: 20px;
            line-height: 1.2;
        }
        
        .hero-text .highlight {
            background: var(--gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .hero-text p {
            font-size: 1.2rem;
            color: var(--text-secondary);
            margin-bottom: 40px;
        }
        
        .cta-buttons {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 15px 30px;
            border: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }
        
        .btn-primary {
            background: var(--gradient);
            color: white;
            box-shadow: 0 10px 30px rgba(124, 120, 255, 0.3);
        }
        
        .btn-secondary {
            background: var(--glass);
            color: var(--text-primary);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(124, 120, 255, 0.4);
        }
        
        /* Hero Visual */
        .hero-visual {
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .phone-mockup {
            width: 300px;
            height: 600px;
            background: linear-gradient(145deg, #2d2d44, #1a1a2e);
            border-radius: 40px;
            padding: 20px;
            position: relative;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.3);
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
        
        .phone-screen {
            width: 100%;
            height: 100%;
            background: var(--primary);
            border-radius: 30px;
            position: relative;
            overflow: hidden;
        }
        
        .app-preview {
            position: absolute;
            top: 20px;
            left: 20px;
            right: 20px;
            bottom: 20px;
            background: var(--gradient);
            border-radius: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 20px;
        }
        
        .app-icon {
            font-size: 48px;
            color: white;
        }
        
        .app-text {
            text-align: center;
            color: white;
            font-weight: 600;
        }
        
        /* Features Section */
        .features {
            padding: 100px 0;
            background: rgba(22, 33, 62, 0.3);
        }
        
        .section-title {
            text-align: center;
            font-size: 3rem;
            font-weight: 900;
            margin-bottom: 60px;
            background: var(--gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 40px;
        }
        
        .feature-card {
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(124, 120, 255, 0.2);
        }
        
        .feature-icon {
            font-size: 48px;
            margin-bottom: 20px;
            background: var(--gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .feature-card h3 {
            font-size: 1.5rem;
            margin-bottom: 15px;
            font-weight: 700;
        }
        
        .feature-card p {
            color: var(--text-secondary);
            line-height: 1.6;
        }
        
        /* Ecosystem Section */
        .ecosystem {
            padding: 100px 0;
        }
        
        .ecosystem-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 30px;
            margin-top: 60px;
        }
        
        .ecosystem-item {
            background: var(--glass);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 30px 20px;
            text-align: center;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .ecosystem-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: var(--gradient);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }
        
        .ecosystem-item:hover::before {
            transform: scaleX(1);
        }
        
        .ecosystem-item:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.15);
        }
        
        .ecosystem-icon {
            font-size: 36px;
            margin-bottom: 15px;
            background: var(--gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .ecosystem-item h4 {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .ecosystem-item p {
            font-size: 12px;
            color: var(--text-secondary);
        }
        
        /* Stats Section */
        .stats {
            padding: 80px 0;
            background: rgba(22, 33, 62, 0.5);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 40px;
            text-align: center;
        }
        
        .stat-item h3 {
            font-size: 3rem;
            font-weight: 900;
            color: var(--accent);
            margin-bottom: 10px;
        }
        
        .stat-item p {
            color: var(--text-secondary);
            font-weight: 500;
        }
        
        /* Footer */
        .footer {
            padding: 60px 0 30px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
        }
        
        .footer-content {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 40px;
            margin-bottom: 40px;
        }
        
        .footer-section h4 {
            margin-bottom: 20px;
            font-weight: 700;
        }
        
        .footer-section a {
            color: var(--text-secondary);
            text-decoration: none;
            display: block;
            margin-bottom: 10px;
            transition: color 0.3s ease;
        }
        
        .footer-section a:hover {
            color: var(--accent);
        }
        
        .copyright {
            color: var(--text-secondary);
            font-size: 14px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .nav-menu {
                display: none;
            }
            
            .hero-content {
                grid-template-columns: 1fr;
                text-align: center;
                gap: 40px;
            }
            
            .phone-mockup {
                width: 250px;
                height: 500px;
            }
            
            .ecosystem-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .footer-content {
                grid-template-columns: 1fr;
                text-align: left;
            }
        }
        
        /* Install Button */
        .install-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--gradient);
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 50px;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 10px 30px rgba(124, 120, 255, 0.3);
            transition: all 0.3s ease;
            display: none;
            z-index: 1001;
        }
        
        .install-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(124, 120, 255, 0.4);
        }
        
        .install-btn.show {
            display: flex;
            align-items: center;
            gap: 10px;
        }

            📱 MPP
            
                기능
                생태계
                통계
                연락

                        # 핸드폰을 생산 플랫폼으로
                        소비에서 생산으로, 마인드셋을 전환하여 콘텐츠와 코딩까지 아우르는 새로운 생태계를 경험하세요.

                                시작하기

                                둘러보기

                                        ### 생산 플랫폼
                                        아이디어를 현실로

                ## 핵심 기능

                        ### AI 드로잉 어시스트
                        초안 작성부터 AI 발전, 변형, 최종화까지 창작의 모든 과정을 지원합니다.

                        ### 통합 코딩 환경
                        GitHub Copilot과 Claude를 활용한 자동화된 코딩 워크플로우를 제공합니다.

                        ### 생태계 연동
                        10개 플랫폼을 하나로 연결하여 효율적인 콘텐츠 생산과 배포를 실현합니다.

                        ### 온디바이스 자동화
                        Tasker를 통한 스마트한 자동화로 반복 작업을 최소화합니다.

                        ### 글로벌 확장
                        로컬에서 글로벌까지, 다양한 플랫폼을 통한 콘텐츠 확산을 지원합니다.

                        ### 자산화 & 수익화
                        옵시디언과 워드프레스를 통한 지식 자산화와 지속가능한 수익 모델을 제공합니다.

                ## 메인 생태계

                        Samsung Phone
                        메인 허브

                        ChatGPT
                        아이디어 생성

                        GitHub
                        코드 관리

                        Claude
                        자동화 연결

                        YouTube
                        영상 콘텐츠

                        Naver Blog
                        로컬 시장

                        Tistory
                        백업 아카이브

                        Obsidian
                        지식 자산화

                        WordPress
                        글로벌 판매

                        Tasker
                        온디바이스 자동화

                        ### 10+
                        통합 플랫폼

                        ### 85
                        평가 점수

                        ### 100%
                        모바일 최적화

                        ### 24/7
                        자동화 가능

                    플랫폼
                    Samsung Galaxy
                    ChatGPT
                    GitHub
                    Claude

                    콘텐츠
                    YouTube
                    블로그
                    Tistory
                    WordPress

                    연락처
                    EduArt Engineer CI
                    dtslib.com
                    WebAppsBook Cast
                    유튜브 강의

                &copy; 2024 Mobile Production Platform. 마감작업 프로들의 기술과 테크닉으로 완성.

        앱 설치

        // PWA Install
        let deferredPrompt;
        const installBtn = document.getElementById('installBtn');

        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            installBtn.classList.add('show');
        });

        installBtn.addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const { outcome } = await deferredPrompt.userChoice;
                deferredPrompt = null;
                installBtn.classList.remove('show');
            }
        });

        // Smooth Scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Service Worker Registration (simplified for artifact)
        if ('serviceWorker' in navigator) {
            console.log('Service Worker supported - for full PWA functionality, deploy to server');
        }

        // Interactive Features
        document.addEventListener('DOMContentLoaded', function() {
            // Animate counters
            const counters = document.querySelectorAll('.stat-item h3');
            counters.forEach(counter => {
                const target = counter.textContent.match(/\d+/)[0];
                const increment = target / 100;
                let current = 0;
                
                const timer = setInterval(() => {
                    current += increment;
                    if (current >= target) {
                        counter.textContent = counter.textContent.replace(/\d+/, target);
                        clearInterval(timer);
                    } else {
                        counter.textContent = counter.textContent.replace(/\d+/, Math.ceil(current));
                    }
                }, 20);
            });

            // Add parallax effect
            window.addEventListener('scroll', () => {
                const scrolled = window.pageYOffset;
                const heroVisual = document.querySelector('.hero-visual');
                if (heroVisual) {
                    heroVisual.style.transform = `translateY(${scrolled * 0.5}px)`;
                }
            });
        });