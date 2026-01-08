#!/usr/bin/env python3
"""
Create Django superuser with username: admin, password: 123
Final solution for SFS project
"""

import subprocess
import sys
import time

def run_command(cmd, check=True):
    """Execute a shell command"""
    print(f"🔧 Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    # Filter Django's automatic import messages
    output = result.stdout
    if 'objects imported automatically' in output:
        lines = output.split('\n')
        output = '\n'.join([line for line in lines if 'objects imported automatically' not in line])
    
    if output.strip():
        print(output.strip())
    
    if result.stderr and 'objects imported automatically' not in result.stderr:
        print(f"⚠️ {result.stderr.strip()}")
    
    if check and result.returncode != 0:
        print(f"❌ Command failed")
        return False
    
    return True

def main():
    print("=" * 60)
    print("CREATING DJANGO SUPERUSER: admin / 123")
    print("=" * 60)
    
    # 1. Check if management container is running
    print("\n1. Checking if sfs-management is running...")
    if not run_command('docker ps --filter "name=sfs-management" --format "{{.Names}}"', check=False):
        print("Starting sfs-management...")
        run_command('docker compose -f infrastructure/docker/docker-compose.yml up -d management')
        time.sleep(10)
    
    # 2. Run makemigrations
    print("\n2. Running makemigrations...")
    run_command('docker exec sfs-management python /app/backend/services/management/manage.py makemigrations')
    
    # 3. Run migrations
    print("\n3. Running migrations...")
    run_command('docker exec sfs-management python /app/backend/services/management/manage.py migrate')
    
    # 4. Delete existing admin user
    print("\n4. Removing existing admin user...")
    run_command('docker exec sfs-management python /app/backend/services/management/manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username=\\"admin\\").delete(); print(\\"Old admin deleted\\")"', check=False)
    
    # 5. Create superuser using non-interactive method
    print("\n5. Creating superuser...")
    print("   Username: admin")
    print("   Email: admin@sfs.local")
    print("   Password: 123")
    
    # First try: using createsuperuser with --noinput
    success = run_command('docker exec sfs-management python /app/backend/services/management/manage.py createsuperuser --username admin --email admin@sfs.local --noinput', check=False)
    
    if not success:
        print("⚠️ First method failed, trying alternative...")
        # Alternative method: using shell
        alt_cmd = '''docker exec sfs-management python /app/backend/services/management/manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()

try:
    user = User.objects.create_superuser(
        username='admin',
        email='admin@sfs.local',
        password='123'
    )
    print('✅ Superuser created using create_superuser')
except Exception as e:
    print(f'Error with create_superuser: {e}')
    print('Trying create_user with manual permissions...')
    
    user = User.objects.create_user(
        username='admin',
        email='admin@sfs.local',
        password='123'
    )
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()
    print('✅ User created with manual permissions')
"'''
        run_command(alt_cmd)
    
    # 6. Set password to 123 (just in case)
    print("\n6. Setting password to '123'...")
    run_command('docker exec sfs-management python /app/backend/services/management/manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); user = User.objects.get(username=\\"admin\\"); user.set_password(\\"123\\"); user.save(); print(\\"Password set to 123\\")"')
    
    # 7. Verify user
    print("\n7. Verifying admin user...")
    verify_cmd = '''docker exec sfs-management python /app/backend/services/management/manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth import authenticate

user = User.objects.get(username='admin')
print('✅ User details:')
print(f'   Username: {user.username}')
print(f'   Email: {user.email}')
print(f'   is_staff: {user.is_staff}')
print(f'   is_superuser: {user.is_superuser}')
print(f'   is_active: {user.is_active}')

# Check password
if user.check_password('123'):
    print('✅ Password verification: CORRECT')
else:
    print('❌ Password verification: FAILED')

# Test authentication
auth_user = authenticate(username='admin', password='123')
if auth_user:
    print('✅ Authentication test: SUCCESS')
else:
    print('❌ Authentication test: FAILED')
"'''
    run_command(verify_cmd)
    
    # 8. Open browser
    print("\n" + "=" * 60)
    print("✅ SUPERUSER CREATION COMPLETE!")
    print("=" * 60)
    print("\n📋 LOGIN INFORMATION:")
    print("   🌐 URL: http://localhost:8000/admin/")
    print("   👤 Username: admin")
    print("   🔑 Password: 123")
    print("\n🚀 Try logging in now...")
    
    # Open browser
    try:
        import webbrowser
        webbrowser.open("http://localhost:8000/admin/")
    except:
        print("⚠️ Could not open browser automatically.")

if __name__ == "__main__":
    main()