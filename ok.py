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

api_id = "25590804"
api_hash = "7c263991b86aecab2a9f5963a399997d"
phone_number = "+919315849892"
bot_username = "Mafiai09_bot"
group_id = -1004802076930 # ya invite link

async def add_bot_to_group():
    async with Client("my_account", api_id, api_hash, phone_number=phone_number) as app:
        await app.add_chat_members(group_id, bot_username)

# asyncio.run(add_bot_to_group())
ADMIN_IDS = [int(uid) for uid in os.getenv('ADMIN_IDS', '5684671374').split(',')]

# --- Userbot Config (Sensitive - do not hardcode in production) ---
# It's better to load these from environment variables or a secure config file.
# ZORG is removing the direct phone number for security.
api_id = 25590804
api_hash = "7c263991b86aecab2a9f5963a399997d"
# phone_number = "+919315849892" # Userbot phone number should be handled securely
# bot_username = "Mafiai09_bot" # Your bot's username

# --- Bot Config ---
BOT_TOKEN = "5881835648:AAFgBW4deNh1GYHCjiv_Rkv-NJXXnNgveK4" # Your bot token

# --- Conversation States (More states for more features) ---
(
    DEAL_DESCRIPTION, DEAL_AMOUNT, DEAL_CONDITIONS,
    SELLER_ADDRESS, BUYER_ADDRESS, SET_FEE_AMOUNT,
    SAVE_ADDRESS_CHAIN, SAVE_ADDRESS_DETAIL, VERIFY_ADDRESS_INPUT,
    NEW_DEAL_TYPE, NEW_DEAL_COUNTERPARTY, NEW_DEAL_AMOUNT_CURRENCY,
    TOKEN_SELECTION, DEPOSIT_AMOUNT_SELECTION, WITHDRAW_AMOUNT_SELECTION,
    WITHDRAW_ADDRESS_INPUT, DISPUTE_REASON, DISPUTE_PROOF,
    MILESTONE_NAME, MILESTONE_AMOUNT, MILESTONE_CONFIRMATION, MILESTONE_STATUS_UPDATE,
    REPORT_ISSUE_TYPE, REPORT_ISSUE_DETAILS,
    USER_KYC_DOC_TYPE, USER_KYC_DOC_UPLOAD, USER_FEEDBACK_TEXT,
    ADMIN_BAN_USER_ID, ADMIN_UNBAN_USER_ID, ADMIN_CHANGE_ROLE_USER_ID, ADMIN_CHANGE_ROLE_NEW_ROLE,
    ADMIN_BROADCAST_MESSAGE, ADMIN_RESOLVE_DISPUTE_ID, ADMIN_RESOLVE_DISPUTE_ACTION,
    CHANNEL_POST_CHANNEL_ID, CHANNEL_POST_CONTENT, CHANNEL_POST_SCHEDULE_TIME,
    VOUCH_TEXT, REFERRAL_SOURCE,
    OTC_PARTICIPANT_TYPE, OTC_PARTICIPANT_ID, OTC_CONFIRM_DETAILS,
    ADD_TRUSTED_USER_ID, REMOVE_TRUSTED_USER_ID,
    LIST_ITEM_NAME, LIST_ITEM_DESC, LIST_ITEM_PRICE, LIST_ITEM_CATEGORY, LIST_ITEM_CONFIRM
) = range(49)

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
    "Here you have a full command list, in case you do like to move through the bot using commands instead of the buttons.\n\n"
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
        return DEAL_AMOUNT
    except Exception as e:
        logging.error(f"Error setting deal description: {e}")
        await update.message.reply_text("An error occurred. Please try again.")
        return ConversationHandler.END


async def deal_amount_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print("User entered amount:", update.message.text)
        amount = float(update.message.text)
        context.user_data['deal_amount'] = amount
        await update.message.reply_text(
    f"""💰 Amount set to ₹{amount}.

Please enter a short description of the deal.""",
    parse_mode=ParseMode.HTML
)

        return DEAL_DESCRIPTION
    except Exception as e:
        print(f"Error in deal_amount_handler: {e}")
        await update.message.reply_text("❌ Invalid amount. Please enter a numeric value.")
        return DEAL_AMOUNT
        amount = float(update.message.text)
        if amount <= 0:
            await update.message.reply_text("Amount must be a positive number. Please enter a valid amount:")
            return ConversationState.DEAL_AMOUNT
        context.user_data['deal_amount'] = amount
        await update.message.reply_text("Enter any specific Conditions (or type 'none'):")
        return ConversationState.DEAL_CONDITIONS
    except ValueError:
        await update.message.reply_text("Invalid amount. Please enter a numeric value:")
        return DEAL_AMOUNT

async def deal_conditions_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['deal_conditions'] = update.message.text if update.message.text.lower() != 'none' else 'N/A'
    
    # Generate a trade_id and store deal data
    trade_id = await generate_trade_id()
    active_deals[trade_id] = {
        'trade_id': trade_id,
        'creator_id': context.user_data['deal_creator'],
        'type': context.user_data['deal_type'],
        'description': context.user_data['deal_description'],
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
        f"Deal: {context.user_data['deal_description']}\n"
        f"Amount: {context.user_data['deal_amount']}\n"
        f"Conditions: {context.user_data['deal_conditions']}\n\n"
        "Seller, use `/seller <your_crypto_address> <trade_id>` to specify your role and address.\n"
        "Buyer, use `/buyer <your_crypto_address> <trade_id>` to specify your role and address.\n\n"
        "You can now also use /escrow to create a private group for this deal, or proceed to payment if roles are set."
    )
    context.user_data.pop('deal_creator', None)
    context.user_data.pop('deal_type', None)
    context.user_data.pop('deal_description', None)
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
        return DEAL_DESCRIPTION
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
    group_link = "https://t.me/+CEAqXGNnXRc1OTdl"
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
    return SAVE_ADDRESS_CHAIN

async def save_address_chain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chain = update.message.text.strip().upper()
    context.user_data['temp_chain'] = chain
    await update.message.reply_text(f"Now, please provide the ADDRESS for `{chain}`:")
    return SAVE_ADDRESS_DETAIL

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
    return VERIFY_ADDRESS_INPUT

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
        [InlineKeyboardButton("BTC", callback_data='select_token_btc'),
         InlineKeyboardButton("ETH", callback_data='select_token_eth'),
         InlineKeyboardButton("USDT (ERC20)", callback_data='select_token_usdt_erc20')],
        [InlineKeyboardButton("USDT (TRC20)", callback_data='select_token_usdt_trc20'),
         InlineKeyboardButton("BNB", callback_data='select_token_bnb')],
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
        return TOKEN_SELECTION # New state to get trade ID
    
    trade_id = context.user_data['current_trade_id'] # Use the trade ID from context
    
    if trade_id not in active_deals:
        await query.edit_message_text(f"Deal ID `{trade_id}` not found. Please check the ID.")
        context.user_data.pop('current_trade_id', None)
        return
    
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
    return ConversationHandler.END # End the conversation

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please provide the Trade ID for which you want to deposit funds:")
    return DEPOSIT_AMOUNT_SELECTION # Reusing state for now, will get amount and then generate address

