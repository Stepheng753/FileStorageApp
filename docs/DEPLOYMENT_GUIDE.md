# Tooth Manager - Production VPS Deployment Guide

This guide documents the exact production server architecture and deployment configuration for Tooth Manager on `dev.toothmanager.com` (`69.62.71.85`).

---

## 1. Production Server Overview

| Property | Configuration |
| :--- | :--- |
| **Server Hostname** | `srv805154` |
| **Public IP** | `69.62.71.85` |
| **Domain** | `dev.toothmanager.com` |
| **SSH User** | `stepheng753` |
| **App Group** | `www-data` |
| **Repository Root** | `/home/stepheng753/FileStorageApp` |
| **Backend Root** | `/home/stepheng753/FileStorageApp/Backend` |
| **Virtual Environment** | `/home/stepheng753/FileStorageApp/.venv` |
| **Static Storage Path** | `/home/stepheng753/FileStorageApp/Backend/static/` |
| **Database Path** | `/home/stepheng753/FileStorageApp/Backend/database/users.db` |
| **Gunicorn Unix Socket**| `/tmp/gunicorn.sock` |

---

## 2. Nginx Web Server Configuration

The site is configured at `/etc/nginx/sites-available/dev.toothmanager.com`:

```nginx
server {
    server_name dev.toothmanager.com;

    client_max_body_size 1G;

    # Serve static files directly from the filesystem for high speed
    location /static/ {
        alias /home/stepheng753/FileStorageApp/Backend/static/;
        try_files $uri $uri/ =404;
    }

    # Proxy all API requests and application routes to Gunicorn Unix socket
    location / {
        proxy_pass http://unix:/tmp/gunicorn.sock;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/dev.toothmanager.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/dev.toothmanager.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

server {
    listen 80;
    server_name dev.toothmanager.com;
    return 301 https://$host$request_uri;
}
```

To test and reload Nginx:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

## 3. Gunicorn Systemd Service

The application runs as a systemd service managed at `/etc/systemd/system/gunicorn.service`:

```ini
[Unit]
Description=Gunicorn application server for dev.toothmanager.com
After=network.target

[Service]
User=stepheng753
Group=www-data
WorkingDirectory=/home/stepheng753/FileStorageApp/Backend
ExecStart=/home/stepheng753/FileStorageApp/.venv/bin/gunicorn app:app --bind unix:/tmp/gunicorn.sock -m 007 --limit-request-line 8190 --timeout 1800

[Install]
WantedBy=multi-user.target
```

### Key Service Parameters:
- `--bind unix:/tmp/gunicorn.sock`: Creates high-performance local Unix socket.
- `-m 007`: Sets socket permissions so user `stepheng753` and group `www-data` have read/write access.
- `--limit-request-line 8190`: Handles long request query strings safely.
- `--timeout 1800`: 30-minute timeout to allow uploading massive files (up to 1 GB).

### Useful Service Commands:
```bash
# Restart the backend service
sudo systemctl restart gunicorn

# Check service status
sudo systemctl status gunicorn

# View live service logs
sudo journalctl -u gunicorn -f -n 50
```

---

## 4. File Storage Directory & Permissions

Because Gunicorn runs under user `stepheng753` and group `www-data`, the file storage directory must allow both to read and write:

```bash
# Ensure directory exists
mkdir -p /home/stepheng753/FileStorageApp/Backend/static

# Set ownership
sudo chown -R stepheng753:www-data /home/stepheng753/FileStorageApp/Backend/static

# Set directory permissions (rwxrwxr-x)
chmod -R 775 /home/stepheng753/FileStorageApp/Backend/static
```

---

## 5. Configuration via `secrets.json`

Create the production configuration on the server at `/home/stepheng753/FileStorageApp/Backend/secrets.json`:

```json
{
  "SECRET_KEY": "PROD_SECURE_RANDOM_KEY_HERE",
  "JWT_SECRET_KEY": "PROD_JWT_SIGNING_KEY_HERE",
  "JWT_EXPIRES_HOURS": 24,
  "SERVER_NAME": null,
  "DATABASE_PATH": "database/users.db",
  "STORAGE_DIR": "static",
  "CORS_ORIGINS": [
    "https://dev.toothmanager.com",
    "http://localhost:3000"
  ],
  "PORT": 3000
}
```

*Note: `secrets.json` is gitignored to protect sensitive keys from leaking.*
