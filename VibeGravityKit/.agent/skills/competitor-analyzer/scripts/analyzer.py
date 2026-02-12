#!/usr/bin/env python3
"""
Competitor Analyzer — Phân tích đối thủ cạnh tranh theo loại sản phẩm.

Usage:
    python analyzer.py --product "ecommerce fashion" --market "vietnam"
"""

import argparse
import json
import sys

# === Database phân tích sản phẩm phổ biến ===
PRODUCT_TEMPLATES = {
    "ecommerce": {
        "display_name": "E-commerce / Bán hàng online",
        "keywords": ["ecommerce", "shop", "store", "bán hàng", "cửa hàng", "mua bán", "shopping"],
        "must_have_features": [
            "Trang chủ với featured products",
            "Danh mục sản phẩm với filter & sort",
            "Trang chi tiết sản phẩm (ảnh, giá, mô tả, biến thể)",
            "Giỏ hàng (add, remove, update quantity)",
            "Checkout flow (thông tin giao hàng, thanh toán)",
            "Đăng ký / Đăng nhập",
            "Lịch sử đơn hàng",
            "Tìm kiếm sản phẩm"
        ],
        "should_have_features": [
            "Wishlist / Yêu thích",
            "Filter theo giá, size, màu, brand",
            "Đánh giá & review sản phẩm",
            "Mã giảm giá / coupon",
            "So sánh sản phẩm",
            "Quick view (xem nhanh không cần vào detail)"
        ],
        "could_have_features": [
            "AI recommender (gợi ý sản phẩm)",
            "Chat với shop",
            "Loyalty points / Tích điểm",
            "AR try-on (thử đồ ảo)",
            "Social sharing",
            "Flash sale / Deal theo giờ"
        ],
        "competitors": {
            "vietnam": [
                {"name": "Shopee", "url": "shopee.vn", "strengths": "Marketplace lớn, flash sale, free ship", "weaknesses": "Quá nhiều sản phẩm nhái, UX cluttered"},
                {"name": "Tiki", "url": "tiki.vn", "strengths": "TikiNOW giao nhanh, sản phẩm chính hãng", "weaknesses": "Ít seller hơn Shopee, giá cao hơn"},
                {"name": "Sendo", "url": "sendo.vn", "strengths": "Giá rẻ, focus hàng Việt", "weaknesses": "UI dated, ít traffic"}
            ],
            "global": [
                {"name": "Shopify stores", "url": "shopify.com", "strengths": "Professional, customizable, ecosystem lớn", "weaknesses": "Phí hàng tháng, cần marketing riêng"},
                {"name": "WooCommerce", "url": "woocommerce.com", "strengths": "Free, flexible, WordPress ecosystem", "weaknesses": "Cần hosting, maintenance"},
                {"name": "Etsy", "url": "etsy.com", "strengths": "Handmade/unique items, built-in traffic", "weaknesses": "Commission cao, ít kiểm soát brand"}
            ]
        },
        "trends": [
            "Mobile-first checkout",
            "Buy Now Pay Later (BNPL)",
            "Social commerce (mua qua Instagram, TikTok)",
            "VietQR / Bank transfer integration (VN market)",
            "Headless commerce"
        ]
    },
    "saas": {
        "display_name": "SaaS (Software as a Service)",
        "keywords": ["saas", "platform", "tool", "service", "dashboard", "management"],
        "must_have_features": [
            "Landing page giới thiệu sản phẩm",
            "Pricing plans & Subscription",
            "User dashboard",
            "Settings / Profile management",
            "Authentication & Authorization",
            "Onboarding flow",
            "Billing & Invoice"
        ],
        "should_have_features": [
            "Team / Organization management",
            "API access cho developers",
            "Notifications (email + in-app)",
            "Analytics dashboard",
            "Export data (CSV, PDF)",
            "Integrations (Slack, email...)"
        ],
        "could_have_features": [
            "White-label / Custom branding",
            "Marketplace / Plugin system",
            "AI features (automation, suggestions)",
            "Multi-language support",
            "Mobile app"
        ],
        "competitors": {
            "vietnam": [],
            "global": [
                {"name": "Notion", "url": "notion.so", "strengths": "All-in-one, flexible blocks", "weaknesses": "Chậm với large databases"},
                {"name": "Linear", "url": "linear.app", "strengths": "UI đẹp, fast, focused", "weaknesses": "Ít integrations"},
                {"name": "Vercel", "url": "vercel.com", "strengths": "DX tuyệt vời, deploy nhanh", "weaknesses": "Vendor lock-in, giá scale cao"}
            ]
        },
        "trends": [
            "Product-Led Growth (PLG)",
            "AI-assisted features",
            "Usage-based pricing",
            "Open source alternatives",
            "Developer-first approach"
        ]
    },
    "blog": {
        "display_name": "Blog / Content Platform",
        "keywords": ["blog", "content", "magazine", "news", "article", "bài viết", "tin tức"],
        "must_have_features": [
            "Trang chủ với bài viết mới nhất",
            "Danh mục / Categories",
            "Trang chi tiết bài viết",
            "Tìm kiếm bài viết",
            "SEO-friendly URLs",
            "Responsive design",
            "RSS feed"
        ],
        "should_have_features": [
            "Comments / Bình luận",
            "Tags system",
            "Related posts",
            "Social sharing buttons",
            "Author profiles",
            "Newsletter subscription",
            "Reading time estimate"
        ],
        "could_have_features": [
            "Dark mode",
            "Bookmarks / Save for later",
            "Content series / Collections",
            "Multi-author support",
            "Analytics",
            "CMS admin panel"
        ],
        "competitors": {
            "vietnam": [
                {"name": "Viblo", "url": "viblo.asia", "strengths": "Community tech VN lớn, Markdown support", "weaknesses": "Chỉ focus tech"},
                {"name": "Spiderum", "url": "spiderum.com", "strengths": "Nội dung chất lượng, community engaged", "weaknesses": "UI dated"}
            ],
            "global": [
                {"name": "Medium", "url": "medium.com", "strengths": "Clean reading experience, built-in audience", "weaknesses": "Paywall, ít kiểm soát"},
                {"name": "Hashnode", "url": "hashnode.dev", "strengths": "Custom domain, free, dev-focused", "weaknesses": "Ít customizable"},
                {"name": "Ghost", "url": "ghost.org", "strengths": "Self-hosted, membership/newsletter built-in", "weaknesses": "Cần hosting, phí nếu dùng managed"}
            ]
        },
        "trends": [
            "Newsletter-first content",
            "AI writing assistant",
            "Paid subscriptions / Memberships",
            "Interactive content (code playgrounds)",
            "Static site + CMS (Headless)"
        ]
    },
    "portfolio": {
        "display_name": "Portfolio / Personal Website",
        "keywords": ["portfolio", "personal", "resume", "cv", "showcase", "profile"],
        "must_have_features": [
            "Hero section với giới thiệu bản thân",
            "Projects showcase (gallery/grid)",
            "About me / Bio",
            "Contact form",
            "Responsive design",
            "Social links"
        ],
        "should_have_features": [
            "Blog section",
            "Skills / Tech stack display",
            "Testimonials",
            "Download CV/Resume",
            "Dark/Light mode",
            "Animations & micro-interactions"
        ],
        "could_have_features": [
            "Interactive 3D elements",
            "Case studies (detailed project breakdown)",
            "Analytics",
            "Guestbook"
        ],
        "competitors": {
            "vietnam": [],
            "global": [
                {"name": "Dribbble portfolios", "url": "dribbble.com", "strengths": "Design community, showcase shots", "weaknesses": "Limited customization"},
                {"name": "Behance", "url": "behance.net", "strengths": "Adobe ecosystem, project-focused", "weaknesses": "Template-based"}
            ]
        },
        "trends": [
            "Motion design / GSAP animations",
            "3D with Three.js",
            "Bento grid layouts",
            "Dark mode default",
            "Minimalist with bold typography"
        ]
    },
    "landing": {
        "display_name": "Landing Page / Marketing",
        "keywords": ["landing", "marketing", "startup", "product", "launch", "giới thiệu"],
        "must_have_features": [
            "Hero section với CTA rõ ràng",
            "Features / Benefits section",
            "Social proof (testimonials, logos, numbers)",
            "Pricing section (nếu có)",
            "FAQ",
            "Footer với links & contact",
            "Mobile responsive"
        ],
        "should_have_features": [
            "Email signup / Newsletter",
            "Video demo / Product screenshots",
            "Comparison table",
            "Live chat widget",
            "Analytics tracking"
        ],
        "could_have_features": [
            "Interactive demo",
            "Animated scroll effects",
            "Multi-language",
            "A/B testing ready"
        ],
        "competitors": {
            "vietnam": [],
            "global": []
        },
        "trends": [
            "Scroll-triggered animations",
            "Glassmorphism & gradients",
            "Video backgrounds",
            "AI copywriting",
            "One-page with smooth scroll"
        ]
    }
}


