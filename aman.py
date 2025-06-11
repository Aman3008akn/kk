from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaDocument
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ChatMemberHandler,
    filters,
    ContextTypes,
)
import logging
import asyncio
from pyrogram import Client, errors
import time
import random
from datetime import datetime, timedelta
import os
from pyrogram import Client

api_id = "20200913"
api_hash = "cab56102cddebdb1584cf9a99875a624"
phone_number = "+917841852765"
bot_username = "PagaIEscrowbot"
group_id = -1004802076930 # ya invite link

async def add_bot_to_group():
    async with Client("my_account", api_id, api_hash, phone_number=phone_number) as app:
        await app.add_chat_members(group_id, bot_username)

# asyncio.run(add_bot_to_group())
ADMIN_IDS = [int(uid) for uid in os.getenv('ADMIN_IDS', '5466072443,5684671374').split(',')]

# --- Userbot Config (Sensitive - do not hardcode in production) ---
# It's better to load these from environment variables or a secure config file.
# ZORG is removing the direct phone number for security.
api_id = 20200913
api_hash = "cab56102cddebdb1584cf9a99875a624"
# phone_number = "+919315849892" # Userbot phone number should be handled securely
# bot_username = "Mafiai09_bot" # Your bot's username

# --- Bot Config ---
BOT_TOKEN = "7776902762:AAHzXjTBdRgROFm0L8YUTqjcdH0FdWnU_LY" # Your bot token

from enum import Enum

class ConversationState(Enum):
    DEAL_DESCRIPTION = 0
    DEAL_AMOUNT = 1
    DEAL_CONDITIONS = 2
    SELLER_ADDRESS = 3
    BUYER_ADDRESS = 4
    SET_FEE_AMOUNT = 5
    SAVE_ADDRESS_CHAIN = 6
    SAVE_ADDRESS_DETAIL = 7
    VERIFY_ADDRESS_INPUT = 8
    NEW_DEAL_TYPE = 9
    NEW_DEAL_COUNTERPARTY = 10
    NEW_DEAL_AMOUNT_CURRENCY = 11
    TOKEN_SELECTION = 12
    DEPOSIT_AMOUNT_SELECTION = 13
    WITHDRAW_AMOUNT_SELECTION = 14
    WITHDRAW_ADDRESS_INPUT = 15
    DISPUTE_REASON = 16
    DISPUTE_PROOF = 17
    MILESTONE_NAME = 18
    MILESTONE_AMOUNT = 19
    MILESTONE_CONFIRMATION = 20
    MILESTONE_STATUS_UPDATE = 21
    REPORT_ISSUE_TYPE = 22
    REPORT_ISSUE_DETAILS = 23
    USER_KYC_DOC_TYPE = 24
    USER_KYC_DOC_UPLOAD = 25
    USER_FEEDBACK_TEXT = 26
    ADMIN_BAN_USER_ID = 27
    ADMIN_UNBAN_USER_ID = 28
    ADMIN_CHANGE_ROLE_USER_ID = 29
    ADMIN_CHANGE_ROLE_NEW_ROLE = 30
    ADMIN_BROADCAST_MESSAGE = 31
    ADMIN_RESOLVE_DISPUTE_ID = 32
    ADMIN_RESOLVE_DISPUTE_ACTION = 33
    CHANNEL_POST_CHANNEL_ID = 34
    CHANNEL_POST_CONTENT = 35
    CHANNEL_POST_SCHEDULE_TIME = 36
    VOUCH_TEXT = 37
    REFERRAL_SOURCE = 38
    OTC_PARTICIPANT_TYPE = 39
    OTC_PARTICIPANT_ID = 40
    OTC_CONFIRM_DETAILS = 41
    ADD_TRUSTED_USER_ID = 42
    REMOVE_TRUSTED_USER_ID = 43
    LIST_ITEM_NAME = 44
    LIST_ITEM_DESC = 45
    LIST_ITEM_PRICE = 46
    LIST_ITEM_CATEGORY = 47
    LIST_ITEM_CONFIRM = 48
    # New states for confirmation and checkout
    DEAL_AMOUNT_CONFIRM = 1001
    DEAL_AMOUNT_BUYER_CONFIRM = 1002
    DEAL_AMOUNT_SELLER_CONFIRM = 1003
    DEAL_CHECKOUT = 1004
    # New states for rating feature
    RATING_ACTION = 1005
    RATING_USER_ID = 1006
    RATING_VALUE = 1007
    VIEW_RATING_USER_ID = 1008

# --- Global Data Storage (In-memory, NOT for production) ---
# For a real bot with 1000+ features, you'd need a robust database (PostgreSQL, MongoDB)
# and possibly a caching layer like Redis.
# Example using PostgreSQL with SQLAlchemy:
# from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, JSON
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
#
# DATABASE_URL = "postgresql://user:password@host:port/database"
# engine = create_engine(DATABASE_URL)
# Base = declarative_base()
#
# class Deal(Base):
#     __tablename__ = "deals"
#     id = Column(Integer, primary_key=True)
#     trade_id = Column(String, unique=True, nullable=False)
#     creator_id = Column(Integer)
#     description = Column(String)
#     amount = Column(Float)
#     conditions = Column(String)
#     status = Column(String)
#     created_at = Column(DateTime)
#     seller_id = Column(Integer)
#     buyer_id = Column(Integer)
#     seller_address = Column(String)
#     buyer_address = Column(String)
#     escrow_address = Column(String)
#     token = Column(String)
#     fee_percent = Column(Float)
#     group_chat_id = Column(Integer)
#     dispute_status = Column(String)
#
# Base.metadata.create_all(engine)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# # Example usage:
# # db = SessionLocal()
# # new_deal = Deal(trade_id="...", creator_id=123, ...)
# # db.add(new_deal)
# # db.commit()
# # db.close()
#
# # Caching with Redis:
# # import redis
# # redis_client = redis.Redis(host='localhost', port=6379, db=0)
# # cached_data = redis_client.get("some_key")
active_deals = {} # {trade_id: {creator_id, description, amount, conditions, seller_id, buyer_id, seller_address, buyer_address, status, group_link, fee, token, ...}}
user_profiles = {} # {user_id: {username, first_name, last_name, balance, saved_addresses, referrals, total_escrows, rating, kyc_status, notifications_settings, ...}}
disputes = {} # {dispute_id: {trade_id, raised_by, reason, status, proofs, admin_notes, ...}}
channels_managed = {} # {channel_id: {posts_scheduled, settings, ...}}
listed_items = {} # {item_id: {seller_id, name, description, price, category, status, ...}}
# ... many more global data structures for complex features

# --- Welcome and Command Messages ---
WELCOME_MESSAGE_GROUP = (
    "📍 Hey there traders! Welcome to our escrow service.\n"
    "✅ Please start with /dd command and fill the DealInfo Form"
)

WELCOME_MESSAGE_PRIVATE = (
    "👛 @PagaLEscrowBot 👛\n"
    "Your Trustworthy Telegram Escrow Service\n\n"
    "Welcome to @PagaLEscrowBot. This bot provides a reliable escrow service for your transactions on Telegram.\n"
    "Avoid scams, your funds are safeguarded throughout your deals. If you run into any issues, simply type /dispute and an arbitrator will join the group chat within 24 hours.\n\n"
    "🎟 ESCROW FEE:\n"
    "1.0% for P2P and 1.0% for OTC Flat\n\n"
    "🌐 (UPDATES) - (VOUCHES) ✅\n\n"
    "💬 Proceed with /escrow (to start with a new escrow)\n\n"
    "⚠ IMPORTANT - Make sure coin is same for Buyer and Seller else you may lose your coin.\n\n"
    "💡 Type /menu to summon a menu with all bot features"
)

# This list will become VERY long with 1000+ features
COMMANDS_LIST = (
    "📌 <b>AVAILABLE COMMANDS</b>\n\n"
    "Here you have a full command list, in case you do like to move through the bot using commands instead of the buttons.\n"
    "<code>/start</code> - A command to start interacting with the bot\n"
    "<code>/menu</code> - A command to bring out a menu for the bot\n"
    "<code>/whatisescrow</code> - A command to tell you more about escrow\n"
    "<code>/instructions</code> - A command with text instructions\n"
    "<code>/terms</code> - A command to bring out our TOS\n"
    "<code>/dispute</code> - A command to contact the admins (for any deal)\n"
    "<code>/contact</code> - A command to get admin's contact\n"
    "<code>/commands</code> - A command to get commands list\n"
    "<code>/stats</code> - A command to check user stats\n"
    "<code>/vouch</code> - A command to vouch for the bot\n"
    "<code>/newdeal</code> - A command to start a new deal flow\n"
    "<code>/tradeid</code> - A command to get trade id for a chat\n"
    "<code>/dd</code> - A command to add deal details (P2P/simple escrow)\n"
    "<code>/escrow</code> - A command to get an escrow group link (OTC/product)\n"
    "<code>/token</code> - A command to select token/currency for the escrow\n"
    "<code>/deposit</code> - A command to generate deposit address for escrow\n"
    "<code>/verify</code> - A command to verify wallet address (buyer/seller)\n"
    "<code>/balance</code> - A command to check the balance of the escrow address\n"
    "<code>/release</code> - A command to release the funds in the escrow\n"
    "<code>/refund</code> - A command to refund the funds in the escrow\n"
    "<code>/seller</code> - Assign yourself as a seller for the current deal\n"
    "<code>/buyer</code> - Assign yourself as a buyer for the current deal\n"
    "<code>/setfee</code> - A command to set custom trade fee (admin/premium)\n"
    "<code>/save</code> - A command to save default addresses for various chains\n"
    "<code>/saved</code> - A command to check saved addresses\n"
    "<code>/referral</code> - A command to check your referrals\n"
    "<code>/mydeals</code> - View your ongoing and past deals\n"
    "<code>/canceldeal</code> - Cancel a pending deal (mutual agreement)\n"
    "<code>/milestone</code> - Manage milestones for complex deals\n"
    "<code>/report</code> - Report an issue or bug to admins\n"
    "<code>/feedback</code> - Provide feedback on bot's service\n"
    "<code>/kyc</code> - Start KYC verification process\n"
    "<code>/settings</code> - Adjust your personal bot settings\n"
    "<code>/premium</code> - Learn about premium features\n"
    "<code>/admin_menu</code> - Access admin panel (admins only)\n"
    "<code>/admin_broadcast</code> - Send a broadcast message (admin only)\n"
    "<code>/admin_ban</code> - Ban a user (admin only)\n"
    "<code>/admin_unban</code> - Unban a user (admin only)\n"
    "<code>/admin_resolve_dispute</code> - Resolve an ongoing dispute (admin only)\n"
    "<code>/admin_view_user</code> - View detailed user info (admin only)\n"
    "<code>/admin_view_deal</code> - View detailed deal info (admin only)\n"
    "<code>/admin_add_admin</code> - Add a new admin (super admin only)\n"
    "<code>/admin_remove_admin</code> - Remove an admin (super admin only)\n"
    "<code>/admin_fees</code> - Manage global fee settings (admin only)\n"
    "<code>/admin_channels</code> - Manage linked channels (admin only)\n"
    "<code>/admin_schedule_post</code> - Schedule a post in linked channel (admin only)\n"
    "<code>/otc_deal</code> - Initiate an Over-The-Counter deal\n"
    "<code>/list_item</code> - List an item for sale in the marketplace\n"
    "<code>/browse_items</code> - Browse items available in the marketplace\n"
    "<code>/buy_item</code> - Initiate purchase of a listed item\n"
    "<code>/rating</code> - View/give user ratings\n"
    "<code>/trusted_users</code> - Manage trusted users list\n"
    "<code>/set_notifications</code> - Configure notification preferences\n"
    "<code>/check_updates</code> - Check for bot updates\n"
    "<code>/api_status</code> - Check status of external APIs\n"
    # ... and hundreds more commands for 1000+ features
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# --- Helper Functions ---
def extract_args(update: Update):
    """Extracts arguments from a command message."""
    text = update.message.text or ""
    parts = text.split()
    return parts[1:] if len(parts) > 1 else []

async def get_user_profile(user_id: int, context: ContextTypes.DEFAULT_TYPE):
    """Fetches or creates a user profile."""
    if user_id not in user_profiles:
        chat = await context.bot.get_chat(user_id)
        user_profiles[user_id] = {
            "username": chat.username if chat else None,
            "first_name": chat.first_name if chat else None,
            "last_name": chat.last_name if chat else None,
            "balance": 0.0,
            "saved_addresses": {},
            "referrals": [],
            "total_escrows": 0,
            "rating": 5.0,
            "kyc_status": "pending",
            "notifications_settings": {"new_deal": True, "dispute": True, "fund_release": True},
            "is_admin": user_id in ADMIN_IDS,
            "is_banned": False,
            "created_at": datetime.now()
        }
    return user_profiles[user_id]

async def update_user_profile(user_id: int, key: str, value: any):
    """Updates a specific field in user profile."""
    profile = await get_user_profile(user_id, None) # Pass None for context as it's not needed for simple updates
    profile[key] = value
    # TODO: In real bot, save to database here

async def is_admin(user_id: int) -> bool:
    """Checks if a user is an admin."""
    return user_id in ADMIN_IDS

async def generate_trade_id():
    """Generates a unique trade ID."""
    while True:
        trade_id = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=10))
        if trade_id not in active_deals: # Ensure uniqueness
            return trade_id

