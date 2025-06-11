import asyncio
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

user_predict_state = {}
user_dice_state = {}

def get_predict_keyboard(state, fast_mode=False, last_outcome=None):
    chosen = state.get('chosen', [])
    keyboard = [
        [
            InlineKeyboardButton(f"{'✅' if 1 in chosen else ''}1", callback_data="predict_num_1"),
            InlineKeyboardButton(f"{'✅' if 2 in chosen else ''}2", callback_data="predict_num_2"),
            InlineKeyboardButton(f"{'✅' if 3 in chosen else ''}3", callback_data="predict_num_3"),
            InlineKeyboardButton(f"{'✅' if 4 in chosen else ''}4", callback_data="predict_num_4"),
            InlineKeyboardButton(f"{'✅' if 5 in chosen else ''}5", callback_data="predict_num_5"),
            InlineKeyboardButton(f"{'✅' if 6 in chosen else ''}6", callback_data="predict_num_6"),
        ],
        [
            InlineKeyboardButton("1-3", callback_data="predict_range_1_3"),
            InlineKeyboardButton("4-6", callback_data="predict_range_4_6"),
        ],
        [
            InlineKeyboardButton("1-2", callback_data="predict_range_1_2"),
            InlineKeyboardButton("3-4", callback_data="predict_range_3_4"),
            InlineKeyboardButton("5-6", callback_data="predict_range_5_6"),
        ],
        [
            InlineKeyboardButton("ODD", callback_data="predict_odd"),
            InlineKeyboardButton("EVEN" + (" 🔄" if last_outcome == "EVEN" else ""), callback_data="predict_even"),
        ],
        [
            InlineKeyboardButton("Bet amount", callback_data="predict_bet_amount")
        ],
        [
            InlineKeyboardButton(f"Minimum amount is ₹0", callback_data="predict_min_amount")
        ]
    ]
    if fast_mode:
        keyboard.append([
            InlineKeyboardButton("⬅️ BACK", callback_data="predict_fastbet_off")
        ])
    else:
        keyboard.append([
            InlineKeyboardButton("Roll 🎲", callback_data="predict_roll")
        ])
        keyboard.append([
            InlineKeyboardButton("⬅️ BACK", callback_data="back_to_emoji_games")
        ])
    return InlineKeyboardMarkup(keyboard)

def format_outcome(chosen):
    if chosen == [1,2,3,4,5,6]:
        return "ANY"
    if chosen == [2,4,6]:
        return "EVEN"
    if chosen == [1,3,5]:
        return "ODD"
    if chosen == [1,2,3]:
        return "1-3"
    if chosen == [4,5,6]:
        return "4-6"
    if chosen == [1,2]:
        return "1-2"
    if chosen == [3,4]:
        return "3-4"
    if chosen == [5,6]:
        return "5-6"
    if len(chosen) == 1:
        return str(chosen[0])
    return ",".join(map(str, chosen))

def get_predict_text(state, fast_mode=False):
    chosen = sorted(state.get('chosen', []))
    bet = state.get('bet', 0.0)
    balance = state.get('balance', 0.0)
    if 'last_outcome' in state and state['last_outcome']:
        outcome = ','.join(map(str, state['last_outcome']))
        multiplier = state.get('last_multiplier', 0.0)
        won = state.get('last_win', False)
        win_amount = round(bet * multiplier, 2) if won else 0
        bet_text = f"₹{bet} → ₹{win_amount}"
    else:
        outcome = "—"
        multiplier = round(6 / len(chosen), 2) if chosen else "—"
        bet_text = f"₹{bet} → ₹—"
    if fast_mode:
        return (
            "🔮 <b>Predict</b>\n\n"
            "You can also <b>send many dice yourself</b>\n"
            "and get your <b>bets summary</b> at the end!\n\n"
            f"Outcome: <b>{format_outcome(chosen)}</b>\n"
            f"Multiplier: <b>{multiplier}x</b>\n"
            f"Bet amount: {bet_text}\n"
            f"Balance: ₹{balance}\n\n"
            "<b>Fast-bet mode ON</b>\n"
            "Any outcome clicked will place a bet.\n"
            "Click back to turn it off."
        )
    else:
        return (
            "🔮 <b>Predict</b>\n\n"
            "<i>Choose dice outcome, bet amount and try your luck!</i>\n\n"
            "You can <b>send many dice yourself</b> and get your <b>bets summary</b> at the end!\n\n"
            f"Outcome: {outcome}\n"
            f"Multiplier: {multiplier if multiplier != 0 else '—'}x\n"
            f"Bet amount: {bet_text}\n"
            f"Balance: ₹{balance}\n"
        )

def get_bet_summary_text(outcome_str, multiplier, bet):
    return (
        f"🔮 <b>Predict - Bet placed</b>\n\n"
        f"Outcome: <b>{outcome_str}</b>\n"
        f"Multiplier: <b>{multiplier}x</b>\n"
        f"Bet amount: ₹{bet} → ₹{bet if bet else 0}\n\n"
        "<i>Rolling...</i>"
    )

def get_dice_keyboard(state):
    game_types = [
        ("dice", "🎲"),
        ("bowling", "🎳"),
        ("dart", "🎯"),
        ("soccer", "⚽"),
        ("basket", "🏀"),
    ]
    selected_game = state.get("game", "dice")
    game_row = [
        InlineKeyboardButton(
            f"{emoji}{'✅' if selected_game == key else ''}",
            callback_data=f"dice_game_{key}"
        ) for key, emoji in game_types
    ]
    first_to = state.get("first_to", 3)
    first_to_row = [
        InlineKeyboardButton(
            f"{num}{'✅' if first_to == num else ''}",
            callback_data=f"dice_firstto_{num}"
        ) for num in range(1, 6)
    ]
    rolls = state.get("rolls", 1)
    rolls_row = [
        InlineKeyboardButton(
            f"{num}{'✅' if rolls == num else ''}",
            callback_data=f"dice_rolls_{num}"
        ) for num in range(1, 4)
    ]
    bet_row = [
        InlineKeyboardButton("₹0 - 100%", callback_data="dice_bet")
    ]
    play_btn = []
    if state.get("bet", 0) > 0:
        play_btn = [InlineKeyboardButton("Play 🎲", callback_data="dice_play")]
    return InlineKeyboardMarkup([
        game_row,
        first_to_row,
        rolls_row,
        bet_row,
        play_btn,
        [InlineKeyboardButton("Back", callback_data="back_to_emoji_games")]
    ])

