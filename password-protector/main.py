import streamlit as st
import hashlib
from cryptography.fernet import Fernet

# --- Initialization ---
st.set_page_config(page_title="🔐 Secure Data Encryption", layout="centered")

# Generate Fernet key (normally you store this safely)
if "KEY" not in st.session_state:
    st.session_state.KEY = Fernet.generate_key()
    st.session_state.cipher = Fernet(st.session_state.KEY)

# In-memory data and security tracking
if "stored_data" not in st.session_state:
    st.session_state.stored_data = {}
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

# --- Utility Functions ---
def hash_passkey(passkey):
    # print("pk",passkey)
    # print("hash",hashlib.sha256(passkey.encode()).hexdigest())
    return hashlib.sha256(passkey.encode()).hexdigest()

def encrypt_data(text, passkey):
    # print("text",text)
    # print("pk",passkey)
    # print("session state",st.session_state)
    # print("encrypt func",st.session_state.cipher.encrypt(text.encode()).decode())
    return st.session_state.cipher.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text, passkey):
    hashed = hash_passkey(passkey)
    print("hashed 2",hashed)
    for data in st.session_state.stored_data.values():
        print("data val",st.session_state.stored_data.values)
        print("data",data)
        if data["encrypted_text"] == encrypted_text and data["passkey"] == hashed:
            st.session_state.failed_attempts = 0
            return st.session_state.cipher.decrypt(encrypted_text.encode()).decode()
    st.session_state.failed_attempts += 1
    return None

def reauth_required():
    return st.session_state.failed_attempts >= 3

# --- Page Logic ---
st.title("🛡️ Secure Data Encryption System")

menu = ["Home", "Store Data", "Retrieve Data"]
if reauth_required():
    menu = ["Login"]

choice = st.sidebar.selectbox("Navigate", menu)

if choice == "Home":
    st.markdown("""
    ## 🏠 Welcome
    Use this tool to securely **store** and **retrieve** data using passkey encryption.
    - 🔐 SHA-256 Passkey Hashing
    - 🔒 Fernet Symmetric Encryption
    - 🚫 Lockout after 3 failed attempts
    """)

elif choice == "Store Data":
    st.header("📂 Store New Data")
    user_data = st.text_area("Enter your data to encrypt")
    passkey = st.text_input("Create a Passkey", type="password")

    if st.button("🔐 Encrypt and Save"):
        if user_data and passkey:
            hashed_passkey = hash_passkey(passkey)
            encrypted = encrypt_data(user_data, passkey)
            st.session_state.stored_data[encrypted] = {
                "encrypted_text": encrypted,
                
                "passkey": hashed_passkey
            }
            st.success("✅ Data encrypted and stored in memory")
            st.code(encrypted, language="text")
        else:
            st.error("⚠️ Please provide both data and passkey")

elif choice == "Retrieve Data":
    st.header("🔍 Retrieve Data")
    encrypted_text = st.text_area("Paste the Encrypted Data")
    passkey = st.text_input("Enter Your Passkey", type="password")

    if st.button("🔓 Decrypt"):
        if encrypted_text and passkey:
            result = decrypt_data(encrypted_text, passkey)
            if result:
                st.success("✅ Decrypted Data:")
                st.code(result, language="text")
            else:
                remaining = 3 - st.session_state.failed_attempts
                st.error(f"❌ Incorrect Passkey. Attempts left: {remaining}")
                if reauth_required():
                    st.warning("🔒 Too many failed attempts. Redirecting to Login...")
                    st.rerun()
        else:
            st.error("⚠️ Provide both encrypted data and passkey")

elif choice == "Login":
    st.header("🔑 Reauthorization Required")
    master_key = st.text_input("Enter Master Password", type="password")

    if st.button("Login"):
        if master_key == "admin123":
            st.session_state.failed_attempts = 0
            st.success("✅ Access granted. Returning to menu...")
            st.rerun()
        else:
            st.error("❌ Invalid master password")