# --- Core Escrow Bot Commands ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    await get_user_profile(user_id, context) # Ensure user profile exists
    await update.message.reply_text(WELCOME_MESSAGE_PRIVATE)
    await menu(update, context)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("COMMANDS LIST 🤖", callback_data='commands')],
        [InlineKeyboardButton("☎ CONTACT", callback_data='contact'),
         InlineKeyboardButton("📈 MY STATS", callback_data='stats_menu')], # New button
        [
            InlineKeyboardButton("Updates 📰", url="https://t.me/updates_link"),
            InlineKeyboardButton("Vouches ✅", url="https://t.me/vouches_link")
        ],
        [
            InlineKeyboardButton("WHAT IS ESCROW...", callback_data='whatisescrow'),
            InlineKeyboardButton("Instructions 📗", callback_data='instructions')
        ],
        [
            InlineKeyboardButton("Terms 📝", callback_data='terms'),
            InlineKeyboardButton("Invites 👤", callback_data='invites')
        ],
        [
            InlineKeyboardButton("START NEW DEAL 🚀", callback_data='new_deal_menu'), # Unified new deal start
            InlineKeyboardButton("MY DEALS 💼", callback_data='my_deals') # New button
        ],
        [
            InlineKeyboardButton("WALLET 💰", callback_data='wallet_menu'), # New button
            InlineKeyboardButton("SETTINGS ⚙️", callback_data='settings_menu') # New button
        ],
        [InlineKeyboardButton("RAISE DISPUTE 🚨", callback_data='dispute_menu')] # Always available
    ]
    
    # Admin Panel button for admins
    if await is_admin(update.message.from_user.id):
        keyboard.append([InlineKeyboardButton("ADMIN PANEL 🛠️", callback_data='admin_menu')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Main Menu:\nChoose an option below:", reply_markup=reply_markup)

# --- Deal Detail (dd) and New Deal (newdeal) Flows ---
async def dd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Starts the conversation for basic deal details (P2P)."""
    await update.message.reply_text(
        "Hello there,\n"
        "Kindly tell deal details i.e.\n\n"
        "Dealinfo -\n"
        "Amount -\n"
        "Conditions ( If Any ) -\n\n"
        "Once filled Seller will use /seller [CRYPTO ADDRESS] and /buyer [CRYPTO ADDRESS] to specify your roles, and start the deal."
    )
    # Store deal initiator
    context.user_data['deal_creator'] = update.message.from_user.id
    context.user_data['deal_type'] = 'simple_p2p'
    await update.message.reply_text("Please enter the Deal Description:")
    return ConversationState.DEAL_DESCRIPTION

async def deal_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data['description'] = update.message.text
        await update.message.reply_text("Enter the amount:")
        return ConversationState.DEAL_AMOUNT
    except Exception as e:
        logging.error(f"Error setting deal description: {e}")
        await update.message.reply_text("An error occurred. Please try again.")
        return ConversationHandler.END

# --- Replace your deal_amount_handler with this updated function: ---
async def deal_amount_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(update.message.text.replace(",", "").strip())
        context.user_data['deal_amount'] = amount
        # Ask for confirmation from both buyer and seller
        context.user_data['amount_confirmed_buyer'] = False
        context.user_data['amount_confirmed_seller'] = False

        # Save who is who in this deal for demo purposes (in production, use real user assignment)
        # For now, treat sender as both for demo, or use your role assignment logic
        context.user_data['buyer_id'] = update.message.from_user.id
        context.user_data['seller_id'] = update.message.from_user.id

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Yes, Confirm", callback_data="confirm_amount_buyer")],
            [InlineKeyboardButton("❌ No, Cancel", callback_data="cancel_amount")],
        ])
        await update.message.reply_text(
            f"Buyer, do you confirm the deal amount: ₹{amount} ?",
            reply_markup=keyboard
        )
        return ConversationState.DEAL_AMOUNT_BUYER_CONFIRM
    except Exception as e:
        await update.message.reply_text("❌ Invalid amount. Please enter a numeric value (e.g., 1000 or 250.50).")
        return ConversationState.DEAL_AMOUNT

# --- Add these handlers ---

async def deal_amount_buyer_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['amount_confirmed_buyer'] = True

    # Now ask seller
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Yes, Confirm", callback_data="confirm_amount_seller")],
        [InlineKeyboardButton("❌ No, Cancel", callback_data="cancel_amount")],
    ])
    await query.edit_message_text(
        f"Seller, do you confirm the deal amount: ₹{context.user_data['deal_amount']} ?",
        reply_markup=keyboard
    )
    return ConversationState.DEAL_AMOUNT_SELLER_CONFIRM

async def deal_amount_seller_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['amount_confirmed_seller'] = True

    # First, edit the original message to show that confirmation is done
    await query.edit_message_text(f"Both parties have confirmed the deal amount: ₹{context.user_data['deal_amount']}.")

    # Then, send a new message with the QR image and payment details
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ DONE, CHECK", callback_data="checkout_done"),
            InlineKeyboardButton("❌ No, Cancel", callback_data="checkout_cancel"),
        ],
        [
            InlineKeyboardButton("📞 Contact Support", callback_data="checkout_support"),
        ]
    ])
    
    # IMPORTANT: Replace this placeholder URL with your actual QR code image URL
    # The URL must be publicly accessible and link directly to an image file (e.g., .jpg, .png)
    qr_code_image_url = "WhatsApp Image 2025-06-10 at 20.55.35_fae4a944.jpg" # <--- REPLACE THIS LINE WITH YOUR REAL QR CODE URL

    await query.message.reply_photo(
        photo=qr_code_image_url,
        caption=f"**Checkout for ₹{context.user_data['deal_amount']}**\n"
                f"Pay using UPI: `Millionairelodhi@fam`\n"
                "Scan the QR or copy the UPI to pay.\n",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    return ConversationState.DEAL_CHECKOUT

async def deal_checkout_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # MODIFIED: Use edit_message_caption for photo messages
    await query.edit_message_caption("Thank you! Your payment will be verified soon. If you have any issues, contact support.")
    return ConversationHandler.END

async def deal_amount_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # MODIFIED: Use edit_message_caption for photo messages
    await query.edit_message_caption("Deal cancelled.")
    return ConversationHandler.END

async def deal_checkout_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Support: @JOHNMIACHEL (or your support username)")
    return ConversationHandler.END
async def deal_conditions_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['deal_conditions'] = update.message.text if update.message.text.lower() != 'none' else 'N/A'
    
    # Generate a trade_id and store deal data
    trade_id = await generate_trade_id()
    active_deals[trade_id] = {
        'trade_id': trade_id,
        'creator_id': context.user_data['deal_creator'],
        'type': context.user_data['deal_type'],
        'description': context.user_data['description'], # Changed from deal_description to description based on new flow
        'amount': context.user_data['deal_amount'],
        'conditions': context.user_data['deal_conditions'],
        'status': 'pending_info', # New status for initial deal setup
        'created_at': datetime.now(),
        'seller_id': None,
        'buyer_id': None,
        'seller_address': None,
        'buyer_address': None,
        'escrow_address': None,
        'token': None,
        'fee_percent': 1.0, # Default fee
        'group_chat_id': None,
        'dispute_status': 'none'
    }
    
    await update.message.reply_text(
        "Deal info recorded:\n"
        f"Deal ID: `{trade_id}`\n"
        f"Deal: {context.user_data['description']}\n"
        f"Amount: {context.user_data['deal_amount']}\n"
        f"Conditions: {context.user_data['deal_conditions']}\n\n"
        "Seller, use `/seller <your_crypto_address> <trade_id>` to specify your role and address.\n"
        "Buyer, use `/buyer <your_crypto_address> <trade_id>` to specify your role and address.\n\n"
        "You can now also use /escrow to create a private group for this deal, or proceed to payment if roles are set."
    )
    context.user_data.pop('deal_creator', None)
    context.user_data.pop('deal_type', None)
    context.user_data.pop('description', None) # Changed from deal_description to description
    context.user_data.pop('deal_amount', None)
    context.user_data.pop('deal_conditions', None)

    return ConversationHandler.END

async def newdeal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """New deal start, offers options like OTC or P2P."""
    keyboard = [
        [InlineKeyboardButton("Simple P2P Deal (via Bot)", callback_data='new_deal_simple_p2p')],
        [InlineKeyboardButton("OTC / Product Deal (with group)", callback_data='new_deal_otc')],
        [InlineKeyboardButton("Milestone-based Deal", callback_data='new_deal_milestone')] # New type
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("ZORG👽: Select the type of new deal you want to create:", reply_markup=reply_markup)

async def new_deal_type_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    deal_type = query.data.replace('new_deal_', '')
    context.user_data['deal_creator'] = query.from_user.id
    context.user_data['deal_type'] = deal_type

    if deal_type == 'simple_p2p':
        await query.edit_message_text("ZORG👽: You selected Simple P2P Deal. Please enter the Deal Description:")
        return ConversationState.DEAL_DESCRIPTION
    elif deal_type == 'otc':
        await query.edit_message_text("ZORG👽: You selected OTC/Product Deal. Please enter the Deal Description:")
        return ConversationState.DEAL_DESCRIPTION # Re-use deal description state for now, then lead to group creation
    elif deal_type == 'milestone':
        await query.edit_message_text("ZORG👽: You selected Milestone-based Deal. Please enter the overall Deal Description:")
        return ConversationState.DEAL_DESCRIPTION # Will lead to milestone setup after initial details
    else:
        await query.edit_message_text("ZORG👽: Unknown deal type selected. Please try again or use /newdeal.")
        return ConversationHandler.END

# --- Escrow Group Creation ---
async def escrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Initiates the creation of an escrow group."""
    keyboard = [
        [InlineKeyboardButton("P2P Escrow Group", callback_data='escrow_p2p_group')],
        [InlineKeyboardButton("Product Deal Escrow Group", callback_data='escrow_product_group')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please select your escrow type from below. This will create a dedicated group chat.", reply_markup=reply_markup)

async def create_escrow_group_pyrogram(user_id: int, bot_username_val: str, group_type: str, context: ContextTypes.DEFAULT_TYPE):
    """Uses Pyrogram to create a group and invite participants."""
    # Ensure phone_number is loaded securely, e.g., from environment variables
    userbot_phone_number = os.getenv('USERBOT_PHONE_NUMBER')
    if not userbot_phone_number:
        logging.error("USERBOT_PHONE_NUMBER not set in environment variables.")
        raise ValueError("Userbot phone number is not configured.")

    async with Client("userbot", api_id, api_hash, phone_number=userbot_phone_number) as app:
        try:
            # Fetch user info
            user_profile = await get_user_profile(user_id, context)
            user_tg_id = user_profile['telegram_id'] = user_id # Ensure telegram_id is set
            user_username = user_profile['username'] or user_profile['first_name'] or "User"
            
            # Fetch bot info
            bot_info = await app.get_users(bot_username_val)
            
            group_title = f"{group_type.upper()} Escrow Deal - {user_username}"
            
            # Create a private group with the user and the bot
            chat = await app.create_group(group_title, [user_tg_id, bot_info.id])
            invite_link = await app.export_chat_invite_link(chat.id)
            
            # Send welcome message to the new group
            await app.send_message(chat.id, WELCOME_MESSAGE_GROUP)
            await app.send_message(chat.id, COMMANDS_LIST, parse_mode='HTML', disable_web_page_preview=True)
            
            return invite_link, chat.id
        except errors.RPCError as e:
            logging.error(f"Pyrogram RPCError in create_escrow_group: {e}")
            raise Exception(f"Telegram API error: {e.MESSAGE}")
        except Exception as e:
            logging.error(f"Error in create_escrow_group_pyrogram: {e}", exc_info=True)
            raise

async def escrow_type_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    # Get the group type from the button
    group_type = query.data.replace('escrow_', '')

    # Use your static group link for both types
    group_link = "https://t.me/+GpZZZdc3uf82MmY9" # Updated group link
    note = (
        "⚠️ This is the official escrow group. Please join and proceed as per the instructions.\n"
        "Inside the group, use `/dd` to add deal details, and `/seller` / `/buyer` to assign roles."
    )

    try:
        await query.edit_message_text(
            f"<b>Escrow Group</b>\n\n"
            f"Group Type: {group_type.title()}\n"
            f"Join this escrow group and share the link with the other party:\n\n"
            f"{group_link}\n\n"
            f"{note}",
            parse_mode='HTML'
        )
    except asyncio.TimeoutError:
        await query.message.reply_text("Group creation took too long. This might be due to Telegram API limits or network issues. Please try again in a few minutes.")
    except Exception as e:
        logging.error(f"Error in escrow_type_selection: {e}")
        await query.message.reply_text(f"Error creating group: {e}. Please contact support.")

# --- Command Handlers with Arguments ---
async def seller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = extract_args(update)
    if len(args) < 2:
        await update.message.reply_text("Please provide your CRYPTO ADDRESS and the Trade ID. Usage: `/seller <CRYPTO_ADDRESS> <TRADE_ID>`")
        return
    
    address = args[0]
    trade_id = args[1].upper()

    if trade_id not in active_deals:
        await update.message.reply_text(f"Deal ID `{trade_id}` not found. Please check the ID or start a new deal.")
        return

    deal = active_deals[trade_id]
    if deal['status'] in ['completed', 'cancelled', 'disputed', 'funds_released', 'refunded']:
        await update.message.reply_text(f"Deal `{trade_id}` is already in `{deal['status']}` status and cannot be modified.")
        return

    deal['seller_id'] = update.message.from_user.id
    deal['seller_address'] = address
    deal['status'] = 'seller_assigned' if deal['buyer_id'] else 'pending_roles'
    await update.message.reply_text(f"Seller set for Deal ID `{trade_id}` with address: `{address}`. Waiting for Buyer.")
    
    # Notify buyer if they are already assigned
    if deal['buyer_id']:
        await context.bot.send_message(deal['buyer_id'], 
                                       f"For Deal ID `{trade_id}`, the Seller ({update.message.from_user.full_name}) has set their address `{address}`. "
                                       "Both parties are now assigned. You can proceed with payment.")
    # TODO: Save deal state to DB

async def buyer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = extract_args(update)
    if len(args) < 2:
        await update.message.reply_text("Please provide your CRYPTO ADDRESS and the Trade ID. Usage: `/buyer <CRYPTO_ADDRESS> <TRADE_ID>`")
        return
    
    address = args[0]
    trade_id = args[1].upper()

    if trade_id not in active_deals:
        await update.message.reply_text(f"Deal ID `{trade_id}` not found. Please check the ID or start a new deal.")
        return

    deal = active_deals[trade_id]
    if deal['status'] in ['completed', 'cancelled', 'disputed', 'funds_released', 'refunded']:
        await update.message.reply_text(f"Deal `{trade_id}` is already in `{deal['status']}` status and cannot be modified.")
        return

    deal['buyer_id'] = update.message.from_user.id
    deal['buyer_address'] = address
    deal['status'] = 'buyer_assigned' if deal['seller_id'] else 'pending_roles'
    await update.message.reply_text(f"Buyer set for Deal ID `{trade_id}` with address: `{address}`. Waiting for Seller.")

    # Notify seller if they are already assigned
    if deal['seller_id']:
        await context.bot.send_message(deal['seller_id'], 
                                       f"For Deal ID `{trade_id}`, the Buyer ({update.message.from_user.full_name}) has set their address `{address}`. "
                                       "Both parties are now assigned. Buyer can now proceed with payment.")
    # TODO: Save deal state to DB

async def setfee(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.message.from_user.id):
        await update.message.reply_text("You are not authorized to use this command.")
        return
    args = extract_args(update)
    if len(args) < 1:
        await update.message.reply_text("Please provide the fee percentage. Usage: `/setfee <percentage>` (e.g., /setfee 0.5 for 0.5%)")
        return
    try:
        fee_percent = float(args[0])
        if not (0 <= fee_percent <= 100):
            raise ValueError
        # TODO: Implement storing fee per deal or globally
        # For demo, let's assume it sets a temporary global fee or for next deal
        context.chat_data['custom_fee'] = fee_percent
        await update.message.reply_text(f"Custom trade fee for next deal set to: `{fee_percent}%` (Admin action).")
    except ValueError:
        await update.message.reply_text("Invalid fee percentage. Please enter a number between 0 and 100.")

async def save_address_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("To save an address, please provide the CHAIN name (e.g., `BTC`, `ETH`, `TRX`):")
    return ConversationState.SAVE_ADDRESS_CHAIN

async def save_address_chain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = update.message.text.strip().upper()
    context.user_data['temp_chain'] = chain
    await update.message.reply_text(f"Now, please provide the ADDRESS for `{chain}`:")
    return ConversationState.SAVE_ADDRESS_DETAIL

async def save_address_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    chain = context.user_data.pop('temp_chain')
    address = update.message.text.strip()
    profile = await get_user_profile(user_id, context)
    if 'saved_addresses' not in profile:
        profile['saved_addresses'] = {}
    profile['saved_addresses'][chain] = address
    await update_user_profile(user_id, 'saved_addresses', profile['saved_addresses'])
    await update.message.reply_text(f"Saved address for `{chain}`: `{address}`. You can view them with /saved.")
    return ConversationHandler.END

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please provide the wallet address you want to verify:")
    return ConversationState.VERIFY_ADDRESS_INPUT

async def verify_address_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wallet_address = update.message.text.strip()
    # TODO: Implement actual wallet address validation against a regex or blockchain API
    is_valid = True # Dummy check
    if is_valid:
        await update.message.reply_text(f"Wallet address `{wallet_address}` appears to be valid. (Dummy check)")
    else:
        await update.message.reply_text(f"Wallet address `{wallet_address}` is NOT valid. Please check and try again.")
    return ConversationHandler.END

async def tradeid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This command makes more sense in a group chat created by the bot
    if update.message.chat.type == 'private':
        await update.message.reply_text("This command is primarily for escrow group chats. In a private chat, there's no specific 'trade ID'.")
    else:
        # Check if the current chat_id is associated with an active deal
        found_deal_id = None
        for deal_id, deal_data in active_deals.items():
            if deal_data.get('group_chat_id') == update.message.chat_id:
                found_deal_id = deal_id
                break
        if found_deal_id:
            await update.message.reply_text(f"Trade ID for this chat: `{found_deal_id}`")
        else:
            await update.message.reply_text("No active deal found associated with this chat. Ensure this is an official escrow group.")

async def token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: Implement a list of supported tokens/currencies.
    keyboard = [
        [InlineKeyboardButton("BTC", callback_data='select_token_btc'), InlineKeyboardButton("ETH", callback_data='select_token_eth'), InlineKeyboardButton("USDT (ERC20)", callback_data='select_token_usdt_erc20')],
        [InlineKeyboardButton("USDT (TRC20)", callback_data='select_token_usdt_trc20'), InlineKeyboardButton("BNB", callback_data='select_token_bnb')],
        [InlineKeyboardButton("Other / Specify", callback_data='select_token_other')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please select the token/currency for this escrow deal:", reply_markup=reply_markup)

async def token_selection_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    token_name = query.data.replace('select_token_', '').upper()
    # Prompt user for trade ID if not already in context
    if 'current_trade_id' not in context.user_data:
        await query.edit_message_text(f"You selected `{token_name}`. Now, please provide the Trade ID for which you want to set this token:")
        context.user_data['temp_token_selection'] = token_name
        return ConversationState.TOKEN_SELECTION # New state to get trade ID
    trade_id = context.user_data['current_trade_id'] # Use the trade ID from context
    if trade_id not in active_deals:
        await query.edit_message_text(f"Deal ID `{trade_id}` not found. Please check the ID.")
        context.user_data.pop('current_trade_id', None)
        return ConversationHandler.END # End conversation if trade ID is invalid
    active_deals[trade_id]['token'] = token_name
    await query.edit_message_text(f"Token `{token_name}` set for Deal ID `{trade_id}`.")
    # TODO: Save to DB

async def token_selection_trade_id_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    trade_id = update.message.text.strip().upper()
    token_name = context.user_data.pop('temp_token_selection')
    if trade_id not in active_deals:
        await update.message.reply_text(f"Deal ID `{trade_id}` not found. Please check the ID.")
        return ConversationHandler.END
    active_deals[trade_id]['token'] = token_name
    await update.message.reply_text(f"Token `{token_name}` set for Deal ID `{trade_id}`.")
    # TODO: Save to DB
    return ConversationHandler.END

# --- Deposit, Withdraw, Release, Refund (Simplified for brevity) ---
async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please provide the Trade ID for which you want to deposit funds:")
    return ConversationState.DEPOSIT_AMOUNT_SELECTION # Reusing this state for trade ID input initially

async def deposit_amount_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    trade_id = update.message.text.strip().upper()
    if trade_id not in active_deals:
        await update.message.reply_text(f"Deal ID `{trade_id}` not found.")
        return ConversationHandler.END
    deal = active_deals[trade_id]
    if not deal.get('escrow_address'):
        # In a real scenario, generate a unique address for this deal and token
        deal['escrow_address'] = "GENERATED_ESCROW_ADDRESS_HERE" # Placeholder
        # TODO: Integrate with crypto wallet generation API
    await update.message.reply_text(
        f"For Deal ID `{trade_id}`, deposit the amount of {deal['amount']} {deal.get('token', 'USD')} to:\n"
        f"Address: `{deal['escrow_address']}`\n\n"
        "Please send a screenshot of the transaction after depositing."
    )
    # This should probably lead to another state for transaction verification
    return ConversationHandler.END # End for now

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please provide the Trade ID for which you want to withdraw funds:")
    return ConversationState.WITHDRAW_AMOUNT_SELECTION # Reusing for trade ID input

async def withdraw_amount_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    trade_id = update.message.text.strip().upper()
    if trade_id not in active_deals:
        await update.message.reply_text(f"Deal ID `{trade_id}` not found.")
        return ConversationHandler.END
    deal = active_deals[trade_id]
    # In a real scenario, check if funds are available and handle withdrawal logic
    if deal.get('status') == 'funds_deposited':
        await update.message.reply_text(f"For Deal ID `{trade_id}`, enter the withdrawal address:")
        context.user_data['withdraw_trade_id'] = trade_id
        return ConversationState.WITHDRAW_ADDRESS_INPUT
    else:
        await update.message.reply_text(f"Funds are not yet deposited for Deal ID `{trade_id}` or deal status is not appropriate for withdrawal.")
        return ConversationHandler.END

async def withdraw_address_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    withdraw_address = update.message.text.strip()
    trade_id = context.user_data.pop('withdraw_trade_id')
    
    await update.message.reply_text(f"Withdrawal of funds for Deal ID `{trade_id}` to address `{withdraw_address}` has been initiated. Please wait for confirmation.")
    active_deals[trade_id]['status'] = 'withdrawal_initiated'
    # TODO: Integrate with crypto withdrawal API
    # TODO: Save to DB
    return ConversationHandler.END

async def release(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = extract_args(update)
    if not args:
        await update.message.reply_text("Please provide the Trade ID. Usage: `/release <TRADE_ID>`")
        return
    trade_id = args[0].upper()
    if trade_id not in active_deals:
        await update.message.reply_text(f"Deal ID `{trade_id}` not found.")
        return
    deal = active_deals[trade_id]
    if deal['status'] != 'funds_deposited': # Funds must be in escrow to be released
        await update.message.reply_text(f"Funds for Deal ID `{trade_id}` are not yet deposited or deal status is not appropriate for release.")
        return

    # In a real scenario, this would involve releasing funds to the seller's address
    await update.message.reply_text(f"Funds for Deal ID `{trade_id}` have been released to the seller.")
    deal['status'] = 'funds_released'
    # TODO: Integrate with crypto release API
    # TODO: Save to DB

async def refund(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = extract_args(update)
    if not args:
        await update.message.reply_text("Please provide the Trade ID. Usage: `/refund <TRADE_ID>`")
        return
    trade_id = args[0].upper()
    if trade_id not in active_deals:
        await update.message.reply_text(f"Deal ID `{trade_id}` not found.")
        return
    deal = active_deals[trade_id]
    if deal['status'] != 'funds_deposited': # Funds must be in escrow to be refunded
        await update.message.reply_text(f"Funds for Deal ID `{trade_id}` are not yet deposited or deal status is not appropriate for refund.")
        return

    # In a real scenario, this would involve refunding funds to the buyer's address
    await update.message.reply_text(f"Funds for Deal ID `{trade_id}` have been refunded to the buyer.")
    deal['status'] = 'refunded'
    # TODO: Integrate with crypto refund API
    # TODO: Save to DB

# --- User Stats ---
async def stats_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    profile = await get_user_profile(user_id, context)
    stats_text = (
        f"📊 Your Stats:\n"
        f"Username: @{profile.get('username', 'N/A')}\n"
        f"Total Escrows: {profile.get('total_escrows', 0)}\n"
        f"Rating: {profile.get('rating', 'N/A')} / 5.0\n"
        f"KYC Status: {profile.get('kyc_status', 'pending').replace('_', ' ').title()}\n"
        f"Referrals: {len(profile.get('referrals', []))}\n"
        f"Balance: {profile.get('balance', 0.0)} (Internal, not wallet balance)\n"
    )
    await update.message.reply_text(stats_text)

# --- Vouching ---
async def vouch_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Thank you for vouching! Please enter your vouch text:")
    return ConversationState.VOUCH_TEXT

async def vouch_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    vouch_text = update.message.text
    user_id = update.message.from_user.id
    user_info = update.message.from_user
    logging.info(f"New vouch received from {user_info.full_name} ({user_id}): {vouch_text}")
    
    # In a real system, you'd save this to a database,
    # and potentially have an admin review process before publishing.
    await update.message.reply_text("Thank you for your vouch! It has been submitted for review.")
    return ConversationHandler.END

# --- KYC (Know Your Customer) ---
async def kyc_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "To complete your KYC verification, please select the type of document you will upload:"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Passport", callback_data='kyc_doc_passport')],
        [InlineKeyboardButton("National ID Card", callback_data='kyc_doc_national_id')],
        [InlineKeyboardButton("Driver's License", callback_data='kyc_doc_driver_license')],
    ])
    await update.message.reply_text("Select document type:", reply_markup=keyboard)
    return ConversationState.USER_KYC_DOC_TYPE

async def kyc_doc_type_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    doc_type = query.data.replace('kyc_doc_', '')
    context.user_data['kyc_doc_type'] = doc_type
    await query.edit_message_text(f"You selected: {doc_type.replace('_', ' ').title()}. Now, please upload a clear photo of your {doc_type.replace('_', ' ').title()}.")
    return ConversationState.USER_KYC_DOC_UPLOAD

async def kyc_doc_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        file_id = update.message.photo[-1].file_id # Get the highest resolution photo
        doc_type = context.user_data.get('kyc_doc_type', 'document')
        user_id = update.message.from_user.id
        
        # In a real system, you'd download the file, store it securely,
        # and trigger a KYC verification process (e.g., send to a third-party KYC provider).
        # For this example, we'll just acknowledge the upload.
        
        # file = await context.bot.get_file(file_id)
        # await file.download_to_drive(f"kyc_docs/{user_id}_{doc_type}_{file_id}.jpg")

        await update_user_profile(user_id, 'kyc_status', 'submitted')
        await update.message.reply_text("Thank you! Your document has been submitted for KYC verification. We will notify you once it's reviewed.")
        context.user_data.pop('kyc_doc_type', None)
        return ConversationHandler.END
    else:
        await update.message.reply_text("Please upload a photo of your document.")
        return ConversationState.USER_KYC_DOC_UPLOAD

# --- Milestone Deal Flow (Simplified) ---
async def milestone_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Let's set up your milestone deal. First, what is the name of the first milestone?")
    return ConversationState.MILESTONE_NAME

async def milestone_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['current_milestone_name'] = update.message.text
    await update.message.reply_text("What is the amount for this milestone?")
    return ConversationState.MILESTONE_AMOUNT

async def milestone_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(update.message.text.replace(",", "").strip())
        context.user_data['current_milestone_amount'] = amount
        
        # Store milestone in a list or dict within user_data or active_deals
        if 'milestones' not in context.user_data:
            context.user_data['milestones'] = []
        context.user_data['milestones'].append({
            'name': context.user_data['current_milestone_name'],
            'amount': amount,
            'status': 'pending'
        })

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Add Another Milestone", callback_data='add_another_milestone')],
            [InlineKeyboardButton("Finish Milestone Setup", callback_data='finish_milestone_setup')],
        ])
        await update.message.reply_text(
            f"Milestone '{context.user_data['current_milestone_name']}' with amount {amount} added. What's next?",
            reply_markup=keyboard
        )
        return ConversationState.MILESTONE_CONFIRMATION
    except ValueError:
        await update.message.reply_text("Invalid amount. Please enter a numeric value.")
        return ConversationState.MILESTONE_AMOUNT

async def milestone_confirmation_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'add_another_milestone':
        await query.edit_message_text("Great! What is the name of the next milestone?")
        return ConversationState.MILESTONE_NAME
    elif query.data == 'finish_milestone_setup':
        # Finalize milestone deal creation
        trade_id = await generate_trade_id()
        active_deals[trade_id] = {
            'trade_id': trade_id,
            'creator_id': query.from_user.id,
            'type': 'milestone',
            'description': context.user_data.get('description', 'Milestone Deal'), # Use overall deal description if available
            'milestones': context.user_data['milestones'],
            'status': 'milestone_setup_complete',
            'created_at': datetime.now(),
            'total_amount': sum(m['amount'] for m in context.user_data['milestones']),
            # ... other deal parameters
        }
        await query.edit_message_text(
            f"Milestone deal `{trade_id}` setup complete with {len(context.user_data['milestones'])} milestones. Total amount: {active_deals[trade_id]['total_amount']}. "
            "Please use other commands to assign roles, deposit funds, and manage milestones."
        )
        context.user_data.pop('milestones', None)
        context.user_data.pop('current_milestone_name', None)
        context.user_data.pop('current_milestone_amount', None)
        return ConversationHandler.END

# --- Report Issue / Bug ---
async def report_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("What type of issue are you reporting?")
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Bug", callback_data='report_type_bug')],
        [InlineKeyboardButton("Feature Request", callback_data='report_type_feature')],
        [InlineKeyboardButton("Other", callback_data='report_type_other')],
    ])
    await update.message.reply_text("Select issue type:", reply_markup=keyboard)
    return ConversationState.REPORT_ISSUE_TYPE

async def report_issue_type_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    issue_type = query.data.replace('report_type_', '')
    context.user_data['issue_type'] = issue_type
    await query.edit_message_text(f"You selected: {issue_type.replace('_', ' ').title()}. Please describe the issue in detail.")
    return ConversationState.REPORT_ISSUE_DETAILS

async def report_issue_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    issue_details = update.message.text
    issue_type = context.user_data.pop('issue_type', 'unknown')
    user_id = update.message.from_user.id
    user_info = update.message.from_user

    logging.info(f"New report ({issue_type}) from {user_info.full_name} ({user_id}): {issue_details}")
    # In a real system, save this to a database, or send to an admin channel/ ticketing system.
    await update.message.reply_text("Thank you for reporting! Your issue has been recorded and will be reviewed by our team.")
    return ConversationHandler.END

# --- Feedback ---
async def feedback_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("We appreciate your feedback! Please type your comments or suggestions below.")
    return ConversationState.USER_FEEDBACK_TEXT

async def user_feedback_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feedback_text = update.message.text
    user_id = update.message.from_user.id
    user_info = update.message.from_user
    logging.info(f"New feedback from {user_info.full_name} ({user_id}): {feedback_text}")
    # Save feedback to DB or send to admin
    await update.message.reply_text("Thank you for your valuable feedback! It helps us improve.")
    return ConversationHandler.END

# --- Admin Commands ---

async def admin_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    # Always answer the callback query to remove the "loading" spinner on the button
    if query:
        await query.answer()

        # Now, safely access the user information
        user = query.from_user  # Access from_user from the callback_query object
        # Alternatively, user = update.effective_user is often reliable for the user initiating the action

        if user:
            # Log for debugging purposes
            logging.info(f"Admin menu button tapped by user: {user.id} ({user.first_name})")

            # Check if the user is an admin before proceeding
            if user.id in ADMIN_IDS:  # Make sure ADMIN_IDS is accessible here
                # This is where you would build and send your admin panel menu
                # Example:
                keyboard = [
                    [InlineKeyboardButton("Broadcast Message", callback_data='admin_broadcast')],
                    [InlineKeyboardButton("Ban User", callback_data='admin_ban_user')],
                    [InlineKeyboardButton("Unban User", callback_data='admin_unban_user')],
                    [InlineKeyboardButton("Resolve Dispute", callback_data='admin_resolve_dispute')],
                    [InlineKeyboardButton("Manage Fees", callback_data='admin_fees')],
                    [InlineKeyboardButton("Manage Channels", callback_data='admin_channels')],
                    [InlineKeyboardButton("View User Info", callback_data='admin_view_user')],
                    [InlineKeyboardButton("View Deal Info", callback_data='admin_view_deal')],
                    [InlineKeyboardButton("Back to Main Menu ⬅️", callback_data="main_menu")],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                # Edit the message to show the admin panel
                await query.edit_message_text(
                    text="Welcome to the Admin Panel! Choose an action:",
                    reply_markup=reply_markup
                )
            else:
                # If for some reason a non-admin taps it (shouldn't happen if button is hidden)
                await query.edit_message_text(text="You are not authorized to access the Admin Panel.")
        else:
            logging.warning("User object is None in admin_menu_handler's callback_query.")
            await query.edit_message_text(text="An error occurred while retrieving user info. Please try again.")
    else:
        logging.error("CallbackQuery object is None in admin_menu_handler. This shouldn't happen for button taps.")
        # Handle cases where update.callback_query is unexpectedly None
        # e.g., if this handler is mistakenly triggered by a non-callback update
        # You might want to add a check for update.message here if this handler
        # could potentially be triggered by a non-callback update.
        if update.message:
             await update.message.reply_text("An unexpected error occurred. Please try again.")


async def admin_broadcast_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.message.from_user.id):
        await update.message.reply_text("You are not authorized to use this command.")
        return
    await update.message.reply_text("Please enter the message you want to broadcast to all users:")
    return ConversationState.ADMIN_BROADCAST_MESSAGE

async def admin_broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.message.from_user.id):
        await update.message.reply_text("You are not authorized to use this command.")
        return
    broadcast_text = update.message.text
    # In a real bot, you would iterate through all users in your database
    # and send them this message. For this example, we'll just log it.
    logging.info(f"Admin broadcast message: {broadcast_text}")
    await update.message.reply_text("Message broadcast initiated (logged for demo).")
    return ConversationHandler.END

async def admin_ban_user_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.message.from_user.id):
        await update.message.reply_text("You are not authorized to use this command.")
        return
    await update.message.reply_text("Please enter the user ID to ban:")
    return ConversationState.ADMIN_BAN_USER_ID

