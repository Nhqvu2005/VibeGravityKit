// VibeGravityKit Docs — app.js
// Bilingual (EN/VI), Theme Toggle, Changelog Fetcher

const CHANGELOG_URL = 'https://raw.githubusercontent.com/Nhqvu2005/VibeGravityKit/refs/heads/main/CHANGELOG.md';

// DOM
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');
const langToggle = document.getElementById('lang-toggle');
const mobileMenu = document.getElementById('mobile-menu');
const navLinks = document.getElementById('nav-links');
const changelogEl = document.getElementById('changelog-content');

// ========== i18n TRANSLATIONS ==========
const i18n = {
    en: {
        // Nav
        'nav.about': 'About',
        'nav.modes': 'How It Works',
        'nav.team': 'Team',
        'nav.install': 'Install',
        'nav.agents': 'Agents',
        'nav.changelog': 'Changelog',
        // Hero
        'hero.badge': 'Open Source · 18 AI Agents · 4 IDEs',
        'hero.title': 'The AI-Native<br><span class="gradient-text">Software House</span> in a Box',
        'hero.sub': 'Build enterprise-grade software with a coordinated team of 18 specialized AI agents. Parallel delegation for <strong>maximum speed</strong> and <strong>minimum token costs</strong>.',
        'hero.cta': 'Get Started →',
        'hero.github': 'View on GitHub',
        'hero.stat1': 'AI Agents',
        'hero.stat2': 'Data Sources',
        'hero.stat3': 'IDE Support',
        'hero.stat4': 'Token Savings',
        // About
        'about.title': '🎩 What is VibeGravityKit?',
        'about.desc': 'Imagine having a <strong>full-stack engineering team</strong> living inside your IDE.',
        'about.f1': 'Minifies your code before AI sees it.',
        'about.f1b': 'Saves ~50% tokens',
        'about.f2': 'Queries only relevant data from 34+ sources.',
        'about.f2b': 'Saves ~70% tokens',
        'about.f3': 'Applies surgical patches instead of rewriting files.',
        'about.f3b': 'Saves ~90% tokens',
        // Modes
        'modes.title': '🚀 Two Ways to Build',
        'modes.desc': 'Choose your workflow style — from instant autopilot to full control.',
        'modes.q.title': 'Quickstart Mode',
        'modes.q.desc': 'Full autopilot. One prompt → complete project. The AI team handles everything end-to-end.',
        'modes.l.title': 'Leader Mode',
        'modes.l.desc': 'Phase-by-phase orchestration. You approve each step. Maximum control over quality & direction.',
        // Team
        'team.title': '🧬 Team Profiles',
        'team.desc': 'Carry your coding style across projects. The team <strong>learns from you automatically</strong> — zero config needed.',
        'team.problem': '<strong>❌ Problem:</strong> Every <code>vibegravity init</code> starts fresh — agents forget your coding style, tech preferences, and bug fixes.',
        'team.solution': '<strong>✅ Solution:</strong> Persistent team profiles that learn passively as you work, and carry that knowledge to every new project.',
        'team.qs': '⚡ Quick Start',
        'team.qs1': 'Create an empty team',
        'team.qs2': 'Init your project with that team',
        'team.qs3': 'Just work normally',
        'team.qs.note': 'No config files, no manual setup. The team learns passively.',
        'team.auto': '🔄 How Auto-Learn Works',
        'team.t1.title': 'Plan Confirmed',
        'team.t1.desc': 'Scans project source → detects stack, naming style, architecture → updates Team DNA',
        'team.t2.title': 'Phase Completed',
        'team.t2.desc': 'Leader observed your directives (e.g. "write in English") → saves as rule',
        'team.t3.title': 'Bug Fixed',
        'team.t3.desc': 'Journal entry auto-syncs to team profile → available in future projects',
        'team.t4.title': 'Manual Scan',
        'team.t4.desc': 'Force-scan existing codebase: <code>vibegravity team scan my-team --path ./project</code>',
        'team.dna': '🧬 Team DNA — Your Style in One Line',
        'team.dna.note': 'This compact format (~50 tokens) tells every agent exactly how you like your code. It grows automatically.',
        'team.mem': '📦 3-Tier Memory System',
        'team.mem.hot': 'Always Loaded',
        'team.mem.hot.desc': 'Team DNA (1 line) + top rules',
        'team.mem.warm': 'On Demand',
        'team.mem.warm.desc': 'Full rules + journal index (TF-IDF search)',
        'team.mem.cold': 'Archived',
        'team.mem.cold.desc': 'Old DNA versions + history for rollback',
        'team.dedup': '🔁 Rule Deduplication',
        'team.dedup.desc': 'Prevents file bloat. Similar rules auto-merge instead of duplicating.',
        'team.cli': '🛠️ Team CLI Commands',
        // Install
        'install.title': '⚙️ Installation',
        'install.desc': 'Get started in 3 steps. Requires Python 3.9+ & Node.js 18+.',
        'install.s1': 'Clone & Install',
        'install.s2': 'Initialize in Your Project',
        'install.s2.note': 'This installs all 18 agents for your IDE automatically.',
        'install.s3': 'Start Building',
        'install.ide': '🌐 Multi-IDE Support',
        // Agents
        'agents.title': '🎮 The 18 Agents',
        'agents.desc': 'You are the Boss. Just chat with your agents using <code>@</code> mentions.',
        'agents.strategy': '🧠 Strategy & Vision Team',
        'agents.design': '🎨 Design & Product Team',
        'agents.eng': '💻 Engineering Team',
        'agents.quality': '🛡️ Quality & Support Team',
        // Changelog
        'cl.title': '📋 Changelog',
        'cl.desc': 'Latest updates and releases.',
        // Footer
        'footer.made': 'Made with ❤️ by',
    },
    vi: {
        // Nav
        'nav.about': 'Giới Thiệu',
        'nav.modes': 'Cách Hoạt Động',
        'nav.team': 'Team',
        'nav.install': 'Cài Đặt',
        'nav.agents': 'Agents',
        'nav.changelog': 'Nhật Ký',
        // Hero
        'hero.badge': 'Mã Nguồn Mở · 18 Agent AI · 4 IDE',
        'hero.title': 'Công Ty Phần Mềm<br><span class="gradient-text">AI-Native</span> Trong Một Hộp',
        'hero.sub': 'Xây dựng phần mềm cấp doanh nghiệp với đội ngũ 18 agent AI chuyên biệt. Giao việc song song cho <strong>tốc độ tối đa</strong> và <strong>tiết kiệm token tối đa</strong>.',
        'hero.cta': 'Bắt Đầu Ngay →',
        'hero.github': 'Xem trên GitHub',
        'hero.stat1': 'Agent AI',
        'hero.stat2': 'Nguồn Dữ Liệu',
        'hero.stat3': 'Hỗ Trợ IDE',
        'hero.stat4': 'Tiết Kiệm Token',
        // About
        'about.title': '🎩 VibeGravityKit là gì?',
        'about.desc': 'Hãy tưởng tượng bạn có một đội <strong>kỹ sư full-stack</strong> ngay trong IDE.',
        'about.f1': 'Nén code trước khi AI đọc.',
        'about.f1b': 'Tiết kiệm ~50% token',
        'about.f2': 'Chỉ truy vấn dữ liệu liên quan từ 34+ nguồn.',
        'about.f2b': 'Tiết kiệm ~70% token',
        'about.f3': 'Áp dụng bản vá chính xác thay vì viết lại file.',
        'about.f3b': 'Tiết kiệm ~90% token',
        // Modes
        'modes.title': '🚀 Hai Cách Để Xây Dựng',
        'modes.desc': 'Chọn phong cách làm việc — từ tự động toàn bộ đến kiểm soát hoàn toàn.',
        'modes.q.title': 'Chế Độ Quickstart',
        'modes.q.desc': 'Tự động toàn bộ. Một prompt → dự án hoàn chỉnh. Đội AI xử lý mọi thứ từ đầu đến cuối.',
        'modes.l.title': 'Chế Độ Leader',
        'modes.l.desc': 'Điều phối từng giai đoạn. Bạn duyệt từng bước. Kiểm soát tối đa chất lượng & hướng đi.',
        // Team
        'team.title': '🧬 Team Profiles',
        'team.desc': 'Mang style code của bạn qua các dự án. Team <strong>tự học từ bạn</strong> — không cần cấu hình.',
        'team.problem': '<strong>❌ Vấn đề:</strong> Mỗi <code>vibegravity init</code> bắt đầu từ đầu — agent quên style code, sở thích tech, và bug fix trước đó.',
        'team.solution': '<strong>✅ Giải pháp:</strong> Team profile liên tục tự học khi bạn làm việc, và mang kiến thức đó tới mọi dự án mới.',
        'team.qs': '⚡ Bắt Đầu Nhanh',
        'team.qs1': 'Tạo team rỗng',
        'team.qs2': 'Khởi tạo dự án với team đó',
        'team.qs3': 'Làm việc bình thường',
        'team.qs.note': 'Không cần file cấu hình, không cần thiết lập thủ công. Team tự học thụ động.',
        'team.auto': '🔄 Cơ Chế Tự Học',
        'team.t1.title': 'Kế Hoạch Được Duyệt',
        'team.t1.desc': 'Quét mã nguồn → phát hiện stack, naming style, kiến trúc → cập nhật Team DNA',
        'team.t2.title': 'Giai Đoạn Hoàn Thành',
        'team.t2.desc': 'Leader ghi nhận chỉ thị của bạn (ví dụ "viết bằng tiếng Anh") → lưu thành quy tắc',
        'team.t3.title': 'Bug Được Sửa',
        'team.t3.desc': 'Bài journal tự đồng bộ về team profile → dùng được ở dự án sau',
        'team.t4.title': 'Quét Thủ Công',
        'team.t4.desc': 'Quét codebase có sẵn: <code>vibegravity team scan my-team --path ./project</code>',
        'team.dna': '🧬 Team DNA — Style Của Bạn Trong Một Dòng',
        'team.dna.note': 'Định dạng nhỏ gọn (~50 token) cho mọi agent biết bạn thích code như thế nào. Tự lớn lên khi bạn làm việc.',
        'team.mem': '📦 Hệ Thống Bộ Nhớ 3 Tầng',
        'team.mem.hot': 'Luôn Tải',
        'team.mem.hot.desc': 'Team DNA (1 dòng) + quy tắc top',
        'team.mem.warm': 'Theo Yêu Cầu',
        'team.mem.warm.desc': 'Toàn bộ quy tắc + index journal (tìm TF-IDF)',
        'team.mem.cold': 'Lưu Trữ',
        'team.mem.cold.desc': 'Phiên bản DNA cũ + lịch sử rollback',
        'team.dedup': '🔁 Chống Trùng Lặp Quy Tắc',
        'team.dedup.desc': 'Ngăn file phình to. Quy tắc tương tự tự gộp thay vì trùng lặp.',
        'team.cli': '🛠️ Lệnh CLI Quản Lý Team',
        // Install
        'install.title': '⚙️ Cài Đặt',
        'install.desc': 'Bắt đầu trong 3 bước. Yêu cầu Python 3.9+ & Node.js 18+.',
        'install.s1': 'Clone & Cài Đặt',
        'install.s2': 'Khởi Tạo Trong Dự Án',
        'install.s2.note': 'Cài đặt tự động tất cả 18 agent cho IDE của bạn.',
        'install.s3': 'Bắt Đầu Xây Dựng',
        'install.ide': '🌐 Hỗ Trợ Đa IDE',
        // Agents
        'agents.title': '🎮 18 Agent',
        'agents.desc': 'Bạn là Ông Chủ. Chỉ cần chat với agent bằng <code>@</code>.',
        'agents.strategy': '🧠 Đội Chiến Lược & Tầm Nhìn',
        'agents.design': '🎨 Đội Thiết Kế & Sản Phẩm',
        'agents.eng': '💻 Đội Kỹ Thuật',
        'agents.quality': '🛡️ Đội Chất Lượng & Hỗ Trợ',
        // Changelog
        'cl.title': '📋 Nhật Ký Thay Đổi',
        'cl.desc': 'Cập nhật và phiên bản mới nhất.',
        // Footer
        'footer.made': 'Được tạo với ❤️ bởi',
    }
};

