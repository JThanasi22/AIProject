# Dosjet e të Dhënave

Ky dosje përmban të gjitha dosjet e të dhënave të sistemit.

## Dosjet e Nevojshme

### 1. `criminal_code_raw.txt`
Teksti i papërpunuar i Kodit Penal të Shqipërisë. Duhet të shkarkoni këtë nga pp.gov.al dhe ta vendosni këtu.

**Format i pritur:**
Teksti duhet të ketë artikuj që fillojnë me "Neni" ose "Artikulli" e ndjekur nga një numër.

**Shembull:**
```
Neni 1. Ky kod rregullon...
Neni 2. Vrasja është...
Artikulli 3. Dënimet janë...
```

### 2. `articles.json` (krijohet automatikisht)
Artikujt e strukturuar në format JSON. Krijohet nga `download_code.py`.

### 3. `embeddings.npy` (krijohet automatikisht)
Embeddings të artikujve. Krijohet nga `create_index.py`.

### 4. `faiss_index.index` (krijohet automatikisht)
Indeksi FAISS për kërkim të shpejtë. Krijohet nga `create_index.py`.

### 5. `embeddings_metadata.json` (krijohet automatikisht)
Metadata për artikujt. Krijohet nga `create_index.py`.

## Si të merrni të dhënat

1. Vizitoni https://pp.gov.al
2. Gjeni faqen e Kodit Penal
3. Kopjoni të gjithë tekstin
4. Ruajeni në `criminal_code_raw.txt`
5. Ekzekutoni `python download_code.py`

## Shënim

Të gjitha dosjet përveç `criminal_code_raw.txt` krijohen automatikisht nga skriptet e projektit.