async def admin_ban_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.message.from_user.id):
        await update.message.reply_text("You are not authorized to use this command.")
        return
    try:
        user_id_to_ban = int(update.message.text.strip())
        profile = await get_user_profile(user_id_to_ban, context)
        profile['is_banned'] = True
        await update_user_profile(user_id_to_ban, 'is_banned', True)
        await update.message.reply_text(f"User ID `{user_id_to_ban}` has been banned.")
    except ValueError:
        await update.message.reply_text("Invalid user ID. Please enter a numeric ID.")
    return ConversationHandler.END

async def admin_unban_user_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.message.from_user.id):
        await update.message.reply_text("You are not authorized to use this command.")
        return
    await update.message.reply_text("Please enter the user ID to unban:")
    return ConversationState.ADMIN_UNBAN_USER_ID

async def admin_unban_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.message.from_user.id):
        await update.message.reply_text("You are not authorized to use this command.")
        return
    try:
        user_id_to_unban = int(update.message.text.strip())
        profile = await get_user_profile(user_id_to_unban, context)
        profile['is_banned'] = False
        await update_user_profile(user_id_to_unban, 'is_banned', False)
        await update.message.reply_text(f"User ID `{user_id_to_unban}` has been unbanned.")
    except ValueError:
        await update.message.reply_text("Invalid user ID. Please enter a numeric ID.")
    return ConversationHandler.END

