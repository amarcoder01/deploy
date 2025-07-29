#!/usr/bin/env python3
"""
Test script to verify webhook setup and Telegram bot configuration
"""
import asyncio
import os
from dotenv import load_dotenv
from telegram import Bot
from logger import logger

# Load environment variables
load_dotenv()

async def test_webhook_setup():
    """Test webhook setup and bot configuration"""
    try:
        # Get bot token
        bot_token = os.getenv('TELEGRAM_API_TOKEN')
        if not bot_token:
            logger.error("TELEGRAM_API_TOKEN not found")
            return
        
        # Create bot instance
        bot = Bot(token=bot_token)
        
        # Test bot connection
        logger.info("Testing bot connection...")
        me = await bot.get_me()
        logger.info(f"✅ Bot connected successfully: @{me.username} ({me.first_name})")
        
        # Check current webhook info
        logger.info("Checking current webhook info...")
        webhook_info = await bot.get_webhook_info()
        logger.info(f"Current webhook URL: {webhook_info.url}")
        logger.info(f"Webhook has custom certificate: {webhook_info.has_custom_certificate}")
        logger.info(f"Pending update count: {webhook_info.pending_update_count}")
        logger.info(f"Last error date: {webhook_info.last_error_date}")
        logger.info(f"Last error message: {webhook_info.last_error_message}")
        logger.info(f"Max connections: {webhook_info.max_connections}")
        logger.info(f"Allowed updates: {webhook_info.allowed_updates}")
        
        # Test webhook URL construction logic
        logger.info("\nTesting webhook URL construction...")
        webhook_url = os.environ.get('WEBHOOK_URL')
        if not webhook_url:
            app_url = os.environ.get('RENDER_EXTERNAL_URL')
            if not app_url:
                service_name = os.environ.get('RENDER_SERVICE_NAME', 'tradeai-companion')
                webhook_url = f"https://{service_name}.onrender.com/webhook"
            else:
                webhook_url = f"{app_url}/webhook"
        
        logger.info(f"Constructed webhook URL: {webhook_url}")
        
        # Check if webhook URL is accessible (basic validation)
        if webhook_url.startswith('https://'):
            logger.info("✅ Webhook URL format looks correct")
        else:
            logger.warning("⚠️ Webhook URL should use HTTPS")
        
        # Test setting webhook (only if we have a valid URL)
        if 'onrender.com' in webhook_url or 'ngrok' in webhook_url:
            logger.info(f"\nTesting webhook setup with URL: {webhook_url}")
            try:
                await bot.set_webhook(
                    url=webhook_url,
                    drop_pending_updates=True,
                    allowed_updates=None
                )
                logger.info("✅ Webhook set successfully!")
                
                # Verify webhook was set
                new_webhook_info = await bot.get_webhook_info()
                logger.info(f"Verified webhook URL: {new_webhook_info.url}")
                
            except Exception as e:
                logger.error(f"❌ Failed to set webhook: {e}")
        else:
            logger.info("Skipping webhook setup test (not a deployment environment)")
        
    except Exception as e:
        logger.error(f"Error during webhook test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_webhook_setup())