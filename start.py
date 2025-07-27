#!/usr/bin/env python3
"""
Smart startup script for Replit deployment
Detects if heavy deps are available and runs appropriate version
"""
import os
import sys
import subprocess

def main():
    """Main startup function"""
    print("=== TradeAI Companion Bot Smart Startup ===")
    print(f"Python: {sys.version}")
    
    # Check if we're in a deployment environment with size constraints
    if os.environ.get('REPL_SLUG') or os.environ.get('DEPLOYMENT_MODE'):
        print("Deployment mode detected - using minimal bot")
        # Use minimal bot for deployment
        bot_script = 'deploy_bot.py'
    else:
        print("Development mode - using full bot")
        # Use full bot in development
        bot_script = 'main.py'
    
    # Change to Bot_Deployment directory
    bot_dir = os.path.join(os.getcwd(), 'Bot_Deployment')
    if os.path.exists(bot_dir):
        os.chdir(bot_dir)
        print(f"Starting from: {os.getcwd()}")
        print(f"Running: {bot_script}")
    else:
        print("ERROR: Bot_Deployment directory not found!")
        sys.exit(1)
    
    # Run the appropriate bot
    try:
        result = subprocess.run([sys.executable, bot_script], check=True)
        sys.exit(result.returncode)
    except subprocess.CalledProcessError as e:
        print(f"Bot failed with exit code: {e.returncode}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Bot error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()