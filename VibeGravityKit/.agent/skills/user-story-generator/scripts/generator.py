#!/usr/bin/env python3
"""
User Story Generator — Tạo user stories template từ features và roles.

Usage:
    python generator.py --features "login,product listing,cart,checkout" --roles "buyer,admin"
"""

import argparse
import json
import sys

# === Templates user stories theo feature type ===
STORY_TEMPLATES = {
    "login": {
        "title": "Đăng nhập",
        "stories": [
            {
                "role": "user",
                "action": "đăng nhập bằng email và mật khẩu",
                "benefit": "truy cập tài khoản và sử dụng các tính năng cá nhân",
                "priority": "Must",
                "size": "M",
                "criteria": [
                    "Given trang login, when nhập email + password đúng, then chuyển hướng tới dashboard/trang chủ",
                    "Given trang login, when nhập sai password 3 lần, then hiện thông báo và cho retry sau 30s",
                    "Given chưa đăng nhập, when truy cập trang protected, then redirect tới login page",
                    "Given đăng nhập thành công, when reload page, then vẫn giữ session"
                ]
            },
            {
                "role": "user",
                "action": "đăng nhập bằng Google/Facebook",
                "benefit": "đăng nhập nhanh không cần nhớ mật khẩu",
                "priority": "Should",
                "size": "M",
                "criteria": [
                    "Given trang login, when click 'Đăng nhập bằng Google', then redirect tới Google OAuth",
                    "Given OAuth thành công, when callback, then tạo/cập nhật tài khoản và đăng nhập"
                ]
            }
        ]
    },
    "register": {
        "title": "Đăng ký tài khoản",
        "stories": [
            {
                "role": "user",
                "action": "đăng ký tài khoản mới bằng email",
                "benefit": "bắt đầu sử dụng dịch vụ",
                "priority": "Must",
                "size": "M",
                "criteria": [
                    "Given trang đăng ký, when nhập thông tin hợp lệ, then tạo tài khoản thành công",
                    "Given email đã tồn tại, when đăng ký, then hiện lỗi 'Email đã được sử dụng'",
                    "Given password yếu, when submit, then hiện yêu cầu password mạnh hơn",
                    "Given đăng ký thành công, when hoàn tất, then gửi email xác nhận"
                ]
            }
        ]
    },
    "product listing": {
        "title": "Danh sách sản phẩm",
        "stories": [
            {
                "role": "buyer",
                "action": "xem danh sách sản phẩm theo danh mục",
                "benefit": "tìm được sản phẩm mình quan tâm",
                "priority": "Must",
                "size": "L",
                "criteria": [
                    "Given trang danh mục, when load page, then hiển thị sản phẩm dạng grid/list",
                    "Given có nhiều sản phẩm, when scroll, then load thêm (infinite scroll hoặc pagination)",
                    "Given mỗi sản phẩm, when hiển thị, then có ảnh, tên, giá, rating"
                ]
            },
            {
                "role": "buyer",
                "action": "filter sản phẩm theo giá, màu, size",
                "benefit": "nhanh chóng tìm đúng sản phẩm phù hợp",
                "priority": "Should",
                "size": "M",
                "criteria": [
                    "Given trang danh mục, when chọn filter giá, then chỉ hiện sản phẩm trong range",
                    "Given nhiều filters, when chọn cùng lúc, then kết hợp AND filters",
                    "Given filter đang active, when bỏ filter, then reset danh sách"
                ]
            },
            {
                "role": "buyer",
                "action": "tìm kiếm sản phẩm bằng từ khóa",
                "benefit": "tìm nhanh sản phẩm biết tên",
                "priority": "Must",
                "size": "M",
                "criteria": [
                    "Given search bar, when nhập keyword, then hiện kết quả liên quan",
                    "Given keyword không match, when search, then hiện 'Không tìm thấy sản phẩm'",
                    "Given đang gõ, when dừng 300ms, then auto-suggest kết quả"
                ]
            }
        ]
    },
    "product detail": {
        "title": "Chi tiết sản phẩm",
        "stories": [
            {
                "role": "buyer",
                "action": "xem chi tiết sản phẩm với ảnh, giá, mô tả",
                "benefit": "đánh giá sản phẩm trước khi mua",
                "priority": "Must",
                "size": "M",
                "criteria": [
                    "Given trang chi tiết, when load, then hiện gallery ảnh, giá, mô tả đầy đủ",
                    "Given sản phẩm có biến thể, when chọn size/màu, then cập nhật giá và tồn kho",
                    "Given ảnh sản phẩm, when click, then zoom/lightbox"
                ]
            }
        ]
    },
    "cart": {
        "title": "Giỏ hàng",
        "stories": [
            {
                "role": "buyer",
                "action": "thêm sản phẩm vào giỏ hàng",
                "benefit": "lưu sản phẩm muốn mua để thanh toán sau",
                "priority": "Must",
                "size": "M",
                "criteria": [
                    "Given trang chi tiết sản phẩm, when click 'Thêm vào giỏ', then sản phẩm được thêm vào cart",
                    "Given sản phẩm đã có trong giỏ, when thêm lại, then tăng số lượng",
                    "Given thêm thành công, when animation, then hiện badge số lượng trên cart icon"
                ]
            },
            {
                "role": "buyer",
                "action": "xem và chỉnh sửa giỏ hàng",
                "benefit": "review lại trước khi thanh toán",
                "priority": "Must",
                "size": "M",
                "criteria": [
                    "Given trang giỏ hàng, when load, then hiện danh sách sản phẩm với ảnh, tên, giá, số lượng",
                    "Given item trong giỏ, when thay đổi số lượng, then cập nhật tổng tiền",
                    "Given item trong giỏ, when click xóa, then remove khỏi giỏ",
                    "Given giỏ hàng trống, when load, then hiện 'Giỏ hàng trống' + link tới shop"
                ]
            }
        ]
    },
    "checkout": {
        "title": "Thanh toán",
        "stories": [
            {
                "role": "buyer",
                "action": "thanh toán đơn hàng",
                "benefit": "hoàn tất mua sản phẩm",
                "priority": "Must",
                "size": "L",
                "criteria": [
                    "Given trang checkout, when load, then hiện form địa chỉ giao hàng",
                    "Given form hợp lệ, when chọn phương thức thanh toán, then hiện chi tiết thanh toán",
                    "Given thanh toán thành công, when hoàn tất, then hiện trang confirmation + gửi email",
                    "Given thanh toán thất bại, when error, then hiện thông báo lỗi + cho retry"
                ]
            }
        ]
    },
    "admin": {
        "title": "Quản trị",
        "stories": [
            {
                "role": "admin",
                "action": "quản lý sản phẩm (thêm, sửa, xóa)",
                "benefit": "cập nhật catalog sản phẩm",
                "priority": "Must",
                "size": "L",
                "criteria": [
                    "Given admin panel, when thêm sản phẩm mới, then sản phẩm hiện trên website",
                    "Given danh sách sản phẩm, when sửa thông tin, then cập nhật ngay",
                    "Given sản phẩm, when xóa, then confirm trước khi xóa vĩnh viễn"
                ]
            },
            {
                "role": "admin",
                "action": "xem và quản lý đơn hàng",
                "benefit": "xử lý đơn hàng kịp thời",
                "priority": "Must",
                "size": "M",
                "criteria": [
                    "Given admin panel, when xem đơn hàng, then hiện danh sách với filter trạng thái",
                    "Given đơn hàng mới, when cập nhật trạng thái, then thông báo cho buyer"
                ]
            }
        ]
    },
    "dashboard": {
        "title": "Dashboard",
        "stories": [
            {
                "role": "user",
                "action": "xem dashboard với thống kê tổng quan",
                "benefit": "nắm bắt nhanh tình hình",
                "priority": "Must",
                "size": "L",
                "criteria": [
                    "Given dashboard, when load, then hiện cards thống kê (users, revenue, orders...)",
                    "Given charts, when hover, then hiện tooltip chi tiết",
                    "Given data thay đổi, when refresh, then cập nhật realtime"
                ]
            }
        ]
    },
    "profile": {
        "title": "Hồ sơ cá nhân",
        "stories": [
            {
                "role": "user",
                "action": "xem và chỉnh sửa thông tin cá nhân",
                "benefit": "cập nhật thông tin tài khoản",
                "priority": "Should",
                "size": "S",
                "criteria": [
                    "Given trang profile, when load, then hiện thông tin hiện tại",
                    "Given form edit, when submit, then cập nhật và hiện thông báo thành công",
                    "Given upload avatar, when chọn ảnh, then resize và lưu"
                ]
            }
        ]
    }
}


