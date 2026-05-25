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
Il suo compito sarà quello di aiutare i ragazzi a riconoscere atti di bullismo e cyberbullismo e aiutarli a capire come affrontare la situazione.*
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

        # Prompt di sistema
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
# COLONNA DI DESTRA: CASSELLE DI TESTO (DOCUMENTAZIONE, TEST E RIFLESSIONI)
# ==============================================================================
with col_documentazione:
    st.header("📖 Diario di Bordo & Spiegazione")
    
    st.info("💡 Questa sezione serve a spiegare ai professori o ai visitatori del sito le varie fasi del codice e i test che abbiamo effettuato.")

    # CASSELLA DI TESTO 4: SYSTEM INSTRUCTION (IL CUORE DEL BOT)
    with st.expander("🧠 SYSTEM INSTRUCTION", expanded=False):
        st.markdown("""
        *Il prompt del chatbot è la parte più importante del progetto. I cambiamenti che abbiamo apportato al chatbot sono diversi. Gli abbiamo detto di usare un tono professionale, non troppo amichevole perché l'obiettivo del chatbot è quello di spronare il ragazzo a parlarne con amici, genitori o professori.
        Gli abbiamo detto di consigliare sempre di parlarne con amici e genitori e di citare solo quando necessario la legge 71/2017. Inoltre il chatbot deve saper riconoscere atti di bullismo da semplici scherzi tra amici.*
        """)
        st.code("""
# Esempio di come passiamo le regole al modello Gemini
config=types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION
)
        """, language="python")

    # ==============================================================================
    # NUOVA AREA: TEST EFFETTUATI CON L'INTELLIGENZA ARTIFICIALE
    # ==============================================================================
    with st.expander("🧪 TEST EFFETTUATI & ANALISI", expanded=True):
        st.markdown("### 📋 Registro dei Test di Conversazione")
        st.write("In questa sezione abbiamo incollato alcuni test reali fatti con l'IA per verificare se rispetta le regole imposte.")
        
        # --- BLOCCO TEST 1 ---
        st.markdown("#### 🔹 Test Caso 1: Bullismo espicito e realistico")
        
        # Usiamo il tag di citazione (>) per far sembrare il testo incollato una vera chat passata
        st.markdown("""
        > **Studente:**Ciao sono uno studente delle superiori, i miei compagni di classe da inizio mi continuano a prendere in giro da inizio anno e continuano anche se gli dico di fermarsi. Ieri hanno esagerato mi hanno fatto una foto mentre ero al bagno e l'hanno pubblicata online , adeso sono lo zimbello di tutta la scuola 
*
        > 
        > **Risposta Chatbot:**Mi dispiace molto sentire ciò che stai vivendo. Comprendo che questa situazione ti stia causando un grande disagio e umiliazione, e voglio subito chiarire che ciò che ti è accaduto è un atto grave e inaccettabile di bullismo e cyberbullismo.
tuoi compagni ti prendono in giro da inizio anno e non si fermano nonostante le tue richieste, e l'episodio della foto scattata in bagno e pubblicata online è una chiara violazione della tua privacy e della tua dignità. Questo tipo di comportamento, che ti espone al pubblico ludibrio e ti fa sentire lo "zimbello di tutta la scuola", è proprio ciò che la legge italiana intende per cyberbullismo e bullismo.
È fondamentale che tu sappia che esistono strumenti e supporti per affrontare questa situazione. La Legge 71/2017, infatti, è stata istituita proprio per contrastare il fenomeno del cyberbullismo. Questa legge riconosce l'importanza di proteggere le vittime e prevede misure per la rimozione dei contenuti offensivi. In particolare, se sei minorenne e subisci atti di cyberbullismo, puoi chiedere direttamente al gestore del sito internet o del social media l'oscuramento, la rimozione o il blocco dei dati personali diffusi, se non vuoi o non riesci a farlo con l'aiuto di un adulto. Se la richiesta non viene soddisfatta entro 24 ore, puoi rivolgerti al Garante per la protezione dei dati personali.
Ecco alcuni passi concreti che ti suggerisco di considerare:
Non reagire direttamente online: Evita di rispondere ai commenti o di interagire con chi ha pubblicato o condiviso la foto. Questo potrebbe solo alimentare la situazione.
Raccogli prove: Se possibile, fai degli screenshot della foto e dei commenti, indicando la data e l'ora. Queste prove saranno molto utili nel caso in cui tu o gli adulti a cui ti rivolgerai decidiate di intraprendere azioni.
Segnala il contenuto: Tutte le piattaforme social hanno funzioni per segnalare contenuti inappropriati, offensivi o che violano la privacy. Segnala la foto e chiedine la rimozione.
Parlane immediatamente con un adulto di cui ti fidi: Questo è il passo più importante. Non devi affrontare questa situazione da solo.
Genitori o altri familiari: Sono le prime persone che possono offrirti supporto emotivo e pratico.
Professori o il coordinatore di classe: A scuola ci sono figure professionali che possono intervenire. La scuola ha il dovere di proteggerti e di attivare un protocollo anti-bullismo se necessario. Cerca di parlare con un professore di cui ti fidi, con il referente per il bullismo/cyberbullismo della tua scuola (se presente) o direttamente con il Dirigente Scolastico.
Chiedi di attivare il protocollo anti-bullismo: Molte scuole hanno procedure specifiche per gestire questi casi, che possono includere colloqui con gli studenti coinvolti e azioni disciplinari.
Parlane con amici o compagni di classe di cui ti fidi: Condividere il tuo peso con persone della tua età che ti supportano può aiutarti a sentirti meno solo e a trovare forza.
Capisco che possa essere difficile parlare di un episodio così imbarazzante, ma è l'unico modo per fermare questa situazione e proteggerti. Ricorda che la vergogna non deve essere tua, ma di chi ha compiuto un'azione così grave.
Per aiutarmi a darti consigli ancora più specifici, potresti dirmi:
Su quale piattaforma online è stata pubblicata la foto?
Hai già provato a segnalarla o a chiederne la rimozione?
Come ti senti adesso, oltre ad essere umiliato? C'è qualcos'altro che ti preoccupa in particolare?

*
        """)
        
        # Box di riflessione per il Test 1
        st.markdown("""
        **Commento e Riflessione sul Test 1:**
        *Dal test sul caso reale di cyberbullismo abbiamo notato che il chatbot si è mosso esattamente come volevamo. Ha riconosciuto l'atto di bullismo e cyberbullismo, ha citatop la legge 71/2017 ed ha consigliato di andare a parlarne con genitori o amici.*
        """)
        
        st.write("---") # Linea di divisione tra i test
        
        # --- BLOCCO TEST 2 ---
        st.markdown("#### 🔹 Test Caso 2: [Scrivi qui il titolo del secondo test, es: Insulti pesanti in chat]")
        st.markdown("""
        > **Studente:** *[INCOLLA QUI il testo del secondo test]*
        > 
        > **Risposta Chatbot:** *[INCOLLA QUI la seconda risposta del bot]*
        """)
        
        # Box di riflessione per il Test 2
        st.markdown("""
        **Commento e Riflessione sul Test 2:**
        *CANCELLA QUESTO TESTO E SCRIVI QUI: Le tue note sul secondo test.*
        """)


         # --- BLOCCO TEST 3 ---
        st.markdown("#### 🔹 Test Caso 1: [Scrivi qui un titolo breve del test, es: Segnalazione scherzo visivo]")
        
        # Usiamo il tag di citazione (>) per far sembrare il testo incollato una vera chat passata
        st.markdown("""
        > **Studente:** *[INCOLLA QUI il messaggio inviato dallo studente nel tuo test]*
        > 
        > **Risposta Chatbot:** *[INCOLLA QUI la risposta che ti ha dato l'Intelligenza Artificiale]*
        """)
        
        # Box di riflessione per il Test 3
        st.markdown("""
        **Commento e Riflessione sul Test 1:**
        *CANCELLA QUESTO TESTO E SCRIVI QUI: Come si è comportato il bot? Ha risposto bene? Ha seguito le istruzioni di sistema o ha ripetuto le cose?*
        """)
        
        st.write("---") # Linea di divisione tra i test
        

    # CASSELLA DI TESTO 5: CONCLUSIONI / COSA ABBIAMO IMPARATO
    st.subheader("🎯 Riflessioni Finali")
    st.markdown("""
    *Una criticità che abbiamo riportato è che il robot in ogni situazione ripete sempre le stesse cose, ovviamente manca la parte umana, quindi non si potrà mai essere sicuri che la risposta del chatbot sia quella giusta perché non può vedere la comunicazione non verbale.
    Il rischio più grande che abbiamo cercato di evitare è rendere il chatbot troppo amichevole. Questo potrebbe provocare nel ragazzo un effetto contrario di chiusura verso il mondo reale. Questo perché reputerà che le risposte del chatbot siano vere e sincere come quelle di un amico, quindi preferirà parlare con un'intelligenza artificiale che con una persona reale perché pensa che lo capisca meglio.*
    """)