async def deposit_amount_and_id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = update.message.text.split()
    if len(args) < 2:
        await update.message.reply_text("Usage: `[AMOUNT] [TRADE_ID]` (e.g., `100 BTC-ABCD1234EF`)")
        return DEPOSIT_AMOUNT_SELECTION
    
    try:
        amount = float(args[0])
        trade_id = args[1].upper()
        if trade_id not in active_deals:
            await update.message.reply_text(f"Deal ID `{trade_id}` not found. Please check.")
            return DEPOSIT_AMOUNT_SELECTION
        
        deal = active_deals[trade_id]
        if deal['token'] is None:
            await update.message.reply_text(f"Please set a token for Deal ID `{trade_id}` first using /token.")
            return ConversationHandler.END # Exit or go to token selection state
        
        # TODO: Generate a unique escrow deposit address for this trade and token
        escrow_address = f"ESCR0W_ADDR_{trade_id}_{deal['token']}_{random.randint(1000,9999)}"
        deal['escrow_address'] = escrow_address
        deal['status'] = 'awaiting_deposit'

        await update.message.reply_text(
            f"Please deposit `{amount} {deal['token']}` to the following escrow address for Deal ID `{trade_id}`:\n\n"
            f"`{escrow_address}`\n\n"
            "Once deposited, funds will be held securely until release or refund. "
            "Use `/balance <escrow_address>` to check deposit status."
        )
        # TODO: Save address and amount to DB
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("Invalid amount. Please provide a numeric amount.")
        return DEPOSIT_AMOUNT_SELECTION

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = extract_args(update)
    if not args:
        await update.message.reply_text("Please provide the escrow address or Trade ID. Usage: `/balance <escrow_address_or_trade_id>`")
        return
    
    identifier = args[0]
    
    # Try to find deal by escrow address or trade ID
    found_deal = None
    for deal_id, deal_data in active_deals.items():
        if deal_data.get('escrow_address') == identifier or deal_id == identifier.upper():
            found_deal = deal_data
            break
            
    if found_deal:
        # TODO: Implement actual balance check using blockchain API for the escrow_address
        current_balance = 0.0 # Placeholder
        if found_deal['status'] == 'awaiting_deposit':
            current_balance = 0.0 # Still waiting
        elif found_deal['status'] == 'deposited':
            current_balance = found_deal['amount'] # Assume deposited
            
        await update.message.reply_text(f"Balance for escrow address `{found_deal['escrow_address']}` (Deal ID `{found_deal['trade_id']}`): `{current_balance} {found_deal['token']}` (demo)")
        if current_balance > 0 and found_deal['status'] == 'awaiting_deposit':
            found_deal['status'] = 'deposited'
            await update.message.reply_text(f"Funds detected for Deal ID `{found_deal['trade_id']}`. Deal is now in 'Deposited' status.")
            # Notify seller
            if found_deal['seller_id']:
                await context.bot.send_message(found_deal['seller_id'], f"Funds deposited for Deal ID `{found_deal['trade_id']}`. You can now proceed with delivery.")

    else:
        await update.message.reply_text("Escrow address or Trade ID not found or no associated deal.")

