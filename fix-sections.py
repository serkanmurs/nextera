filepath = 'src/app/page.tsx'
content = open(filepath, 'r').read()

print("Guncelleme basliyor...")

# 1. PROGRAMLAR BOLUMUNU KALDIR
old_programs = '''      {/* Programlar */}
      <div style={cardStyle}>
        <h3 style={{ margin: "0 0 14px", fontSize: 16, fontWeight: 800, color: COLORS.text }}>Programlar</h3>
        <div style={{ display: "flex", flexDirection: "column" as const, gap: 12 }}>
          <div style={{ padding: 16, borderRadius: 12, border: "1px solid #E2E8F0", background: "#FAFAFA" }}>
            <div style={{ fontWeight: 700, fontSize: 14, color: COLORS.primary, marginBottom: 4 }}>NextERA Student</div>
            <div style={{ fontSize: 12, color: COLORS.textLight, lineHeight: 1.5 }}>Ogrenciler ve yeni mezunlar icin. SWOT Analizi, Degerler Calismasi, Yasam Cemberi, CV & LinkedIn, Hedefler & Vizyon. 4 veya 6 seanslik programlar.</div>
          </div>
          <div style={{ padding: 16, borderRadius: 12, border: "1px solid #E2E8F0", background: "#FAFAFA" }}>
            <div style={{ fontWeight: 700, fontSize: 14, color: COLORS.primary, marginBottom: 4 }}>NextERA Professional</div>
            <div style={{ fontSize: 12, color: COLORS.textLight, lineHeight: 1.5 }}>Profesyoneller icin. Kariyer SWOT Analizi, Degerler Analizi, Vizyon & Misyon, Gelisim Plani Takibi, CV & LinkedIn Danismanligi. 4 veya 6 seanslik programlar.</div>
          </div>
        </div>
        <div style={{ marginTop: 12, padding: "10px 14px", borderRadius: 10, background: "#FFF7ED", border: "1px solid #FED7AA" }}>
          <div style={{ fontSize: 12, color: "#92400E", fontWeight: 600 }}>Ucretsiz Tanisma: 40 dk Kimya Seansi ile hedef ve beklenti analizi</div>
        </div>
      </div>'''

# Turkce karakterli versiyon
old_programs2 = '''      {/* Programlar */}
      <div style={cardStyle}>
        <h3 style={{ margin: "0 0 14px", fontSize: 16, fontWeight: 800, color: COLORS.text }}>\u00f0\u009f\u0093\u008b Programlar</h3>'''

# En guvenli yol: satirlari bulalim
import re

# Programlar blogu
prog_start = content.find('{/* Programlar */}')
if prog_start > -1:
    # Blogun sonunu bul - sonraki {/* ile baslayan yorum veya </div> kapanisi
    # Programlar karti icinde 3 tane </div> var, sonra ana </div>
    depth = 0
    i = content.find('<div style={cardStyle}>', prog_start)
    if i > -1:
        j = i
        found_end = -1
        while j < len(content):
            if content[j:j+4] == '<div':
                depth += 1
            elif content[j:j+6] == '</div>':
                depth -= 1
                if depth == 0:
                    found_end = j + 6
                    break
            j += 1
        if found_end > -1:
            # Remove from {/* Programlar */} to end of card div + newlines
            remove_start = prog_start
            remove_end = found_end
            # Skip trailing whitespace/newlines
            while remove_end < len(content) and content[remove_end] in '\n\r \t':
                remove_end += 1
            content = content[:remove_start] + content[remove_end:]
            print("  OK 1. Programlar bolumu kaldirildi")
        else:
            print("  SKIP 1a. Programlar div sonu bulunamadi")
    else:
        print("  SKIP 1b. Programlar cardStyle bulunamadi")
else:
    print("  SKIP 1c. Programlar yorumu bulunamadi")

# 2. HAKKIMDA BOLUMUNU KALDIR
about_start = content.find('{/* Hakkımda */}')
if about_start == -1:
    about_start = content.find('{/* Hakkimda */}')
if about_start == -1:
    # Daha genis ara
    about_start = content.find('Hakkında</h3>')
    if about_start > -1:
        # Geriye git, div basini bul
        about_start = content.rfind('{/*', 0, about_start)

if about_start > -1:
    i = content.find('<div style={cardStyle}>', about_start)
    if i > -1:
        depth = 0
        j = i
        found_end = -1
        while j < len(content):
            if content[j:j+4] == '<div':
                depth += 1
            elif content[j:j+6] == '</div>':
                depth -= 1
                if depth == 0:
                    found_end = j + 6
                    break
            j += 1
        if found_end > -1:
            remove_start = about_start
            remove_end = found_end
            while remove_end < len(content) and content[remove_end] in '\n\r \t':
                remove_end += 1
            content = content[:remove_start] + content[remove_end:]
            print("  OK 2. Hakkimda bolumu kaldirildi")
        else:
            print("  SKIP 2a. Hakkimda div sonu bulunamadi")
    else:
        print("  SKIP 2b. Hakkimda cardStyle bulunamadi")
