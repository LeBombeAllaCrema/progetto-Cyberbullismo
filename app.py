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
*Ciao a tutti, questo è il nostro chat-bot addestrato per essere un tutor specializzato in bullismo e cyberbullismo.
Il suo sarà compito sarà quello di aiutare i ragazzi a riconoscere atti di bullismo e cyberbullismo e aiutarli capire come affrontare la situazione.*
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
        2. Fornire consigli su come comportarsi spiegndo la legge 71/2017(solo ce ne è davvero bisogno).
        3. Spronarli a parlarne con degli adulti, quali professori o genitori, e amici. compagni i classe o qualcuno di cui si fida.
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

   



    # CASSELLA DI TESTO 4: SYSTEM INSTRUCTION (IL CUORE DEL BOT)
    with st.expander("🧠 SYSTEM INSTRUCTION", expanded=False):
        st.markdown("""
       
        *Il prompt del chatbot è la parte più importante del progetto. I cambiamenti che abbiamo apportato al chatbot sono diversi. gli abbiamo detto di usare un tono professionale, non troppo amichevole perché l'obiettivo del chatbot è quello di spronare il ragazzo a parlarne con amici, genitori o professori.
        Gli abbiamo detto di consigliare sempre di parlarne con amici e genitori e di citare solo quando necessario la legge 71/2017. Inoltre il chatbot deve saper riconoscere atti di bullismo da semplici scherzi tra amici.*
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
  
    *Una criticità che abbiamo riportato è che il robot in ogni situazione ripete sempre le stesse cose, ovviamente manca la parte umana, quindi non si potrà mai essere sicuri che la risposta del chatbot sia quella giusta perché non può vedere la comunicazione non verbale.
    Il rischio più grande che abbiamo cercato di evitare è rendere il chatbot troppo amichevole. Questo protrebbe provocare nel ragazzo un effetto contrario di chiusura verso il mondo reale. Questo perché reputerà che le risposte del chatbot siano vere e sincere come quelle di un amico, quindi preferirà parlare con un intelligenza artificiale che con una persona reale perchè pensa che lo capisce meglio*
    """)