def get_dice_text(state):
    balance = state.get("balance", 0.0)
    first_to = state.get("first_to", 3)
    rolls = state.get("rolls", 1)
    multiplier = 1.92
    win_chance = 50
    rounds_user = state.get("rounds_user", 0)
    rounds_bot = state.get("rounds_bot", 0)
    last_result = state.get("last_result", "")
    bet = state.get("bet", 0)
    game = state.get('game', 'dice')
    if game == "dart":
        title = "🎯 <b>Dart</b>"
        description = (
            "Match against the bot, 1 roll each, highest roll wins the round. First to reach 3 rounds wins the match.\n"
        )
    elif game == "bowling":
        title = "🎳 <b>Bowling</b>"
        description = (
            "Match against the bot, 1 roll each, highest roll wins the round. First to reach 3 rounds wins the match.\n"
        )
    elif game == "soccer":
        title = "⚽ <b>Soccer</b>"
        description = (
            "Match against the bot, 1 roll each, highest roll wins the round. First to reach 3 rounds wins the match.\n"
        )
    elif game == "basket":
        title = "🏀 <b>Basket</b>"
        description = (
            "Match against the bot, 1 roll each, highest roll wins the round. First to reach 3 rounds wins the match.\n"
        )
    else:
        title = "🎲 <b>Dice</b>"
        description = (
            "Match against the bot, 1 roll each, highest roll wins the round. First to reach 3 rounds wins the match.\n"
        )
    text = (
        f"{title}\n"
        f"{description}"
        f"Multiplier: <b>{multiplier}x</b>\n"
        f"Winning chance: {win_chance}%\n\n"
        f"Balance: ₹{balance}\n\n"
        f"<b>Game</b>: {state.get('game','dice').capitalize()}\n"
        f"<b>First to</b>: {first_to}\n"
        f"<b>Rolls count</b>: {rolls}\n"
        f"<b>Bet amount</b>: ₹{bet}\n"
    )
    if rounds_user or rounds_bot:
        text += f"\nYou: {rounds_user} | Bot: {rounds_bot}\n"
    if last_result:
        text += f"\n{last_result}\n"
    return text