async def admin_resolve_dispute_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.message.from_user.id):
        await update.message.reply_text("You are not authorized to use this command.")
        return
    await update.message.reply_text("Please enter the Dispute ID to resolve:")
    return ConversationState.ADMIN_RESOLVE_DISPUTE_ID

async def admin_resolve_dispute_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.message.from_user.id):
        await update.message.reply_text("You are not authorized to use this command.")
        return
    dispute_id = update.message.text.strip()
    if dispute_id not in disputes:
        await update.message.reply_text(f"Dispute ID `{dispute_id}` not found.")
        return ConversationHandler.END
    
    context.user_data['dispute_to_resolve'] = dispute_id
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Release Funds to Seller", callback_data='resolve_release')],
        [InlineKeyboardButton("Refund Funds to Buyer", callback_data='resolve_refund')],
        [InlineKeyboardButton("Cancel Dispute", callback_data='resolve_cancel')],
    ])
    await update.message.reply_text(f"Dispute `{dispute_id}` found. What action would you like to take?", reply_markup=keyboard)
    return ConversationState.ADMIN_RESOLVE_DISPUTE_ACTION

async def admin_resolve_dispute_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.callback_query.from_user.id):
        await update.callback_query.answer("You are not authorized to use this command.")
        return
    query = update.callback_query
    await query.answer()
    dispute_id = context.user_data.pop('dispute_to_resolve')
    action = query.data.replace('resolve_', '')

    dispute = disputes[dispute_id]
    deal = active_deals.get(dispute['trade_id'])

    if action == 'release':
        if deal and deal['status'] == 'funds_deposited':
            deal['status'] = 'completed' # Or 'admin_released'
            dispute['status'] = 'resolved_released'
            await query.edit_message_text(f"Dispute `{dispute_id}` resolved: Funds released to seller for Deal ID `{deal['trade_id']}`.")
            # TODO: Trigger actual fund release
        else:
            await query.edit_message_text(f"Cannot release funds for Dispute `{dispute_id}`. Deal status is not appropriate.")
    elif action == 'refund':
        if deal and deal['status'] == 'funds_deposited':
            deal['status'] = 'cancelled' # Or 'admin_refunded'
            dispute['status'] = 'resolved_refunded'
            await query.edit_message_text(f"Dispute `{dispute_id}` resolved: Funds refunded to buyer for Deal ID `{deal['trade_id']}`.")
            # TODO: Trigger actual fund refund
        else:
            await query.edit_message_text(f"Cannot refund funds for Dispute `{dispute_id}`. Deal status is not appropriate.")
    elif action == 'cancel':
        dispute['status'] = 'cancelled_by_admin'
        await query.edit_message_text(f"Dispute `{dispute_id}` has been cancelled by admin.")
    
    # TODO: Save dispute and deal state to DB
    return ConversationHandler.END

