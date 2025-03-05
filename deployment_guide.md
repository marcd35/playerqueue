# Queue Tracker Deployment Guide

This document outlines how to deploy the Queue Tracker application on various hosting platforms, including Hostinger.

## Project Structure

The application has been organized into separate files for better maintainability:

```
queue-tracker/
├── app.py                 # Flask application entry point
├── queue_tracker.py       # Backend queue tracking logic
├── requirements.txt       # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css      # Styles (optional, currently embedded in HTML)
│   └── js/
│       └── main.js        # Frontend JavaScript logic
├── templates/
│   └── index.html         # HTML template (references main.js)
└── wsgi.py                # WSGI entry point for production deployment
```

## Setup Instructions

### 1. Local Development

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the development server**:
   ```bash
   python app.py
   ```

5. **Access the application**:
   - Open http://127.0.0.1:5000/ in your browser

### 2. Deployment on Hostinger

#### A. Shared Hosting with cPanel

1. **Log in to your Hostinger control panel**

2. **Create a Python application (if available)**:
   - Navigate to the "Python" or "Setup Python App" section
   - Create a new application and select Python 3.x
   - Set the application path to your domain or subdomain

3. **Upload your files**:
   - Use FTP or the file manager to upload all project files
   - Ensure proper directory structure

4. **Install dependencies**:
   - Connect via SSH (if available) and run:
     ```bash
     pip install -r requirements.txt
     ```
   - If SSH is not available, check if Hostinger has a way to install Python packages through cPanel

5. **Configure .htaccess**:
   - Create an `.htaccess` file in your root directory:
     ```apache
     <IfModule mod_rewrite.c>
         RewriteEngine On
         RewriteBase /
         RewriteRule ^(.*)$ wsgi.py [L]
     </IfModule>
     ```

#### B. Using Hostinger with Python Selector

If Hostinger provides a Python Selector or similar tool:

1. **Create a Python application**:
   - Select Python 3.x
   - Set your application path
   - Configure the entry point to `wsgi.py`

2. **Upload your files** as described above

3. **Set environment variables** if needed

#### C. Using Docker (if supported by Hostinger)

1. **Create a Dockerfile**:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app"]
   ```

2. **Build and deploy** the Docker container

### 3. Production Considerations

1. **Use a production WSGI server**:
   - Add a WSGI server to your requirements:
     ```bash
     pip install gunicorn  # or waitress for Windows
     ```
   - Create a `wsgi.py` file:
     ```python
     from app import app
     
     if __name__ == "__main__":
         app.run()
     ```
   - Run with gunicorn:
     ```bash
     gunicorn --bind 0.0.0.0:8080 wsgi:app
     ```

2. **Enable HTTPS**:
   - Set up SSL certificates (Let's Encrypt is free)
   - Configure your web server to use HTTPS

3. **Set DEBUG=False in production**:
   - Modify `app.py` to use environment variables:
     ```python
     debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
     app.run(debug=debug_mode, host='0.0.0.0', port=port)
     ```

## Troubleshooting

1. **Import errors**:
   - Ensure all Python dependencies are installed
   - Check if your hosting provider supports the required Python version

2. **Permission issues**:
   - Set proper file permissions:
     ```bash
     chmod 755 *.py
     chmod 644 *.html *.css *.js
     ```

3. **Path issues**:
   - Make sure the file paths are correct for your hosting environment
   - Some hosts may require absolute paths

4. **502/504 errors**:
   - Check server logs for specific error messages
   - May indicate a timeout or memory issue

## Additional Resources

- Flask Deployment: https://flask.palletsprojects.com/en/2.0.x/deploying/
- Hostinger Python Support: Check Hostinger's knowledge base
- Contact Hostinger Support for hosting-specific configuration needs

For any further questions or issues, consult Hostinger's documentation or contact their support team.