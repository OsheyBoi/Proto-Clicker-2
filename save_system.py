import os
import json
import base64
import pygame

# ==============================================================================
# SECURE DIRECTORY & PATH SETUP
# ==============================================================================
try:
    save_dir = pygame.system.get_pref_path("Oshey Studios", "Proto Clicker 2")
    save_path = os.path.join(save_dir, "save_Data.dat")
    save_path_backup = os.path.join(save_dir, "save_data_Backup.dat")
except AttributeError:
    save_dir = "."
    save_path = "save_Data.dat"
    save_path_backup = "save_data_Backup.dat"

# ==============================================================================
# OBFUSCATED SALT CIPHER PIPELINES
# ==============================================================================
# Change this random string to whatever you want! It acts as your encryption key.
SECRET_SALT_KEY = "ProtoClicker2_AntiCheat_OsheyStudios_2026_X9!"


def _encrypt_string(plain_text):
    """Obfuscates and encodes a text string using a custom split salt technique."""
    try:
        # 1. Reverse the raw string data first to confuse basic pattern recognition
        reversed_text = plain_text[::-1]

        # 2. Blend your secret key directly into the center of the payload
        mid_point = len(reversed_text) // 2
        salted_payload = reversed_text[:mid_point] + SECRET_SALT_KEY + reversed_text[mid_point:]

        # 3. Double encode it through base64 blocks to break normal string formats
        raw_bytes = salted_payload.encode('utf-8')
        scrambled_bytes = base64.b64encode(raw_bytes)

        # 4. Turn it upside down a final time before writing to disk
        final_string = scrambled_bytes.decode('utf-8')[::-1]
        return final_string
    except Exception as e:
        print(f"[SAVE CIPHER] Encryption pipeline failure: {e}")
        return ""


def _decrypt_string(secure_text):
    """De-obfuscates data structures, isolating and validating salt boundaries."""
    try:
        # 1. Reverse the string back to get the baseline base64 structure
        unreversed_string = secure_text[::-1]

        # 2. Decode the baseline base64 text block safely back to bytes
        secure_bytes = unreversed_string.encode('utf-8')
        raw_bytes = base64.b64decode(secure_bytes)
        salted_payload = raw_bytes.decode('utf-8')

        # 3. Check for the secret salt key. If it's missing, someone modified the file!
        if SECRET_SALT_KEY not in salted_payload:
            print("[SAVE MAN] Data Tampering Detected! Salt integrity verification failed.")
            return None

        # 4. Extract and remove the secret salt key to isolate the game data strings
        cleaned_payload = salted_payload.replace(SECRET_SALT_KEY, "", 1)

        # 5. Flip the text back one final time to restore the original JSON syntax
        plain_text = cleaned_payload[::-1]
        return plain_text
    except Exception as e:
        print(f"[SAVE MAN] Severe warning: Data string decoding failure or save file tampering: {e}")
        return None


# ==============================================================================
# CORE SAVE AND LOAD ENGINE
# ==============================================================================
def save_game(game_state, backup=False):
    """Encrypts and writes the game state dictionary to disk."""
    target_path = save_path_backup if backup else save_path
    try:
        json_string = json.dumps(game_state, indent=4)
        encrypted_data = _encrypt_string(json_string)

        if not encrypted_data:
            raise IOError("Encryption pipeline returned empty string.")

        with open(target_path, "w", encoding="utf-8") as f:
            f.write(encrypted_data)
        return True
    except IOError:
        print(f"[SYSTEM] Error: Could not write save file.")
        return False


def load_game():
    """Loads and decrypts saved profiles, falling back to backup or defaults if needed."""
    try:
        with open(save_path, "r", encoding="utf-8") as f:
            encrypted_data = f.read().strip()

        json_string = _decrypt_string(encrypted_data)
        if json_string:
            return json.loads(json_string)
    except (FileNotFoundError, Exception):
        print("[SYSTEM] Primary save file missing or corrupted. Trying backup...")

    try:
        with open(save_path_backup, "r", encoding="utf-8") as f:
            encrypted_data = f.read().strip()

        json_string = _decrypt_string(encrypted_data)
        if json_string:
            return json.loads(json_string)
    except (FileNotFoundError, Exception):
        print("[SYSTEM] Backup save file missing or corrupted. Deploying defaults.")

    return {
        "clicks": 0, "rebirths": 0, "current_tier": 0, "total_time_played": 0, "xp": 0,
        "CU1": 0, "CU2": 0, "CU3": 0, "CU4": 0, "CU5": 0,
        "RU1": 0, "RU2": 0, "RU3": 0,
        "current_ascension": 0, "ascension_tokens": 0, "ascension_stage": 0, "ascension_stage_2": 0
    }