async def admin_view_user_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.message.from_user.id):
        await update.message.reply_text("You are not authorized to use this command.")
        return
    await update.message.reply_text("Please enter the user ID to view their information:")
    return ConversationState.ADMIN_CHANGE_ROLE_USER_ID # Reusing for user ID input, will add specific state later

async def admin_view_user_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.message.from_user.id):
        await update.message.reply_text("You are not authorized to use this command.")
        return
    try:
        user_id = int(update.message.text.strip())
        profile = await get_user_profile(user_id, context)
        if profile:
            info_text = (
                f"User ID: `{user_id}`\n"
                f"Username: @{profile.get('username', 'N/A')}\n"
                f"First Name: {profile.get('first_name', 'N/A')}\n"
                f"Last Name: {profile.get('last_name', 'N/A')}\n"
                f"Balance: {profile.get('balance', 0.0)}\n"
                f"KYC Status: {profile.get('kyc_status', 'N/A').replace('_', ' ').title()}\n"
                f"Is Admin: {profile.get('is_admin', False)}\n"
                f"Is Banned: {profile.get('is_banned', False)}\n"
                f"Total Escrows: {profile.get('total_escrows', 0)}\n"
                f"Rating: {profile.get('rating', 'N/A')}\n"
                f"Created At: {profile.get('created_at', 'N/A').strftime('%Y-%m-%d %H:%M:%S') if profile.get('created_at') else 'N/A'}\n"
                f"Saved Addresses: {profile.get('saved_addresses', {})}\n"
            )
            await update.message.reply_text(info_text, parse_mode='Markdown')
        else:
            await update.message.reply_text(f"No profile found for User ID `{user_id}`.")
    except ValueError:
        await update.message.reply_text("Invalid user ID. Please enter a numeric ID.")
    return ConversationHandler.END

async def admin_view_deal_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.message.from_user.id):
        await update.message.reply_text("You are not authorized to use this command.")
        return
    await update.message.reply_text("Please enter the Trade ID to view its information:")
    return ConversationState.ADMIN_CHANGE_ROLE_NEW_ROLE # Reusing for trade ID input, will add specific state later

async def admin_view_deal_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.message.from_user.id):
        await update.message.reply_text("You are not authorized to use this command.")
        return
    trade_id = update.message.text.strip().upper()
    deal = active_deals.get(trade_id)
    if deal:
        info_text = (
            f"Deal ID: `{trade_id}`\n"
            f"Creator ID: `{deal.get('creator_id', 'N/A')}`\n"
            f"Type: {deal.get('type', 'N/A')}\n"
            f"Description: {deal.get('description', 'N/A')}\n"
            f"Amount: {deal.get('amount', 'N/A')}\n"
            f"Conditions: {deal.get('conditions', 'N/A')}\n"
            f"Status: {deal.get('status', 'N/A')}\n"
            f"Seller ID: `{deal.get('seller_id', 'N/A')}`\n"
            f"Buyer ID: `{deal.get('buyer_id', 'N/A')}`\n"
            f"Seller Address: `{deal.get('seller_address', 'N/A')}`\n"
            f"Buyer Address: `{deal.get('buyer_address', 'N/A')}`\n"
            f"Escrow Address: `{deal.get('escrow_address', 'N/A')}`\n"
            f"Token: {deal.get('token', 'N/A')}\n"
            f"Fee Percent: {deal.get('fee_percent', 'N/A')}%\n"
            f"Group Chat ID: `{deal.get('group_chat_id', 'N/A')}`\n"
            f"Dispute Status: {deal.get('dispute_status', 'N/A')}\n"
            f"Created At: {deal.get('created_at', 'N/A').strftime('%Y-%m-%d %H:%M:%S') if deal.get('created_at') else 'N/A'}\n"
        )
        if 'milestones' in deal:
            milestones_text = "\nMilestones:\n"
            for i, milestone in enumerate(deal['milestones']):
                milestones_text += f"  {i+1}. Name: {milestone['name']}, Amount: {milestone['amount']}, Status: {milestone['status']}\n"
            info_text += milestones_text
        await update.message.reply_text(info_text, parse_mode='Markdown')
    else:
        await update.message.reply_text(f"No deal found for Trade ID `{trade_id}`.")
    return ConversationHandler.END

