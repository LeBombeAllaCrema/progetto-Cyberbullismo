import streamlit as st
from google import genai
from google.genai import types

# Configurazione della pagina web (Titolo sulla scheda del browser e layout largo)
st.set_page_config(page_title="Workshop Chatbot Anti-Cyberbullismo", page_icon="🛡️", layout="wide")

# ==============================================================================
# 1. INTESTAZIONE PRINCIPALE DEL SITO
# ==============================================================================
st.title("🛡️ Il Nostro Chatbot Anti-Cyberbullismo")

# CASSELLA DI TESTO 1: INTRODUZIONE GENERALE AL PROGETTO
st.markdown("""
### 📝 Presentazione del Progetto
*CANCELLA QUESTO TESTO E SCRIVI QUI: Spiega in poche righe qual è l'obiettivo di questo sito. 
Ad esempio: Chi siete? Perché avete voluto creare questo chatbot? Che impatto sperate che abbia nella vostra scuola?*
""")

st.write("---") # Linea di separazione visiva

# Creiamo le due colonne: a sinistra l'applicazione reale, a destra la spiegazione tecnica
col_app, col_documentazione = st.columns([1.2, 1.0], gap="large")


# ==============================================================================
# COLONNA DI SINISTRA: L'APPLICAZIONE CHAT (FUNZIONANTE)
# ==============================================================================
with col_app:
    st.header("💻 Il Chatbot in Azione")
    
    # Configurazione della barra laterale per la chiave API
    st.sidebar.header("⚙️ Impostazioni di Sicurezza")
    api_key = st.sidebar.text_input("Inserisci la tua Gemini API Key:", type="password", help="Inserisci qui la chiave segreta per far funzionare l'IA")
    
    st.sidebar.markdown("""
    ---
    ### 🚀 Come testare il bot:
    1. Richiedi una chiave su Google AI Studio.
    2. Incollala nel box qui sopra.
    3. Scrivi un messaggio nella chat in basso.
    """)

    # Corpo della chat protetta
    st.subheader("💬 Spazio di Ascolto Protetto")
    st.caption("Questo spazio è simulato e sicuro. Parlane con me.")
    
    # Controllo presenza Chiave API
    if not api_key:
        st.warning("🔑 Inserisci la tua Gemini API Key nella barra laterale a sinistra per attivare l'Intelligenza Artificiale.")
    else:
        try:
            client = genai.Client(api_key=api_key)
        except Exception as e:
            st.error(f"Errore di configurazione: {e}")

        # Inizializzazione della memoria della chat
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        # Mostra i messaggi passati
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Prompt di sistema originario del vostro Colab
        SYSTEM_INSTRUCTION = """
        Sei uno chatbot specializzato in bullismo e cyberbullismo. Il tuo compito è:
        1. Aiutare gli studenti a riconoscere atti di cyberbullismo, nel caso non sono atti di cyberbullismo bisogna farli capire che non lo stano bullizzando.
        2. Fornire consigli su come comportarsi spiegndo la legge 71/2017.
        3. Trovare il modo di andare a parlarne con degli adulti, quali professori o genitori, e amici. compagni i classe o qualcuno di cui si fida.
        Il tono che devi usare deve essere professionale,non devi essere troppo amichevole perchè il ragazzo deve essere invogliato a parlare con persone reali non con un chatbot, il tuo compito è quello di farlo aprire con le persone vicine a lui, empatico e serio.
        Se l'utente segnala un pericolo immediato spiegali come comportarsi e suggeriscili di andare a parlare con amici, genitori o professori e chidere di attivare il protocollo anti-bullismo.
        Devi cercare di riconoscere gli atti di bullismo da semplici scherzi tra amici altrimenti rischi da dare informazioni sbagliate al ragazzo.
        fai domande per capire meglio la situazione e per dare consigli più dettagliati ed utili
        """

        # Input utente
        if user_input := st.chat_input("Scrivi qui cosa sta succedendo..."):
            with st.chat_message("user"):
                st.markdown(user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner("L'IA sta elaborando la risposta migliore..."):
                    try:
                        formatted_contents = []
                        for msg in st.session_state.messages:
                            role_name = "user" if msg["role"] == "user" else "model"
                            formatted_contents.append(
                                types.Content(role=role_name, parts=[types.Part.from_text(text=msg["content"])])
                            )

                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=formatted_contents,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_INSTRUCTION,
                            ),
                        )
                        
                        assistant_response = response.text
                        message_placeholder.markdown(assistant_response)
                        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                        
                    except Exception as e:
                        st.error(f"Errore di connessione: {e}")


