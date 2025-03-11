
import asyncio
import redis.asyncio as redis_async
import os
import json

async def check_redis_entry(key_pattern="presentation:*"):
    """Check if entries matching the pattern exist in Redis cache."""
    try:
        # Connect to Redis
        redis_client = redis_async.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=int(os.getenv('REDIS_DB', 0)),
            decode_responses=True,
            socket_connect_timeout=5
        )
        
        # Test the connection
        await redis_client.ping()
        print("✅ Redis connection successful")
        
        # Get all keys matching the pattern
        keys = await redis_client.keys(key_pattern)
        
        if not keys:
            print(f"❌ No keys found matching pattern '{key_pattern}'")
            return
        
        print(f"🔑 Found {len(keys)} keys matching pattern '{key_pattern}':")
        
        # Display each key and its value
        for key in keys:
            value = await redis_client.get(key)
            print(f"\n📌 Key: {key}")
            
            # Try to parse as JSON if possible
            try:
                parsed_value = json.loads(value)
                print(f"📄 Value (JSON):")
                print(json.dumps(parsed_value, indent=2))
            except json.JSONDecodeError:
                print(f"📄 Value: {value}")
            
            # Get TTL (time to live)
            ttl = await redis_client.ttl(key)
            if ttl > 0:
                print(f"⏱️ TTL: {ttl} seconds")
            elif ttl == -1:
                print(f"⏱️ TTL: No expiration")
            else:
                print(f"⏱️ TTL: Key doesn't exist or has expired")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        # Close Redis connection
        if 'redis_client' in locals():
            await redis_client.close()

async def check_specific_presentation(presentation_id):
    """Check if a specific presentation ID exists in Redis cache."""
    key = f"presentation:{presentation_id}"
    await check_redis_entry(key)

async def main():
    print("Redis Cache Inspector")
    print("====================")
    
    while True:
        print("\nOptions:")
        print("1. Check all presentation entries")
        print("2. Check specific presentation ID")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            await check_redis_entry("presentation:*")
        elif choice == '2':
            presentation_id = input("Enter presentation ID: ")
            await check_specific_presentation(presentation_id)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    asyncio.run(main())
