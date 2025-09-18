# Jupyter configuration for secure lab environment
c = get_config()

# Security and interface settings
c.NotebookApp.allow_root = True
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.NotebookApp.token = ''
c.NotebookApp.password = ''

# Disable file browser and hide system files
c.ContentsManager.hide_globs = [
    '.*', '*.pyc', '*.pyo', '__pycache__',
    'Dockerfile', 'Procfile', 'requirements.txt', 
    'README.md', 'app.json', '.python-version',
    'utils.py'
]

# Set default to open the lab notebook directly
c.NotebookApp.default_url = '/notebooks/lab_notebook.ipynb'

# Disable terminals and other potentially dangerous features
c.NotebookApp.terminals_enabled = False
c.LabApp.terminals_enabled = False

# Additional security
c.NotebookApp.disable_check_xsrf = False