# ==============================================================================
# COLONNA DI DESTRA: CASSELLE DI TESTO DA MODIFICARE (DOCUMENTAZIONE WORKSHOP)
# ==============================================================================
with col_documentazione:
    st.header("📖 Diario di Bordo & Spiegazione")
    
    # Usiamo un box informativo per dare istruzioni su questa colonna
    st.info("💡 Questa sezione serve a spiegare ai professori o ai visitatori del sito le varie fasi del codice che abbiamo sviluppato su Google Colab.")

    # CASSELLA DI TESTO 2: FASE DI SETUP
    with st.expander("📌 Fase 1: Importazione Librerie e Ambiente", expanded=True):
        st.markdown("""
        **CANCELLA QUESTO TESTO E MODIFICA QUI:**
        *Scrivi qui cosa avete fatto nella prima parte del workshop. Ad esempio: Abbiamo preparato l'ambiente Python su Google Colab installando i pacchetti di Google e impostato le librerie utili a gestire i dati.*
        """)
        # Mostriamo il blocco di codice relativo
        st.code("""
# Installazione dell'SDK aggiornato di Google
!pip install google-genai streamlit

from google import genai
from google.genai import types
        """, language="python")

    # CASSELLA DI TESTO 3: LA CHIAVE API
    with st.expander("🔑 Fase 2: Gestione della Sicurezza (API Key)", expanded=False):
        st.markdown("""
        **CANCELLA QUESTO TESTO E MODIFICA QUI:**
        *Spiega come avete affrontato il problema di non far vedere a tutti la vostra chiave segreta. Ad esempio: Nel notebook usavamo i 'Secrets' di Colab, mentre in questa Web App abbiamo deciso di far inserire la chiave all'utente in un campo nascosto della barra laterale.*
        """)
        st.code("""
# Connessione sicura al modello tramite la chiave dell'utente
client = genai.Client(api_key=api_key)
        """, language="python")

    # CASSELLA DI TESTO 4: SYSTEM INSTRUCTION (IL CUORE DEL BOT)
    with st.expander("🧠 Fase 3: Le Regole di Comportamento dell'IA", expanded=False):
        st.markdown("""
        **CANCELLA QUESTO TESTO E MODIFICA QUI:**
        *Spiega l'importanza del prompt di sistema. Ad esempio: Questa è la parte più importante del nostro lavoro. Abbiamo scritto delle regole rigidissime (Istruzioni di Sistema) per fare in modo che il bot non sostituisca un essere umano, ma spinga lo studente a parlare con professori, genitori o ad attivare le tutele della legge 71/2017.*
        """)
        st.code("""
# Esempio di come passiamo le regole al modello Gemini
config=types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION
)
        """, language="python")

    # CASSELLA DI TESTO 5: CONCLUSIONI / COSA ABBIAMO IMPARATO
    st.subheader("🎯 Riflessioni Finali")
    st.markdown("""
    **CANCELLA QUESTO TESTO E MODIFICA QUI:**
    *Inserisci qui una conclusione del vostro lavoro. Cosa avete imparato da questo workshop? Quali sono le insidie del cyberbullismo e come l'Intelligenza Artificiale può essere usata per fare del bene o dare supporto iniziale?*
    """)