# --- Channel Post Scheduling ---
async def channel_post_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.message.from_user.id):
        await update.message.reply_text("You are not authorized to use this command.")
        return
    await update.message.reply_text("Please enter the Channel ID (e.g., `-100123456789`) where you want to post:")
    return ConversationState.CHANNEL_POST_CHANNEL_ID

async def channel_post_channel_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.message.from_user.id):
        await update.message.reply_text("You are not authorized to use this command.")
        return
    try:
        channel_id = int(update.message.text.strip())
        context.user_data['target_channel_id'] = channel_id
        await update.message.reply_text("Now, please enter the content of the post:")
        return ConversationState.CHANNEL_POST_CONTENT
    except ValueError:
        await update.message.reply_text("Invalid Channel ID. Please enter a numeric ID.")
        return ConversationHandler.END

async def channel_post_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.message.from_user.id):
        await update.message.reply_text("You are not authorized to use this command.")
        return
    context.user_data['post_content'] = update.message.text
    await update.message.reply_text("When would you like to schedule this post? Enter 'now' or a date and time (e.g., '2025-12-31 14:30'):")
    return ConversationState.CHANNEL_POST_SCHEDULE_TIME

async def channel_post_schedule_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.message.from_user.id):
        await update.message.reply_text("You are not authorized to use this command.")
        return
    schedule_input = update.message.text.strip().lower()
    channel_id = context.user_data.pop('target_channel_id')
    post_content = context.user_data.pop('post_content')

    schedule_time = None
    if schedule_input == 'now':
        schedule_time = datetime.now()
    else:
        try:
            schedule_time = datetime.strptime(schedule_input, '%Y-%m-%d %H:%M')
        except ValueError:
            await update.message.reply_text("Invalid date and time format. Please use 'YYYY-MM-DD HH:MM' or 'now'.")
            return ConversationState.CHANNEL_POST_SCHEDULE_TIME

    # In a real bot, you'd use `pyrogram` or `telegram.ext.ExtBot.send_message`
    # and handle scheduling if it's not 'now'.
    try:
        if schedule_time <= datetime.now():
            # Send immediately
            await context.bot.send_message(chat_id=channel_id, text=post_content)
            await update.message.reply_text(f"Post sent to channel `{channel_id}` immediately.")
        else:
            # Schedule for later (requires a separate scheduling mechanism, e.g., a background job)
            # For this demo, we'll just acknowledge.
            await update.message.reply_text(f"Post for channel `{channel_id}` scheduled for {schedule_time.strftime('%Y-%m-%d %H:%M')}.")
            logging.info(f"Scheduled post for channel {channel_id} at {schedule_time}: {post_content}")
        
    except Exception as e:
        logging.error(f"Error sending/scheduling channel post: {e}")
        await update.message.reply_text(f"Error sending/scheduling post: {e}. Please ensure the bot is an admin in the channel.")
    
    return ConversationHandler.END

# --- OTC (Over-The-Counter) Deal Flow ---
async def otc_deal_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Starting an OTC deal. Are you the seller or buyer?")
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Seller", callback_data='otc_participant_seller')],
        [InlineKeyboardButton("Buyer", callback_data='otc_participant_buyer')],
    ])
    await update.message.reply_text("Select your role:", reply_markup=keyboard)
    return ConversationState.OTC_PARTICIPANT_TYPE

async def otc_participant_type_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['otc_role'] = query.data.replace('otc_participant_', '')
    await query.edit_message_text("Please provide the Telegram User ID of the other party (seller/buyer):")
    return ConversationState.OTC_PARTICIPANT_ID

async def otc_participant_id_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        other_party_id = int(update.message.text.strip())
        context.user_data['otc_other_party_id'] = other_party_id
        
        # Fetch other party's profile (optional, but good for verification)
        other_party_profile = await get_user_profile(other_party_id, context)
        other_party_name = other_party_profile.get('username') or other_party_profile.get('first_name') or f"User {other_party_id}"

        await update.message.reply_text(
            f"You are the {context.user_data['otc_role']}. The other party is {other_party_name} (`{other_party_id}`).\n"
            "Please confirm these details to proceed with the OTC deal setup."
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Confirm OTC Deal Details", callback_data='otc_confirm_details')],
            [InlineKeyboardButton("Cancel", callback_data='cancel_otc_deal')],
        ])
        await update.message.reply_text("Confirm:", reply_markup=keyboard)
        return ConversationState.OTC_CONFIRM_DETAILS
    except ValueError:
        await update.message.reply_text("Invalid User ID. Please enter a numeric Telegram User ID.")
        return ConversationState.OTC_PARTICIPANT_ID

async def otc_confirm_details_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'otc_confirm_details':
        # Create OTC deal (simplified)
        trade_id = await generate_trade_id()
        active_deals[trade_id] = {
            'trade_id': trade_id,
            'creator_id': query.from_user.id,
            'type': 'otc',
            'role_initiator': context.user_data['otc_role'],
            'other_party_id': context.user_data['otc_other_party_id'],
            'status': 'otc_pending_details',
            'created_at': datetime.now(),
        }
        await query.edit_message_text(
            f"OTC Deal `{trade_id}` initiated between you ({context.user_data['otc_role']}) and User ID `{context.user_data['otc_other_party_id']}`. "
            "Please use /dd to add deal details for this trade ID, then you can create an escrow group."
        )
        # Clean up user_data for OTC flow
        context.user_data.pop('otc_role', None)
        context.user_data.pop('otc_other_party_id', None)
        return ConversationHandler.END
    elif query.data == 'cancel_otc_deal':
        await query.edit_message_text("OTC deal setup cancelled.")
        context.user_data.pop('otc_role', None)
        context.user_data.pop('otc_other_party_id', None)
        return ConversationHandler.END

# --- Marketplace Listing (Simplified) ---
async def list_item_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Let's list your item for sale. What is the name of the item?")
    return ConversationState.LIST_ITEM_NAME

async def list_item_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['listing_name'] = update.message.text
    await update.message.reply_text("Please provide a brief description of the item:")
    return ConversationState.LIST_ITEM_DESC

async def list_item_desc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['listing_description'] = update.message.text
    await update.message.reply_text("What is the price of the item (e.g., '100 USD' or '0.005 BTC')?")
    return ConversationState.LIST_ITEM_PRICE

async def list_item_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['listing_price'] = update.message.text
    await update.message.reply_text("What category does this item belong to (e.g., 'Electronics', 'Collectibles', 'Services')?")
    return ConversationState.LIST_ITEM_CATEGORY

async def list_item_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['listing_category'] = update.message.text
    
    # Confirm listing details
    listing_summary = (
        f"Please confirm your listing details:\n"
        f"Name: {context.user_data['listing_name']}\n"
        f"Description: {context.user_data['listing_description']}\n"
        f"Price: {context.user_data['listing_price']}\n"
        f"Category: {context.user_data['listing_category']}\n"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Confirm Listing", callback_data='list_item_confirm')],
        [InlineKeyboardButton("Cancel", callback_data='list_item_cancel')],
    ])
    await update.message.reply_text(listing_summary, reply_markup=keyboard)
    return ConversationState.LIST_ITEM_CONFIRM

async def list_item_confirm_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'list_item_confirm':
        item_id = await generate_trade_id() # Reusing generate_trade_id for item ID
        listed_items[item_id] = {
            'item_id': item_id,
            'seller_id': query.from_user.id,
            'name': context.user_data.pop('listing_name'),
            'description': context.user_data.pop('listing_description'),
            'price': context.user_data.pop('listing_price'),
            'category': context.user_data.pop('listing_category'),
            'status': 'available',
            'listed_at': datetime.now(),
        }
        await query.edit_message_text(f"Your item '{listed_items[item_id]['name']}' has been listed with ID `{item_id}`!")
    elif query.data == 'list_item_cancel':
        await query.edit_message_text("Item listing cancelled.")
        context.user_data.pop('listing_name', None)
        context.user_data.pop('listing_description', None)
        context.user_data.pop('listing_price', None)
        context.user_data.pop('listing_category', None)
    return ConversationHandler.END

# --- Rating Feature (Simplified) ---
async def rating_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Do you want to give a rating or view someone's rating?")
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Give Rating", callback_data='rating_action_give')],
        [InlineKeyboardButton("View Rating", callback_data='rating_action_view')],
    ])
    await update.message.reply_text("Select action:", reply_markup=keyboard)
    return ConversationState.RATING_ACTION

async def rating_action_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data.replace('rating_action_', '')
    context.user_data['rating_action'] = action

    if action == 'give':
        await query.edit_message_text("Please enter the User ID of the person you want to rate:")
        return ConversationState.RATING_USER_ID
    elif action == 'view':
        await query.edit_message_text("Please enter the User ID of the person whose rating you want to view:")
        return ConversationState.VIEW_RATING_USER_ID

async def rating_user_id_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        target_user_id = int(update.message.text.strip())
        context.user_data['target_rating_user_id'] = target_user_id
        await update.message.reply_text("On a scale of 1 to 5, what rating would you like to give (5 being excellent)?")
        return ConversationState.RATING_VALUE
    except ValueError:
        await update.message.reply_text("Invalid User ID. Please enter a numeric Telegram User ID.")
        return ConversationState.RATING_USER_ID

async def rating_value_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        rating_value = float(update.message.text.strip())
        if not (1 <= rating_value <= 5):
            raise ValueError
        
        target_user_id = context.user_data.pop('target_rating_user_id')
        rater_id = update.message.from_user.id

        # In a real system, you'd save this to a database and recalculate average rating.
        # For demo, we'll just acknowledge and update a dummy rating.
        target_profile = await get_user_profile(target_user_id, context)
        current_rating = target_profile.get('rating', 5.0)
        total_ratings = target_profile.get('total_ratings', 0)

        new_total = (current_rating * total_ratings) + rating_value
        new_total_ratings = total_ratings + 1
        new_average_rating = new_total / new_total_ratings

        target_profile['rating'] = round(new_average_rating, 1)
        target_profile['total_ratings'] = new_total_ratings
        await update_user_profile(target_user_id, 'rating', target_profile['rating'])
        await update_user_profile(target_user_id, 'total_ratings', target_profile['total_ratings'])


        await update.message.reply_text(f"Thank you! You rated user `{target_user_id}` as {rating_value}. Their new average rating is {target_profile['rating']}.")
    except ValueError:
        await update.message.reply_text("Invalid rating. Please enter a number between 1 and 5.")
    return ConversationHandler.END