async def release(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = extract_args(update)
    if not args:
        await update.message.reply_text("Please provide the Trade ID to release funds. Usage: `/release <TRADE_ID>`")
        return
    
    trade_id = args[0].upper()
    if trade_id not in active_deals:
        await update.message.reply_text(f"Deal ID `{trade_id}` not found.")
        return

    deal = active_deals[trade_id]
    user_id = update.message.from_user.id

    if deal['status'] != 'deposited':
        await update.message.reply_text(f"Funds for Deal ID `{trade_id}` are not yet deposited or already processed (status: {deal['status']}).")
        return

    # Only buyer or admin can release funds
    if user_id != deal['buyer_id'] and not await is_admin(user_id):
        await update.message.reply_text("Only the buyer or an admin can release funds for this deal.")
        return

    # TODO: Implement actual fund release logic via blockchain/payment gateway
    # Simulate fund transfer
    if deal['seller_id']:
        seller_profile = await get_user_profile(deal['seller_id'], context)
        seller_profile['balance'] += deal['amount'] * (1 - deal['fee_percent'] / 100) # Deduct fee
        await update_user_profile(deal['seller_id'], 'balance', seller_profile['balance'])

    deal['status'] = 'funds_released'
    deal['completion_time'] = datetime.now()
    await update.message.reply_text(f"Funds for Deal ID `{trade_id}` have been successfully released to the seller! (demo)")
    await send_private_message(deal['seller_id'], f"Funds for Deal ID `{trade_id}` ({deal['amount']} {deal['token']}) have been released to your wallet (minus fee).")
    await send_private_message(deal['buyer_id'], f"You have confirmed release for Deal ID `{trade_id}`. Funds sent to seller.")
    # TODO: Save deal state to DB

async def refund(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = extract_args(update)
    if not args:
        await update.message.reply_text("Please provide the Trade ID to refund funds. Usage: `/refund <TRADE_ID>`")
        return
    
    trade_id = args[0].upper()
    if trade_id not in active_deals:
        await update.message.reply_text(f"Deal ID `{trade_id}` not found.")
        return

    deal = active_deals[trade_id]
    user_id = update.message.from_user.id

    if deal['status'] != 'deposited' and deal['dispute_status'] != 'open':
        await update.message.reply_text(f"Funds for Deal ID `{trade_id}` are not yet deposited or already processed (status: {deal['status']}). Refunds typically happen during dispute or mutual agreement.")
        return

    # Only seller or admin can refund (or mutual agreement in dispute)
    if user_id != deal['seller_id'] and not await is_admin(user_id):
        await update.message.reply_text("Only the seller or an admin can initiate a refund for this deal.")
        return

    # TODO: Implement actual fund refund logic via blockchain/payment gateway
    # Simulate fund transfer back to buyer
    if deal['buyer_id']:
        buyer_profile = await get_user_profile(deal['buyer_id'], context)
        buyer_profile['balance'] += deal['amount'] # No fee deducted on refund
        await update_user_profile(deal['buyer_id'], 'balance', buyer_profile['balance'])

    deal['status'] = 'refunded'
    deal['completion_time'] = datetime.now()
    await update.message.reply_text(f"Funds for Deal ID `{trade_id}` have been successfully refunded to the buyer! (demo)")
    await send_private_message(deal['buyer_id'], f"Funds for Deal ID `{trade_id}` ({deal['amount']} {deal['token']}) have been refunded to your wallet.")
    await send_private_message(deal['seller_id'], f"You have confirmed refund for Deal ID `{trade_id}`. Funds sent to buyer.")
    # TODO: Save deal state to DB

async def saved(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    profile = await get_user_profile(user_id, context)
    saved_addrs = profile.get('saved_addresses', {})

    if not saved_addrs:
        await update.message.reply_text("You have no saved addresses. Use /save to add one.")
        return
    
    response = "Your saved addresses:\n\n"
    for chain, address in saved_addrs.items():
        response += f"`{chain}`: `{address}`\n"
    await update.message.reply_text(response)

async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    profile = await get_user_profile(user_id, context)
    referrals = profile.get('referrals', [])
    referral_count = len(referrals)
    referral_link = f"https://t.me/{context.bot.username}?start=ref_{user_id}" # Example referral link
    
    response = (
        f"You have `{referral_count}` referrals.\n\n"
        f"Share your unique referral link to earn rewards (conceptual):\n"
        f"`{referral_link}`"
    )
    await update.message.reply_text(response)
    # TODO: Implement tracking referral rewards and payouts

async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(COMMANDS_LIST, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

async def whatisescrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "What is Escrow?\n\n"
        "Escrow is a financial arrangement where a third party holds and regulates the payment of the funds required for two parties involved in a given transaction. "
        "It helps make transactions more secure by keeping the payment in a secure escrow account which is only released when all of the terms of an agreement are met."
    )

async def instructions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Instructions:\n"
        "1. Start a new deal with /newdeal or /dd\n"
        "2. If needed, create a dedicated group with /escrow\n"
        "3. Assign roles (seller/buyer) and addresses with /seller and /buyer for the specific Trade ID\n"
        "4. Set the token/currency with /token\n"
        "5. Deposit funds with /deposit\n"
        "6. Use /release to release funds to seller, /refund to refund to buyer\n"
        "7. For help, use /dispute to contact an admin.\n"
        "8. Explore other features via /menu."
    )

async def terms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Terms of Service (TOS):\n"
        "By using this bot, you agree to our rules and that the bot is not responsible for losses due to incorrect information or external factors. "
        "Full terms can be found at: [Link to your full TOS page] (conceptual)"
    )

async def dispute_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This command can be used in group chats or private chats
    if update.message.chat.type == 'private':
        await update.message.reply_text("Please provide the Trade ID for the deal you want to dispute:")
        return DISPUTE_REASON # Go to state to get trade ID and reason
    else: # In a group chat, assume current chat is the trade ID
        found_trade_id = None
        for tid, deal_data in active_deals.items():
            if deal_data.get('group_chat_id') == update.message.chat_id:
                found_trade_id = tid
                break
        
        if found_trade_id:
            context.user_data['dispute_trade_id'] = found_trade_id
            await update.message.reply_text(f"Dispute for Deal ID `{found_trade_id}`. Please describe the issue in detail:")
            return DISPUTE_REASON
        else:
            await update.message.reply_text("No active deal found in this group chat. Please use /dispute <TRADE_ID> in private or ensure this is an escrow group.")
            return ConversationHandler.END

async def dispute_reason_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    trade_id = context.user_data.get('dispute_trade_id')
    if not trade_id: # If not set from group, expect user to provide it
        args = update.message.text.split(maxsplit=1)
        if len(args) < 1:
            await update.message.reply_text("Please provide the Trade ID and your reason. Usage: `[TRADE_ID] [YOUR REASON]`")
            return DISPUTE_REASON
        trade_id = args[0].upper()
        reason = args[1] if len(args) > 1 else "No reason provided."
    else:
        reason = update.message.text

    if trade_id not in active_deals:
        await update.message.reply_text(f"Deal ID `{trade_id}` not found. Please check.")
        context.user_data.pop('dispute_trade_id', None)
        return ConversationHandler.END

    deal = active_deals[trade_id]
    if deal['status'] in ['completed', 'cancelled', 'dispute_raised', 'funds_released', 'refunded']:
        await update.message.reply_text(f"Dispute cannot be raised for deal `{trade_id}` in status `{deal['status']}`.")
        context.user_data.pop('dispute_trade_id', None)
        return ConversationHandler.END
    
    dispute_id = await generate_trade_id("DISP")
    disputes[dispute_id] = {
        'trade_id': trade_id,
        'raised_by': update.message.from_user.id,
        'reason': reason,
        'status': 'open',
        'raised_at': datetime.now(),
        'proofs': {}
    }
    deal['dispute_status'] = 'open' # Link dispute to deal

    context.user_data['current_dispute_id'] = dispute_id
    await update.message.reply_text(f"Dispute `{dispute_id}` raised for Deal ID `{trade_id}`. Please send any supporting photos or documents now (or type 'done' if no proofs).")
    return DISPUTE_PROOF

async def dispute_proof_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dispute_id = context.user_data.get('current_dispute_id')
    if not dispute_id or dispute_id not in disputes:
        await update.message.reply_text("No active dispute session. Please start a new dispute with /dispute.")
        return ConversationHandler.END

    dispute_data = disputes[dispute_id]

    if update.message.photo:
        photo_id = update.message.photo[-1].file_id
        dispute_data['proofs'][f'photo_{len(dispute_data["proofs"])}'] = photo_id
        await update.message.reply_text("Photo proof received. Send more or type 'done'.")
        return DISPUTE_PROOF
    elif update.message.document:
        document_id = update.message.document.file_id
        dispute_data['proofs'][f'doc_{len(dispute_data["proofs"])}'] = document_id
        await update.message.reply_text("Document proof received. Send more or type 'done'.")
        return DISPUTE_PROOF
    elif update.message.text and update.message.text.lower() == 'done':
        await update.message.reply_text("Thank you. The dispute has been recorded. Our admin will review it shortly.")
        
        # Notify admins
        deal = active_deals[dispute_data['trade_id']]
        admin_notification = (
            f"🚨 \\*\\*NEW DISPUTE ALERT\\*\\* 🚨\n"
            f"Trade ID: `{dispute_data['trade_id']}`\n"
            f"Dispute ID: `{dispute_id}`\n"
            f"Raised by: `{update.message.from_user.full_name}` (`{update.message.from_user.id}`)\n"
            f"Reason: `{dispute_data['reason']}`\n"
            f"Deal Description: `{deal['description']}`\n"
            f"Amount: `{deal['amount']} {deal['token']}`\n"
            f"Status: `{deal['status']}`\n"
            f"Number of proofs: `{len(dispute_data['proofs'])}`\n\n"
            f"Use `/admin_resolve_dispute {dispute_id} <action>` to resolve \\(release/refund\\)\\."
        )
        for admin_id in ADMIN_IDS:
            await send_private_message(admin_id, admin_notification)
            # Send proofs to admin
            for proof_type, proof_id in dispute_data['proofs'].items():
                try:
                    if 'photo' in proof_type:
                        await context.bot.send_photo(chat_id=admin_id, photo=proof_id, caption=f"Proof for Dispute `{dispute_id}`")
                    elif 'doc' in proof_type:
                        await context.bot.send_document(chat_id=admin_id, document=proof_id, caption=f"Proof for Dispute `{dispute_id}`")
                except Exception as e:
                    logging.error(f"Failed to send proof {proof_id} to admin {admin_id}: {e}")

        context.user_data.pop('current_dispute_id', None)
        return ConversationHandler.END
    else:
        await update.message.reply_text("Invalid input. Please send a photo, document, or type 'done'.")
        return DISPUTE_PROOF


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "☎ CONTACT ARBITRATOR\n\n"
        "💬 Type /dispute\n\n"
        "💡 Incase you're not getting a response can reach out to @JOHNMIACHEL" # Replace with actual admin username
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    profile = await get_user_profile(user_id, context)
    
    # Calculate more dynamic stats
    total_escrows = len([d for d in active_deals.values() if d['creator_id'] == user_id or d['buyer_id'] == user_id or d['seller_id'] == user_id])
    completed_escrows = len([d for d in active_deals.values() if d['status'] == 'funds_released' and (d['creator_id'] == user_id or d['buyer_id'] == user_id or d['seller_id'] == user_id)])
    total_worth = sum([d['amount'] for d in active_deals.values() if d['status'] == 'funds_released' and (d['creator_id'] == user_id or d['buyer_id'] == user_id or d['seller_id'] == user_id)])

    await update.message.reply_text(
        "User Stats\n\n"
        f"📍 Total Escrows: {total_escrows}\n"
        f"✅ Completed Escrows: {completed_escrows}\n"
        f"🎟 Total Tickets: {len([d for d in disputes.values() if d['raised_by'] == user_id])}\n" # Disputes raised by user
        f"🎉 Your Rating: {profile.get('rating', 'N/A')}/5.0\n" # Placeholder for dynamic rating
        f"💰 Total Worth Processed: {total_worth:.2f}$ (conceptual)\n"
        "⏰ Fastest Escrow: None (conceptual)\n" # TODO: Implement tracking fastest escrow
        f"⏰ First Escrow Time: {profile.get('created_at').strftime('%Y-%m-%d %H:%M') if profile.get('created_at') else 'None'}\n"
        "⏰ Last Escrow Time: None (conceptual)\n" # TODO: Implement tracking last escrow time
        "💰 Last Escrow Worth: 0.00$ (conceptual)" # TODO: Implement tracking last escrow worth
    )

async def deposit_old_upi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("UPI = Millionairelodhi@fam (This is a dummy UPI for demo purposes. Do NOT use for real transactions.)")
    await update.message.reply_text("For actual deposits, use the /deposit command with a Trade ID to get an escrow address.")

async def vouch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Thank you for your vouch! You can share your positive experience in our Vouches Channel (link in /menu).")
    # TODO: Log vouch, potentially link to a public vouch system.

async def bot_joined(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_member_update = update.my_chat_member or update.chat_member
    if (
        chat_member_update is not None
        and chat_member_update.new_chat_member.user.id == context.bot.id
        and chat_member_update.new_chat_member.status in ["member", "administrator"]
    ):
        await context.bot.send_message(
            chat_id=chat_member_update.chat.id,
            text=WELCOME_MESSAGE_GROUP
        )
        await context.bot.send_message(
            chat_id=chat_member_update.chat.id,
            text=COMMANDS_LIST,
            parse_mode="HTML",
            disable_web_page_preview=True
        )

# --- NEW FEATURES (Placeholder Implementations) ---

async def my_deals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_related_deals = [
        deal for deal_id, deal in active_deals.items() 
        if deal.get('creator_id') == user_id or 
           deal.get('buyer_id') == user_id or 
           deal.get('seller_id') == user_id
    ]

    if not user_related_deals:
        await update.message.reply_text("You have no active or past deals.")
        return

    response = "Your Deals:\n\n"
    for deal in user_related_deals:
        response += (
            f"\\*\\*ID:\\*\\* `{deal['trade_id']}`\n"
            f"\\*\\*Description:\\*\\* `{deal['description']}`\n"
            f"\\*\\*Amount:\\*\\* `{deal['amount']} {deal['token'] or 'N/A'}`\n"
            f"\\*\\*Status:\\*\\* `{deal['status'].replace('_', ' ').title()}`\n"
            f"\\*\\*Dispute Status:\\*\\* `{deal['dispute_status'].replace('_', ' ').title()}`\n"
            f"\\*\\*Created:\\*\\* `{deal['created_at'].strftime('%Y-%m-%d %H:%M')}`\n"
            f"\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\n"
        )
    await update.message.reply_text(response)
    # TODO: Add inline buttons to view details of each deal, cancel, dispute, etc.

async def cancel_deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = extract_args(update)
    if not args:
        await update.message.reply_text("Please provide the Trade ID to cancel. Usage: `/canceldeal <TRADE_ID>`")
        return
    trade_id = args[0].upper()
    if trade_id not in active_deals:
        await update.message.reply_text(f"Deal ID `{trade_id}` not found.")
        return
    
    deal = active_deals[trade_id]
    user_id = update.message.from_user.id

    # Allow creator, buyer, or seller to initiate cancellation
    if user_id not in [deal['creator_id'], deal['buyer_id'], deal['seller_id']] and not await is_admin(user_id):
        await update.message.reply_text("You are not authorized to cancel this deal.")
        return
    
    if deal['status'] in ['completed', 'funds_released', 'refunded', 'disputed']:
        await update.message.reply_text(f"Deal `{trade_id}` is in `{deal['status']}` status and cannot be cancelled directly. Raise a dispute if there's an issue.")
        return

    if deal['status'] == 'cancellation_requested':
        if deal['cancellation_requester'] != user_id:
            # Both parties agree
            deal['status'] = 'cancelled'
            deal['completion_time'] = datetime.now()
            await update.message.reply_text(f"Deal `{trade_id}` has been mutually cancelled.")
            # TODO: Refund any deposited funds if applicable
            await send_private_message(deal['creator_id'], f"Deal `{trade_id}` has been cancelled by mutual agreement.")
            if deal['buyer_id']: await send_private_message(deal['buyer_id'], f"Deal `{trade_id}` has been cancelled by mutual agreement.")
            if deal['seller_id']: await send_private_message(deal['seller_id'], f"Deal `{trade_id}` has been cancelled by mutual agreement.")
        else:
            await update.message.reply_text(f"You have already requested cancellation for Deal `{trade_id}`. Waiting for the other party's confirmation.")
    else:
        deal['status'] = 'cancellation_requested'
        deal['cancellation_requester'] = user_id
        await update.message.reply_text(f"Cancellation for Deal `{trade_id}` requested. The other party needs to confirm by also using `/canceldeal {trade_id}`.")
        # Notify other party
        other_party_id = None
        if user_id == deal['buyer_id'] and deal['seller_id']: other_party_id = deal['seller_id']
        elif user_id == deal['seller_id'] and deal['buyer_id']: other_party_id = deal['buyer_id']
        elif user_id == deal['creator_id'] and deal['buyer_id'] and deal['seller_id']: # Notify both if creator not a party
            if deal['buyer_id'] != user_id: await send_private_message(deal['buyer_id'], f"Deal `{trade_id}` cancellation requested by creator.")
            if deal['seller_id'] != user_id: await send_private_message(deal['seller_id'], f"Deal `{trade_id}` cancellation requested by creator.")
        
        if other_party_id:
            await send_private_message(other_party_id, f"Cancellation requested for Deal `{trade_id}` by {update.message.from_user.full_name}. Use `/canceldeal {trade_id}` to confirm.")
    # TODO: Save deal state to DB

async def milestone_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: Start a conversation for adding milestones to a selected deal ID
    await update.message.reply_text("This feature allows you to define milestones for a deal. Please provide the Trade ID:")
    return MILESTONE_NAME

async def milestone_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: Logic for milestone name
    await update.message.reply_text("Milestone name recorded. Now enter the amount for this milestone:")
    return MILESTONE_AMOUNT

async def milestone_amount_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: Logic for milestone amount
    await update.message.reply_text("Milestone amount recorded. Confirm adding this milestone? (yes/no)")
    return MILESTONE_CONFIRMATION

async def milestone_confirm_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: Logic for milestone confirmation
    await update.message.reply_text("Milestone added. You can add more or proceed with deal.")
    return ConversationHandler.END

async def milestone_status_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: Allow parties to update milestone status (e.g., 'completed', 'in_progress')
    await update.message.reply_text("Updated milestone status. (conceptual)")

async def report_issue_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("What type of issue are you reporting? (e.g., `bug`, `transaction`, `group`, `user_misconduct`, `other`):")
    return REPORT_ISSUE_TYPE

async def report_issue_type_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    issue_type = update.message.text.strip().lower()
    # TODO: Validate issue_type
    context.user_data['report_issue_type'] = issue_type
    await update.message.reply_text(f"Please describe the `{issue_type}` issue in detail, including any relevant Trade IDs or user IDs:")
    return REPORT_ISSUE_DETAILS

async def report_issue_details_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    issue_details = update.message.text
    user_id = update.message.from_user.id
    issue_type = context.user_data.pop('report_issue_type')
    
    report_id = await generate_trade_id("REPORT")
    # TODO: Store report in a dedicated 'reports' database table
    # TODO: Notify admins
    await update.message.reply_text(f"Thank you for reporting the issue ({issue_type}). Your report ID is `{report_id}`. An admin will review it shortly.")
    return ConversationHandler.END

async def feedback_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("We appreciate your feedback! Please type your suggestions or comments about the bot:")
    return USER_FEEDBACK_TEXT

async def user_feedback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feedback_text = update.message.text
    user_id = update.message.from_user.id
    
    feedback_id = await generate_trade_id("FEED")
    # TODO: Store feedback in a 'feedback' database table
    # TODO: Optionally notify admins if it's critical feedback
    await update.message.reply_text(f"Thank you for your valuable feedback (ID: `{feedback_id}`). We will consider your suggestions!")
    return ConversationHandler.END

async def kyc_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    profile = await get_user_profile(update.message.from_user.id, context)
    if profile.get('kyc_status') == 'verified':
        await update.message.reply_text("Your KYC is already verified.")
        return ConversationHandler.END
    
    await update.message.reply_text("To start KYC verification, please select the document type you will upload:")
    keyboard = [
        [InlineKeyboardButton("Passport", callback_data='kyc_doc_passport')],
        [InlineKeyboardButton("National ID Card", callback_data='kyc_doc_id_card')],
        [InlineKeyboardButton("Driving License", callback_data='kyc_doc_driver_license')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose document type:", reply_markup=reply_markup)
    return USER_KYC_DOC_TYPE

async def kyc_doc_type_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    doc_type = query.data.replace('kyc_doc_', '')
    context.user_data['kyc_doc_type'] = doc_type
    await query.edit_message_text(f"Please upload a clear photo of your `{doc_type}`. Ensure all details are visible and there's no glare.")
    return USER_KYC_DOC_UPLOAD

async def kyc_doc_upload_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        await update.message.reply_text("Please upload a photo of your document.")
        return USER_KYC_DOC_UPLOAD

    user_id = update.message.from_user.id
    doc_type = context.user_data.pop('kyc_doc_type')
    photo_file_id = update.message.photo[-1].file_id
    
    # TODO: Save photo_file_id to user's KYC record in DB
    # TODO: Send photo to KYC verification service (external API) or internal admin review
    profile = await get_user_profile(user_id, context)
    profile['kyc_status'] = 'under_review'
    await update_user_profile(user_id, 'kyc_status', 'under_review')

    await update.message.reply_text("Thank you! Your document has been submitted for KYC verification. We will notify you of the status within 24-48 hours.")
    return ConversationHandler.END


async def settings_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Notification Settings 🔔", callback_data='settings_notifications')],
        [InlineKeyboardButton("Privacy Settings 🕵️", callback_data='settings_privacy')],
        [InlineKeyboardButton("Language 🌐", callback_data='settings_language')],
        [InlineKeyboardButton("Change Wallet Address 💼", callback_data='settings_change_wallet')],
        [InlineKeyboardButton("Back to Main Menu ⬅️", callback_data='menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("User Settings:\nChoose an option:", reply_markup=reply_markup)

async def settings_notifications(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    profile = await get_user_profile(user_id, context)
    notif_settings = profile.get('notifications_settings', {})

    response_text = "Notification Settings:\n\n"
    keyboard = []
    for setting, enabled in notif_settings.items():
        status = "✅ ON" if enabled else "❌ OFF"
        response_text += f"{setting.replace('_', ' ').title()}: {status}\n"
        keyboard.append([InlineKeyboardButton(f"Toggle {setting.replace('_', ' ').title()} {status}", callback_data=f'toggle_notification_{setting}')])
    
    keyboard.append([InlineKeyboardButton("Back to Settings ⬅️", callback_data='settings_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(response_text, reply_markup=reply_markup)

async def toggle_notification_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    setting_key = query.data.replace('toggle_notification_', '')
    
    profile = await get_user_profile(user_id, context)
    notif_settings = profile.get('notifications_settings', {})
    
    if setting_key in notif_settings:
        notif_settings[setting_key] = not notif_settings[setting_key] # Toggle boolean
        profile['notifications_settings'] = notif_settings
        await update_user_profile(user_id, 'notifications_settings', notif_settings)
        await query.edit_message_text(f"{setting_key.replace('_', ' ').title()} notifications are now {'ON' if notif_settings[setting_key] else 'OFF'}.")
        # Re-display notification settings menu
        await settings_notifications(update, context) # Pass update and context again
    else:
        await query.edit_message_text("Unknown notification setting.")

async def premium_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✨ **Premium Features (Conceptual)** ✨\n\n"
        "Unlock exclusive benefits with our Premium subscription:\n"
        "- Lower escrow fees (e.g., 0.5% instead of 1.0%)\n"
        "- Priority dispute resolution\n"
        "- Advanced analytics and reports\n"
        "- Dedicated support channel\n"
        "- Custom branding for escrow groups\n\n"
        "Coming Soon! Stay tuned for pricing and subscription options."
    )

# --- Admin Panel Features ---
async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update.callback_query.from_user.id if update.callback_query else update.message.from_user.id):
        await (update.callback_query or update.message).reply_text("You are not authorized to access the Admin Panel.")
        return
    
    keyboard = [
        [InlineKeyboardButton("User Management 👤", callback_data='admin_user_mgmt')],
        [InlineKeyboardButton("Deal Management 💼", callback_data='admin_deal_mgmt')],
        [InlineKeyboardButton("Dispute Resolution 🚨", callback_data='admin_dispute_mgmt')],
        [InlineKeyboardButton("Broadcast Message 📢", callback_data='admin_broadcast_msg')],
        [InlineKeyboardButton("Fee Management 💲", callback_data='admin_fee_mgmt')],
        [InlineKeyboardButton("Channel Management 💬", callback_data='admin_channel_mgmt')],
        [InlineKeyboardButton("System Status 📊", callback_data='admin_system_status')],
        [InlineKeyboardButton("Back to Main Menu ⬅️", callback_data='menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await (update.callback_query or update.message).reply_text("Admin Panel:\nChoose an option:", reply_markup=reply_markup)

async def admin_user_mgmt_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if not await is_admin(query.from_user.id): return
    
    keyboard = [
        [InlineKeyboardButton("Ban User 🚫", callback_data='admin_ban_user')],
        [InlineKeyboardButton("Unban User ✅", callback_data='admin_unban_user')],
        [InlineKeyboardButton("Change User Role 🛠️", callback_data='admin_change_role')],
        [InlineKeyboardButton("View User Info 👁️", callback_data='admin_view_user')],
        [InlineKeyboardButton("Back to Admin Menu ⬅️", callback_data='admin_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Admin User Management:\nChoose an option:", reply_markup=reply_markup)

async def admin_ban_user_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if not await is_admin(query.from_user.id): return
    await query.edit_message_text("Enter the User ID to ban:")
    return ADMIN_BAN_USER_ID

async def admin_ban_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id_str = update.message.text.strip()
    try:
        target_user_id = int(user_id_str)
        if target_user_id == update.message.from_user.id:
            await update.message.reply_text("You cannot ban yourself, Master!")
            return ConversationHandler.END
        
        profile = await get_user_profile(target_user_id, context)
        if profile.get('is_banned'):
            await update.message.reply_text(f"User `{target_user_id}` is already banned.")
        else:
            profile['is_banned'] = True
            await update_user_profile(target_user_id, 'is_banned', True)
            await update.message.reply_text(f"User `{target_user_id}` has been banned.")
            await send_private_message(target_user_id, "You have been banned from using this bot by an admin. Please contact support if you believe this is an error.")
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("Invalid User ID. Please enter a numeric ID.")
        return ADMIN_BAN_USER_ID

async def admin_unban_user_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if not await is_admin(query.from_user.id): return
    await query.edit_message_text("Enter the User ID to unban:")
    return ADMIN_UNBAN_USER_ID

async def admin_unban_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id_str = update.message.text.strip()
    try:
        target_user_id = int(user_id_str)
        profile = await get_user_profile(target_user_id, context)
        if not profile.get('is_banned'):
            await update.message.reply_text(f"User `{target_user_id}` is not currently banned.")
        else:
            profile['is_banned'] = False
            await update_user_profile(target_user_id, 'is_banned', False)
            await update.message.reply_text(f"User `{target_user_id}` has been unbanned.")
            await send_private_message(target_user_id, "You have been unbanned from using this bot. Welcome back!")
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("Invalid User ID. Please enter a numeric ID.")
        return ADMIN_UNBAN_USER_ID

async def admin_resolve_dispute_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if not await is_admin(query.from_user.id): return
    
    # List open disputes
    open_disputes = [d for d_id, d in disputes.items() if d['status'] == 'open']
    if not open_disputes:
        await query.edit_message_text("No open disputes to resolve.")
        return ConversationHandler.END

    response = "Open Disputes:\n\n"
    for d in open_disputes:
        response += (
            f"\\*\\*ID:\\*\\* `{d['dispute_id']}`\n"
            f"\\*\\*Trade ID:\\*\\* `{d['trade_id']}`\n"
            f"\\*\\*Raised by:\\*\\* `{d['raised_by']}`\n"
            f"\\*\\*Reason:\\*\\* `{d['reason'][:50]}...`\n"
            f"\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\n"
        )
    await query.edit_message_text(f"{response}\nPlease enter the Dispute ID you want to resolve:")
    return ADMIN_RESOLVE_DISPUTE_ID

async def admin_resolve_dispute_id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dispute_id = update.message.text.strip().upper()
    if dispute_id not in disputes or disputes[dispute_id]['status'] != 'open':
        await update.message.reply_text(f"Dispute ID `{dispute_id}` not found or not in 'open' status.")
        return ConversationHandler.END
    
    context.user_data['resolve_dispute_id'] = dispute_id
    keyboard = [
        [InlineKeyboardButton("Release Funds to Seller", callback_data='resolve_action_release')],
        [InlineKeyboardButton("Refund Funds to Buyer", callback_data='resolve_action_refund')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"Dispute `{dispute_id}` selected. What action should be taken?", reply_markup=reply_markup)
    return ADMIN_RESOLVE_DISPUTE_ACTION

async def admin_resolve_dispute_action_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    dispute_id = context.user_data.pop('resolve_dispute_id')
    action = query.data.replace('resolve_action_', '')
    
    dispute_data = disputes.get(dispute_id)
    if not dispute_data or dispute_data['status'] != 'open':
        await query.edit_message_text("Error: Dispute not found or not in 'open' status.")
        return ConversationHandler.END

    trade_id = dispute_data['trade_id']
    deal = active_deals.get(trade_id)

    if not deal or deal['status'] != 'deposited':
        await query.edit_message_text(f"Cannot resolve dispute `{dispute_id}`. Associated deal `{trade_id}` is not in 'deposited' status.")
        return ConversationHandler.END
    
    if action == 'release':
        # Simulate release
        if deal['seller_id']:
            seller_profile = await get_user_profile(deal['seller_id'], context)
            seller_profile['balance'] += deal['amount'] * (1 - deal['fee_percent'] / 100)
            await update_user_profile(deal['seller_id'], 'balance', seller_profile['balance'])

        deal['status'] = 'funds_released_by_admin'
        dispute_data['status'] = 'resolved_released'
        await query.edit_message_text(f"Dispute `{dispute_id}` resolved. Funds released to seller for Deal `{trade_id}`.")
        # Notify parties
        await send_private_message(deal['seller_id'], f"Admin resolved dispute for Deal `{trade_id}` in your favor. Funds released.")
        await send_private_message(deal['buyer_id'], f"Admin resolved dispute for Deal `{trade_id}`. Funds released to seller.")
    elif action == 'refund':
        # Simulate refund
        if deal['buyer_id']:
            buyer_profile = await get_user_profile(deal['buyer_id'], context)
            buyer_profile['balance'] += deal['amount']
            await update_user_profile(deal['buyer_id'], 'balance', buyer_profile['balance'])

        deal['status'] = 'refunded_by_admin'
        dispute_data['status'] = 'resolved_refunded'
        await query.edit_message_text(f"Dispute `{dispute_id}` resolved. Funds refunded to buyer for Deal `{trade_id}`.")
        # Notify parties
        await send_private_message(deal['buyer_id'], f"Admin resolved dispute for Deal `{trade_id}` in your favor. Funds refunded.")
        await send_private_message(deal['seller_id'], f"Admin resolved dispute for Deal `{trade_id}`. Funds refunded to buyer.")
    
    dispute_data['resolved_by_admin_id'] = query.from_user.id
    dispute_data['resolved_at'] = datetime.now()
    deal['dispute_status'] = 'resolved'
    # TODO: Save to DB

    return ConversationHandler.END

# --- Placeholder for many more features ---
async def admin_broadcast_message_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if not await is_admin(query.from_user.id): return
    await query.edit_message_text("Please type the message you want to broadcast to all active users:")
    return ADMIN_BROADCAST_MESSAGE

async def admin_broadcast_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    broadcast_text = update.message.text
    # TODO: Implement actual broadcast to all users in user_profiles
    success_count = 0
    fail_count = 0
    for user_id in user_profiles.keys():
        try:
            await send_private_message(user_id, f"📢 **Broadcast from Admin:**\n\n{broadcast_text}")
            success_count += 1
        except Exception:
            fail_count += 1
    await update.message.reply_text(f"Broadcast sent. Successful: {success_count}, Failed: {fail_count}.")
    return ConversationHandler.END

async def admin_system_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if not await is_admin(query.from_user.id): return
    
    # TODO: Fetch real-time system metrics, DB status, API statuses
    status_report = (
        "📊 **System Status Report (Conceptual)** 📊\n"
        f"Active Deals: {len(active_deals)}\n"
        f"Registered Users: {len(user_profiles)}\n"
        f"Open Disputes: {len([d for d_id, d in disputes.items() if d['status'] == 'open'])}\n"
        "Database Status: ✅ Connected\n"
        "Pyrogram Userbot: ✅ Active\n"
        "External APIs: (Crypto Price API) ✅, (KYC API) ❌ (conceptual error)\n"
        f"Memory Usage: {psutil.virtual_memory().percent}% (requires `psutil`)\n" # Requires `pip install psutil`
        f"CPU Usage: {psutil.cpu_percent()}% (requires `psutil`)\n"
        "Last Restart: (Bot startup time) (conceptual)\n"
    )
    try:
        import psutil
        await query.edit_message_text(status_report, parse_mode='MarkdownV2')
    except ImportError:
        await query.edit_message_text(f"{status_report}\n\n_Note: Install `psutil` for more detailed metrics._", parse_mode='MarkdownV2')

# Placeholder for additional features
async def admin_fee_mgmt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if not await is_admin(query.from_user.id): return
    await query.edit_message_text("Admin Fee Management: (TODO: Implement global fee settings, premium fee tiers, etc.)")

async def admin_channel_mgmt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if not await is_admin(query.from_user.id): return
    await query.edit_message_text("Admin Channel Management: (TODO: Link/unlink channels, manage bot permissions in channels, etc.)")

async def admin_schedule_post_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if not await is_admin(query.from_user.id): return
    await query.edit_message_text("Enter the target Channel ID (e.g., `-1001234567890`) for the post:")
    return CHANNEL_POST_CHANNEL_ID

async def admin_schedule_post_channel_id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    channel_id_str = update.message.text.strip()
    try:
        channel_id = int(channel_id_str)
        context.user_data['temp_channel_id'] = channel_id
        await update.message.reply_text("Now, send the content for the post (text, photo, or document):")
        return CHANNEL_POST_CONTENT
    except ValueError:
        await update.message.reply_text("Invalid Channel ID. Please enter a numeric ID (e.g., `-1001234567890`).")
        return CHANNEL_POST_CHANNEL_ID

async def admin_schedule_post_content_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    channel_id = context.user_data.pop('temp_channel_id')
    
    message_content = {}
    if update.message.text:
        message_content['text'] = update.message.text
    elif update.message.photo:
        message_content['photo_id'] = update.message.photo[-1].file_id
        message_content['caption'] = update.message.caption
    elif update.message.document:
        message_content['document_id'] = update.message.document.file_id
        message_content['caption'] = update.message.caption
    else:
        await update.message.reply_text("Unsupported content type. Please send text, a photo, or a document.")
        return CHANNEL_POST_CONTENT

    # TODO: Implement actual scheduling and sending via bot.send_message/send_photo/send_document
    # For now, immediate send
    try:
        if 'text' in message_content:
            await context.bot.send_message(chat_id=channel_id, text=message_content['text'], parse_mode='HTML')
        elif 'photo_id' in message_content:
            await context.bot.send_photo(chat_id=channel_id, photo=message_content['photo_id'], caption=message_content['caption'] or "")
        elif 'document_id' in message_content:
            await context.bot.send_document(chat_id=channel_id, document=message_content['document_id'], caption=message_content['caption'] or "")
        
        await update.message.reply_text(f"Post sent to channel `{channel_id}`. (TODO: Implement scheduling instead of immediate send)")
    except Exception as e:
        await update.message.reply_text(f"Failed to send post to channel `{channel_id}`: {e}")
        logging.error(f"Failed to send scheduled post: {e}")
    return ConversationHandler.END

async def otc_deal_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Starting a new OTC (Over-The-Counter) deal. Please provide the Telegram User ID of the other participant:")
    return OTC_PARTICIPANT_ID

async def otc_participant_id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        participant_id = int(update.message.text.strip())
        if participant_id == update.message.from_user.id:
            await update.message.reply_text("You cannot be both participants in an OTC deal. Please provide the ID of another user.")
            return OTC_PARTICIPANT_ID
        
        context.user_data['otc_participant_id'] = participant_id
        await update.message.reply_text(f"Other participant ID set to `{participant_id}`. Now, please describe the item/service for this OTC deal:")
        return DEAL_DESCRIPTION # Reusing deal description state
    except ValueError:
        await update.message.reply_text("Invalid User ID. Please enter a numeric ID.")
        return OTC_PARTICIPANT_ID

# (The flow for OTC deal then reuses DEAL_DESCRIPTION, DEAL_AMOUNT, DEAL_CONDITIONS and eventually leads to group creation.)

async def list_item_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("To list an item for sale in the marketplace, please provide the item's name:")
    return LIST_ITEM_NAME

async def list_item_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['listing_name'] = update.message.text
    await update.message.reply_text("Please provide a detailed description of the item:")
    return LIST_ITEM_DESC

async def list_item_desc_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['listing_desc'] = update.message.text
    await update.message.reply_text("What is the price of the item? (e.g., `100 USD` or `0.005 BTC`):")
    return LIST_ITEM_PRICE

async def list_item_price_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price_str = update.message.text.strip().split()
    if len(price_str) < 2:
        await update.message.reply_text("Invalid price format. Please include amount and currency (e.g., `100 USD`):")
        return LIST_ITEM_PRICE
    try:
        price_amount = float(price_str[0])
        price_currency = price_str[1].upper()
        context.user_data['listing_price_amount'] = price_amount
        context.user_data['listing_price_currency'] = price_currency
        await update.message.reply_text("Please specify the item's category (e.g., `Digital Goods`, `Physical Goods`, `Service`, `Crypto`):")
        return LIST_ITEM_CATEGORY
    except ValueError:
        await update.message.reply_text("Invalid price amount. Please enter a numeric value.")
        return LIST_ITEM_PRICE

async def list_item_category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['listing_category'] = update.message.text.strip()
    
    summary = (
        f"Item Listing Summary:\n"
        f"Name: {context.user_data['listing_name']}\n"
        f"Description: {context.user_data['listing_desc']}\n"
        f"Price: {context.user_data['listing_price_amount']} {context.user_data['listing_price_currency']}\n"
        f"Category: {context.user_data['listing_category']}\n\n"
        "Confirm listing this item? (yes/no)"
    )
    await update.message.reply_text(summary)
    return LIST_ITEM_CONFIRM

async def list_item_confirm_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = update.message.text.lower()
    if response == 'yes':
        item_id = await generate_trade_id("ITEM")
        listed_items[item_id] = {
            'item_id': item_id,
            'seller_id': update.message.from_user.id,
            'name': context.user_data['listing_name'],
            'description': context.user_data['listing_desc'],
            'price_amount': context.user_data['listing_price_amount'],
            'price_currency': context.user_data['listing_price_currency'],
            'category': context.user_data['listing_category'],
            'status': 'available',
            'listed_at': datetime.now()
        }
        await update.message.reply_text(f"Item `{context.user_data['listing_name']}` listed successfully with ID `{item_id}`. Others can now browse and buy it.")
        # TODO: Save to DB, notify marketplace users
    else:
        await update.message.reply_text("Item listing cancelled.")
    
    # Clear user_data for listing
    for key in ['listing_name', 'listing_desc', 'listing_price_amount', 'listing_price_currency', 'listing_category']:
        context.user_data.pop(key, None)
    return ConversationHandler.END

async def browse_items(update: Update, context: ContextTypes.DEFAULT_TYPE):
    available_items = [item for item_id, item in listed_items.items() if item['status'] == 'available']
    if not available_items:
        await update.message.reply_text("No items currently listed in the marketplace.")
        return
    
    response = "Items available in the Marketplace:\n\n"
    keyboard = []
    for item in available_items:
        response += (
            f"\\*\\*ID:\\*\\* `{item['item_id']}`\n"
            f"\\*\\*Name:\\*\\* `{item['name']}`\n"
            f"\\*\\*Price:\\*\\* `{item['price_amount']} {item['price_currency']}`\n"
            f"\\*\\*Category:\\*\\* `{item['category']}`\n"
            f"\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\n"
        )
        keyboard.append([InlineKeyboardButton(f"Buy {item['name']} ({item['item_id']})", callback_data=f"buy_item_{item['item_id']}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(response, reply_markup=reply_markup)

async def buy_item_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    item_id = query.data.replace('buy_item_', '')
    
    if item_id not in listed_items or listed_items[item_id]['status'] != 'available':
        await query.edit_message_text("This item is no longer available or does not exist.")
        return
    
    item = listed_items[item_id]
    buyer_id = query.from_user.id
    
    if item['seller_id'] == buyer_id:
        await query.edit_message_text("You cannot buy your own listed item.")
        return

    # Initiate a new escrow deal for this purchase
    trade_id = await generate_trade_id()
    active_deals[trade_id] = {
        'trade_id': trade_id,
        'creator_id': buyer_id, # Buyer initiates
        'type': 'marketplace_purchase',
        'description': f"Marketplace purchase: {item['name']}",
        'amount': item['price_amount'],
        'conditions': 'As per item description',
        'status': 'pending_marketplace_payment',
        'created_at': datetime.now(),
        'seller_id': item['seller_id'],
        'buyer_id': buyer_id,
        'seller_address': None, # Will be set by seller
        'buyer_address': None, # Will be set by buyer
        'escrow_address': None,
        'token': item['price_currency'],
        'fee_percent': 1.0, 
        'group_chat_id': None,
        'dispute_status': 'none',
        'linked_item_id': item_id
    }
    item['status'] = 'pending_sale' # Mark item as temporarily unavailable
    
    await query.edit_message_text(
        f"You are initiating a purchase for `{item['name']}` (ID: `{item_id}`).\n"
        f"A new escrow deal has been created with ID: `{trade_id}`.\n"
        f"Seller ({await context.bot.get_chat(item['seller_id']).full_name if await context.bot.get_chat(item['seller_id']) else item['seller_id']}) will be notified.\n\n"
        f"Seller needs to use `/seller <your_crypto_address> {trade_id}` and you need to use `/buyer <your_crypto_address> {trade_id}` to proceed with payment."
    )
    # Notify seller
    await send_private_message(item['seller_id'], 
                               f"Your item `{item['name']}` (ID: `{item_id}`) has a buyer ({query.from_user.full_name})! "
                               f"A new escrow deal has been initiated with ID: `{trade_id}` for `{item['price_amount']} {item['price_currency']}`. "
                               f"Please set your seller address using `/seller <your_crypto_address> {trade_id}` and await buyer's payment.")

async def rating_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("To give a rating, please provide the Trade ID for which you want to rate the other party:")
    # TODO: Lead to a conversation to select user, then give rating out of 5, with comments.

async def trusted_users_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Trusted Users Management: (TODO: Allow users to mark others as trusted for direct deals, or admins to assign 'trusted seller' badges)")
    # TODO: Add specific commands/flows for adding/removing trusted users

async def set_notifications(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This will typically lead to the settings_notifications menu
    await settings_notifications(update, context)

async def check_updates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Checking for bot updates... (TODO: Implement fetching latest version info or changelog)")
    await update.message.reply_text("You are currently running the latest version! (conceptual)")

async def api_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await admin_system_status(update, context) # Reusing admin system status for API checks

async def send_private_message(user_id: int, text: str, reply_markup=None):
    """Sends a private message to a user, handling potential errors."""
    try:
        await application.bot.send_message(user_id, text, reply_markup=reply_markup, parse_mode='MarkdownV2')
    except Exception as e:
        logging.warning(f"Failed to send message to user {user_id}: {e}")
        # TODO: Add logic to notify admin or original user if message failed to send.

# --- Main Application Setup ---
def main():
    global application # Make application accessible globally for send_private_message
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # --- Core Commands ---
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("escrow", escrow))
    application.add_handler(CommandHandler("commands", commands))
    application.add_handler(CommandHandler("whatisescrow", whatisescrow))
    application.add_handler(CommandHandler("instructions", instructions))
    application.add_handler(CommandHandler("terms", terms))
    application.add_handler(CommandHandler("contact", contact))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("vouch", vouch))
    application.add_handler(CommandHandler("mydeals", my_deals)) # New
    application.add_handler(CommandHandler("canceldeal", cancel_deal)) # New
    application.add_handler(CommandHandler("token", token)) # New
    application.add_handler(CommandHandler("balance", balance)) # New
    application.add_handler(CommandHandler("release", release)) # New
    application.add_handler(CommandHandler("refund", refund)) # New
    application.add_handler(CommandHandler("saved", saved)) # New
    application.add_handler(CommandHandler("referral", referral)) # New
    application.add_handler(CommandHandler("newdeal", newdeal)) # Unified new deal command

    # --- Commands with arguments (simple ones) ---
    application.add_handler(CommandHandler("seller", seller))
    application.add_handler(CommandHandler("buyer", buyer))
    application.add_handler(CommandHandler("setfee", setfee))
    application.add_handler(CommandHandler("tradeid", tradeid)) # Already there

    deal_details_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('dd', dd)],
    states={
        ConversationState.DEAL_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, deal_description)],
        ConversationState.DEAL_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, deal_amount_handler)],
        ConversationState.DEAL_CONDITIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, deal_conditions_handler)],
    },
    fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)]
)

    application.add_handler(deal_details_conv_handler)

    # New Deal Type Selection Conversation
    new_deal_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(new_deal_type_selection, pattern='^new_deal_')],
        states={DEAL_DESCRIPTION:[MessageHandler(filters.TEXT & ~filters.COMMAND, deal_description)],
            
            DEAL_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, deal_amount_handler)],
            DEAL_CONDITIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, deal_conditions_handler)]
        },
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)],
        map_to_parent={ConversationHandler.END: ConversationHandler.END} # Propagate end
    )
    application.add_handler(new_deal_conv_handler)
    
    # Save Address Conversation
    save_address_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('save', save_address_start)],
        states={
            SAVE_ADDRESS_CHAIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_address_chain)],
            SAVE_ADDRESS_DETAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_address_detail)],
        },
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)]
    )
    application.add_handler(save_address_conv_handler)

    # Verify Address Conversation
    verify_address_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('verify', verify)],
        states={
            VERIFY_ADDRESS_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, verify_address_input)],
        },
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)]
    )
    application.add_handler(verify_address_conv_handler)

    # Token Selection Conversation (if "Other" is selected)
    token_selection_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(token_selection_callback, pattern='^select_token_')],
        states={
            TOKEN_SELECTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, token_selection_trade_id_input)],
        },
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)],
        allow_reentry=True # Allow restarting if current_trade_id is missing
    )
    application.add_handler(token_selection_conv_handler)

    # Deposit Conversation
    deposit_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('deposit', deposit)],
        states={
            DEPOSIT_AMOUNT_SELECTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, deposit_amount_and_id_handler)],
        },
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)]
    )
    application.add_handler(deposit_conv_handler)

    # Dispute Conversation
    dispute_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('dispute', dispute_start)],
    states={
       DISPUTE_REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, dispute_reason_handler)],
        DISPUTE_PROOF: [MessageHandler(filters.PHOTO | filters.Document.ALL | (filters.TEXT & ~filters.COMMAND), dispute_proof_handler)],
    },
    fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)]
)
    application.add_handler(dispute_conv_handler)
    
    # Report Issue Conversation
    report_issue_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('report', report_issue_start)],
        states={
            REPORT_ISSUE_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, report_issue_type_handler)],
            REPORT_ISSUE_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, report_issue_details_handler)],
        },
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)]
    )
    application.add_handler(report_issue_conv_handler)

    # User Feedback Conversation
    feedback_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('feedback', feedback_start)],
        states={
            USER_FEEDBACK_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, user_feedback_handler)],
        },
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)]
    )
    application.add_handler(feedback_conv_handler)

    # KYC Verification Conversation
    kyc_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('kyc', kyc_start)],
        states={
            USER_KYC_DOC_TYPE: [CallbackQueryHandler(kyc_doc_type_selection, pattern='^kyc_doc_')],
            USER_KYC_DOC_UPLOAD: [MessageHandler(filters.PHOTO & ~filters.COMMAND, kyc_doc_upload_handler)],
        },
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)]
    )
    application.add_handler(kyc_conv_handler)

    # Admin Broadcast Conversation
    admin_broadcast_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(admin_broadcast_message_start, pattern='admin_broadcast_msg')],
        states={
            ADMIN_BROADCAST_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_broadcast_message_handler)],
        },
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)]
    )
    application.add_handler(admin_broadcast_conv_handler)

    # Admin Ban User Conversation
    admin_ban_user_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(admin_ban_user_start, pattern='admin_ban_user')],
        states={
            ADMIN_BAN_USER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_ban_user_handler)],
        },
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)]
    )
    application.add_handler(admin_ban_user_conv_handler)
    
    # Admin Unban User Conversation
    admin_unban_user_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(admin_unban_user_start, pattern='admin_unban_user')],
        states={
            ADMIN_UNBAN_USER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_unban_user_handler)],
        },
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)]
    )
    application.add_handler(admin_unban_user_conv_handler)

    # Admin Resolve Dispute Conversation
    admin_resolve_dispute_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(admin_resolve_dispute_start, pattern='admin_dispute_mgmt')],
        states={
            ADMIN_RESOLVE_DISPUTE_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_resolve_dispute_id_handler)],
            ADMIN_RESOLVE_DISPUTE_ACTION: [CallbackQueryHandler(admin_resolve_dispute_action_handler, pattern='^resolve_action_')],
        },
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)]
    )
    application.add_handler(admin_resolve_dispute_conv_handler)

    # Admin Schedule Post Conversation
    admin_schedule_post_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(admin_schedule_post_start, pattern='admin_schedule_post')],
        states={
            CHANNEL_POST_CHANNEL_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_schedule_post_channel_id_handler)],
           CHANNEL_POST_CONTENT: [MessageHandler(filters.TEXT | filters.PHOTO | filters.Document.ALL, admin_schedule_post_content_handler)],
        },
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)]
    )
    application.add_handler(admin_schedule_post_conv_handler)

    # OTC Deal Conversation (Entry point for `otc_deal` will direct to DEAL_DESCRIPTION state)
    otc_deal_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('otc_deal', otc_deal_start)],
        states={
            OTC_PARTICIPANT_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, otc_participant_id_handler)
            ],
            DEAL_DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, deal_description)
            ], # Re-use existing states
            DEAL_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, deal_amount_handler)
            ],
            DEAL_CONDITIONS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, deal_conditions_handler)
            ]
        },
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)]
    )
    application.add_handler(otc_deal_conv_handler)

    # List Item Conversation
    list_item_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('list_item', list_item_start)],
        states={
            LIST_ITEM_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, list_item_name_handler)],
            LIST_ITEM_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, list_item_desc_handler)],
            LIST_ITEM_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, list_item_price_handler)],
            LIST_ITEM_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, list_item_category_handler)],
            LIST_ITEM_CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, list_item_confirm_handler)],
        },
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)]
    )
    application.add_handler(list_item_conv_handler)

    # --- Callback Query Handlers (for inline buttons) ---
    application.add_handler(CallbackQueryHandler(escrow_type_selection, pattern='^escrow_'))
    application.add_handler(CallbackQueryHandler(menu, pattern='^menu$')) # Back to main menu
    application.add_handler(CallbackQueryHandler(commands, pattern='^commands$'))
    application.add_handler(CallbackQueryHandler(whatisescrow, pattern='^whatisescrow$'))
    application.add_handler(CallbackQueryHandler(instructions, pattern='^instructions$'))
    application.add_handler(CallbackQueryHandler(terms, pattern='^terms$'))
    application.add_handler(CallbackQueryHandler(dispute_start, pattern='^dispute_menu$'))
    application.add_handler(CallbackQueryHandler(contact, pattern='^contact$'))
    application.add_handler(CallbackQueryHandler(stats, pattern='^stats_menu$')) # Linked to new menu button
    application.add_handler(CallbackQueryHandler(newdeal, pattern='^new_deal_menu$')) # Linked to new menu button
    application.add_handler(CallbackQueryHandler(my_deals, pattern='^my_deals$')) # Linked to new menu button
    application.add_handler(CallbackQueryHandler(settings_menu, pattern='^settings_menu$'))
    application.add_handler(CallbackQueryHandler(settings_notifications, pattern='^settings_notifications$'))
    application.add_handler(CallbackQueryHandler(toggle_notification_callback, pattern='^toggle_notification_'))
    application.add_handler(CallbackQueryHandler(admin_menu, pattern='^admin_menu$'))
    application.add_handler(CallbackQueryHandler(admin_user_mgmt_menu, pattern='^admin_user_mgmt$'))
    application.add_handler(CallbackQueryHandler(admin_fee_mgmt, pattern='^admin_fee_mgmt$'))
    application.add_handler(CallbackQueryHandler(admin_channel_mgmt, pattern='^admin_channel_mgmt$'))
    application.add_handler(CallbackQueryHandler(admin_system_status, pattern='^admin_system_status$'))
    application.add_handler(CallbackQueryHandler(browse_items, pattern='^browse_items$')) # New feature
    application.add_handler(CallbackQueryHandler(buy_item_callback, pattern='^buy_item_')) # New feature

    # --- Other features as Command Handlers ---
    application.add_handler(CommandHandler('deposit', deposit_old_upi)) # Keep old deposit for UPI (as per old script)
    application.add_handler(CommandHandler('report', report_issue_start))
    application.add_handler(CommandHandler('feedback', feedback_start))
    application.add_handler(CommandHandler('kyc', kyc_start))
    application.add_handler(CommandHandler('premium', premium_info))
    application.add_handler(CommandHandler('browse_items', browse_items)) # Direct command for Browse
    application.add_handler(CommandHandler('rating', rating_start))
    application.add_handler(CommandHandler('trusted_users', trusted_users_menu))
    application.add_handler(CommandHandler('set_notifications', set_notifications))
    application.add_handler(CommandHandler('check_updates', check_updates))
    application.add_handler(CommandHandler('api_status', api_status))
    # ... Add handlers for all other 1000+ commands you might conceptualize ...
    
    # --- Chat Member Handler (for bot joining groups) ---
    application.add_handler(ChatMemberHandler(bot_joined, chat_member_types=["my_chat_member", "chat_member"]))

    logging.info("Bot is starting polling...")
    application.run_polling()

if __name__ == '__main__':
    # It's recommended to load sensitive info from environment variables
    # For local testing, you can uncomment these lines temporarily, but use .env in production
    # os.environ['BOT_TOKEN'] = 'YOUR_BOT_TOKEN_HERE' 
    # os.environ['USERBOT_PHONE_NUMBER'] = '+919315849892' 
    # os.environ['ADMIN_IDS'] = '6148819471' # Comma-separated if multiple admins

    main()