def parse_args():
    parser = argparse.ArgumentParser(description="User Story Generator")
    parser.add_argument("--features", type=str, required=True, help="Danh sách features, phân cách bằng dấu phẩy")
    parser.add_argument("--roles", type=str, default="user", help="Danh sách roles, phân cách bằng dấu phẩy")
    parser.add_argument("--json", action="store_true", help="Output dạng JSON")
    return parser.parse_args()


def find_matching_template(feature_query):
    """Tìm template phù hợp nhất với feature query."""
    query_lower = feature_query.lower().strip()

    # Direct match
    if query_lower in STORY_TEMPLATES:
        return STORY_TEMPLATES[query_lower]

    # Partial match
    for key, template in STORY_TEMPLATES.items():
        if key in query_lower or query_lower in key:
            return template
        if template["title"].lower() in query_lower or query_lower in template["title"].lower():
            return template

    return None


def generate_stories(features, roles):
    """Generate user stories từ features."""
    all_stories = []
    story_id = 1

    for feature in features:
        template = find_matching_template(feature)

        if template:
            for story in template["stories"]:
                # Replace role if needed
                role = story["role"]
                if role == "user" and roles and roles[0] != "user":
                    role = roles[0]

                all_stories.append({
                    "id": f"US-{story_id:03d}",
                    "feature": template["title"],
                    "role": role,
                    "action": story["action"],
                    "benefit": story["benefit"],
                    "priority": story["priority"],
                    "size": story["size"],
                    "criteria": story["criteria"]
                })
                story_id += 1
        else:
            # Generate generic story for unknown features
            all_stories.append({
                "id": f"US-{story_id:03d}",
                "feature": feature.strip().title(),
                "role": roles[0] if roles else "user",
                "action": f"sử dụng tính năng {feature.strip()}",
                "benefit": "đáp ứng nhu cầu sử dụng",
                "priority": "Should",
                "size": "M",
                "criteria": [
                    f"Given trang {feature.strip()}, when load, then hiển thị đầy đủ nội dung",
                    f"Given {feature.strip()}, when tương tác, then phản hồi đúng mong đợi"
                ]
            })
            story_id += 1

    return all_stories


