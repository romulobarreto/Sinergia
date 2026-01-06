import sqlite3
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from pathlib import Path

# Define o caminho do .env (mesma lógica do Django)
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

# --- CONFIGURAÇÕES VIA ENV ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Tabelas que queremos sincronizar
TABELAS = [
    'register_type',
    'register_team',
    'register_customuser',
    'register_service'
]

def get_sqlite_data(table_name):
    # Usa o BASE_DIR para garantir que ele ache o db.sqlite3 no lugar certo
    conn = sqlite3.connect(BASE_DIR / 'db.sqlite3')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def sync():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Erro: SUPABASE_URL ou SUPABASE_KEY não encontradas no .env")
        return

    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    for tabela in TABELAS:
        print(f"🔄 Sincronizando {tabela}...")
        dados = get_sqlite_data(tabela)
        
        if not dados:
            print(f"⚠️  Tabela {tabela} vazia no SQLite.")
            continue

        batch_size = 500
        total = len(dados)
        for i in range(0, total, batch_size):
            batch = dados[i:i + batch_size]
            # .upsert() garante que não duplique dados
            supabase.table(tabela).upsert(batch).execute()
            print(f"✅ Enviados {min(i + batch_size, total)}/{total} registros para {tabela}")

if __name__ == "__main__":
    print("🚀 Iniciando sincronização segura SQLite → Supabase...")
    sync()
    print("🎉 Sincronização concluída!")