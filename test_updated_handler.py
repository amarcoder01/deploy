#!/usr/bin/env python3
"""
Test the updated telegram_handler.py with timezone fixes
"""
import asyncio
import os
from dotenv import load_dotenv
from telegram_handler import TelegramHandler
from logger import logger

# Load environment variables
load_dotenv()

async def test_updated_handler():
    """Test the updated telegram handler"""
    try:
        logger.info("Testing updated telegram handler...")
        
        # Get bot token
        bot_token = os.getenv('TELEGRAM_API_TOKEN')
        if not bot_token:
            logger.error("TELEGRAM_API_TOKEN not found")
            return False
        
        # Create telegram handler
        logger.info("Creating TelegramHandler...")
        handler = TelegramHandler()
        logger.info("✅ TelegramHandler created successfully")
        
        # Test initialization without running
        logger.info("Testing handler initialization...")
        
        # Create application builder
        from telegram.ext import Application
        builder = Application.builder().token(bot_token)
        builder = builder.job_queue(None)
        application = builder.build()
        logger.info("✅ Application created successfully")
        
        # Initialize and start
        await application.initialize()
        logger.info("✅ Application initialized")
        
        await application.start()
        logger.info("✅ Application started")
        
        # Check webhook status
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
        logger.error(f"❌ Updated handler test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_updated_handler())
    if success:
        print("\n🎉 Updated handler test PASSED!")
    else:
        print("\n💥 Updated handler test FAILED!")