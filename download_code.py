import requests
from bs4 import BeautifulSoup
import re
import json
import os
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    try:
        import pdfplumber
        print(f"Duke lexuar PDF me pdfplumber: {pdf_path}")
        text_parts = []
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Numri i faqeve: {len(pdf.pages)}")
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
                if (i + 1) % 50 == 0:
                    print(f"  Faqet e lexuara: {i + 1}/{len(pdf.pages)}")
        
        full_text = '\n'.join(text_parts)
        print(f"Teksti i nxjerrë: {len(full_text)} karaktere")
        return full_text
    
    except ImportError:
        try:
            import PyPDF2
            print(f"Duke lexuar PDF me PyPDF2: {pdf_path}")
            text_parts = []
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                print(f"Numri i faqeve: {len(pdf_reader.pages)}")
                for i, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
                    if (i + 1) % 50 == 0:
                        print(f"  Faqet e lexuara: {i + 1}/{len(pdf_reader.pages)}")
            
            full_text = '\n'.join(text_parts)
            print(f"Teksti i nxjerrë: {len(full_text)} karaktere")
            return full_text
        
        except ImportError:
            print("Gabim: Duhet të instaloni pdfplumber ose PyPDF2")
            print("Ekzekutoni: pip install pdfplumber PyPDF2")
            return None
    
    except Exception as e:
        print(f"Gabim gjatë leximit të PDF: {e}")
        return None

def download_criminal_code(url=None):
    import requests
    
    if url is None:
        base_url = "https://pp.gov.al"
        possible_urls = [
            f"{base_url}/kodet/kodi-penal",
            f"{base_url}/kodi-penal",
            f"{base_url}/legjislacioni/kodi-penal",
        ]
    else:
        possible_urls = [url]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for url_to_try in possible_urls:
        try:
            print(f"Tentojmë të shkarkojmë nga: {url_to_try}")
            response = requests.get(url_to_try, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for script in soup(["script", "style"]):
                script.decompose()
            
            text = soup.get_text()
            
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            if len(text) > 1000:
                print(f"Shkarkimi i suksesshëm! Gjithsej {len(text)} karaktere.")
                return text
            else:
                print(f"Teksti i shkarkuar është shumë i shkurtër ({len(text)} karaktere).")
        
        except requests.RequestException as e:
            print(f"Gabim gjatë shkarkimit nga {url_to_try}: {e}")
            continue
    
    print("\nShkarkimi automatik dështoi.")
    print("Ju lutem shkarkoni manualisht tekstin dhe ruajeni në data/criminal_code_raw.txt")
    return None

def parse_articles_from_text(text):
    articles = []
    
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    
    article_pattern = r'(?:^|\n)\s*(?:Neni|Artikulli|ARTIKULLI|NENI)\s+(\d+)[\.\)\/]?\s*(.*?)(?=(?:^|\n)\s*(?:Neni|Artikulli|ARTIKULLI|NENI)\s+\d+[\.\)\/]?|$)'
    
    matches = re.finditer(article_pattern, text, re.DOTALL | re.IGNORECASE | re.MULTILINE)
    
    for match in matches:
        article_num = match.group(1)
        article_text = match.group(2).strip()
        
        article_text = re.sub(r'\s+', ' ', article_text)
        article_text = re.sub(r'\n+', ' ', article_text)
        article_text = article_text.strip()
        
        if article_text and len(article_text) > 20:
            try:
                articles.append({
                    "number": int(article_num),
                    "text": article_text,
                    "full_text": f"Neni {article_num}. {article_text}"
                })
            except ValueError:
                continue
    
    articles.sort(key=lambda x: x['number'])
    
    return articles

def save_articles(articles, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(articles)} articles to {output_file}")

def main():
    from config import DATA_DIR, ARTICLES_JSON
    
    print("=" * 60)
    print("Shkarkuesi i Kodit Penal")
    print("=" * 60)
    
    pdf_files = []
    current_dir_pdf = "Ligj nr. 7895-1995- Kodi penal -i përditësuar.pdf"
    data_dir_pdf = os.path.join(DATA_DIR, "Ligj nr. 7895-1995- Kodi penal -i përditësuar.pdf")
    
    if os.path.exists(current_dir_pdf):
        pdf_files.append(current_dir_pdf)
    if os.path.exists(data_dir_pdf):
        pdf_files.append(data_dir_pdf)
    
    if not pdf_files:
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.lower().endswith('.pdf') and 'penal' in file.lower():
                    pdf_files.append(os.path.join(root, file))
                    break
    
    text = None
    
    if pdf_files:
        pdf_path = pdf_files[0]
        print(f"\nU gjet PDF: {pdf_path}")
        text = extract_text_from_pdf(pdf_path)
        
        raw_file = os.path.join(DATA_DIR, "criminal_code_raw.txt")
        if text:
            os.makedirs(DATA_DIR, exist_ok=True)
            with open(raw_file, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Teksti u ruajt në: {raw_file}")
    
    if text is None:
        print("\nDuke tentuar shkarkim nga web...")
        text = download_criminal_code()
    
    if text is None:
        raw_file = os.path.join(DATA_DIR, "criminal_code_raw.txt")
        if os.path.exists(raw_file):
            print(f"\nDuke lexuar nga dosja ekzistuese: {raw_file}")
            with open(raw_file, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            print(f"\nDosja e tekstit nuk u gjet: {raw_file}")
            print("\nJu lutem:")
            print("1. Vendosni PDF-në e Kodit Penal në dosjen e projektit")
            print("2. Ose vendosni tekstin në data/criminal_code_raw.txt")
            print("3. Ose ekzekutoni përsëri këtë skript")
            return
    
    print(f"\nDuke përpunuar tekstin ({len(text)} karaktere)...")
    articles = parse_articles_from_text(text)
    
    if articles:
        save_articles(articles, ARTICLES_JSON)
        print(f"\n✓ U përpunuan me sukses {len(articles)} artikuj!")
        print(f"✓ Artikujt u ruajtën në {ARTICLES_JSON}")
        
        if articles:
            print(f"\nStatistika:")
            print(f"  Artikulli më i vogël: {min(a['number'] for a in articles)}")
            print(f"  Artikulli më i madh: {max(a['number'] for a in articles)}")
            print(f"  Numri total i artikujve: {len(articles)}")
        
        print("\nHapi tjetër: Ekzekutoni 'python create_index.py' për të krijuar indeksin.")
    else:
        print("\n✗ Nuk u gjetën artikuj. Ju lutem kontrolloni formatin e tekstit.")
        print("Artikujt duhet të fillojnë me 'Neni' ose 'Artikulli' e ndjekur nga një numër.")
        print("\nShembull:")
        print("  Neni 1. Ky kod rregullon...")
        print("  Artikulli 2. Vrasja është...")
        print("\nNëse keni PDF, sigurohuni që të keni instaluar: pip install pdfplumber PyPDF2")

if __name__ == "__main__":
    main()