// ========== i18n ENGINE ==========
let currentLang = localStorage.getItem('vgk-lang') || 'en';

function applyLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('vgk-lang', lang);
    document.documentElement.setAttribute('lang', lang);
    langToggle.textContent = lang === 'en' ? 'VI' : 'EN';

    const dict = i18n[lang];
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dict[key]) {
            if (el.hasAttribute('data-i18n-html')) {
                el.innerHTML = dict[key];
            } else {
                el.textContent = dict[key];
            }
        }
    });
}

function toggleLang() {
    applyLanguage(currentLang === 'en' ? 'vi' : 'en');
}

// ========== THEME ==========
function loadTheme() {
    const saved = localStorage.getItem('vgk-theme') || 'light';
    document.documentElement.setAttribute('data-theme', saved);
    themeIcon.textContent = saved === 'dark' ? '☀️' : '🌙';
}

function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('vgk-theme', next);
    themeIcon.textContent = next === 'dark' ? '☀️' : '🌙';
}

// ========== MOBILE MENU ==========
function toggleMobile() {
    navLinks.classList.toggle('open');
}

// ========== CHANGELOG ==========
async function loadChangelog() {
    try {
        const res = await fetch(CHANGELOG_URL);
        if (!res.ok) throw new Error('Failed to fetch');
        const md = await res.text();
        renderChangelog(md);
    } catch (e) {
        changelogEl.innerHTML = '<p style="color:var(--text-muted)">Could not load changelog. <a href="https://github.com/Nhqvu2005/VibeGravityKit/blob/main/CHANGELOG.md" target="_blank">View on GitHub →</a></p>';
    }
}

