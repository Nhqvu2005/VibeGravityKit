#!/usr/bin/env python3
"""
Readme Generator — Create Engaging, Standardized Project Docs.

Usage:
    python readme_gen.py --name "Project Name" --slogan "The best project ever"
"""

import argparse

TEMPLATE_ENGAGING = """# 🚀 {name}

> {slogan}

![Banner](https://via.placeholder.com/1000x300?text=Project+Banner)

## 🌟 Why {name}?
Explain the unique value prop here. Why should users care?
- **Fast**: Built for speed.
- **Simple**: Easy to use.
- **Secure**: Privacy first.

## ✨ Features
| Feature | Description |
| :--- | :--- |
| ⚡ **Instant Setup** | Get running in < 5 seconds. |
| 🛡️ **Secure** | Enterprise-grade encryption. |
| 🎨 **Themable** | Dark mode included. |

## 🛠️ Installation

### Prerequisites
- Node.js 18+
- Python 3.9+

### Quick Start
```bash
# 1. Clone the repo
git clone https://github.com/my-org/{slug}.git

# 2. Install dependencies
npm install

# 3. Start the engine
npm start
```

## 📖 Usage
Describe how to use the project here.

### Example: Basic Usage
```python
import my_lib

# Initialize
app = my_lib.App()

# Run magic
app.do_magic()
```

## 🤝 Contributing
We love contributions! Please read our [Contributing Guide](CONTRIBUTING.md).

## 📄 License
MIT © [Your Name]
"""

def generate(name, slogan):
    slug = name.lower().replace(' ', '-')
    print(TEMPLATE_ENGAGING.format(name=name, slogan=slogan, slug=slug))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", default="My Awesome Project")
    parser.add_argument("--slogan", default="Building the future, one line at a time.")
    args = parser.parse_args()
    generate(args.name, args.slogan)

if __name__ == "__main__":
    main()