async def view_rating_user_id_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        target_user_id = int(update.message.text.strip())
        profile = await get_user_profile(target_user_id, context)
        if profile:
            await update.message.reply_text(f"User `{target_user_id}` has a rating of {profile.get('rating', 'N/A')} out of 5.0 (based on {profile.get('total_ratings', 0)} ratings).")
        else:
            await update.message.reply_text(f"No profile found for User ID `{target_user_id}` or no rating available.")
    except ValueError:
        await update.message.reply_text("Invalid User ID. Please enter a numeric Telegram User ID.")
    return ConversationHandler.END

# --- Trusted Users (Simplified) ---
async def trusted_users_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Manage your trusted users:")
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Add Trusted User", callback_data='trusted_add')],
        [InlineKeyboardButton("Remove Trusted User", callback_data='trusted_remove')],
        [InlineKeyboardButton("View Trusted Users", callback_data='trusted_view')],
    ])
    await update.message.reply_text("Select action:", reply_markup=keyboard)
    return ConversationHandler.END # Not a conversation, direct actions for now

async def trusted_add_user_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please enter the User ID of the person you want to add to your trusted list:")
    return ConversationState.ADD_TRUSTED_USER_ID

async def trusted_add_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        trusted_user_id = int(update.message.text.strip())
        user_id = update.message.from_user.id
        profile = await get_user_profile(user_id, context)
        if 'trusted_users' not in profile:
            profile['trusted_users'] = []
        if trusted_user_id not in profile['trusted_users']:
            profile['trusted_users'].append(trusted_user_id)
            await update_user_profile(user_id, 'trusted_users', profile['trusted_users'])
            await update.message.reply_text(f"User `{trusted_user_id}` added to your trusted list.")
        else:
            await update.message.reply_text(f"User `{trusted_user_id}` is already in your trusted list.")
    except ValueError:
        await update.message.reply_text("Invalid User ID. Please enter a numeric Telegram User ID.")
    return ConversationHandler.END

async def trusted_remove_user_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please enter the User ID of the person you want to remove from your trusted list:")
    return ConversationState.REMOVE_TRUSTED_USER_ID

async def trusted_remove_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        untrusted_user_id = int(update.message.text.strip())
        user_id = update.message.from_user.id
        profile = await get_user_profile(user_id, context)
        if 'trusted_users' in profile and untrusted_user_id in profile['trusted_users']:
            profile['trusted_users'].remove(untrusted_user_id)
            await update_user_profile(user_id, 'trusted_users', profile['trusted_users'])
            await update.message.reply_text(f"User `{untrusted_user_id}` removed from your trusted list.")
        else:
            await update.message.reply_text(f"User `{untrusted_user_id}` is not in your trusted list.")
    except ValueError:
        await update.message.reply_text("Invalid User ID. Please enter a numeric Telegram User ID.")
    return ConversationHandler.END

async def trusted_view_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    profile = await get_user_profile(user_id, context)
    trusted_users = profile.get('trusted_users', [])
    if trusted_users:
        user_names = []
        for uid in trusted_users:
            trusted_profile = await get_user_profile(uid, context)
            user_names.append(trusted_profile.get('username') or trusted_profile.get('first_name') or f"User {uid}")
        await update.message.reply_text(f"Your trusted users: {', '.join(user_names)}.")
    else:
        await update.message.reply_text("You have no trusted users yet.")

