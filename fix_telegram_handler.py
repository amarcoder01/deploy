#!/usr/bin/env python3
"""
Fixed version of telegram handler that completely bypasses job queue issues
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# CRITICAL: Patch timezone handling BEFORE any telegram imports
try:
    import sys
    import pytz
    
    # Set environment variables to force UTC
    os.environ['TZ'] = 'UTC'
    os.environ['APSCHEDULER_TIMEZONE'] = 'UTC'
    
    # Patch apscheduler before it's imported by telegram
    if 'apscheduler' not in sys.modules:
        # Pre-import and patch apscheduler
        import apscheduler.util
        import apscheduler.schedulers.base
        
        def force_utc_timezone(obj=None):
            """Force UTC timezone for all APScheduler operations"""
            return pytz.UTC
        
        # Replace all timezone-related functions
        apscheduler.util.astimezone = force_utc_timezone
        apscheduler.util.get_localzone = force_utc_timezone
        apscheduler.schedulers.base.astimezone = force_utc_timezone
        apscheduler.schedulers.base.get_localzone = force_utc_timezone
        
        print("✅ APScheduler timezone patching completed")
        
except Exception as e:
    print(f"⚠️ Timezone patching failed: {e}")

# Now import telegram
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from logger import logger

async def test_fixed_bot():
    """Test the fixed bot initialization"""
    try:
        logger.info("Testing fixed bot initialization...")
        
        # Get bot token
        bot_token = os.getenv('TELEGRAM_API_TOKEN')
        if not bot_token:
            logger.error("TELEGRAM_API_TOKEN not found")
            return False
        
        # Create application with completely disabled job queue
        logger.info("Creating application with disabled job queue...")
        
        # Method 1: Try with explicit job_queue=None
        try:
            application = Application.builder().token(bot_token).job_queue(None).build()
            logger.info("✅ Method 1 successful: job_queue(None)")
        except Exception as e:
            logger.error(f"❌ Method 1 failed: {e}")
            
            # Method 2: Try with custom job queue configuration
            try:
                from telegram.ext import JobQueue
                
                # Create a dummy job queue that doesn't use APScheduler
                class DummyJobQueue:
                    def __init__(self):
                        pass
                    
                    async def start(self):
                        pass
                    
                    async def stop(self):
                        pass
                
                application = Application.builder().token(bot_token).build()
                # Replace the job queue after creation
                application._job_queue = None
                logger.info("✅ Method 2 successful: post-creation job queue removal")
                
            except Exception as e2:
                logger.error(f"❌ Method 2 failed: {e2}")
                return False
        
        # Test basic functionality
        async def test_start(update: Update, context):
            await update.message.reply_text("✅ Bot is working!")
            logger.info("Start command executed")
        
        # Add handlers
        application.add_handler(CommandHandler("start", test_start))
        logger.info("✅ Handlers added")
        
        # Initialize and start
        await application.initialize()
        logger.info("✅ Application initialized")
        
        await application.start()
        logger.info("✅ Application started")
        
        # Test webhook info
        bot = application.bot
        webhook_info = await bot.get_webhook_info()
        logger.info(f"Current webhook URL: {webhook_info.url or 'None'}")
        logger.info(f"Pending updates: {webhook_info.pending_update_count}")
        
        # Stop application
        await application.stop()
        await application.shutdown()
        logger.info("✅ Application stopped successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Fixed bot test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_fixed_bot())
    if success:
        print("\n🎉 Bot initialization test PASSED!")
    else:
        print("\n💥 Bot initialization test FAILED!")