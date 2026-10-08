import os
import json
import base64
import pygame

# ==============================================================================
# SECURE DIRECTORY & PATH SETUP
# ==============================================================================
try:
    save_dir = pygame.system.get_pref_path("Oshey Studios", "Proto Clicker 2")
    save_path = os.path.join(save_dir, "save_Data.dat")  # Secure encrypted extension
    save_path_backup = os.path.join(save_dir, "save_data_Backup.dat")
except AttributeError:
    save_dir = "."
    save_path = "save_Data.dat"
    save_path_backup = "save_data_Backup.dat"


# ==============================================================================
# BASE64 ENCRYPTION PIPELINES
# ==============================================================================
def _encrypt_string(plain_text):
    """Converts raw plain JSON string text into scrambled base64 strings."""
    raw_bytes = plain_text.encode('utf-8')
    secure_bytes = base64.b64encode(raw_bytes)
    return secure_bytes.decode('utf-8')


def _decrypt_string(secure_text):
    """Converts scrambled base64 string bytes back into readable JSON text structures."""
    try:
        secure_bytes = secure_text.encode('utf-8')
        raw_bytes = base64.b64decode(secure_bytes)
        return raw_bytes.decode('utf-8')
    except Exception as e:
        print(f"[SAVE MAN] Warning: Data string decoding failure or tampering detected: {e}")
        return None


# ==============================================================================
# CORE SAVE AND LOAD ENGINE
# ==============================================================================
def save_game(game_state, backup=False):
    """Encrypts and writes the game state dictionary to disk."""
    target_path = save_path_backup if backup else save_path
    try:
        # Convert state dictionary to a clean JSON string
        json_string = json.dumps(game_state, indent=4)

        # Scramble the string using base64 encryption
        encrypted_data = _encrypt_string(json_string)

        # Write out encrypted text payload
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(encrypted_data)
        return True
    except IOError:
        print(f"[SYSTEM] Error: Could not write save file.")
        return False


def load_game():
    """Loads and decrypts saved profiles, falling back to backup or defaults if needed."""
    # Attempt Primary File Load
    try:
        with open(save_path, "r", encoding="utf-8") as f:
            encrypted_data = f.read().strip()

        json_string = _decrypt_string(encrypted_data)
        if json_string:
            return json.loads(json_string)
    except (FileNotFoundError, Exception):
        print("[SYSTEM] Primary save file missing or corrupted. Trying backup...")

    # Attempt Backup File Load
    try:
        with open(save_path_backup, "r", encoding="utf-8") as f:
            encrypted_data = f.read().strip()

        json_string = _decrypt_string(encrypted_data)
        if json_string:
            return json.loads(json_string)
    except (FileNotFoundError, Exception):
        print("[SYSTEM] Backup save file missing or corrupted. Deploying defaults.")

    # Factory Default Configuration Profile (If both loads fail)
    return {
        "clicks": 0,
        "rebirths": 0,
        "current_tier": 0,
        "total_time_played": 0,
        "xp": 0,
        "CU1": 0, "CU2": 0, "CU3": 0, "CU4": 0, "CU5": 0,
        "RU1": 0, "RU2": 0, "RU3": 0,
        "current_ascension": 0,
        "ascension_tokens": 0,
        "ascension_stage": 0,
        "ascension_stage_2": 0
    }
