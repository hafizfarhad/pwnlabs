# Jupyter configuration for secure lab environment
c = get_config()

# Security and interface settings
c.NotebookApp.allow_root = True
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.NotebookApp.token = ''
c.NotebookApp.password = ''

# Hide system and configuration files from file browser
c.ContentsManager.hide_globs = [
    '.*', '*.pyc', '*.pyo', '__pycache__',
    'Dockerfile', 'Procfile', 'requirements.txt', 
    'README.md', 'app.json', '.python-version',
    'utils.py', 'jupyter_config.py', 'index.html'
]

# Set root directory and default file
c.NotebookApp.notebook_dir = '/'
c.NotebookApp.default_url = '/notebooks/lab_notebook.ipynb'

# Disable terminals and file operations for security
c.NotebookApp.terminals_enabled = False
c.NotebookApp.shutdown_no_activity_timeout = 1800  # 30 minutes

# Additional security
c.NotebookApp.disable_check_xsrf = False
c.NotebookApp.allow_remote_access = True
