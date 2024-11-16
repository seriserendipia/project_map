#!/usr/bin/env python
import os
import sys
import traceback

def main():
    """Run administrative tasks."""
    try:
        print("Python version:", sys.version)
        print("Current directory:", os.getcwd())
        print("Python path:", sys.path)
        print("Starting Django management script...")
        
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        print("Settings module set to:", os.environ['DJANGO_SETTINGS_MODULE'])
        
        try:
            import django
            print("Django version:", django.get_version())
        except ImportError as e:
            print("Failed to import Django:", str(e))
            print(traceback.format_exc())
            return
        
        try:
            from django.core.management import execute_from_command_line
            print("Django management imported successfully")
            execute_from_command_line(sys.argv)
        except ImportError as exc:
            print("Error importing Django management:", str(exc))
            print(traceback.format_exc())
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed?"
            ) from exc
    except Exception as e:
        print("Unexpected error:", str(e))
        print(traceback.format_exc())
        raise

if __name__ == '__main__':
    print("Script starting...")
    sys.stdout.flush()  # 强制输出
    main()