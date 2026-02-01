# 🐧 Linux System Administration API

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green?style=for-the-badge&logo=flask)
![Platform](https://img.shields.io/badge/Platform-Linux-orange?style=for-the-badge&logo=linux)

A powerful, RESTful API server built with Python and Flask designed to manage Linux systems remotely. It allows authorized users to manage system users, groups, files, and processes, and retrieve system information securely via HTTP requests.

---

## 📑 Table of Contents
- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Authentication](#-authentication)
- [API Reference](#-api-reference)
    - [System Information](#system-information)
    - [File Management](#file-management)
    - [Process Management](#process-management)
    - [User Management](#user-management)
    - [Group Management](#group-management)
- [Security Notice](#-security-notice)

---

## ✨ Features

- **📂 File System Operations**: Create, Read, Update, Delete files and directories. Supports recursive deletion and permission management (`chmod`, `chown`).
- **👥 User & Group Management**: Directly interact with the Linux system (`/etc/passwd`, `/etc/group`) to add, remove, or modify users and groups.
- **⚡ Process Control**: Monitor running processes and terminate them by PID.
- **🖥️ System Monitoring**: Retrieve real-time hardware and OS statistics.
- **🔒 Secure Access**: Token-based authentication system using SQLite backend.

---

## 🏗 Architecture

The API acts as a secure gateway between the HTTP client and the Linux operating system.

```mermaid
graph TD
    Client[HTTP Client] -->|JSON Requests| API[Flask API Server]
    API --> Auth{Authentication}
    Auth -->|Valid Token| Router[Route Handler]
    Auth -->|Invalid| 401[401 Unauthorized]
    
    Router --> Sys[System Info]
    Router --> Files[File Manager]
    Router --> Procs[Process Manager]
    Router --> Users[User/Group Manager]
    
    Files --> FS[(File System)]
    Procs --> Kernel[Linux Kernel]
    Users --> SysFiles[/etc/passwd & /etc/group]
    
    subgraph "Server (Root Privileges)"
        API
        Auth
        Router
        Sys
        Files
        Procs
        Users
    end
```

---

## 🚀 Installation

### Prerequisites
- **Linux OS** (Ubuntu, Debian, CentOS, etc.)
- **Python 3.8+**
- **Root/Sudo Access** (Required for user/group management and system-wide file access)

### Setup
1.  **Clone the repository**
    ```bash
    git clone https://github.com/your-repo/sys-admin-api.git
    cd sys-admin-api
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Initialize Database**
    The database (`database.db`) is initialized automatically on the first run.

4.  **Run the Server**
    ⚠️ **Note:** Must be run with `sudo` to enable system management features.
    ```bash
    sudo python app.py
    ```
    The server will start on `http://0.0.0.0:5000`.

---

## 🔐 Authentication

All API endpoints (except login) require a **Bearer Token**.

1.  **Login** to get a token:
    *   **POST** `/auth/login`
    *   **Body:** `{ "username": "admin", "password": "password" }`
    *   **Response:** `{ "token": "a1b2c3d4...", "user_id": 1 }`

2.  **Use the token** in subsequent requests:
    *   **Header:** `Authorization: a1b2c3d4...` (Note: The implementation expects the raw token in the header, not "Bearer <token>").

---

## 📚 API Reference

### System Information

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/systems/` | Get CPU, Memory, and OS details. |

### File Management

| Method | Endpoint | Parameters / Body | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/files/` | `?path=/tmp/test` | **Unified Endpoint:** <br>• **File:** Returns content. <br>• **Directory:** Returns detailed metadata list ordered by: `name`, `type`, `owner`, `permissions`, `group`, `size`, `modified`. |
| `POST` | `/files/` | `{ "path": "/tmp/new", "is_dir": true }` | Create a file or directory. |
| `PUT` | `/files/` | `?path=/tmp/file`<br>Body: `{ "content": "text", "chmod": "755" }` | Update content, permissions, or owner. |
| `DELETE`| `/files/` | `?path=/tmp/file&recursive=true` | Delete a file or directory. |

### Process Management

| Method | Endpoint | Parameters | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/processes/` | `?limit=50` | List running processes. |
| `DELETE`| `/processes/<pid>` | | Terminate (Kill) a process. |

### User Management

**⚠️ Affects actual system users (`/etc/passwd`)**

| Method | Endpoint | Body | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/users/` | | List all system users. |
| `POST` | `/users/` | `{ "username": "dave", "password": "123" }` | Create a new Linux user. |
| `PUT` | `/users/<name>`| `{ "groups": "sudo", "shell": "/bin/bash" }` | Modify user groups, shell, or password. |
| `DELETE`| `/users/<name>`| | Delete a user and their home directory. |

### Group Management

**⚠️ Affects actual system groups (`/etc/group`)**

| Method | Endpoint | Body | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/groups/` | | List all system groups. |
| `POST` | `/groups/` | `{ "name": "devops" }` | Create a new group. |
| `PUT` | `/groups/<name>`| `{ "name": "engineers" }` | Rename a group. |

---

## 🛡 Security Notice

This application runs with **root privileges** and exposes critical system functionality over a network interface. 

*   **Production Use:** NEVER run this on a public network without a reverse proxy (Nginx/Apache) handling SSL/TLS encryption.
*   **Firewall:** Restrict access to the API port (5000) to trusted IP addresses only.
*   **Token Safety:** Keep authentication tokens secure.

---

*Generated by Gemini CLI*
