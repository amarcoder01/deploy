#!/usr/bin/env python3
"""
Test script to verify command processing and handler registration
"""
import asyncio
import os
from dotenv import load_dotenv
from telegram import Update, User, Chat, Message
from telegram.ext import Application
from telegram_handler import TelegramHandler
from logger import logger

# Load environment variables
load_dotenv()

async def test_command_processing():
    """Test command processing and handler registration"""
    try:
        logger.info("Testing command processing...")
        
        # Create TelegramHandler instance
        handler = TelegramHandler()
        
        # Create application
        builder = Application.builder().token(handler.bot_token)
        builder = builder.job_queue(None)
        application = builder.build()
        handler.application = application
        
        # Setup handlers
        handler._setup_handlers()
        logger.info("✅ Handlers setup completed")
        
        # Initialize application
        await application.initialize()
        await application.start()
        logger.info("✅ Application started")
        
        # List registered handlers
        logger.info("\nRegistered handlers:")
        for group_id, group in application.handlers.items():
            logger.info(f"Group {group_id}: {len(group)} handlers")
            for i, handler_obj in enumerate(group):
                handler_type = type(handler_obj).__name__
                if hasattr(handler_obj, 'command'):
                    logger.info(f"  {i}: {handler_type} - Command: /{handler_obj.command}")
                elif hasattr(handler_obj, 'filters'):
                    logger.info(f"  {i}: {handler_type} - Filters: {handler_obj.filters}")
                else:
                    logger.info(f"  {i}: {handler_type}")
        
        # Create a mock update for /start command
        logger.info("\nTesting /start command processing...")
        
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
        
        # Create update
        update = Update(
            update_id=1,
            message=message
        )
        
        # Process the update
        try:
            await application.process_update(update)
            logger.info("✅ /start command processed successfully")
        except Exception as e:
            logger.error(f"❌ Error processing /start command: {e}")
            import traceback
            traceback.print_exc()
        
        # Test /help command
        logger.info("\nTesting /help command processing...")
        message.text = "/help"
        update.message = message
        
        try:
            await application.process_update(update)
            logger.info("✅ /help command processed successfully")
        except Exception as e:
            logger.error(f"❌ Error processing /help command: {e}")
            import traceback
            traceback.print_exc()
        
        # Test /price command
        logger.info("\nTesting /price command processing...")
        message.text = "/price AAPL"
        update.message = message
        
        try:
            await application.process_update(update)
            logger.info("✅ /price command processed successfully")
        except Exception as e:
            logger.error(f"❌ Error processing /price command: {e}")
            import traceback
            traceback.print_exc()
        
        # Test regular message
        logger.info("\nTesting regular message processing...")
        message.text = "Hello bot"
        update.message = message
        
        try:
            await application.process_update(update)
            logger.info("✅ Regular message processed successfully")
        except Exception as e:
            logger.error(f"❌ Error processing regular message: {e}")
            import traceback
            traceback.print_exc()
        
        # Stop application
        await application.stop()
        await application.shutdown()
        logger.info("✅ Application stopped")
        
    except Exception as e:
        logger.error(f"Error during command processing test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_command_processing())