import streamlit as st
from google import genai
from google.genai import types

# Configurazione della pagina web
st.set_page_config(page_title="Chatbot Anti-Cyberbullismo", page_icon="🛡️", layout="centered")

# Titolo e introduzione dell'interfaccia web
st.title("🛡️ Workshop: Chatbot Anti-Cyberbullismo")
st.markdown("""
Benvenuto. Questo spazio è sicuro. Se hai dubbi sul comportamento di alcuni compagni, 
parlane con me. Ti aiuterò a capire la situazione e a trovare le soluzioni migliori.
""")

# Spazio nella barra laterale per inserire la chiave API in sicurezza
st.sidebar.header("Configurazione")
api_key = st.sidebar.text_input("Inserisci la tua Gemini API Key:", type="password")

# Definizione dell'Istruzione di Sistema (System Instruction) originaria
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

# Controllo se la chiave API è stata inserita
if not api_key:
    st.info("Per favore, inserisci la tua Gemini API Key nella barra laterale per iniziare.", icon="🔑")
else:
    # Inizializzazione del client Gemini (Nuovo SDK ufficiale)
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"Errore nella configurazione del client: {e}")

    # Gestione della cronologia della chat nello stato della pagina (Streamlit Session State)
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    # Mostra i messaggi precedenti ad ogni ricaricamento della pagina
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Spazio di input per lo studente
    if user_input := st.chat_input("Scrivi qui cosa sta succedendo..."):
        
        # Mostra il messaggio dello studente nel sito
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Generazione della risposta da parte di Gemini
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Sto riflettendo..."):
                try:
                    # Ricostruiamo la cronologia nel formato corretto richiesto dal nuovo SDK
                    formatted_contents = []
                    for msg in st.session_state.messages:
                        role_name = "user" if msg["role"] == "user" else "model"
                        formatted_contents.append(
                            types.Content(role=role_name, parts=[types.Part.from_text(text=msg["content"])])
                        )

                    # Chiamata al modello passando le istruzioni di sistema e la cronologia
                    response = client.models.generate_content(
                        model='gemini-2.5-flash', # Usiamo la versione di produzione più recente e stabile
                        contents=formatted_contents,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_INSTRUCTION,
                        ),
                    )
                    
                    assistant_response = response.text
                    message_placeholder.markdown(assistant_response)
                    
                    # Salva la risposta dell'assistente nella cronologia
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                    
                except Exception as e:
                    st.error(f"Si è verificato un errore durante la generazione della risposta: {e}")