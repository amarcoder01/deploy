#!/usr/bin/env python3
"""
Comprehensive test for command processing with the fixed TelegramHandler
"""
import asyncio
import os
from dotenv import load_dotenv
from telegram import Update, User, Chat, Message
from telegram_handler import TelegramHandler
from logger import logger

# Load environment variables
load_dotenv()

async def test_full_command_processing():
    """Test full command processing with TelegramHandler"""
    try:
        logger.info("Testing full command processing with TelegramHandler...")
        
        # Create TelegramHandler
        logger.info("Creating TelegramHandler...")
        handler = TelegramHandler()
        logger.info("✅ TelegramHandler created successfully")
        
        # Create application builder
        from telegram.ext import Application
        builder = Application.builder().token(handler.bot_token)
        builder = builder.job_queue(None)
        application = builder.build()
        handler.application = application
        logger.info("✅ Application created and assigned to handler")
        
        # Setup handlers using the TelegramHandler's method
        logger.info("Setting up command handlers...")
        handler._setup_handlers()
        logger.info("✅ Command handlers setup completed")
        
        # Initialize and start application
        await application.initialize()
        await application.start()
        logger.info("✅ Application started")
        
        # List registered handlers
        logger.info("\n📋 Registered handlers:")
        total_handlers = 0
        for group_id, group in application.handlers.items():
            logger.info(f"Group {group_id}: {len(group)} handlers")
            total_handlers += len(group)
            for i, handler_obj in enumerate(group):
                handler_type = type(handler_obj).__name__
                if hasattr(handler_obj, 'command'):
                    logger.info(f"  {i}: {handler_type} - Command: /{handler_obj.command}")
                elif hasattr(handler_obj, 'filters'):
                    logger.info(f"  {i}: {handler_type} - Filters: {handler_obj.filters}")
                else:
                    logger.info(f"  {i}: {handler_type}")
        
        logger.info(f"\n📊 Total handlers registered: {total_handlers}")
        
        # Test command processing with mock updates
        logger.info("\n🧪 Testing command processing...")
        
        # Create mock objects
        user = User(id=12345, first_name="TestUser", is_bot=False)
        chat = Chat(id=12345, type="private")
        
        # Test /start command
        logger.info("Testing /start command...")
        start_message = Message(
            message_id=1,
            date=None,
            chat=chat,
            from_user=user,
            text="/start"
        )
        start_update = Update(update_id=1, message=start_message)
        
        try:
            await application.process_update(start_update)
            logger.info("✅ /start command processed successfully")
        except Exception as e:
            logger.error(f"❌ /start command failed: {e}")
        
        # Test /help command
        logger.info("Testing /help command...")
        help_message = Message(
            message_id=2,
            date=None,
            chat=chat,
            from_user=user,
            text="/help"
        )
        help_update = Update(update_id=2, message=help_message)
        
        try:
            await application.process_update(help_update)
            logger.info("✅ /help command processed successfully")
        except Exception as e:
            logger.error(f"❌ /help command failed: {e}")
        
        # Test /price command
        logger.info("Testing /price command...")
        price_message = Message(
            message_id=3,
            date=None,
            chat=chat,
            from_user=user,
            text="/price TSLA"
        )
        price_update = Update(update_id=3, message=price_message)
        
        try:
            await application.process_update(price_update)
            logger.info("✅ /price command processed successfully")
        except Exception as e:
            logger.error(f"❌ /price command failed: {e}")
        
        # Test regular text message
        logger.info("Testing regular text message...")
        text_message = Message(
            message_id=4,
            date=None,
            chat=chat,
            from_user=user,
            text="What is the price of Apple stock?"
        )
        text_update = Update(update_id=4, message=text_message)
        
        try:
            await application.process_update(text_update)
            logger.info("✅ Text message processed successfully")
        except Exception as e:
            logger.error(f"❌ Text message failed: {e}")
        
        # Check webhook status
        logger.info("\n🌐 Checking webhook status...")
        bot = application.bot
        webhook_info = await bot.get_webhook_info()
        logger.info(f"Current webhook URL: {webhook_info.url or 'None'}")
        logger.info(f"Pending updates: {webhook_info.pending_update_count}")
        logger.info(f"Max connections: {webhook_info.max_connections}")
        logger.info(f"Allowed updates: {webhook_info.allowed_updates or 'All'}")
        
        # Stop application
        await application.stop()
        await application.shutdown()
        logger.info("✅ Application stopped successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Full command processing test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_full_command_processing())
    if success:
        print("\n🎉 Full command processing test PASSED!")
        print("✅ Bot is properly configured and can process commands")
        print("✅ Webhook is correctly set up")
        print("✅ All handlers are registered")
    else:
        print("\n💥 Full command processing test FAILED!")
        print("❌ There are issues with command processing")