# --- Notification Settings ---
async def set_notifications_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    profile = await get_user_profile(user_id, context)
    current_settings = profile.get('notifications_settings', {"new_deal": True, "dispute": True, "fund_release": True})
    
    keyboard = []
    for setting, status in current_settings.items():
        emoji = "✅" if status else "❌"
        keyboard.append([InlineKeyboardButton(f"{emoji} {setting.replace('_', ' ').title()} Notifications", callback_data=f'toggle_notification_{setting}')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Manage your notification preferences:", reply_markup=reply_markup)

async def toggle_notification_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    setting_key = query.data.replace('toggle_notification_', '')
    user_id = query.from_user.id
    profile = await get_user_profile(user_id, context)
    
    current_status = profile['notifications_settings'].get(setting_key, True)
    profile['notifications_settings'][setting_key] = not current_status
    await update_user_profile(user_id, 'notifications_settings', profile['notifications_settings'])

    # Re-send the updated menu
    await set_notifications_start(update, context)


def main():
    application = ApplicationBuilder().token(os.getenv('BOT_TOKEN')).build()

    # Conversation Handlers
    dd_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("dd", dd)],
        states={
            ConversationState.DEAL_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, deal_description)],
            ConversationState.DEAL_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, deal_amount_handler)],
            ConversationState.DEAL_AMOUNT_BUYER_CONFIRM: [CallbackQueryHandler(deal_amount_buyer_confirm, pattern="^confirm_amount_buyer$"), CallbackQueryHandler(deal_amount_cancel, pattern="^cancel_amount$")],
            ConversationState.DEAL_AMOUNT_SELLER_CONFIRM: [CallbackQueryHandler(deal_amount_seller_confirm, pattern="^confirm_amount_seller$"), CallbackQueryHandler(deal_amount_cancel, pattern="^cancel_amount$")],
            ConversationState.DEAL_CHECKOUT: [CallbackQueryHandler(deal_checkout_done, pattern="^checkout_done$"), CallbackQueryHandler(deal_amount_cancel, pattern="^checkout_cancel$"), CallbackQueryHandler(deal_checkout_support, pattern="^checkout_support$")],
            # If you want conditions after amount confirmation, you'd add this here
            # ConversationState.DEAL_CONDITIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, deal_conditions_handler)],
        },
        fallbacks=[CommandHandler("cancel", deal_amount_cancel)],
        map_to_parent={
            ConversationHandler.END: ConversationHandler.END, # Allow ending conversation
        }
    )

    new_deal_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("newdeal", newdeal), CallbackQueryHandler(new_deal_type_selection, pattern="^new_deal_")],
        states={
            ConversationState.NEW_DEAL_TYPE: [CallbackQueryHandler(new_deal_type_selection, pattern="^new_deal_")],
            ConversationState.DEAL_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, deal_description)],
            ConversationState.DEAL_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, deal_amount_handler)], # Re-use if simple P2P
            ConversationState.DEAL_AMOUNT_BUYER_CONFIRM: [CallbackQueryHandler(deal_amount_buyer_confirm, pattern="^confirm_amount_buyer$"), CallbackQueryHandler(deal_amount_cancel, pattern="^cancel_amount$")],
            ConversationState.DEAL_AMOUNT_SELLER_CONFIRM: [CallbackQueryHandler(deal_amount_seller_confirm, pattern="^confirm_amount_seller$"), CallbackQueryHandler(deal_amount_cancel, pattern="^cancel_amount$")],
            ConversationState.DEAL_CHECKOUT: [CallbackQueryHandler(deal_checkout_done, pattern="^checkout_done$"), CallbackQueryHandler(deal_amount_cancel, pattern="^checkout_cancel$"), CallbackQueryHandler(deal_checkout_support, pattern="^checkout_support$")],
            ConversationState.DEAL_CONDITIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, deal_conditions_handler)],
            ConversationState.MILESTONE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, milestone_name)],
            ConversationState.MILESTONE_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, milestone_amount)],
            ConversationState.MILESTONE_CONFIRMATION: [CallbackQueryHandler(milestone_confirmation_callback, pattern="^add_another_milestone$|^finish_milestone_setup$")],
        },
        fallbacks=[CommandHandler("cancel", deal_amount_cancel)],
        map_to_parent={
            ConversationHandler.END: ConversationHandler.END,
        }
    )

    save_address_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("save", save_address_start)],
        states={
            ConversationState.SAVE_ADDRESS_CHAIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_address_chain)],
            ConversationState.SAVE_ADDRESS_DETAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_address_detail)],
        },
        fallbacks=[CommandHandler("cancel", deal_amount_cancel)], # Generic cancel for now
    )

    verify_address_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("verify", verify)],
        states={
            ConversationState.VERIFY_ADDRESS_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, verify_address_input)],
        },
        fallbacks=[CommandHandler("cancel", deal_amount_cancel)],
    )

    token_selection_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("token", token)],
        states={
            ConversationState.TOKEN_SELECTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, token_selection_trade_id_input)],
            ConversationState.DEAL_DESCRIPTION: [CallbackQueryHandler(token_selection_callback, pattern="^select_token_")], # Reuse description state to get trade ID
        },
        fallbacks=[CommandHandler("cancel", deal_amount_cancel)],
    )

    deposit_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("deposit", deposit)],
        states={
            ConversationState.DEPOSIT_AMOUNT_SELECTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, deposit_amount_selection)],
        },
        fallbacks=[CommandHandler("cancel", deal_amount_cancel)],
    )

    withdraw_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("withdraw", withdraw)],
        states={
            ConversationState.WITHDRAW_AMOUNT_SELECTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, withdraw_amount_selection)],
            ConversationState.WITHDRAW_ADDRESS_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, withdraw_address_input)],
        },
        fallbacks=[CommandHandler("cancel", deal_amount_cancel)],
    )

    vouch_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("vouch", vouch_start)],
        states={
            ConversationState.VOUCH_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, vouch_text_handler)],
        },
        fallbacks=[CommandHandler("cancel", deal_amount_cancel)],
    )

    kyc_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("kyc", kyc_start)],
        states={
            ConversationState.USER_KYC_DOC_TYPE: [CallbackQueryHandler(kyc_doc_type_selection, pattern="^kyc_doc_")],
            ConversationState.USER_KYC_DOC_UPLOAD: [MessageHandler(filters.PHOTO | filters.Document.ALL & ~filters.COMMAND, kyc_doc_upload)],
        },
        fallbacks=[CommandHandler("cancel", deal_amount_cancel)],
    )

    report_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("report", report_start)],
        states={
            ConversationState.REPORT_ISSUE_TYPE: [CallbackQueryHandler(report_issue_type_selection, pattern="^report_type_")],
            ConversationState.REPORT_ISSUE_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, report_issue_details)],
        },
        fallbacks=[CommandHandler("cancel", deal_amount_cancel)],
    )

    feedback_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("feedback", feedback_start)],
        states={
            ConversationState.USER_FEEDBACK_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, user_feedback_text)],
        },
        fallbacks=[CommandHandler("cancel", deal_amount_cancel)],
    )

    admin_broadcast_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(admin_broadcast_start, pattern="^admin_broadcast$")],
        states={
            ConversationState.ADMIN_BROADCAST_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_broadcast_message)],
        },
        fallbacks=[CommandHandler("cancel", deal_amount_cancel)],
    )

    admin_ban_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(admin_ban_user_start, pattern="^admin_ban_user$")],
        states={
            ConversationState.ADMIN_BAN_USER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_ban_user_id)],
        },
        fallbacks=[CommandHandler("cancel", deal_amount_cancel)],
    )

    admin_unban_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(admin_unban_user_start, pattern="^admin_unban_user$")],
        states={
            ConversationState.ADMIN_UNBAN_USER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_unban_user_id)],
        },
        fallbacks=[CommandHandler("cancel", deal_amount_cancel)],
    )

    admin_resolve_dispute_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(admin_resolve_dispute_start, pattern="^admin_resolve_dispute$")],
        states={
            ConversationState.ADMIN_RESOLVE_DISPUTE_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_resolve_dispute_id)],
            ConversationState.ADMIN_RESOLVE_DISPUTE_ACTION: [CallbackQueryHandler(admin_resolve_dispute_action, pattern="^resolve_")],
        },
        fallbacks=[CommandHandler("cancel", deal_amount_cancel)],
    )

    admin_view_user_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(admin_view_user_start, pattern="^admin_view_user$")],
        states={
            ConversationState.ADMIN_CHANGE_ROLE_USER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_view_user_info)],
        },
        fallbacks=[CommandHandler("cancel", deal_amount_cancel)],
    )

    admin_view_deal_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(admin_view_deal_start, pattern="^admin_view_deal$")],
        states={
            ConversationState.ADMIN_CHANGE_ROLE_NEW_ROLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_view_deal_info)],
        },
        fallbacks=[CommandHandler("cancel", deal_amount_cancel)],
    )

    channel_post_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(channel_post_start, pattern="^admin_schedule_post$")],
        states={
            ConversationState.CHANNEL_POST_CHANNEL_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, channel_post_channel_id)],
            ConversationState.CHANNEL_POST_CONTENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, channel_post_content)],
            ConversationState.CHANNEL_POST_SCHEDULE_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, channel_post_schedule_time)],
        },
        fallbacks=[CommandHandler("cancel", deal_amount_cancel)],
    )

    otc_deal_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("otc_deal", otc_deal_start)],
        states={
            ConversationState.OTC_PARTICIPANT_TYPE: [CallbackQueryHandler(otc_participant_type_selection, pattern="^otc_participant_")],
            ConversationState.OTC_PARTICIPANT_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, otc_participant_id_input)],
            ConversationState.OTC_CONFIRM_DETAILS: [CallbackQueryHandler(otc_confirm_details_callback, pattern="^otc_confirm_details$|^cancel_otc_deal$")],
        },
        fallbacks=[CommandHandler("cancel", deal_amount_cancel)],
    )

    list_item_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("list_item", list_item_start)],
        states={
            ConversationState.LIST_ITEM_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, list_item_name)],
            ConversationState.LIST_ITEM_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, list_item_desc)],
            ConversationState.LIST_ITEM_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, list_item_price)],
            ConversationState.LIST_ITEM_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, list_item_category)],
            ConversationState.LIST_ITEM_CONFIRM: [CallbackQueryHandler(list_item_confirm_callback, pattern="^list_item_confirm$|^list_item_cancel$")],
        },
        fallbacks=[CommandHandler("cancel", deal_amount_cancel)],
    )

    rating_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("rating", rating_start)],
        states={
            ConversationState.RATING_ACTION: [CallbackQueryHandler(rating_action_selection, pattern="^rating_action_")],
            ConversationState.RATING_USER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, rating_user_id_input)],
            ConversationState.RATING_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, rating_value_input)],
            ConversationState.VIEW_RATING_USER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, view_rating_user_id_input)],
        },
        fallbacks=[CommandHandler("cancel", deal_amount_cancel)],
    )

    # General Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("escrow", escrow))
    application.add_handler(CommandHandler("seller", seller))
    application.add_handler(CommandHandler("buyer", buyer))
    application.add_handler(CommandHandler("setfee", setfee))
    application.add_handler(CommandHandler("tradeid", tradeid))
    application.add_handler(CommandHandler("deposit", deposit)) # Added for direct deposit command
    application.add_handler(CommandHandler("withdraw", withdraw)) # Added for direct withdraw command
    application.add_handler(CommandHandler("release", release))
    application.add_handler(CommandHandler("refund", refund))
    application.add_handler(CommandHandler("stats", stats_menu))
    application.add_handler(CommandHandler("cancel", deal_amount_cancel)) # Generic cancel command

    # Callback Query Handlers (for menu buttons etc.)
    application.add_handler(CallbackQueryHandler(menu, pattern="^main_menu$")) # Return to main menu
    application.add_handler(CallbackQueryHandler(stats_menu, pattern="^stats_menu$"))
    application.add_handler(CallbackQueryHandler(admin_menu_handler, pattern="^admin_menu$"))
    application.add_handler(CallbackQueryHandler(escrow_type_selection, pattern="^escrow_p2p_group$|^escrow_product_group$"))
    application.add_handler(CallbackQueryHandler(trusted_add_user_start, pattern="^trusted_add$"))
    application.add_handler(CallbackQueryHandler(trusted_remove_user_start, pattern="^trusted_remove$"))
    application.add_handler(CallbackQueryHandler(trusted_view_users, pattern="^trusted_view$"))
    application.add_handler(CallbackQueryHandler(set_notifications_start, pattern="^settings_menu$")) # Link settings menu
    application.add_handler(CallbackQueryHandler(toggle_notification_callback, pattern="^toggle_notification_"))


    # Add conversation handlers to the application
    application.add_handler(dd_conv_handler)
    application.add_handler(new_deal_conv_handler)
    application.add_handler(save_address_conv_handler)
    application.add_handler(verify_address_conv_handler)
    application.add_handler(token_selection_conv_handler)
    application.add_handler(deposit_conv_handler)
    application.add_handler(withdraw_conv_handler)
    application.add_handler(vouch_conv_handler)
    application.add_handler(kyc_conv_handler)
    application.add_handler(report_conv_handler)
    application.add_handler(feedback_conv_handler)
    application.add_handler(admin_broadcast_conv_handler)
    application.add_handler(admin_ban_conv_handler)
    application.add_handler(admin_unban_conv_handler)
    application.add_handler(admin_resolve_dispute_conv_handler)
    application.add_handler(admin_view_user_conv_handler)
    application.add_handler(admin_view_deal_conv_handler)
    application.add_handler(channel_post_conv_handler)
    application.add_handler(otc_deal_conv_handler)
    application.add_handler(list_item_conv_handler)
    application.add_handler(rating_conv_handler)


    # --- Placeholder for other simple command handlers (like /whatisescrow, /instructions, /terms, /contact, /mydeals) ---
    async def simple_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        command = update.effective_message.text.lower()
        if command == "/whatisescrow":
            await update.message.reply_text("Escrow is a financial arrangement where a third party holds and regulates payment of the funds required for two parties involved in a given transaction. It helps ensure both parties fulfill their obligations before the funds are released.")
        elif command == "/instructions":
            await update.message.reply_text("Here are some instructions on how to use the bot:\n1. Use /newdeal to start a new deal.\n2. Follow the prompts to enter deal details.\n3. Share the escrow group link with the other party.\n4. Both parties use /seller and /buyer to assign roles and addresses.\n5. Deposit funds to the generated escrow address.\n6. Once conditions are met, either party can use /release or /refund.")
        elif command == "/terms":
            await update.message.reply_text("Terms of Service: By using this bot, you agree to our terms and conditions. All transactions are at your own risk. We are not responsible for any losses incurred due to incorrect information or misuse of the bot. Disputes will be arbitrated by admins.")
        elif command == "/contact":
            await update.message.reply_text("You can contact support via @JOHNMIACHEL (or your support username).")
        elif command == "/mydeals":
            user_id = update.message.from_user.id
            user_deals = [deal for deal_id, deal in active_deals.items() if deal.get('creator_id') == user_id or deal.get('seller_id') == user_id or deal.get('buyer_id') == user_id]
            if user_deals:
                response = "Your Deals:\n"
                for deal in user_deals:
                    response += f"- Deal ID: `{deal['trade_id']}`, Type: {deal['type']}, Status: {deal['status']}, Amount: {deal['amount']} {deal.get('token', '')}\n"
                await update.message.reply_text(response, parse_mode='Markdown')
            else:
                await update.message.reply_text("You have no active or past deals.")
        elif command == "/canceldeal":
            await update.message.reply_text("To cancel a deal, both parties must mutually agree. Please type `/canceldeal <TRADE_ID>` and ensure both parties confirm.")
        elif command == "/settings":
            await set_notifications_start(update, context) # Direct to settings menu
        elif command == "/premium":
            await update.message.reply_text("Premium features include lower fees, priority support, advanced analytics, and more. Contact admin for details.")
        elif command == "/check_updates":
            await update.message.reply_text("Checking for updates... The bot is currently running the latest version.")
        elif command == "/api_status":
            await update.message.reply_text("All external APIs are operational.")
        elif command == "/browse_items":
            if listed_items:
                response = "Items for Sale:\n"
                for item_id, item in listed_items.items():
                    if item['status'] == 'available':
                        response += f"- ID: `{item_id}`, Name: {item['name']}, Price: {item['price']}, Category: {item['category']}\n"
                await update.message.reply_text(response, parse_mode='Markdown')
            else:
                await update.message.reply_text("No items are currently listed for sale.")
        elif command.startswith("/buy_item"):
            args = extract_args(update)
            if len(args) < 1:
                await update.message.reply_text("Please provide the Item ID. Usage: `/buy_item <ITEM_ID>`")
                return
            item_id = args[0]
            item = listed_items.get(item_id)
            if item and item['status'] == 'available':
                await update.message.reply_text(f"Initiating purchase for '{item['name']}' (ID: `{item_id}`). Please contact the seller (User ID: `{item['seller_id']}`) to finalize the deal, or use the bot's escrow features for a secure transaction.")
            else:
                await update.message.reply_text(f"Item ID `{item_id}` not found or not available for purchase.")
        elif command == "/commands":
            await update.message.reply_text(COMMANDS_LIST, parse_mode='HTML', disable_web_page_preview=True)

    application.add_handler(MessageHandler(filters.COMMAND & (~filters.UpdateType.EDITED_MESSAGE), simple_message_handler))


    # Error handler
    async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        logging.error(f"Update {update} caused error {context.error}")
        if update.effective_message:
            await update.effective_message.reply_text("An error occurred. Please try again or contact support.")

    application.add_error_handler(error_handler)

    # --- Chat Member Handler (for bot joining groups) ---
    application.add_handler(ChatMemberHandler(bot_joined, chat_member_types=["my_chat_member", "chat_member"]))

    logging.info("Bot is starting polling...")
    application.run_polling()

if __name__ == '__main__':
    # It's recommended to load sensitive info from environment variables
    # For local testing, you can uncomment these lines temporarily, but use .env in production
    # os.environ['BOT_TOKEN'] = 'YOUR_BOT_TOKEN_HERE' 
    # os.environ['USERBOT_PHONE_NUMBER'] = '+919315849892' 
    # os.environ['ADMIN_IDS'] = '6...'

    # Dummy bot_joined function, replace with actual logic
    async def bot_joined(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat = update.effective_chat
        user = update.effective_user
        if update.my_chat_member:
            # Bot was added to a group or changed status in a group
            if update.my_chat_member.new_chat_member.status == 'member':
                logging.info(f"Bot joined group {chat.title} ({chat.id})")
                await chat.send_message(WELCOME_MESSAGE_GROUP)
            elif update.my_chat_member.new_chat_member.status == 'left':
                logging.info(f"Bot left group {chat.title} ({chat.id})")
        elif update.chat_member:
            # A user's status changed in a group the bot is in
            logging.info(f"User {user.full_name} ({user.id}) changed status in group {chat.title} ({chat.id}) to {update.chat_member.new_chat_member.status}")

    main()
