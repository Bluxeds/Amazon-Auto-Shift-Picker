# Amazon Auto Shift Picker

> Automate your Amazon shift selection process with this powerful, easy-to-use tool.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

Amazon Auto Shift Picker is an automated solution designed to streamline the process of selecting shifts on Amazon Flex and similar platforms. This tool eliminates the manual effort required to monitor and claim available shifts, allowing you to focus on what matters.

### Why Use This Tool?

- ✨ **Saves Time**: Automatically monitors and claims shifts
- 🚀 **Reliable**: Consistent performance with error handling
- ⚙️ **Customizable**: Configure preferences to match your needs
- 🔒 **Secure**: Handles credentials safely

---

## ✨ Features

### Core Functionality

- **Automated Shift Detection**: Continuously monitors available shifts
- **Smart Selection**: Intelligently selects shifts based on your preferences
- **Real-time Notifications**: Get alerts when shifts are claimed
- **Error Handling**: Robust error detection and recovery
- **Logging**: Detailed logs for debugging and monitoring

### Advanced Options

- Multi-account support
- Custom filtering and sorting
- Scheduled automation
- Performance metrics and analytics

---

## 📦 Requirements

- **Python**: Version 3.8 or higher
- **Dependencies**: See `requirements.txt`
- **OS**: Windows, macOS, or Linux
- **Browser**: Modern browser with Selenium support (Chrome/Firefox)

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/Bluxeds/Amazon-Auto-Shift-Picker.git
cd Amazon-Auto-Shift-Picker
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Settings

Create a `config.json` file in the root directory with your preferences:

```json
{
  "username": "your_amazon_email",
  "headless_mode": true,
  "check_interval": 30,
  "preferred_shifts": ["4-hour", "8-hour"]
}
```

---

## 💻 Usage

### Basic Usage

```bash
python main.py
```

### With Configuration File

```bash
python main.py --config config.json
```

### Command Line Arguments

| Argument | Description |
|----------|-------------|
| `--config` | Path to configuration file |
| `--headless` | Run in headless mode |
| `--debug` | Enable debug logging |
| `--test` | Run in test mode |

### Example Workflow

1. Update `config.json` with your preferences
2. Run the script: `python main.py`
3. Monitor logs for shift selection confirmations
4. Check your Amazon account for claimed shifts

---

## ⚙️ Configuration

### Config File Options

```json
{
  "username": "your_email@example.com",
  "password": "your_password",
  "headless_mode": true,
  "check_interval": 30,
  "preferred_locations": ["warehouse_a", "warehouse_b"],
  "preferred_shifts": ["4-hour", "8-hour"],
  "min_pay": 15.00,
  "notification_enabled": true,
  "notification_method": "email"
}
```

### Environment Variables

Alternative to config file:

```bash
export AMAZON_USERNAME="your_email@example.com"
export AMAZON_PASSWORD="your_password"
export CHECK_INTERVAL=30
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. **Login Fails**
- Verify credentials in `config.json`
- Check if Two-Factor Authentication is enabled
- Temporarily disable 2FA or add app-specific password

#### 2. **Shifts Not Being Detected**
- Increase `check_interval` in configuration
- Verify your account has access to shifts
- Check browser compatibility

#### 3. **Script Crashes**
- Review logs in `logs/` directory
- Ensure all dependencies are installed
- Run with `--debug` flag for more details

#### 4. **Selenium Errors**
- Update WebDriver: `pip install --upgrade webdriver-manager`
- Verify browser is installed (Chrome/Firefox)

### Getting Help

- Check logs in `logs/` directory
- Review GitHub Issues for similar problems
- Enable debug mode: `python main.py --debug`

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Steps to Contribute

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature`
3. **Commit** changes: `git commit -m "Add your feature"`
4. **Push** to branch: `git push origin feature/your-feature`
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- Keep commits focused and descriptive

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

This tool is provided for educational purposes. Users are responsible for ensuring their use complies with Amazon's Terms of Service and applicable laws. Misuse of automation tools may result in account suspension.

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Bluxeds/Amazon-Auto-Shift-Picker/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Bluxeds/Amazon-Auto-Shift-Picker/discussions)

---

**Last Updated**: 2025-12-10 | **Version**: 1.0.0