def print_readable(stories):
    """In user stories dạng dễ đọc."""
    priority_emoji = {"Must": "🔴", "Should": "🟡", "Could": "🟢", "Won't": "⚪"}

    print("=" * 60)
    print("📝 USER STORIES")
    print("=" * 60)

    current_feature = ""
    for story in stories:
        if story["feature"] != current_feature:
            current_feature = story["feature"]
            print(f"\n{'━' * 60}")
            print(f"  📌 {current_feature}")
            print(f"{'━' * 60}")

        emoji = priority_emoji.get(story["priority"], "⚪")
        print(f"\n  {story['id']}: {story['action']}")
        print(f"  Priority: {emoji} {story['priority']} | Size: {story['size']}")
        print(f"  As a {story['role']}, I want to {story['action']},")
        print(f"  so that {story['benefit']}.")
        print(f"  Acceptance Criteria:")
        for ac in story["criteria"]:
            print(f"    ☐ {ac}")

    # Summary
    total = len(stories)
    by_priority = {}
    for s in stories:
        by_priority[s["priority"]] = by_priority.get(s["priority"], 0) + 1

    print(f"\n{'=' * 60}")
    print(f"  📊 Tổng: {total} stories")
    for p, count in sorted(by_priority.items()):
        emoji = priority_emoji.get(p, "⚪")
        print(f"    {emoji} {p}: {count}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    args = parse_args()

    features = [f.strip() for f in args.features.split(",") if f.strip()]
    roles = [r.strip() for r in args.roles.split(",") if r.strip()]

    stories = generate_stories(features, roles)

    if args.json:
        print(json.dumps(stories, ensure_ascii=False, indent=2))
    else:
        print_readable(stories)