def parse_args():
    parser = argparse.ArgumentParser(description="Competitor Analyzer")
    parser.add_argument("--product", type=str, required=True, help="Loại sản phẩm: ecommerce, saas, blog, portfolio, landing")
    parser.add_argument("--market", type=str, default="global", help="Thị trường: vietnam, global")
    parser.add_argument("--json", action="store_true", help="Output dạng JSON")
    return parser.parse_args()


def find_best_template(product_query):
    """Tìm template phù hợp nhất với query."""
    query_lower = product_query.lower()
    best_match = None
    best_score = 0

    for key, template in PRODUCT_TEMPLATES.items():
        score = 0
        for keyword in template["keywords"]:
            if keyword in query_lower:
                score += 10
            elif any(word in keyword for word in query_lower.split()):
                score += 3
        if score > best_score:
            best_score = score
            best_match = key

    # Default to ecommerce if no match
    if best_match is None:
        best_match = "ecommerce"

    return best_match, PRODUCT_TEMPLATES[best_match]


def analyze(product_query, market):
    """Phân tích đối thủ và features."""
    template_key, template = find_best_template(product_query)

    competitors = template["competitors"].get(market, [])
    if not competitors:
        competitors = template["competitors"].get("global", [])

    return {
        "product_type": template["display_name"],
        "template_key": template_key,
        "must_have_features": template["must_have_features"],
        "should_have_features": template["should_have_features"],
        "could_have_features": template["could_have_features"],
        "competitors": competitors,
        "trends": template["trends"],
        "market": market
    }


