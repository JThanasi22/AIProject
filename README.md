# Asistenti i Kodit Penal të Shqipërisë

Një asistent inteligjent dixhital që përgjigjet pyetjeve në shqip për Kodin Penal të Shqipërisë, bazuar në artikujt zyrtarë.

## 📋 Përmbajtja

- [Përshkrimi](#përshkrimi)
- [Teknologjitë e Përdorura](#teknologjitë-e-përdorura)
- [Instalimi](#instalimi)
- [Përdorimi](#përdorimi)
- [Struktura e Projektit](#struktura-e-projektit)
- [Shembuj Pyetje-Përgjigje](#shembuj-pyetje-përgjigje)
- [Arhitektura e Sistemit](#arhitektura-e-sistemit)

## 🎯 Përshkrimi

Ky projekt është një sistem inteligjent që përdor inteligjencën artificiale për të përgjigjur pyetjeve në shqip rreth Kodit Penal të Shqipërisë. Sistemi:

1. **Shkarkon dhe përpunon** tekstin e Kodit Penal nga faqja zyrtare
2. **Ndan tekstin në artikuj** dhe i ruan në format strukturor (JSON)
3. **Krijon embeddings** për çdo artikull duke përdorur modele të avancuara AI
4. **Ndërton një indeks FAISS** për kërkim të shpejtë të artikujve më të ngjashëm
5. **Përgjigjet pyetjeve** duke gjetur artikujt më relevante dhe duke krijuar përgjigje të kuptueshme
6. **Ofron një ndërfaqe web** moderne dhe të lehtë për t'u përdorur

## 🛠 Teknologjitë e Përdorura

### Backend
- **Python 3.8+** - Gjuhë programimi kryesore
- **Flask** - Framework për aplikacionin web
- **Sentence Transformers** - Për krijimin e embeddings në gjuhën shqipe
- **FAISS (Facebook AI Similarity Search)** - Për indeksimin dhe kërkimin e shpejtë të artikujve të ngjashëm
- **BeautifulSoup4** - Për parsing të faqeve web
- **NumPy** - Për operacione matematikore me vektorë

### Frontend
- **HTML5** - Struktura e faqes
- **CSS3** - Stilizimi modern dhe responsive
- **JavaScript (Vanilla)** - Logjika e chat-it dhe komunikimi me backend

### AI/ML
- **Multilingual Sentence Transformers** - Model që mbështet gjuhën shqipe
- **Vector Similarity Search** - Për gjetjen e artikujve më të ngjashëm
- **Semantic Search** - Kërkim bazuar në kuptim, jo vetëm fjalë

## 📦 Instalimi

### Kërkesat
- Python 3.8 ose më i lartë
- pip (Python package manager)

### Hapat e Instalimit

1. **Kloni ose shkarkoni projektin**
```bash
cd "Project AI"
```

2. **Krijoni një mjedis virtual (rekomandohet)**
```bash
python3 -m venv venv
source venv/bin/activate  # Në Windows: venv\Scripts\activate
```

3. **Instaloni varësitë**
```bash
pip install -r requirements.txt
```

4. **Shkarkoni dhe përpunoni Kodin Penal**

   Sistemi mbështet tre mënyra për të marrë tekstin e Kodit Penal:
   
   **Opsioni A: PDF File (Rekomandohet)**
   - Vendosni PDF-në e Kodit Penal në dosjen e projektit
   - Skripti do ta gjejë automatikisht dhe do ta përpunojë
   - Ekzekutoni: `python download_code.py`
   
   **Opsioni B: Tekst File**
   - Shkarkoni tekstin nga https://pp.gov.al
   - Ruajeni në `data/criminal_code_raw.txt`
   - Ekzekutoni: `python download_code.py`
   
   **Opsioni C: Shkarkim Automatik**
   - Përditësoni URL-në në `download_code.py` nëse dihet
   - Ekzekutoni: `python download_code.py`

   Pastaj, ekzekutoni:
```bash
python download_code.py
```

5. **Krijoni indeksin FAISS**
```bash
python create_index.py
```

6. **Nisni aplikacionin web**
```bash
python app.py
```

7. **Hapni shfletuesin**
   Shkoni te: http://localhost:5000

## 🚀 Përdorimi

### Përmes Ndërfaqes Web

1. Hapni aplikacionin në shfletuesin tuaj
2. Shkruani pyetjen tuaj në shqip në kutinë e tekstit
3. Klikoni "Dërgo" ose shtypni Enter
4. Lexoni përgjigjen dhe artikujt e cituar

### Përmes Python API

```python
from chatbot import CriminalCodeAssistant

# Inicializoni asistentin
assistant = CriminalCodeAssistant()

# Bëni një pyetje
question = "Çfarë është vrasja dhe si dënohet?"
result = assistant.generate_answer(question)

print(result['answer'])
for article in result['articles']:
    print(f"\nArtikulli {article['article_number']}: {article['article_text']}")
```

## 📁 Struktura e Projektit

```
Project AI/
│
├── app.py                 # Aplikacioni Flask kryesor
├── chatbot.py             # Logjika e chatbot-it
├── config.py              # Konfigurime
├── download_code.py       # Skript për shkarkim dhe parsing
├── create_index.py        # Skript për krijimin e indeksit FAISS
├── requirements.txt       # Varësitë Python
├── README.md             # Dokumentacioni
│
├── data/                 # Dosjet e të dhënave
│   ├── criminal_code_raw.txt  # Teksti i papërpunuar
│   ├── articles.json          # Artikujt e strukturuar
│   ├── embeddings.npy         # Embeddings të artikujve
│   ├── faiss_index.index      # Indeksi FAISS
│   └── embeddings_metadata.json
│
├── templates/            # Template-et HTML
│   └── index.html
│
└── static/              # Asetet statike
    ├── css/
    │   └── style.css
    └── js/
        └── chat.js
```

## 💬 Shembuj Pyetje-Përgjigje

### Shembull 1: Pyetje për vrasjen
**Pyetje:** "Çfarë është vrasja dhe si dënohet?"

**Përgjigje:**
```
Bazuar në Kodin Penal të Shqipërisë, këtu janë informacionet relevante:

**Artikulli 78:**
Vrasja e qëllimshme është vepër penale e rëndë dhe dënohet me burgim...

**Artikulli 79:**
Vrasja në rrethana të rënda dënohet me burgim...

Këto janë artikujt më të përshtatshëm që lidhen me pyetjen tuaj.
```

### Shembull 2: Pyetje për vjedhjen
**Pyetje:** "Si dënohet vjedhja?"

**Përgjigje:**
```
Bazuar në Kodin Penal të Shqipërisë, këtu janë informacionet relevante:

**Artikulli 134:**
Vjedhja është marrja e pasurisë së tjetrit pa pëlqimin e tij...

**Artikulli 135:**
Vjedhja dënohet me gjobë ose me burgim deri në tre vjet...

Këto janë artikujt më të përshtatshëm që lidhen me pyetjen tuaj.
```

### Shembull 3: Pyetje për shpërblimin
**Pyetje:** "Çfarë është shpërblimi dhe si funksionon?"

**Përgjigje:**
```
Bazuar në Kodin Penal të Shqipërisë, këtu janë informacionet relevante:

**Artikulli 45:**
Shpërblimi është reduktimi i dënimit për veprën penale...

**Artikulli 46:**
Kushtet për dhënien e shpërblimit...

Këto janë artikujt më të përshtatshëm që lidhen me pyetjen tuaj.
```

## 🏗 Arhitektura e Sistemit

### 1. Marrja dhe Përpunimi i të Dhënave

```
pp.gov.al → download_code.py → criminal_code_raw.txt
                                    ↓
                            parse_articles_from_text()
                                    ↓
                            articles.json (strukturor)
```

**Procesi:**
- Teksti shkarkohet nga faqja zyrtare
- Përdoret regex për të identifikuar artikujt (Neni X, Artikulli Y)
- Çdo artikull ruhet si një objekt JSON me numër dhe tekst

### 2. Krijimi i Embeddings dhe Indeksit

```
articles.json → SentenceTransformer → embeddings.npy
                    ↓
            FAISS IndexFlatIP → faiss_index.index
```

**Procesi:**
- Përdoret modeli multilingual `paraphrase-multilingual-MiniLM-L12-v2`
- Çdo artikull konvertohet në një vektor 384-dimensional
- Embeddings normalizohen për cosine similarity
- Indeksi FAISS ndërtohet për kërkim të shpejtë (O(log n))

### 3. Sistemi i Kërkimit dhe Përgjigjes

```
Pyetje e përdoruesit
    ↓
Embedding i pyetjes (SentenceTransformer)
    ↓
Kërkim në FAISS (top-k artikujt më të ngjashëm)
    ↓
Nxjerrja e artikujve relevante
    ↓
Ndërtimi i përgjigjes (me citime)
    ↓
Kthimi i përgjigjes në shqip
```

**Algoritmi:**
1. Pyetja konvertohet në embedding
2. FAISS gjen k artikujt më të ngjashëm (cosine similarity)
3. Artikujt renditen sipas relevancës
4. Përgjigja ndërtohet duke kombinuar informacionin nga artikujt

### 4. Ndërfaqja Web

```
Browser → Flask App (app.py)
            ↓
    chatbot.py (CriminalCodeAssistant)
            ↓
    FAISS Index + Embeddings
            ↓
    Përgjigje JSON
            ↓
    Frontend (HTML/CSS/JS)
```

**Komponentët:**
- **Flask Backend**: Merr kërkesat HTTP dhe kthen përgjigje JSON
- **Frontend**: Ndërfaqe moderne me chat real-time
- **AJAX**: Komunikim asinkron pa ringarkim faqesh

## 🔧 Konfigurimi

Mund të modifikoni `config.py` për të ndryshuar:

- **EMBEDDING_MODEL**: Modeli për embeddings (duhet të mbështetë shqipen)
- **LLM_MODEL**: Modeli për gjenerimin e përgjigjeve (opsional, kërkon OpenAI API)
- **HOST/PORT**: Adresa dhe porta e serverit web

## 📝 Shënime të Rëndësishme

1. **Gjuhë**: Sistemi është i optimizuar për gjuhën shqipe. Modeli i embeddings është multilingual dhe mbështet shqipen.

2. **Saktësia**: Saktësia e përgjigjeve varet nga:
   - Cilësia e tekstit të shkarkuar
   - Strukturimi i saktë i artikujve
   - Relevanca e pyetjes me përmbajtjen

3. **Performanca**: FAISS ofron kërkim shumë të shpejtë edhe me mijëra artikuj.

4. **Zgjerimi**: Sistemi mund të zgjerohet për të mbështetur:
   - Modele LLM lokale (Llama, Mistral, etj.)
   - Integrim me baza të dhënash
   - Historik pyetjesh dhe përgjigjesh
   - Autentifikim përdoruesish

## 🐛 Troubleshooting

### Problemi: "Index file not found"
**Zgjidhje**: Ekzekutoni `python create_index.py` për të krijuar indeksin.

### Problemi: "Articles file not found"
**Zgjidhje**: Ekzekutoni `python download_code.py` dhe sigurohuni që keni tekstin e Kodit Penal në `data/criminal_code_raw.txt`.

### Problemi: "Model download fails"
**Zgjidhje**: Sigurohuni që keni lidhje interneti. Modeli shkarkohet automatikisht herën e parë.

### Problemi: "Port already in use"
**Zgjidhje**: Ndryshoni portin në `config.py` ose mbyllni aplikacionin që përdor portin 5000.

## 📄 Licenca

Ky projekt është krijuar për qëllime edukative dhe informuese. Informacioni i Kodit Penal është i disponueshëm publikisht dhe burimi duhet të citohet siç tregohet.

## 👥 Kontributori

Projekti është krijuar si një sistem inteligjent për ndihmë në kuptimin e Kodit Penal të Shqipërisë.

## 🔮 Zhvillime të Ardhshme

- [ ] Integrim me modele LLM lokale për përgjigje më të sofistikuara
- [ ] Historik pyetjesh dhe përgjigjesh
- [ ] Eksportim i përgjigjeve në PDF
- [ ] API REST për integrim me aplikacione të tjera
- [ ] Mbështetje për dokumente të tjera ligjore
- [ ] Sistem autentifikimi dhe përdorues të shumtë

---

**Burimi i të dhënave**: pp.gov.al - Kodi Penal i Republikës së Shqipërisë
