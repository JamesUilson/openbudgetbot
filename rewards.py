import json
import os

REWARDS_FILE = "data/rewards.json"


def load_rewards():
    if not os.path.exists(REWARDS_FILE):
        return {}
    with open(REWARDS_FILE, "r", encoding="utf-8") as f:
        try:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
        except json.JSONDecodeError:
            return {}


def save_rewards(rewards):
    with open(REWARDS_FILE, "w", encoding="utf-8") as f:
        json.dump(rewards, f, indent=4, ensure_ascii=False)


def give_reward(user_id, amount=1):
    """Foydalanuvchiga mukofot qo‘shish"""
    rewards = load_rewards()
    if str(user_id) not in rewards:
        rewards[str(user_id)] = {"balance": 0, "withdrawn": 0}
    rewards[str(user_id)]["balance"] += amount
    save_rewards(rewards)
    return rewards[str(user_id)]["balance"]


def get_reward(user_id):
    """Foydalanuvchining balansini olish"""
    rewards = load_rewards()
    if str(user_id) not in rewards:
        rewards[str(user_id)] = {"balance": 0, "withdrawn": 0}
    return rewards[str(user_id)]["balance"]


def withdraw_reward(user_id, amount):
    """Foydalanuvchi pul yechsa, balansni kamaytirish va withdrawn ga qo‘shish"""
    rewards = load_rewards()
    if str(user_id) not in rewards:
        rewards[str(user_id)] = {"balance": 0, "withdrawn": 0}
    if amount > rewards[str(user_id)]["balance"]:
        return False  # yetarli balans yo‘q
    rewards[str(user_id)]["balance"] -= amount
    rewards[str(user_id)]["withdrawn"] += amount
    save_rewards(rewards)
    return True