function renderChangelog(md) {
    const lines = md.split('\n');
    const entries = [];
    let current = null;
    let currentSection = null;

    for (const line of lines) {
        const trimmed = line.trim();
        const versionMatch = trimmed.match(/^##\s*\[(.+?)\]\s*-\s*(.+)/);
        if (versionMatch) {
            if (current) entries.push(current);
            current = { version: versionMatch[1], date: versionMatch[2], sections: {} };
            currentSection = null;
            continue;
        }
        const sectionMatch = trimmed.match(/^###\s*(.+)/);
        if (sectionMatch && current) {
            currentSection = sectionMatch[1];
            current.sections[currentSection] = [];
            continue;
        }
        const itemMatch = trimmed.match(/^[-*]\s+(.+)/);
        if (itemMatch && current && currentSection) {
            current.sections[currentSection].push(itemMatch[1]);
        }
    }
    if (current) entries.push(current);

    let html = '';
    for (const entry of entries) {
        html += `<div class="cl-entry">`;
        html += `<div class="cl-version"><code>v${entry.version}</code> <span class="cl-date">${entry.date}</span></div>`;
        for (const [section, items] of Object.entries(entry.sections)) {
            html += `<div class="cl-section"><h4>${section}</h4><ul>`;
            for (const item of items) {
                html += `<li>${escapeHtml(item)}</li>`;
            }
            html += `</ul></div>`;
        }
        html += `</div>`;
    }
    changelogEl.innerHTML = html || '<p>No changelog entries found.</p>';
}

function escapeHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// ========== NAVBAR SCROLL ==========
const sections = document.querySelectorAll('.section[id], .hero[id]');
const navLinksAll = document.querySelectorAll('.nav-link[href^="#"]');

function highlightNav() {
    let current = '';
    for (const s of sections) {
        const top = s.offsetTop - 100;
        if (window.scrollY >= top) current = s.id;
    }
    navLinksAll.forEach(link => {
        link.classList.toggle('active', link.getAttribute('href') === '#' + current);
    });
}

// ========== COPY BUTTONS ==========
function injectCopyButtons() {
    document.querySelectorAll('pre.code-block, .ide-card').forEach(block => {
        if (block.querySelector('.copy-btn')) return;
        block.style.position = 'relative';

        const btn = document.createElement('button');
        btn.className = 'copy-btn';
        btn.textContent = 'Copy';
        btn.setAttribute('aria-label', 'Copy to clipboard');

        btn.addEventListener('click', () => {
            const code = block.querySelector('code');
            const text = code ? code.textContent : block.querySelector('code, span')?.textContent || block.textContent;
            navigator.clipboard.writeText(text.trim()).then(() => {
                btn.textContent = '✓ Copied!';
                btn.classList.add('copied');
                setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 2000);
            }).catch(() => {
                btn.textContent = '✗ Failed';
                setTimeout(() => { btn.textContent = 'Copy'; }, 2000);
            });
        });
        block.appendChild(btn);
    });
}

// ========== INIT ==========
function init() {
    loadTheme();
    loadChangelog();
    injectCopyButtons();
    applyLanguage(currentLang);
    themeToggle.addEventListener('click', toggleTheme);
    langToggle.addEventListener('click', toggleLang);
    mobileMenu.addEventListener('click', toggleMobile);
    window.addEventListener('scroll', highlightNav);

    navLinks.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => navLinks.classList.remove('open'));
    });
}

init();
