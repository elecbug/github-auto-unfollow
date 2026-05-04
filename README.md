# GitHub Auto Unfollow Tool

A Python script to automatically clean up your GitHub following list by unfollowing users who do not follow you back.

Organizations and whitelisted accounts are automatically excluded.

---

## ✨ Features

* Fetches full followers and following lists (handles pagination)
* Detects non-mutual follows (not following back)
* Automatically excludes Organization accounts
* Supports whitelist for protected accounts
* Interactive confirmation (`y / n / q`) before unfollowing
* Uses GitHub REST API

---

## 📦 Requirements

* Python 3.x
* `requests`

```bash
pip install requests
```

---

## 🔐 Setup

### 1. Create a GitHub Personal Access Token

Go to GitHub:

* `Settings → Developer settings → Personal access tokens`
* Required scope: `user:follow`

---

### 2. Create Credential File

Create a file named:

```
NAME_AND_TOKEN
```

Format:

```
your_github_username
your_personal_access_token
```

---

### 3. (Optional) Create Whitelist

Create a file named:

```
WHITELIST
```

Each line contains a username or organization to exclude:

```
microsoft
apple
torvalds
```

---

## 🚀 Usage

Run the script:

```bash
python github_auto_unfollow.py
```

Example output:

```
Followers: 120, Following: 180
Users not following me back: ['user1', 'user2']

user1 Unfollow? (y(es)/n(o)/q(uit)):
```

Options:

* `y` → Unfollow
* `n` → Skip
* `q` → Quit immediately

---

## ⚠️ Notes

* Organization accounts are automatically excluded (they cannot follow users back)
* GitHub API rate limits may apply
* Your social graph (followers/following) may be exposed if logs are shared publicly
* Do **NOT** commit these files:

  * `NAME_AND_TOKEN`
  * `WHITELIST`

---

## 🔧 API Details

This tool uses:

* `GET /users/{username}/followers`
* `GET /users/{username}/following`
* `GET /users/{login}` (to detect Organization)
* `DELETE /user/following/{username}`