def print_readable(result):
    """In kết quả dạng dễ đọc."""
    print("=" * 60)
    print(f"🔍 COMPETITOR ANALYSIS: {result['product_type']}")
    print(f"   Market: {result['market']}")
    print("=" * 60)

    if result["competitors"]:
        print(f"\n{'─' * 60}")
        print("  🏢 ĐỐI THỦ CHÍNH:")
        for i, comp in enumerate(result["competitors"], 1):
            print(f"\n  {i}. {comp['name']} ({comp['url']})")
            print(f"     ✅ Điểm mạnh: {comp['strengths']}")
            print(f"     ⚠️ Điểm yếu: {comp['weaknesses']}")

    print(f"\n{'─' * 60}")
    print("  ✅ FEATURES BẮT BUỘC (Must-have):")
    for f in result["must_have_features"]:
        print(f"    • {f}")

    print(f"\n{'─' * 60}")
    print("  🟡 FEATURES NÊN CÓ (Should-have):")
    for f in result["should_have_features"]:
        print(f"    ○ {f}")

    print(f"\n{'─' * 60}")
    print("  🟢 FEATURES NÂNG CAO (Could-have):")
    for f in result["could_have_features"]:
        print(f"    ◇ {f}")

    print(f"\n{'─' * 60}")
    print("  📈 XU HƯỚNG:")
    for t in result["trends"]:
        print(f"    → {t}")

    print(f"\n{'=' * 60}")


if __name__ == "__main__":
    args = parse_args()
    result = analyze(args.product, args.market)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_readable(result)
