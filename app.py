import streamlit as st
from PIL import Image

# Stil og layout
st.markdown("""
    <style>
    html, body, .main {
        background-color: #fff8f3;
        padding: 0;
        margin: 0;
        width: 100%;
    }
    .block-container {
        padding: 2rem 4rem;
        max-width: 100%;
    }
    h1, h2, h3 {
        font-family: 'Segoe UI', sans-serif;
        color: #2d2a26;
    }
    .stButton > button {
        background-color: #e63946;
        color: white;
        font-size: 16px;
        border-radius: 8px;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #c32f36;
        scale: 1.03;
    }
    .stRadio > div {
        flex-direction: row;
        gap: 2rem;
    }
    </style>
    <script>
    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(function() {
            alert('Prompt kopiert til utklippstavlen!');
        }, function(err) {
            alert('Kunne ikke kopiere teksten: ', err);
        });
    }
    </script>
""", unsafe_allow_html=True)

# Logo og tittel
logo = Image.open("assets/logo.png")
st.image(logo, width=120)
st.title("🍽️ Ukemeny & Middagsassistent")
st.subheader("Personlig menyplan basert på rene råvarer og dine preferanser")

# Brukervalg
mode = st.radio("Hva ønsker du hjelp med?", ["Ukesmeny", "Enkel middag"])

raw_materials = st.multiselect("Velg råvarer", ["Fisk", "Kylling", "Rødt kjøtt", "Svin", "Vegetar", "Vegan", "Glutenfri", "Lam", "Ferdigprodukter"], default=["Fisk", "Kylling", "Rødt kjøtt", "Svin"])
difficulty = st.selectbox("Velg vanskelighetsgrad", ["Enkel", "Middels", "Avansert"])
prep_time = st.multiselect(
    "Velg forberedelsestid (du kan velge flere)",
    ["0–30 min", "30–60 min", "1–2 timer", "2–4 timer", "Mer enn 4 timer"],
    default=["0–30 min", "30–60 min", "1–2 timer"]
)

category = st.multiselect("Velg kategori", [
    "Hverdags", "Fest", "Sunn", "Helgekos", "Usunn og digg", "Barnevennlig", "Restemat", "Tradisjonell", "Internasjonal"], default=["Hverdags"])
people = st.number_input("Antall personer", min_value=1, max_value=20, value=3)
price = st.slider("Maks pris per middag (kr)", min_value=50, max_value=3000, value=150)

stores = st.multiselect(
    "Velg dagligvarebutikker du ønsker å handle i",
    ["KIWI", "REMA 1000", "MENY", "COOP Extra", "COOP Mega", "COOP Prix",
     "SPAR", "EuroSPAR", "Bunnpris", "Joker", "Obs", "Øvrige butikker"],
    default=["KIWI", "REMA 1000", "MENY", "COOP Extra", "COOP Mega", "COOP Prix",
             "SPAR", "EuroSPAR", "Bunnpris", "Joker", "Obs", "Øvrige butikker"]
)

# Generer prompt
if st.button("Generer prompt til ChatGPT"):
    prompt = (
        f"Lag {'en ukesmeny' if mode == 'Ukesmeny' else 'én middag'} for {people} personer med rene råvarer.\n"
        f"- Velg én eller flere av disse råvarene: {', '.join(raw_materials) if raw_materials else 'valgfritt'}\n"
        f"- Vanskelighetsgrad: {difficulty}\n"
        f"- Forberedelsestid: {', '.join(prep_time) if prep_time else 'valgfritt'}\n"
        f"- Kategori: {', '.join(category) if category else 'valgfritt'}\n"
        f"- Maks pris per middag: {price} kr\n"
        f"- Butikker: {', '.join(stores) if stores else 'valgfritt'}\n"
        "Svar med ingredienser, fremgangsmåte og estimert pris."
    )

    st.markdown("### 📋 Klar til bruk i ChatGPT:")
    st.text_area("Prompt", value=prompt, height=250, key="prompt_output")
    st.markdown("Kopier teksten over og lim inn i ChatGPT!")
    st.code(prompt, language="markdown")
    st.download_button("📥 Last ned som tekstfil", prompt, file_name="chatgpt_prompt.txt")

    # Kopier til utklippstavle-knapp (JS workaround)
    st.markdown(f"""
    <button onclick=\"navigator.clipboard.writeText(`{prompt}`); alert('Prompt kopiert til utklippstavlen!');\" 
    style='background-color:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:5px;margin-top:10px;'>
        📋 Kopier til utklippstavle
    </button>
    """, unsafe_allow_html=True)
