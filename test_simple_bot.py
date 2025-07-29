#!/usr/bin/env python3
"""
Simple test to verify basic bot functionality without complex initialization
"""
import asyncio
import os
from dotenv import load_dotenv
from telegram import Update, User, Chat, Message
from telegram.ext import Application, CommandHandler
from logger import logger

# Load environment variables
load_dotenv()

# Patch timezone issues before importing anything else
try:
    import apscheduler.util
    import pytz
    
    def patched_astimezone(obj):
        """Patched version that always returns pytz.UTC"""
        return pytz.UTC
    
    def patched_get_localzone():
        """Patched version that returns pytz.UTC"""
        return pytz.UTC
    
    # Replace the problematic functions
    apscheduler.util.astimezone = patched_astimezone
    apscheduler.util.get_localzone = patched_get_localzone
    
except ImportError:
    pass

async def start_command(update: Update, context):
    """Handle /start command"""
    await update.message.reply_text("🤖 Hello! I'm working correctly!")
    logger.info("✅ /start command executed successfully")

async def help_command(update: Update, context):
    """Handle /help command"""
    await update.message.reply_text("📚 Help: Available commands: /start, /help")
    logger.info("✅ /help command executed successfully")

async def test_simple_bot():
    """Test simple bot functionality"""
    try:
        logger.info("Testing simple bot functionality...")
        
        # Get bot token
        bot_token = os.getenv('TELEGRAM_API_TOKEN')
        if not bot_token:
            logger.error("TELEGRAM_API_TOKEN not found")
            return
        
        # Create application with job queue completely disabled
        logger.info("Creating application...")
        builder = Application.builder().token(bot_token)
        
        # Try different ways to disable job queue
        try:
            builder = builder.job_queue(None)
            logger.info("Job queue disabled via builder")
        except Exception as e:
            logger.warning(f"Could not disable job queue via builder: {e}")
        
        # Build application
        application = builder.build()
        logger.info("✅ Application created successfully")
        
        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        logger.info("✅ Handlers added successfully")
        
        # Initialize and start
        await application.initialize()
        logger.info("✅ Application initialized")
        
        await application.start()
        logger.info("✅ Application started")
        
        # Test command processing with mock update
        logger.info("\nTesting command processing...")
        
        # Create mock objects
        user = User(id=12345, first_name="Test", is_bot=False)
        chat = Chat(id=12345, type="private")
        message = Message(
            message_id=1,
            date=None,
            chat=chat,
            from_user=user,
            text="/start"
        )
        
        update = Update(update_id=1, message=message)
        
        # Process update
        await application.process_update(update)
        logger.info("✅ Update processed successfully")
        
        # Stop application
        await application.stop()
        await application.shutdown()
        logger.info("✅ Application stopped")
        
    except Exception as e:
        logger.error(f"Error during simple bot test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_simple_bot())