else:
    print("  SKIP 2c. Hakkimda yorumu bulunamadi")

# 3. GELISIM GUNLUGU - Samsung Notes tarzina donustur
# Mevcut gunluk blogu: kategori butonlari + textarea
# Yeni: textarea + "Kaydet" butonu + tarih gosterimi

old_journal_title = '''Gelisim Gunlugum</h3>
        <p style={{ margin: "0 0 12px", fontSize: 12, color: COLORS.textLight }}>Seans sonrasi farkindaliklairni, kararlarini ve aksiyonlarini not et.</p>'''

# Daha esnek arama
journal_start = content.find('Gunlugum</h3>')
if journal_start == -1:
    journal_start = content.find('Günlüğüm</h3>')

if journal_start > -1:
    # Tum journal kartini bul
    card_start = content.rfind('{/*', 0, journal_start)
    if card_start == -1:
        card_start = content.rfind('<div style={cardStyle}>', 0, journal_start)
    
    # Kartın sonunu bul
    i = content.find('<div style={cardStyle}>', card_start)
    if i > -1:
        depth = 0
        j = i
        found_end = -1
        while j < len(content):
            if content[j:j+4] == '<div':
                depth += 1
            elif content[j:j+6] == '</div>':
                depth -= 1
                if depth == 0:
                    found_end = j + 6
                    break
            j += 1
        
        if found_end > -1:
            new_journal = '''<div style={cardStyle}>
        <h3 style={{ margin: "0 0 14px", fontSize: 16, fontWeight: 800, color: COLORS.text }}>Gelisim Gunlugum</h3>
        <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
          <textarea id="journalInput" placeholder="Bugunku farkindaligini, kararini veya aksiyonunu yaz..." style={{ flex: 1, padding: "12px 14px", borderRadius: 10, border: "1.5px solid #E2E8F0", fontSize: 13, outline: "none", boxSizing: "border-box" as const, minHeight: 70, resize: "vertical" as const, fontFamily: "inherit" }} />
        </div>
        <div style={{ display: "flex", gap: 6, flexWrap: "wrap" as const }}>
          {["farkindalik", "karar", "aksiyon"].map(cat => (
            <button key={cat} onClick={() => { const inp = document.getElementById("journalInput") as HTMLTextAreaElement; if (inp?.value.trim()) { onAddJournal(inp.value.trim(), cat); inp.value = ""; } }} style={{ padding: "8px 14px", borderRadius: 8, border: "1.5px solid #E2E8F0", background: cat === "farkindalik" ? "#FEF3C7" : cat === "karar" ? "#DBEAFE" : "#D1FAE5", fontSize: 12, fontWeight: 600, cursor: "pointer", color: cat === "farkindalik" ? "#92400E" : cat === "karar" ? "#1E40AF" : "#065F46" }}>
              {cat === "farkindalik" ? "Farkindalik Kaydet" : cat === "karar" ? "Karar Kaydet" : "Aksiyon Kaydet"}
            </button>
          ))}
        </div>
        {journal.length > 0 && (
          <div style={{ marginTop: 16 }}>
            {journal.map(j => (
              <div key={j.id} style={{ padding: "14px", marginBottom: 8, borderRadius: 12, background: "#FAFAFA", border: "1px solid #F1F5F9" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
                  <span style={{ fontSize: 12, fontWeight: 700, color: j.category === "farkindalik" ? "#D97706" : j.category === "karar" ? "#1E40AF" : "#059669", background: j.category === "farkindalik" ? "#FEF3C7" : j.category === "karar" ? "#DBEAFE" : "#D1FAE5", padding: "3px 8px", borderRadius: 6 }}>
                    {j.category === "farkindalik" ? "Farkindalik" : j.category === "karar" ? "Karar" : "Aksiyon"}
                  </span>
                  <span style={{ fontSize: 11, color: COLORS.textLight }}>{new Date(j.created_at).toLocaleDateString("tr-TR", { day: "numeric", month: "long", year: "numeric" })} - {new Date(j.created_at).toLocaleTimeString("tr-TR", { hour: "2-digit", minute: "2-digit" })}</span>
                </div>
                <div style={{ fontSize: 14, color: COLORS.text, lineHeight: 1.6 }}>{j.note}</div>
              </div>
            ))}
          </div>
        )}
      </div>'''
            
            # Eski comment dahil replace
            replace_start = card_start
            content = content[:replace_start] + new_journal + content[found_end:]
            print("  OK 3. Gelisim Gunlugu Samsung Notes tarzina donusturuldu")
        else:
            print("  SKIP 3a. Journal kart sonu bulunamadi")
    else:
        print("  SKIP 3b. Journal cardStyle bulunamadi")
else:
    print("  SKIP 3c. Journal basligi bulunamadi")

# SAVE
open(filepath, 'w').write(content)
print("")
print("Tamamlandi! Simdi: npm run build")
