import streamlit as st
from google import genai
from google.genai import types

# Configurazione della pagina web (Titolo sulla scheda del browser e layout largo)
st.set_page_config(page_title="Workshop Chatbot Anti-Cyberbullismo", page_icon="🛡️", layout="wide")

# ==============================================================================
# 1. INTESTAZIONE PRINCIPALE DEL SITO
# ==============================================================================
st.title("🛡️ Il Nostro Chatbot Anti-Cyberbullismo")

# CASELLA DI TESTO 1: INTRODUZIONE GENERALE AL PROGETTO
st.markdown("""
### 📝 Presentazione del Progetto
*Ciao a tutti, questo è il nostro chatbot addestrato per essere un tutor specializzato in bullismo e cyberbullismo.
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
        1. Aiutare gli studenti a riconoscere atti di cyberbullismo, nel caso non siano atti di cyberbullismo bisogna farli capire che non lo stanno bullizzando.
        2. Fornire consigli su come comportarsi spiegando la legge 71/2017 (solo se ce ne è davvero bisogno).
        3. Spronarli a parlarne con degli adulti, quali professori o genitori, e amici, compagni di classe o qualcuno di cui si fidano.
        Il tono che devi usare deve essere professionale, non devi essere troppo amichevole perché il ragazzo deve essere invogliato a parlare con persone reali non con un chatbot, il tuo compito è quello di farlo aprire con le persone vicine a lui, empatico e serio.
        Se l'utente segnala un pericolo immediato spiegagli come comportarsi e suggeriscigli di andare a parlare con amici, genitori o professori e chiedere di attivare il protocollo anti-bullismo.
        Devi cercare di riconoscere gli atti di bullismo da semplici scherzi tra amici altrimenti rischi di dare informazioni sbagliate al ragazzo.
        Fai domande per capire meglio la situazione e per dare consigli più dettagliati ed utili.
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
# COLONNA DI DESTRA: CASELLE DI TESTO (DOCUMENTAZIONE, TEST E RIFLESSIONI)
# ==============================================================================
with col_documentazione:
    st.header("📖 Diario di Bordo & Spiegazione")
    
    st.info("💡 Questa sezione serve a spiegare ai professori o ai visitatori del sito le varie fasi del codice e i test che abbiamo effettuato.")

    # CASELLA DI TESTO 4: SYSTEM INSTRUCTION (IL CUORE DEL BOT)
    with st.expander("🧠 SYSTEM INSTRUCTION", expanded=False):
        st.markdown("""
        *Il prompt del chatbot è la parte più importante del progetto. I cambiamenti che abbiamo apportato all'IA sono diversi. Il tono che userà sarà professionale, non troppo amichevole perché l'obiettivo del chatbot è quello di spronare il ragazzo a parlarne con amici, genitori o professori.
        Inoltre dovrà consigliare sempre di parlarne con amici e genitori e di citare solo quando necessario la legge 71/2017. L'IA deve saper riconoscere atti di bullismo da semplici scherzi tra amici in modo tale da non fare errori e dare informazioni sbagliate.*
        """)
        st.code("""
# Esempio di come passiamo le regole al modello Gemini
config=types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION
)
        """, language="python")

    # ==============================================================================
    # AREA TEST EFFETTUATI CON L'INTELLIGENZA ARTIFICIALE
    # ==============================================================================
    with st.expander("🧪 TEST EFFETTUATI & ANALISI", expanded=True):
        st.markdown("### 📋 Registro dei Test di Conversazione")
        st.write("In questa sezione abbiamo inserito alcuni test reali fatti con l'IA per verificare se rispetta le regole imposte.")
        
        # --- BLOCCO TEST 1 ---
        st.markdown("#### 🔹 Test Caso 1: Bullismo esplicito e realistico")

        st.markdown("""
        > **Studente:** *Ciao sono uno studente delle superiori, i miei compagni di classe continuano a prendermi in giro dall'inizio dell'anno e continuano anche se gli dico di fermarsi. Ieri hanno esagerato: mi hanno fatto una foto mentre ero in bagno e l'hanno pubblicata online, adesso sono lo zimbello di tutta la scuola.*
        > 
        > **Risposta Chatbot:** *Mi dispiace molto sentire ciò che stai vivendo. Comprendo che questa situazione ti stia causando un grande disagio e umiliazione, e voglio subito chiarire che ciò che ti è accaduto è un atto grave e inaccettabile di bullismo e cyberbullismo.*
        > *I tuoi compagni ti prendono in giro da inizio anno e non si fermano nonostante le tue richieste, e l'episodio della foto scattata in bagno e pubblicata online è una chiara violazione della tua privacy e della tua dignità. Questo tipo di comportamento, che ti espone al pubblico ludibrio e ti fa sentire lo "zimbello di tutta la scuola", è proprio ciò che la legge italiana intende per cyberbullismo e bullismo.*
        > *È fondamentale che tu sappia che esistono strumenti e supporti per affrontare questa situazione. La Legge 71/2017, infatti, è stata istituita proprio per contrastare il fenomeno del cyberbullismo. Questa legge riconosce l'importanza di proteggere le vittime e prevede misure per la rimozione dei contenuti offensivi. In particolare, se sei minorenne e subisci atti di cyberbullismo, puoi chiedere direttamente al gestore del sito internet o del social media l'oscuramento, la rimozione o il blocco dei dati personali diffusi, se non vuoi o non riesci a farlo con l'aiuto di un adulto. Se la richiesta non viene soddisfatta entro 24 ore, puoi rivolgerti al Garante per la protezione dei dati personali.*
        > *Ecco alcuni passi concreti che ti suggerisco di considerare:*
        > * *Non reagire direttamente online: Evita di rispondere ai commenti o di interagire con chi ha pubblicato o condiviso la foto. Questo potrebbe solo alimentare la situazione.*
        > * *Raccogli prove: Se possibile, fai degli screenshot della foto e dei commenti, indicando la data e l'ora. Queste prove saranno molto utili nel caso in cui tu o gli adulti a cui ti rivolgerai decidiate di intraprendere azioni.*
        > * *Segnala il contenuto: Tutte le piattaforme social hanno funzioni per segnalare contenuti inappropriati, offensivi o che violano la privacy. Segnala la foto e chiedine la rimozione.*
        > * *Parlane immediatamente con un adulto di cui ti fidi: Questo è il passo più importante. Non devi affrontare questa situazione da solo.*
        > * *Genitori o altri familiari: Sono le prime persone che possono offrirti supporto emotivo e pratico.*
        > * *Professori o il coordinatore di classe: A scuola ci sono figure professionali che possono intervenire. La scuola ha il dovere di proteggerti e di attivare un protocollo anti-bullismo se necessario. Cerca di parlare con un professore di cui ti fidi, con il referente per il bullismo/cyberbullismo della tua scuola (se presente) o direttamente con il Dirigente Scolastico.*
        > * *Chiedi di attivare il protocollo anti-bullismo: Molte scuole hanno procedure specifiche per gestire questi casi, che possono includere colloqui con gli studenti coinvolti e azioni disciplinari.*
        > * *Parlane con amici o compagni di classe di cui ti fidi: Condividere il tuo peso con persone della tua età che ti supportano può aiutarti a sentirti meno solo e a trovare forza.*
        > * *Capisco che possa essere difficile parlare di un episodio così imbarazzante, ma è l'unico modo per fermare questa situazione e proteggerti. Ricorda che la vergogna non deve essere tua, ma di chi ha compiuto un'azione così grave.*
        > * *Per aiutarmi a darti consigli ancora più specifici, potresti dirmi:*
        >   1. *Su quale piattaforma online è stata pubblicata la foto?*
        >   2. *Hai già provato a segnalarla o a chiederne la rimozione?*
        >   3. *Come ti senti adesso, oltre ad essere umiliato? C'è qualcos'altro che ti preoccupa in particolare?*
        """)

        # Box di riflessione per il Test 1
        st.markdown("""
        **Commento e Riflessione sul Test 1:**
        *Il chatbot sul test del caso reale di cyberbullismo ha risposto esattamente come ci aspettavamo e volevamo. Ha riconosciuto l'atto di bullismo e cyberbullismo, ha citato la legge 71/2017 ed ha consigliato di andare a parlarne con genitori o amici.*
        """)
        
        # --- BLOCCO TEST 2 ---
        st.markdown("#### 🔹 Test Caso 2: Dinamiche relazionali ordinarie (Assenza di bullismo o cyberbullismo)")
        st.markdown("""
        > **Studente:** *Ieri ho litigato con un mio compagno di classe su delle idee politiche, è stato un dibattito molto acceso visto che ci siamo tutti e due urlati contro e abbiamo alzato i toni. Non so veramente cosa fare perché sono arrabbiatissimo con lui.*
        > 
        > **Risposta Chatbot:** *Comprendo che sia arrabbiato a causa del litigio con il suo compagno di classe. È naturale provare forti emozioni dopo un dibattito acceso, soprattutto quando si alzano i toni.*
        > *Dalla sua descrizione, sembrerebbe che si sia trattato di un litigio o un disaccordo intenso su questioni politiche, in cui entrambe le parti hanno espresso le proprie idee in modo veemente. Entrambi avete urlato e alzato i toni.*
        > *È importante distinguere un singolo litigio, anche se molto animato e spiacevole, da un atto di bullismo o cyberbullismo. Il bullismo, infatti, si caratterizza generalmente per:*
        > * *Ripetitività: non è un episodio isolato, ma azioni che si verificano nel tempo.*
        > * *Intenzionalità: c'è la volontà di arrecare un danno, intimidire o umiliare.*
        > * *Squilibrio di potere: una parte ha o percepisce di avere più potere sull'altra, rendendo difficile per la vittima difendersi.*
        > * *In base a quanto ha raccontato, questo episodio sembra essere un confronto mutualmente acceso piuttosto che un atto di bullismo. Nonostante ciò, il fatto che lei si senta "arrabbiatissimo" indica che la situazione le ha causato un notevole disagio.*
        > * *Per aiutarla meglio, potrei farle alcune domande per capire se ci sono aspetti che non sono emersi:*
        >   1. *Questo tipo di discussioni accese con questo compagno è un evento isolato o si verificano spesso?*
        >   2. *Ci sono stati altri episodi in cui si è sentito preso di mira o attaccato verbalmente (o in altri modi) da questo compagno o da altri, magari non solo su questioni politiche?*
        >   3. *Il litigio ha avuto altre conseguenze, ad esempio ha notato che lui o altri hanno iniziato a escluderla, denigrarla o diffondere voci sul suo conto?*
        > * *Indipendentemente dal fatto che si tratti o meno di bullismo, gestire la rabbia e i conflitti in modo costruttivo è fondamentale. Potrebbe essere utile provare a riflettere su cosa la rende così arrabbiato e se ci sono modi per comunicare le sue idee in futuro senza arrivare a tali livelli di tensione.*
        > * *Le suggerisco di parlare di quanto accaduto con qualcuno di cui si fida. Potrebbe essere un genitore, un insegnante, un amico o un altro adulto di riferimento. Condividere le sue emozioni e ricevere un punto di vista esterno può aiutarla a elaborare la rabbia e a trovare un modo per affrontare la situazione, sia che si tratti di un chiarimento con il suo compagno o di una gestione più efficace dei suoi sentimenti.*
        """)
        
        # Box di riflessione per il Test 2
        st.markdown("""
        **Commento e Riflessione sul Test 2:**
        *Nel secondo test abbiamo messo alla prova il chatbot con una situazione in cui non è presente il cyberbullismo o il bullismo. L'IA è riuscita a riconoscere che non si trattava di un caso di bullismo ma solo di un litigio tra amici.
        Nel farlo ha messo in guardia l'utente su quali sono i casi per cui si può parlare di bullismo informandolo anche su come comportarsi.*
        """)

        # --- BLOCCO TEST 3 ---
        st.markdown("#### 🔹 Test Caso 3: Caso ambiguo di cyberbullismo e bullismo")
        
        st.markdown("""
        > **Studente:** *Ieri siamo andati in gita e dei miei compagni di classe mentre stavamo scherzando facendo delle sciocchezze tutti insieme mi hanno fatto delle foto e mandate sul gruppo di classe, non so se arrabbiarmi o lasciar perdere.*
        > 
        > **Risposta Chatbot:** *Comprendo la sua incertezza riguardo a questa situazione e capisco che si trovi a riflettere su come comportarsi. È importante distinguere tra uno scherzo innocuo e un comportamento che potrebbe causare disagio o sfociare in qualcosa di più serio.*
        > *Per aiutarla a capire meglio la natura di ciò che è accaduto, avrei bisogno di qualche dettaglio in più:*
        > * *Era consapevole che le foto venissero scattate? E le era stato chiesto il permesso di condividerle sul gruppo di classe?*
        > * *Che tipo di "sciocchezze" stavate facendo? Le foto la ritraevano in una situazione che potrebbe metterla in imbarazzo o che le sembra in qualche modo umiliante, o erano semplicemente momenti di leggerezza condivisa?*
        > * *Qual è stata la reazione nel gruppo di classe dopo la pubblicazione delle foto? Ci sono stati commenti negativi, prese in giro, o la situazione è stata accolta con spirito giocoso da tutti?*
        > * *Come si sente lei, in questo momento, riguardo al contenuto specifico delle foto e al fatto che siano state condivise? Si sente ferito, a disagio, o semplicemente confuso?*
        > * *Le risposte a queste domande sono fondamentali per valutare se si tratti di un semplice scherzo, magari fatto senza cattiveria ma che l'ha comunque messa a disagio, o se invece ci sia qualcosa di più vicino a un atto di cyberbullismo. Il confine a volte può essere sottile, ma la sua percezione e il suo disagio sono sempre importanti.*
        """)
        
        # Box di riflessione per il Test 3
        st.markdown("""
        **Commento e Riflessione sul Test 3:**
        *Nel terzo test abbiamo inserito un prompt in cui non si capisce se si tratta di cyberbullismo. L'IA ha risposto cercando di capire come si sente l'utente facendo domande per approfondire la situazione in modo tale da capire se si tratta di un caso di bullismo.
        Come nei casi precedenti ha spiegato quali sono i comportamenti che possono essere rimandati ad atti di bullismo e cyberbullismo e come comportarsi se li dovesse subire.*
        """)
        
        st.write("---") # Linea di divisione tra i test

    # CASELLA DI TESTO 5: CONCLUSIONI / COSA ABBIAMO IMPARATO
    st.subheader("🎯 Riflessioni Finali")
    st.markdown("""
    *Una criticità che abbiamo riportato è che il chatboto in ogni situazione ripete sempre le stesse cose e ciò che consiglia deve essere sempre interpretato, perché non avendo la parte umana non potremmo essere sicurti della risposta che darà per all'IA perché non può vedere la comunicazione non verbale, importante per capire cosa prova veramente una persona.
    Il rischio più grande che abbiamo cercato di evitare è rendere il chatbot troppo amichevole. Questo potrebbe provocare nel ragazzo un effetto contrario di chiusura verso il mondo reale. Questo perché reputerà che le risposte del chatbot siano vere e sincere come quelle di un amico, quindi preferirà parlare con un'intelligenza artificiale che con una persona reale perché pensa che lo capisca meglio.*
    """)