def get_currency_keyboard(selected="INR"):
    currency_rows = [
        ["$", "€", "¥", "£"],
        ["CNY", "KRW", "INR", "CAD"],
        ["HKD", "BRL", "AUD", "TWD"],
        ["CHF", "RUB", "THB", "SAR"],
        ["AED", "PLN", "VND", "IDR"],
        ["SEK", "TRY", "PHP", "NOK"],
        ["CZK", "HUF", "UAH", "ARS"],
        ["BTC", "LTC", "TON", "ETH"],
        ["TRX", "SOL", "BNB", "XMR"],
        ["TRUMP", "XRP", "POL", "ARB"],
        ["AVAX", "SHIB", "PEPE", "DOGE"],
        ["KAS"]
    ]
    keyboard = []
    for row in currency_rows:
        row_buttons = []
        for code in row:
            display = f"{code}✅" if code == selected else code
            row_buttons.append(InlineKeyboardButton(display, callback_data=f"currency_{code}"))
        keyboard.append(row_buttons)
    keyboard.append([InlineKeyboardButton("⬅️ BACK", callback_data="settings_back")])
    return InlineKeyboardMarkup(keyboard)

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bal_predict = user_predict_state.get(user_id, {}).get("balance", 0.0)
    bal_dice = user_dice_state.get(user_id, {}).get("balance", 0.0)
    balance = max(bal_predict, bal_dice)
    await update.message.reply_text(
        f"💰 Your account balance:\n\n<b>₹{balance:.2f}</b>",
        parse_mode="HTML"
    )

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    privacy_state = context.user_data.get("privacy", True)
    privacy_text = "✅ Privacy" if privacy_state else "Privacy"
    settings_keyboard = [
        [
            InlineKeyboardButton("💱 Currency", callback_data="settings_currency"),
            InlineKeyboardButton(privacy_text, callback_data="settings_privacy")
        ],
        [
            InlineKeyboardButton("⬅️ BACK", callback_data="back_to_main")
        ]
    ]
    await update.message.reply_text(
        "⚙️ <b>Settings</b>",
        reply_markup=InlineKeyboardMarkup(settings_keyboard),
        parse_mode="HTML"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎁 Deposit gifts", callback_data="/depositgifts")],
        [InlineKeyboardButton("📈 Predictions", callback_data="/predictions"),
         InlineKeyboardButton("🚀 Crash", url="https://t.me/DenaroCasinoBot/crash")],
        [InlineKeyboardButton("👥 Join Group", callback_data="/joingroup")],
        [InlineKeyboardButton("🎱 Games", callback_data="/games")],
        [InlineKeyboardButton("📥 Deposit", callback_data="/deposit"),
         InlineKeyboardButton("📤 Withdraw", callback_data="/withdraw")],
        [InlineKeyboardButton("💰 Refer and Earn", callback_data="/refer")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="/settings")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome to Denaro Casino!\nSelect an option:",
        reply_markup=reply_markup
    )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    # --- Single Emoji Games ---
    if query.data == "single_emoji_games":
        await handle_single_emoji_games_menu(query)
        return
    for game in ["dice", "bowling", "dart", "soccer", "basket"]:
        if query.data == f"singleemoji_{game}":
            bet = single_emoji_bets.get((user_id, game), 10)
            await query.edit_message_text(
                get_single_emoji_game_text(game),
                reply_markup=get_single_emoji_game_keyboard(game, bet),
                parse_mode="HTML"
            )
            return
        if query.data.startswith(f"singleemoji_bet_{game}_"):
            bet = int(query.data.split("_")[-1])
            single_emoji_bets[(user_id, game)] = bet
            await query.edit_message_text(
                get_single_emoji_game_text(game),
                reply_markup=get_single_emoji_game_keyboard(game, bet),
                parse_mode="HTML"
            )
            return
        if query.data == f"singleemoji_play_{game}":
            bet = single_emoji_bets.get((user_id, game), 10)
            emoji_map = {
                "dice": "🎲",
                "bowling": "🎳",
                "dart": "🎯",
                "soccer": "⚽",
                "basket": "🏀",
            }
            emoji = emoji_map[game]
            await query.edit_message_text(
                f"{get_single_emoji_game_text(game)}\n\n<i>Rolling...</i>",
                reply_markup=get_single_emoji_game_keyboard(game, bet),
                parse_mode="HTML"
            )
            dice_msg = await context.bot.send_dice(chat_id=query.message.chat_id, emoji=emoji)
            await asyncio.sleep(4)
            rolled = dice_msg.dice.value
            win = rolled == 6
            balance = user_dice_state.get(user_id, {}).get("balance", 0.0)
            if win:
                balance += bet * 2
                result = f"🎉 <b>WIN!</b> You rolled <b>{rolled}</b> and won ₹{bet*2}!"
            else:
                balance -= bet
                result = f"❌ <b>LOSE!</b> You rolled <b>{rolled}</b> and lost ₹{bet}!"
            if user_id not in user_dice_state:
                user_dice_state[user_id] = {}
            user_dice_state[user_id]["balance"] = round(balance, 2)
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"{result}\n\nCurrent Balance: ₹{balance:.2f}",
                parse_mode="HTML"
            )
            return

    # --- Main Emoji Casino Games Menu ---
    if query.data == "emoji_casino":
        emoji_games_keyboard = [
            [InlineKeyboardButton("🔮 Predict", callback_data="predict")],
            [InlineKeyboardButton("🎲 Dice", callback_data="dice")],
            [
                InlineKeyboardButton("🎳 Bowling", callback_data="bowling"),
                InlineKeyboardButton("🎯 Dart", callback_data="dart")
            ],
            [
                InlineKeyboardButton("⚽ Soccer", callback_data="soccer"),
                InlineKeyboardButton("🏀 Basket", callback_data="basket")
            ],
            [InlineKeyboardButton("🎰 Single Emoji Games", callback_data="single_emoji_games")],
            [InlineKeyboardButton("⬅️ BACK", callback_data="back_to_games")]
        ]
        emoji_games_text = (
            "<b>Emoji Games</b>\n\n"
            "Choose between a variety of different games, all based on telegram-generated emojis!"
        )
        await query.edit_message_text(
            emoji_games_text,
            reply_markup=InlineKeyboardMarkup(emoji_games_keyboard),
            parse_mode="HTML"
        )
        return

    # --- Game State Setup for Dice, Bowling, Dart, Soccer, Basket ---
    if query.data in ["dart", "bowling", "soccer", "basket", "dice"]:
        user_dice_state[user_id] = {
            "game": query.data,
            "first_to": 3,
            "rolls": 1,
            "bet": 0,
            "balance": user_dice_state.get(user_id, {}).get("balance", 0.0),
            "rounds_user": 0,
            "rounds_bot": 0,
            "last_result": ""
        }
        await query.edit_message_text(
            get_dice_text(user_dice_state[user_id]),
            reply_markup=get_dice_keyboard(user_dice_state[user_id]),
            parse_mode="HTML"
        )
        return

    if query.data.startswith("dice_game_"):
        state = user_dice_state[user_id]
        state["game"] = query.data.replace("dice_game_", "")
        state["last_result"] = ""
        await query.edit_message_text(
            get_dice_text(state),
            reply_markup=get_dice_keyboard(state),
            parse_mode="HTML"
        )
        return

    if query.data.startswith("dice_firstto_"):
        state = user_dice_state[user_id]
        state["first_to"] = int(query.data.replace("dice_firstto_", ""))
        state["rounds_user"] = 0
        state["rounds_bot"] = 0
        state["last_result"] = ""
        await query.edit_message_text(
            get_dice_text(state),
            reply_markup=get_dice_keyboard(state),
            parse_mode="HTML"
        )
        return

    if query.data.startswith("dice_rolls_"):
        state = user_dice_state[user_id]
        state["rolls"] = int(query.data.replace("dice_rolls_", ""))
        state["last_result"] = ""
        await query.edit_message_text(
            get_dice_text(state),
            reply_markup=get_dice_keyboard(state),
            parse_mode="HTML"
        )
        return

    if query.data == "dice_bet":
        state = user_dice_state[user_id]
        bet = state.get("bet", 0)
        bet = {0:10, 10:50, 50:100, 100:0}.get(bet, 0)
        state["bet"] = bet
        state["last_result"] = ""
        await query.edit_message_text(
            get_dice_text(state),
            reply_markup=get_dice_keyboard(state),
            parse_mode="HTML"
        )
        return

    if query.data == "dice_play":
        state = user_dice_state[user_id]
        first_to = state.get("first_to", 3)
        rolls = state.get("rolls", 1)
        bet = state.get("bet", 0)
        if bet <= 0:
            await query.answer("Please set a bet amount greater than 0!", show_alert=True)
            return

        rounds_user = 0
        rounds_bot = 0
        emoji = {
            "dice": "🎲",
            "bowling": "🎳",
            "dart": "🎯",
            "soccer": "⚽",
            "basket": "🏀"
        }.get(state.get("game", "dice"), "🎲")

        await query.edit_message_text(
            f"{get_dice_text(state)}\n\n<b>Game starting...</b>",
            parse_mode="HTML"
        )

        while rounds_user < first_to and rounds_bot < first_to:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"Your turn ({emoji}):"
            )
            user_dice_msg = await context.bot.send_dice(chat_id=query.message.chat_id, emoji=emoji)
            await asyncio.sleep(4)
            user_roll_value = user_dice_msg.dice.value

            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"Bot's turn ({emoji}):"
            )
            bot_dice_msg = await context.bot.send_dice(chat_id=query.message.chat_id, emoji=emoji)
            await asyncio.sleep(4)
            bot_roll_value = bot_dice_msg.dice.value

            round_winner = ""
            if user_roll_value > bot_roll_value:
                rounds_user += 1
                round_winner = "You win this round!"
            elif bot_roll_value > user_roll_value:
                rounds_bot += 1
                round_winner = "Bot wins this round!"
            else:
                round_winner = "It's a draw for this round!"

            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=(
                    f"Round Result:\n"
                    f"You rolled: `{user_roll_value}`\n"
                    f"Bot rolled: `{bot_roll_value}`\n"
                    f"<b>{round_winner}</b>\n"
                    f"Current Score: You {rounds_user} | Bot {rounds_bot}"
                ),
                parse_mode="HTML"
            )
            await asyncio.sleep(1)

        state["rounds_user"] = rounds_user
        state["rounds_bot"] = rounds_bot

        final_result_text = ""
        if rounds_user >= first_to:
            win_amount = round(bet * 1.92, 2)
            final_result_text = f"🎉 You win the match! (+₹{win_amount:.2f})"
            state["balance"] = round(state.get("balance", 0.0) + win_amount, 2)
        elif rounds_bot >= first_to:
            loss_amount = round(bet, 2)
            final_result_text = f"😭 Bot wins the match! (-₹{loss_amount:.2f})"
            state["balance"] = round(state.get("balance", 0.0) - loss_amount, 2)
        else:
            final_result_text = "It's a rare full match draw!"

        state["last_result"] = final_result_text

        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"<b>Game Over!</b>\n{final_result_text}",
            parse_mode="HTML"
        )

        await query.edit_message_text(
            get_dice_text(state),
            reply_markup=get_dice_keyboard(state),
            parse_mode="HTML"
        )
        state["rounds_user"] = 0
        state["rounds_bot"] = 0
        return

    # --- Menu Navigation and Settings ---
    if query.data == "back_to_emoji_games":
        emoji_games_keyboard = [
            [InlineKeyboardButton("🔮 Predict", callback_data="predict")],
            [InlineKeyboardButton("🎲 Dice", callback_data="dice")],
            [
                InlineKeyboardButton("🎳 Bowling", callback_data="bowling"),
                InlineKeyboardButton("🎯 Dart", callback_data="dart")
            ],
            [
                InlineKeyboardButton("⚽ Soccer", callback_data="soccer"),
                InlineKeyboardButton("🏀 Basket", callback_data="basket")
            ],
            [InlineKeyboardButton("🎰 Single Emoji Games", callback_data="single_emoji_games")],
            [InlineKeyboardButton("⬅️ BACK", callback_data="back_to_games")]
        ]
        emoji_games_text = (
            "<b>Emoji Games</b>\n\n"
            "Choose between a variety of different games, all based on telegram-generated emojis!"
        )
        await query.edit_message_text(
            emoji_games_text,
            reply_markup=InlineKeyboardMarkup(emoji_games_keyboard),
            parse_mode="HTML"
        )
        return

    if query.data == "back_to_games":
        games_keyboard = [
            [
                InlineKeyboardButton("🎲 Emojis Casino", callback_data="emoji_casino"),
                InlineKeyboardButton("💣 Regular Games", callback_data="regular_games"),
            ],
            [
                InlineKeyboardButton("⬅️ BACK", callback_data="back_to_main")
            ]
        ]
        games_text = (
            "<b>Games</b>\n\n"
            "Choose between emojis-based games and regular ones, all provably fair!"
        )
        await query.edit_message_text(
            games_text,
            reply_markup=InlineKeyboardMarkup(games_keyboard),
            parse_mode="HTML"
        )
        return

    if query.data == "back_to_main":
        await start(update, context)
        return

    # --- Settings and Currency ---
    if query.data == "/settings":
        privacy_state = context.user_data.get("privacy", True)
        privacy_text = "✅ Privacy" if privacy_state else "Privacy"
        settings_keyboard = [
            [
                InlineKeyboardButton("💱 Currency", callback_data="settings_currency"),
                InlineKeyboardButton(privacy_text, callback_data="settings_privacy")
            ],
            [
                InlineKeyboardButton("⬅️ BACK", callback_data="back_to_main")
            ]
        ]
        await query.edit_message_text(
            "⚙️ <b>Settings</b>",
            reply_markup=InlineKeyboardMarkup(settings_keyboard),
            parse_mode="HTML"
        )
        return

    if query.data == "settings_currency":
        current_currency = context.user_data.get("currency", "INR")
        await query.edit_message_text(
            "💱 <b>Currency</b>",
            reply_markup=get_currency_keyboard(selected=current_currency),
            parse_mode="HTML"
        )
        return

    if query.data.startswith("currency_"):
        selected_currency = query.data.replace("currency_", "")
        context.user_data["currency"] = selected_currency
        await query.edit_message_text(
            "💱 <b>Currency</b>",
            reply_markup=get_currency_keyboard(selected=selected_currency),
            parse_mode="HTML"
        )
        return

    if query.data == "settings_back":
        privacy_state = context.user_data.get("privacy", True)
        privacy_text = "✅ Privacy" if privacy_state else "Privacy"
        settings_keyboard = [
            [
                InlineKeyboardButton("💱 Currency", callback_data="settings_currency"),
                InlineKeyboardButton(privacy_text, callback_data="settings_privacy")
            ],
            [
                InlineKeyboardButton("⬅️ BACK", callback_data="back_to_main")
            ]
        ]
        await query.edit_message_text(
            "⚙️ <b>Settings</b>",
            reply_markup=InlineKeyboardMarkup(settings_keyboard),
            parse_mode="HTML"
        )
        return

    if query.data == "settings_privacy":
        current = context.user_data.get("privacy", True)
        context.user_data["privacy"] = not current
        privacy_text = "✅ Privacy" if not current else "Privacy"
        settings_keyboard = [
            [
                InlineKeyboardButton("💱 Currency", callback_data="settings_currency"),
                InlineKeyboardButton(privacy_text, callback_data="settings_privacy")
            ],
            [
                InlineKeyboardButton("⬅️ BACK", callback_data="back_to_main")
            ]
        ]
        await query.edit_message_text(
            "⚙️ <b>Settings</b>",
            reply_markup=InlineKeyboardMarkup(settings_keyboard),
            parse_mode="HTML"
        )
        return

    # --- Predict Game, Menus, and Other Features ---
    # [Insert all the rest of your predict, menu, and game logic as in your previous handle_button here]

    # --- Fallback: Show the raw callback data ---
    await query.edit_message_text(f"{query.data}")
    if query.data == "/settings":
        privacy_state = context.user_data.get("privacy", True)
        privacy_text = "✅ Privacy" if privacy_state else "Privacy"
        settings_keyboard = [
            [
                InlineKeyboardButton("💱 Currency", callback_data="settings_currency"),
                InlineKeyboardButton(privacy_text, callback_data="settings_privacy")
            ],
            [
                InlineKeyboardButton("⬅️ BACK", callback_data="back_to_main")
            ]
        ]
        await query.edit_message_text(
            "⚙️ <b>Settings</b>",
            reply_markup=InlineKeyboardMarkup(settings_keyboard),
            parse_mode="HTML"
        )
    elif query.data == "settings_currency":
        current_currency = context.user_data.get("currency", "INR")
        await query.edit_message_text(
            "💱 <b>Currency</b>",
            reply_markup=get_currency_keyboard(selected=current_currency),
            parse_mode="HTML"
        )
    elif query.data.startswith("currency_"):
        selected_currency = query.data.replace("currency_", "")
        context.user_data["currency"] = selected_currency
        await query.edit_message_text(
            "💱 <b>Currency</b>",
            reply_markup=get_currency_keyboard(selected=selected_currency),
            parse_mode="HTML"
        )
    elif query.data == "settings_back":
        privacy_state = context.user_data.get("privacy", True)
        privacy_text = "✅ Privacy" if privacy_state else "Privacy"
        settings_keyboard = [
            [
                InlineKeyboardButton("💱 Currency", callback_data="settings_currency"),
                InlineKeyboardButton(privacy_text, callback_data="settings_privacy")
            ],
            [
                InlineKeyboardButton("⬅️ BACK", callback_data="back_to_main")
            ]
        ]
        await query.edit_message_text(
            "⚙️ <b>Settings</b>",
            reply_markup=InlineKeyboardMarkup(settings_keyboard),
            parse_mode="HTML"
        )
    elif query.data == "settings_privacy":
        current = context.user_data.get("privacy", True)
        context.user_data["privacy"] = not current
        privacy_text = "✅ Privacy" if not current else "Privacy"
        settings_keyboard = [
            [
                InlineKeyboardButton("💱 Currency", callback_data="settings_currency"),
                InlineKeyboardButton(privacy_text, callback_data="settings_privacy")
            ],
            [
                InlineKeyboardButton("⬅️ BACK", callback_data="back_to_main")
            ]
        ]
        await query.edit_message_text(
            "⚙️ <b>Settings</b>",
            reply_markup=InlineKeyboardMarkup(settings_keyboard),
            parse_mode="HTML"
        )
    elif query.data == "predict":
        user_predict_state[user_id] = {
            "chosen": [],
            "bet": 0.0,
            "balance": 0.0,
            "last_outcome": [],
            "last_multiplier": 0.0,
            "last_win": False,
            "fast_mode": False
        }
        await query.edit_message_text(
            get_predict_text(user_predict_state[user_id]),
            reply_markup=get_predict_keyboard(user_predict_state[user_id]),
            parse_mode="HTML"
        )
    elif query.data.startswith("predict_num_"):
        number = int(query.data.split("_")[-1])
        state = user_predict_state[user_id]
        chosen = set(state.get('chosen', []))
        if number in chosen:
            chosen.remove(number)
        else:
            chosen.add(number)
        state["chosen"] = sorted(list(chosen))
        state["last_outcome"] = []
        await query.edit_message_text(
            get_predict_text(state, fast_mode=state.get('fast_mode', False)),
            reply_markup=get_predict_keyboard(state, fast_mode=state.get('fast_mode', False)),
            parse_mode="HTML"
        )
    elif query.data.startswith("predict_range_"):
        _, _, a, b = query.data.split("_")
        a, b = int(a), int(b)
        state = user_predict_state[user_id]
        state["chosen"] = list(range(a, b+1))
        state["last_outcome"] = []
        await query.edit_message_text(
            get_predict_text(state, fast_mode=state.get('fast_mode', False)),
            reply_markup=get_predict_keyboard(state, fast_mode=state.get('fast_mode', False)),
            parse_mode="HTML"
        )
    elif query.data == "predict_odd":
        state = user_predict_state[user_id]
        state["chosen"] = [1,3,5]
        state["last_outcome"] = []
        await query.edit_message_text(
            get_predict_text(state, fast_mode=state.get('fast_mode', False)),
            reply_markup=get_predict_keyboard(state, fast_mode=state.get('fast_mode', False), last_outcome="ODD"),
            parse_mode="HTML"
        )
    elif query.data == "predict_even":
        state = user_predict_state[user_id]
        state["chosen"] = [2,4,6]
        state["last_outcome"] = []
        await query.edit_message_text(
            get_predict_text(state, fast_mode=state.get('fast_mode', False)),
            reply_markup=get_predict_keyboard(state, fast_mode=state.get('fast_mode', False), last_outcome="EVEN"),
            parse_mode="HTML"
        )
    elif query.data == "predict_bet_amount":
        state = user_predict_state[user_id]
        bet = state['bet']
        next_bet = 0 if bet >= 100 else {0: 10, 10: 50, 50: 100}.get(bet, 0)
        state['bet'] = next_bet
        state["last_outcome"] = []
        await query.edit_message_text(
            get_predict_text(state, fast_mode=state.get('fast_mode', False)),
            reply_markup=get_predict_keyboard(state, fast_mode=state.get('fast_mode', False)),
            parse_mode="HTML"
        )
    elif query.data == "predict_min_amount":
        await query.answer("Minimum bet amount is ₹0", show_alert=True)
    elif query.data == "predict_roll":
        state = user_predict_state[user_id]
        chosen = sorted(state.get('chosen', []))
        bet = state.get('bet', 0.0)
        if not chosen or bet < 0:
            await query.answer("Please choose at least one number and set minimum bet!", show_alert=True)
            return
        multiplier = round(6 / len(chosen), 2)
        outcome_str = format_outcome(chosen)
        await query.edit_message_text(
            get_bet_summary_text(outcome_str, multiplier, bet),
            parse_mode="HTML"
        )
        dice_msg = await context.bot.send_dice(chat_id=query.message.chat_id, emoji="🎲")
        await asyncio.sleep(4)
        rolled = dice_msg.dice.value
        win = rolled in chosen
        state["last_outcome"] = [rolled]
        state["last_multiplier"] = multiplier
        state["last_win"] = win
        if win:
            state["balance"] = round(state.get("balance", 0.0) + bet*multiplier, 2)
        else:
            state["balance"] = round(state.get("balance", 0.0) - bet, 2)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=(
                "🔮 <b>Predict</b>\n\n"
                "You can also <b>send many dice yourself</b>\n"
                "and get your <b>bets summary</b> at the end!\n\n"
                f"Outcome: <b>{format_outcome(chosen)}</b>\n"
                f"Multiplier: <b>{multiplier}x</b>\n"
                f"Bet amount: ₹{bet} → ₹{round(bet*multiplier) if win else 0}\n"
                f"Balance: ₹{state['balance']}\n"
                f"🎲 <b>Rolled value:</b> <code>{rolled}</code>\n\n"
                "<b>Fast-bet mode ON</b>\n"
                "Any outcome clicked will place a bet.\n"
                "Click back to turn it off."
            ),
            parse_mode="HTML",
            reply_markup=get_predict_keyboard(state, fast_mode=True, last_outcome=outcome_str)
        )
        state["fast_mode"] = True
    elif query.data == "predict_fastbet_off":
        state = user_predict_state[user_id]
        state["fast_mode"] = False
        state["last_outcome"] = []
        await query.edit_message_text(
            get_predict_text(state, fast_mode=False),
            reply_markup=get_predict_keyboard(state, fast_mode=False),
            parse_mode="HTML"
        )
    elif query.data == "/depositgifts":
        msg = (
            "Gifts Deposit\n\n"
            "Transfer the gift to @liesence and the deposit amount will be automatically credited to your balance!\n"
            "Gifts bought with stars are not accepted.\n\n"
            "You will also be able to buy your gift back for a small fee."
        )
        await query.edit_message_text(msg)
    elif query.data == "/predictions":
        prediction_keyboard = [
            [InlineKeyboardButton("UEFA Nations League: Germany vs. Portugal", callback_data="pred_1")],
            [InlineKeyboardButton("UEFA Nations League: Spain vs. France", callback_data="pred_2")],
            [InlineKeyboardButton("UEFA Nations League Winner", callback_data="pred_3")],
            [InlineKeyboardButton("NBA Champion", callback_data="pred_4")],
            [InlineKeyboardButton("XRP all time high by when?", callback_data="pred_5")],
            [InlineKeyboardButton("Ethereum all time high by June 30?", callback_data="pred_6")],
            [InlineKeyboardButton("Russia x Ukraine ceasefire before July?", callback_data="pred_7")],
            [InlineKeyboardButton("Zelenskyy out as Ukraine president before...", callback_data="pred_8")],
            [InlineKeyboardButton("Israel x Hamas ceasefire before July?", callback_data="pred_9")],
            [InlineKeyboardButton("Litecoin ETF approved by July 31?", callback_data="pred_10")],
            [InlineKeyboardButton("Will Trump impose large tariffs in his first 6...", callback_data="pred_11")],
            [InlineKeyboardButton("Ballon d'Or Winner 2025", callback_data="pred_12")],
            [InlineKeyboardButton("World Series Champion 2025", callback_data="pred_13")],
            [InlineKeyboardButton("F1 Drivers Champion", callback_data="pred_14")],
            [InlineKeyboardButton("F1 Constructors Champion", callback_data="pred_15")],
            [InlineKeyboardButton("US recognizes Russian sovereignty over U...", callback_data="pred_16")],
            [InlineKeyboardButton("Litecoin ETF approved in 2025?", callback_data="pred_17")],
            [InlineKeyboardButton("What price will Ethereum hit in 2025?", callback_data="pred_18")],
            [InlineKeyboardButton("What price will Bitcoin hit in 2025?", callback_data="pred_19")],
            [InlineKeyboardButton("Ukraine agrees not to join NATO in 2025?", callback_data="pred_20")],
            [InlineKeyboardButton("Will SOL flip ETH in 2025?", callback_data="pred_21")],
            [InlineKeyboardButton("Will the U.S. take over Gaza in 2025?", callback_data="pred_22")],
            [InlineKeyboardButton("Highest grossing movie in 2025?", callback_data="pred_23")],
            [InlineKeyboardButton("Russia x Ukraine ceasefire in 2025?", callback_data="pred_24")],
            [InlineKeyboardButton("Will Trump acquire Greenland in 2025?", callback_data="pred_25")],
        ]
        prediction_markup = InlineKeyboardMarkup(prediction_keyboard)
        await query.edit_message_text(
            "📉 Prediction betting\nSelect from the predictions below:",
            reply_markup=prediction_markup
        )
    elif query.data == "/games":
        games_keyboard = [
            [
                InlineKeyboardButton("🎲 Emojis Casino", callback_data="emoji_casino"),
                InlineKeyboardButton("💣 Regular Games", callback_data="regular_games"),
            ],
            [
                InlineKeyboardButton("⬅️ BACK", callback_data="back_to_main")
            ]
        ]
        games_text = (
            "<b>Games</b>\n\n"
            "Choose between emojis-based games and regular ones, all provably fair!"
        )
        await query.edit_message_text(
            games_text,
            reply_markup=InlineKeyboardMarkup(games_keyboard),
            parse_mode="HTML"
        )
    elif query.data == "emoji_casino":
        emoji_games_keyboard = [
            [InlineKeyboardButton("🔮 Predict", callback_data="predict")],
            [InlineKeyboardButton("🎲 Dice", callback_data="dice")],
            [
                InlineKeyboardButton("🎳 Bowling", callback_data="bowling"),
                InlineKeyboardButton("🎯 Dart", callback_data="dart")
            ],
            [
                InlineKeyboardButton("⚽ Soccer", callback_data="soccer"),
                InlineKeyboardButton("🏀 Basket", callback_data="basket")
            ],
            [InlineKeyboardButton("🎰 Single Emoji Games", callback_data="single_emoji_games")],
            [InlineKeyboardButton("⬅️ BACK", callback_data="back_to_games")]
        ]
        emoji_games_text = (
            "<b>Emoji Games</b>\n\n"
            "Choose between a variety of different games, all based on telegram-generated emojis!"
        )
        await query.edit_message_text(
            emoji_games_text,
            reply_markup=InlineKeyboardMarkup(emoji_games_keyboard),
            parse_mode="HTML"
        )
    elif query.data == "dart":
        user_dice_state[user_id] = {
            "game": "dart",
            "first_to": 3,
            "rolls": 1,
            "bet": 0,
            "balance": 0.0,
            "rounds_user": 0,
            "rounds_bot": 0,
            "last_result": ""
        }
        await query.edit_message_text(
            get_dice_text(user_dice_state[user_id]),
            reply_markup=get_dice_keyboard(user_dice_state[user_id]),
            parse_mode="HTML"
        )
    elif query.data == "dice":
        user_dice_state[user_id] = {
            "game": "dice",
            "first_to": 3,
            "rolls": 1,
            "bet": 0,
            "balance": 0.0,
            "rounds_user": 0,
            "rounds_bot": 0,
            "last_result": ""
        }
        await query.edit_message_text(
            get_dice_text(user_dice_state[user_id]),
            reply_markup=get_dice_keyboard(user_dice_state[user_id]),
            parse_mode="HTML"
        )
    elif query.data.startswith("dice_game_"):
        state = user_dice_state[user_id]
        state["game"] = query.data.replace("dice_game_", "")
        state["last_result"] = ""
        await query.edit_message_text(
            get_dice_text(state),
            reply_markup=get_dice_keyboard(state),
            parse_mode="HTML"
        )
    elif query.data.startswith("dice_firstto_"):
        state = user_dice_state[user_id]
        state["first_to"] = int(query.data.replace("dice_firstto_", ""))
        state["rounds_user"] = 0
        state["rounds_bot"] = 0
        state["last_result"] = ""
        await query.edit_message_text(
            get_dice_text(state),
            reply_markup=get_dice_keyboard(state),
            parse_mode="HTML"
        )
    elif query.data.startswith("dice_rolls_"):
        state = user_dice_state[user_id]
        state["rolls"] = int(query.data.replace("dice_rolls_", ""))
        state["last_result"] = ""
        await query.edit_message_text(
            get_dice_text(state),
            reply_markup=get_dice_keyboard(state),
            parse_mode="HTML"
        )
    elif query.data == "dice_bet":
        state = user_dice_state[user_id]
        bet = state.get("bet", 0)
        bet = {0:10, 10:50, 50:100, 100:0}.get(bet, 0)
        state["bet"] = bet
        state["last_result"] = ""
        await query.edit_message_text(
            get_dice_text(state),
            reply_markup=get_dice_keyboard(state),
            parse_mode="HTML"
        )
    elif query.data == "dice_play":
        state = user_dice_state[user_id]
        first_to = state.get("first_to", 3)
        rolls = state.get("rolls", 1)
        bet = state.get("bet", 0)
        user_score = 0
        bot_score = 0
        rounds_user = 0
        rounds_bot = 0
        last_result = ""
        # Use emoji for the current game
        emoji = {
            "dice": "🎲",
            "bowling": "🎳",
            "dart": "🎯",
            "soccer": "⚽",
            "basket": "🏀"
        }.get(state.get("game", "dice"), "🎲")
        while rounds_user < first_to and rounds_bot < first_to:
            # In real bot, you'd use context.bot.send_dice(emoji=emoji) for real randomness
            # For simulation, we just use random.randint as before
            user_total = sum(random.randint(1, 6) for _ in range(rolls))
            bot_total = sum(random.randint(1, 6) for _ in range(rolls))
            if user_total > bot_total:
                rounds_user += 1
            elif bot_total > user_total:
                rounds_bot += 1
        state["rounds_user"] = rounds_user
        state["rounds_bot"] = rounds_bot
        if rounds_user > rounds_bot:
            last_result = f"You win the match! (+₹{bet*1.92:.2f})"
            state["balance"] = round(state.get("balance", 0.0) + bet*1.92, 2)
        elif rounds_bot > rounds_user:
            last_result = f"Bot wins the match! (-₹{bet:.2f})"
            state["balance"] = round(state.get("balance", 0.0) - bet, 2)
        else:
            last_result = "Match draw! No balance change."
        state["last_result"] = last_result
        await query.edit_message_text(
            get_dice_text(state),
            reply_markup=get_dice_keyboard(state),
            parse_mode="HTML"
        )
    elif query.data == "back_to_emoji_games":
        emoji_games_keyboard = [
            [InlineKeyboardButton("🔮 Predict", callback_data="predict")],
            [InlineKeyboardButton("🎲 Dice", callback_data="dice")],
            [
                InlineKeyboardButton("🎳 Bowling", callback_data="bowling"),
                InlineKeyboardButton("🎯 Dart", callback_data="dart")
            ],
            [
                InlineKeyboardButton("⚽ Soccer", callback_data="soccer"),
                InlineKeyboardButton("🏀 Basket", callback_data="basket")
            ],
            [InlineKeyboardButton("🎰 Single Emoji Games", callback_data="single_emoji_games")],
            [InlineKeyboardButton("⬅️ BACK", callback_data="back_to_games")]
        ]
        emoji_games_text = (
            "<b>Emoji Games</b>\n\n"
            "Choose between a variety of different games, all based on telegram-generated emojis!"
        )
        await query.edit_message_text(
            emoji_games_text,
            reply_markup=InlineKeyboardMarkup(emoji_games_keyboard),
            parse_mode="HTML"
        )
    elif query.data == "back_to_games":
        games_keyboard = [
            [
                InlineKeyboardButton("🎲 Emojis Casino", callback_data="emoji_casino"),
                InlineKeyboardButton("💣 Regular Games", callback_data="regular_games"),
            ],
            [
                InlineKeyboardButton("⬅️ BACK", callback_data="back_to_main")
            ]
        ]
        games_text = (
            "<b>Games</b>\n\n"
            "Choose between emojis-based games and regular ones, all provably fair!"
        )
        await query.edit_message_text(
            games_text,
            reply_markup=InlineKeyboardMarkup(games_keyboard),
            parse_mode="HTML"
        )
    elif query.data == "back_to_main":
        await start(update, context)
    else:
        await query.edit_message_text(f"{query.data}")

