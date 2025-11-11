#!/usr/bin/env python3
"""
Deployment Verification Script for Roboto SAI
Checks if all required dependencies and configurations are in place
"""

import sys
import os
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{BLUE}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{RESET}\n")

def print_success(text):
    """Print success message"""
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    """Print error message"""
    print(f"{RED}✗ {text}{RESET}")

def print_warning(text):
    """Print warning message"""
    print(f"{YELLOW}⚠ {text}{RESET}")

def print_info(text):
    """Print info message"""
    print(f"{BLUE}ℹ {text}{RESET}")

def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    required_major = 3
    required_minor_min = 10
    
    print(f"Current Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == required_major and version.minor >= required_minor_min:
        print_success(f"Python version {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print_error(f"Python {required_major}.{required_minor_min}+ is required")
        return False

def check_required_files():
    """Check if all required deployment files exist"""
    print_header("Checking Required Files")
    
    required_files = {
        'main.py': 'Application entry point',
        'app_enhanced.py': 'Flask application',
        'requirements.txt': 'Python dependencies',
        'Procfile': 'Process configuration for Heroku',
        'runtime.txt': 'Python runtime version',
        '.env.example': 'Environment variables template',
        'templates/index.html': 'Main template',
        'static/': 'Static files directory'
    }
    
    all_present = True
    for file_path, description in required_files.items():
        path = Path(file_path)
        if path.exists():
            print_success(f"{file_path} - {description}")
        else:
            print_error(f"{file_path} - {description} [MISSING]")
            all_present = False
    
    return all_present

def check_dependencies():
    """Check if critical dependencies can be imported"""
    print_header("Checking Critical Dependencies")
    
    critical_deps = [
        ('flask', 'Flask web framework'),
        ('flask_sqlalchemy', 'Database ORM'),
        ('dotenv', 'Environment variables'),
        ('werkzeug', 'WSGI utilities'),
    ]
    
    optional_deps = [
        ('torch', 'PyTorch for ML'),
        ('qiskit', 'Quantum computing'),
        ('openai', 'OpenAI API'),
        ('librosa', 'Audio processing'),
    ]
    
    critical_ok = True
    
    print("Critical dependencies:")
    for module_name, description in critical_deps:
        try:
            __import__(module_name)
            print_success(f"{module_name:20} - {description}")
        except ImportError:
            print_error(f"{module_name:20} - {description} [NOT INSTALLED]")
            critical_ok = False
    
    print("\nOptional dependencies (warnings only):")
    for module_name, description in optional_deps:
        try:
            __import__(module_name)
            print_success(f"{module_name:20} - {description}")
        except ImportError:
            print_warning(f"{module_name:20} - {description} [NOT INSTALLED - some features may not work]")
    
    return critical_ok

def check_environment_variables():
    """Check if required environment variables are set"""
    print_header("Checking Environment Variables")
    
    # Load .env file if it exists
    env_file = Path('.env')
    if env_file.exists():
        print_success(".env file found")
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            print_warning("python-dotenv not installed, cannot load .env file")
    else:
        print_warning(".env file not found - will check environment variables only")
    
    required_vars = {
        'SESSION_SECRET': 'Flask session encryption key (CRITICAL)',
    }
    
    recommended_vars = {
        'FLASK_ENV': 'Flask environment (development/production)',
        'DATABASE_URL': 'Database connection string',
        'OPENAI_API_KEY': 'OpenAI API access',
        'XAI_API_KEY': 'xAI API access',
    }
    
    all_required = True
    
    print("Required variables:")
    for var_name, description in required_vars.items():
        value = os.getenv(var_name)
        if value:
            # Don't print the actual value for security
            print_success(f"{var_name:20} - {description} [SET]")
        else:
            print_error(f"{var_name:20} - {description} [NOT SET]")
            all_required = False
    
    print("\nRecommended variables:")
    for var_name, description in recommended_vars.items():
        value = os.getenv(var_name)
        if value:
            print_success(f"{var_name:20} - {description} [SET]")
        else:
            print_warning(f"{var_name:20} - {description} [NOT SET]")
    
    return all_required

def check_gunicorn_config():
    """Check if gunicorn is properly configured"""
    print_header("Checking Gunicorn Configuration")
    
    procfile = Path('Procfile')
    if procfile.exists():
        content = procfile.read_text()
        if 'gunicorn' in content:
            print_success("Procfile contains gunicorn configuration")
            print(f"  Content: {content.strip()}")
        else:
            print_error("Procfile exists but doesn't mention gunicorn")
            return False
    else:
        print_error("Procfile not found")
        return False
    
    # Check if gunicorn is in requirements.txt
    requirements = Path('requirements.txt')
    if requirements.exists():
        content = requirements.read_text()
        if 'gunicorn' in content.lower():
            print_success("gunicorn is in requirements.txt")
        else:
            print_error("gunicorn is NOT in requirements.txt")
            return False
    
    return True

def check_database():
    """Check database connectivity"""
    print_header("Checking Database")
    
    db_url = os.getenv('DATABASE_URL', 'sqlite:///roboto_sai_complete.db')
    print(f"Database URL: {db_url}")
    
    if db_url.startswith('sqlite:///'):
        db_file = db_url.replace('sqlite:///', '')
        if Path(db_file).exists():
            print_success(f"SQLite database file exists: {db_file}")
        else:
            print_warning(f"SQLite database file doesn't exist yet: {db_file}")
            print_info("Database will be created on first run")
    elif db_url.startswith(('postgresql://', 'postgres://')):
        print_info("PostgreSQL database configured (cannot test connection without credentials)")
    else:
        print_warning(f"Unknown database type: {db_url}")
    
    return True

def check_import_main():
    """Try to import the main application"""
    print_header("Testing Application Import")
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.getcwd())
        
        # Try importing main
        print_info("Attempting to import main module...")
        from main import app
        print_success("Successfully imported Flask app from main.py")
        
        # Check if app has required attributes
        if hasattr(app, 'secret_key') and app.secret_key:
            print_success("Flask app has secret_key configured")
        else:
            print_warning("Flask app doesn't have secret_key - check SESSION_SECRET")
        
        return True
        
    except ImportError as e:
        print_error(f"Failed to import main.py: {e}")
        print_info("This is expected if dependencies are not installed yet")
        return False
    except Exception as e:
        print_error(f"Error importing application: {e}")
        return False

def generate_report(checks):
    """Generate final deployment readiness report"""
    print_header("Deployment Readiness Report")
    
    passed = sum(checks.values())
    total = len(checks)
    
    for check_name, result in checks.items():
        status = "✓ PASS" if result else "✗ FAIL"
        color = GREEN if result else RED
        print(f"{color}{status:10}{RESET} - {check_name}")
    
    print(f"\n{BLUE}Score: {passed}/{total} checks passed{RESET}\n")
    
    if passed == total:
        print(f"{GREEN}{'='*60}")
        print("🎉 ALL CHECKS PASSED - Ready for deployment!")
        print(f"{'='*60}{RESET}\n")
        print_info("Next steps:")
        print("  1. Commit your changes: git add . && git commit -m 'Ready for deployment'")
        print("  2. Deploy to Heroku: git push heroku main")
        print("  3. Or deploy to your chosen platform (see DEPLOYMENT_GUIDE.md)")
        return True
    else:
        print(f"{YELLOW}{'='*60}")
        print("⚠ SOME CHECKS FAILED - Review issues before deployment")
        print(f"{'='*60}{RESET}\n")
        print_info("Required actions:")
        if not checks.get('Environment Variables'):
            print("  • Create .env file and set SESSION_SECRET")
        if not checks.get('Dependencies'):
            print("  • Install dependencies: pip install -r requirements.txt")
        if not checks.get('Gunicorn Config'):
            print("  • Ensure gunicorn is in requirements.txt")
        print("\nSee DEPLOYMENT_GUIDE.md for detailed instructions")
        return False

def main():
    """Run all deployment checks"""
    print(f"{BLUE}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║   Roboto SAI - Deployment Verification Script            ║")
    print("║   Checking deployment readiness...                        ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{RESET}")
    
    # Run all checks
    checks = {
        'Python Version': check_python_version(),
        'Required Files': check_required_files(),
        'Dependencies': check_dependencies(),
        'Environment Variables': check_environment_variables(),
        'Gunicorn Config': check_gunicorn_config(),
        'Database': check_database(),
        'Application Import': check_import_main(),
    }
    
    # Generate report
    ready = generate_report(checks)
    
    # Exit with appropriate code
    sys.exit(0 if ready else 1)

if __name__ == '__main__':
    main()
