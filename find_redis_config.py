
import os
import glob

def find_redis_config():
    """Search for Redis configuration in the codebase."""
    print("Searching for Redis configuration in the codebase...")
    
    # Define patterns to look for
    patterns = [
        "redis.Redis",
        "redis_async.Redis",
        "REDIS_HOST",
        "REDIS_PORT",
        "REDIS_URL"
    ]
    
    # Define file types to search
    extensions = [".py", ".env"]
    
    # Find all Python and .env files
    files = []
    for ext in extensions:
        files.extend(glob.glob("app/**/*" + ext, recursive=True))
    
    found_configs = []
    
    for file_path in files:
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                
                # Check if any pattern exists in the file
                if any(pattern in content for pattern in patterns):
                    print(f"Found Redis references in: {file_path}")
                    
                    # Extract lines containing Redis configuration
                    lines = content.split('\n')
                    redis_lines = [line.strip() for line in lines if any(pattern in line for pattern in patterns)]
                    
                    if redis_lines:
                        found_configs.append({
                            'file': file_path,
                            'config_lines': redis_lines
                        })
        except Exception as e:
            print(f"Error reading {file_path}: {str(e)}")
    
    if found_configs:
        print("\nRedis Configuration Found:")
        for config in found_configs:
            print(f"\nFile: {config['file']}")
            for line in config['config_lines']:
                print(f"  {line}")
    else:
        print("\nNo Redis configuration found in the codebase.")
    
    # Check for environment variables
    print("\nChecking for Redis environment variables:")
    redis_env_vars = {k: v for k, v in os.environ.items() if 'REDIS' in k}
    if redis_env_vars:
        print("Redis environment variables found:")
        for key, value in redis_env_vars.items():
            print(f"  {key}: {value}")
    else:
        print("No Redis environment variables found.")

if __name__ == "__main__":
    find_redis_config()