def main():
    app = ApplicationBuilder().token('7607175238:AAEu7eI38N53gj8HkjKoUYlpuaKN4moUs3E').build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bal", balance))
    app.add_handler(CommandHandler("settings", settings))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(CallbackQueryHandler(handle_button))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

single_emoji_bets = {}

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    # --- Single Emoji Games ---
    for game in ["dice", "bowling", "dart", "soccer", "basket"]:
        if query.data == f"singleemoji_{game}":
            bet = single_emoji_bets.get((user_id, game), 10)
            await query.edit_message_text(
                get_single_emoji_game_text(game),
                reply_markup=get_single_emoji_game_keyboard(game, bet),
                parse_mode="HTML"
            )
            return
        if query.data.startswith(f"singleemoji_bet_{game}_"):
            bet = int(query.data.split("_")[-1])
            single_emoji_bets[(user_id, game)] = bet
            await query.edit_message_text(
                get_single_emoji_game_text(game),
                reply_markup=get_single_emoji_game_keyboard(game, bet),
                parse_mode="HTML"
            )
            return
        if query.data == f"singleemoji_play_{game}":
            bet = single_emoji_bets.get((user_id, game), 10)
            emoji_map = {
                "dice": "🎲",
                "bowling": "🎳",
                "dart": "🎯",
                "soccer": "⚽",
                "basket": "🏀",
            }
            emoji = emoji_map[game]
            await query.edit_message_text(
                f"{get_single_emoji_game_text(game)}\n\n<i>Rolling...</i>",
                reply_markup=get_single_emoji_game_keyboard(game, bet),
                parse_mode="HTML"
            )
            dice_msg = await context.bot.send_dice(chat_id=query.message.chat_id, emoji=emoji)
            await asyncio.sleep(4)
            rolled = dice_msg.dice.value
            win = rolled == 6
            balance = user_dice_state.get(user_id, {}).get("balance", 0.0)
            if win:
                balance += bet * 2
                result = f"🎉 <b>WIN!</b> You rolled <b>{rolled}</b> and won ₹{bet*2}!"
            else:
                balance -= bet
                result = f"❌ <b>LOSE!</b> You rolled <b>{rolled}</b> and lost ₹{bet}!"
            if user_id not in user_dice_state:
                user_dice_state[user_id] = {}
            user_dice_state[user_id]["balance"] = round(balance, 2)
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"{result}\n\nCurrent Balance: ₹{balance:.2f}",
                parse_mode="HTML"
            )
            return

def get_single_emoji_game_text(game):
    return f"Single Emoji Game: {game}"

def get_single_emoji_game_keyboard(game, bet):
    keyboard = [
        [InlineKeyboardButton(f"Bet: {bet}", callback_data=f"singleemoji_bet_{game}_{bet}")],
        [InlineKeyboardButton("Play", callback_data=f"singleemoji_play_{game}")],
    ]
    return InlineKeyboardMarkup(keyboard)
