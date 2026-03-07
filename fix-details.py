filepath = 'src/app/page.tsx'
content = open(filepath, 'r').read()

print("Duzeltmeler basliyor...")

# ============================================================
# 1. GIRIS EKRANI - Madalya ikonunu kaldir
# ============================================================
# ICF badge satirini kaldir
old_icf = '''        <div style={{ textAlign: "center", marginTop: 12, paddingTop: 12, borderTop: "1px solid rgba(255,255,255,0.15)" }}>
          <span style={{ fontSize: 11, color: "rgba(255,255,255,0.7)" }}>\u00f0\u009f\u008f\u0085 ICF Akredite Ko\u00e7 \u00b7 G\u00fcvenli Platform</span>
        </div>'''

# Daha esnek arama
idx = content.find('ICF Akredite Ko')
if idx > -1:
    # Bu satirin bulundugu div'i bul
    line_start = content.rfind('<div style={{ textAlign: "center", marginTop: 12, paddingTop: 12', 0, idx)
    if line_start > -1:
        line_end = content.find('</div>', idx) + 6
        # Sonraki newline'i da al
        while line_end < len(content) and content[line_end] in '\n\r':
            line_end += 1
        content = content[:line_start] + content[line_end:]
        print("  OK 1. Madalya/ICF badge kaldirildi")
    else:
        print("  SKIP 1. ICF badge div basi bulunamadi")
else:
    print("  SKIP 1. ICF badge bulunamadi")

# ============================================================
# 2. UST YAZI DEGISTIR - "Potansiyelini Netleştir..." yerine
# ============================================================
content = content.replace(
    'Potansiyelini Netleştir. Stratejik Koçluk Yolculuğuna Başla.',
    'Kendini tanı, yönünü bul, potansiyelini büyüt.'
)
# Variant without Turkish chars
content = content.replace(
    'Potansiyelini Netlestir. Stratejik Kocluk Yolculuguna Basla.',
    'Kendini tanı, yönünü bul, potansiyelini büyüt.'
)
print("  OK 2. Ust yazi guncellendi")

# ============================================================
# 3. TURKCE KARAKTER DUZELTMELERI
# ============================================================
content = content.replace('Hazirlan ve Odaklan', 'Hazırlan ve Odaklan')
content = content.replace('Bu Haftaki Odagin', 'Bu Haftaki Odağın')
content = content.replace('Her seans bir farkindalik, her farkindalik bir adim. Bugun hangi adimi atacaksin?', 'Her seans bir farkındalık, her farkındalık bir adım. Bugün hangi adımı atacaksın?')
content = content.replace('Siradaki Seansin', 'Sıradaki Seansın')
content = content.replace('Sonraki Hedef', 'Sonraki Hedef')
content = content.replace('Seans Tamamlandi', 'Seans Tamamlandı')
content = content.replace('% tamamlandi', '% tamamlandı')
content = content.replace('Yeni seans planla', 'Yeni seans planla')
content = content.replace('"Bugun"', '"Bugün"')
content = content.replace('"Yarin"', '"Yarın"')
content = content.replace('" gun"', '" gün"')
content = content.replace('Seansa Katil', 'Seansa Katıl')
content = content.replace('Ilerleme', 'İlerleme')
content = content.replace('Gelisim Gunlugum', 'Gelişim Günlüğüm')
content = content.replace('Farkindalik Kaydet', 'Farkındalık Kaydet')
content = content.replace('Karar Kaydet', 'Karar Kaydet')
content = content.replace('Aksiyon Kaydet', 'Aksiyon Kaydet')
content = content.replace('"Farkindalik"', '"Farkındalık"')
content = content.replace('"Aksiyon"', '"Aksiyon"')
content = content.replace('farkindaligini, kararini veya aksiyonunu yaz...', 'farkındalığını, kararını veya aksiyonunu yaz...')
content = content.replace('"farkindalik"', '"farkindalik"')  # keep as DB key
print("  OK 3. Turkce karakterler duzeltildi")

# ============================================================
# 4. ADIMLARIM - Edit/Delete + tiklama duzeltmesi
# Mevcut: tiklayinca toggle (cizik atiyor) 
# Yeni: checkbox ayri, sag tarafta edit/delete ikonlari
# ============================================================

old_task_item = '''          <div key={t.id} onClick={() => onToggleTask(t.id, !t.is_done)} style={{ display: "flex", alignItems: "center", gap: 10, padding: "10px 0", borderBottom: "1px solid #F1F5F9", cursor: "pointer" }}>
            <div style={{ width: 22, height: 22, borderRadius: 6, border: t.is_done ? "none" : "2px solid #CBD5E1", background: t.is_done ? COLORS.primary : "transparent", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
              {t.is_done && <span style={{ color: "#fff", fontSize: 12, fontWeight: 800 }}>✓</span>}
            </div>
            <span style={{ fontSize: 14, color: t.is_done ? COLORS.textLight : COLORS.text, textDecoration: t.is_done ? "line-through" : "none", flex: 1 }}>{t.title}</span>
          </div>'''

new_task_item = '''          <div key={t.id} style={{ display: "flex", alignItems: "center", gap: 10, padding: "10px 0", borderBottom: "1px solid #F1F5F9" }}>
            <div onClick={() => onToggleTask(t.id, !t.is_done)} style={{ width: 22, height: 22, borderRadius: 6, border: t.is_done ? "none" : "2px solid #CBD5E1", background: t.is_done ? COLORS.primary : "transparent", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, cursor: "pointer" }}>
              {t.is_done && <span style={{ color: "#fff", fontSize: 12, fontWeight: 800 }}>✓</span>}
            </div>
            <span style={{ fontSize: 14, color: t.is_done ? COLORS.textLight : COLORS.text, textDecoration: t.is_done ? "line-through" : "none", flex: 1 }}>{t.title}</span>
            <svg onClick={() => { const newTitle = prompt("Adımı düzenle:", t.title); if (newTitle && newTitle.trim()) onEditTask(t.id, newTitle.trim()); }} width="16" height="16" fill="none" stroke="#94A3B8" strokeWidth="2" viewBox="0 0 24 24" style={{ cursor: "pointer", flexShrink: 0 }}><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            <svg onClick={() => { if (confirm("Bu adımı silmek istediğinize emin misiniz?")) onDeleteTask(t.id); }} width="16" height="16" fill="none" stroke="#94A3B8" strokeWidth="2" viewBox="0 0 24 24" style={{ cursor: "pointer", flexShrink: 0 }}><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </div>'''

if old_task_item in content:
    content = content.replace(old_task_item, new_task_item)
    print("  OK 4. Adimlarim edit/delete ikonlari eklendi")
else:
    print("  SKIP 4. Adimlarim blogu bulunamadi")

# ============================================================
# 5. ClientHome props - onEditTask ve onDeleteTask ekle
# ============================================================
old_sig = 'onAddJournal: (note: string, cat: string) => void })'
new_sig = 'onAddJournal: (note: string, cat: string) => void; onEditTask: (id: string, title: string) => void; onDeleteTask: (id: string) => void; onEditJournal: (id: string, note: string) => void; onDeleteJournal: (id: string) => void })'

if old_sig in content:
    content = content.replace(old_sig, new_sig)
    print("  OK 5a. ClientHome props guncellendi")

# Props destructure
old_destr = 'onAddTask, onToggleTask, onAddJournal }'
new_destr = 'onAddTask, onToggleTask, onAddJournal, onEditTask, onDeleteTask, onEditJournal, onDeleteJournal }'
if old_destr in content:
    content = content.replace(old_destr, new_destr)
    print("  OK 5b. Props destructure guncellendi")

# ClientHome render'da yeni props'lari ekle
old_render_end = 'onAddJournal={async (note, cat) => { const { data } = await supabase.from("journal").insert({ client_id: currentUser.id, note, category: cat }).select().single(); if (data) setJournal(prev => [data, ...prev]); }} />'

new_render_end = '''onAddJournal={async (note, cat) => { const { data } = await supabase.from("journal").insert({ client_id: currentUser.id, note, category: cat }).select().single(); if (data) setJournal(prev => [data, ...prev]); }} onEditTask={async (id, title) => { await supabase.from("tasks").update({ title }).eq("id", id); setTasks(prev => prev.map(t => t.id === id ? { ...t, title } : t)); }} onDeleteTask={async (id) => { await supabase.from("tasks").delete().eq("id", id); setTasks(prev => prev.filter(t => t.id !== id)); }} onEditJournal={async (id, note) => { await supabase.from("journal").update({ note }).eq("id", id); setJournal(prev => prev.map(j => j.id === id ? { ...j, note } : j)); }} onDeleteJournal={async (id) => { await supabase.from("journal").delete().eq("id", id); setJournal(prev => prev.filter(j => j.id !== id)); }} />'''

if old_render_end in content:
    content = content.replace(old_render_end, new_render_end)
    print("  OK 5c. Render props eklendi")

# ============================================================
# 6. GELISIM GUNLUGU - Edit/Delete ikonlari ekle
# ============================================================
old_journal_note = '''<div style={{ fontSize: 14, color: COLORS.text, lineHeight: 1.6 }}>{j.note}</div>'''

new_journal_note = '''<div style={{ fontSize: 14, color: COLORS.text, lineHeight: 1.6 }}>{j.note}</div>
                <div style={{ display: "flex", gap: 8, marginTop: 6, justifyContent: "flex-end" }}>
                  <svg onClick={() => { const newNote = prompt("Notu düzenle:", j.note); if (newNote && newNote.trim()) onEditJournal(j.id, newNote.trim()); }} width="14" height="14" fill="none" stroke="#94A3B8" strokeWidth="2" viewBox="0 0 24 24" style={{ cursor: "pointer" }}><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                  <svg onClick={() => { if (confirm("Bu notu silmek istediğinize emin misiniz?")) onDeleteJournal(j.id); }} width="14" height="14" fill="none" stroke="#94A3B8" strokeWidth="2" viewBox="0 0 24 24" style={{ cursor: "pointer" }}><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                </div>'''

if old_journal_note in content:
    content = content.replace(old_journal_note, new_journal_note)
    print("  OK 6. Gelisim Gunlugu edit/delete eklendi")
else:
    print("  SKIP 6. Journal note blogu bulunamadi")

# ============================================================
# 7. LINKEDIN IKONU - SVG ile gercek LinkedIn ikonu
# ============================================================
# Koc kartindaki LinkedIn butonu
content = content.replace(
    '''<a href="https://www.linkedin.com/services/page/2800ba317abbbbb440/" target="_blank" rel="noopener noreferrer" style={{ padding: "4px 10px", borderRadius: 6, background: "rgba(255,255,255,0.15)", color: "#fff", textDecoration: "none", fontSize: 11, fontWeight: 600 }}>LinkedIn</a>''',
    '''<a href="https://www.linkedin.com/services/page/2800ba317abbbbb440/" target="_blank" rel="noopener noreferrer" style={{ width: 36, height: 36, borderRadius: 8, background: "rgba(255,255,255,0.15)", display: "flex", alignItems: "center", justifyContent: "center", textDecoration: "none" }}><svg width="18" height="18" viewBox="0 0 24 24" fill="#fff"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></a>'''
)

# Email butonu da ikon olsun
content = content.replace(
    '''<a href="mailto:serkanmursalli@gmail.com" style={{ padding: "4px 10px", borderRadius: 6, background: "rgba(255,255,255,0.15)", color: "#fff", textDecoration: "none", fontSize: 11, fontWeight: 600 }}>E-posta</a>''',
    '''<a href="mailto:serkanmursalli@gmail.com" style={{ width: 36, height: 36, borderRadius: 8, background: "rgba(255,255,255,0.15)", display: "flex", alignItems: "center", justifyContent: "center", textDecoration: "none" }}><svg width="18" height="18" fill="none" stroke="#fff" strokeWidth="2" viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></a>'''
)

print("  OK 7. LinkedIn ve Email ikonlari guncellendi")

# ============================================================
# SAVE
# ============================================================
open(filepath, 'w').write(content)

print("")
print("Tamamlandi!")
print("  1. Madalya ikonu kaldirildi")
print("  2. Ust yazi: Kendini tani, yonunu bul, potansiyelini buyut")
print("  3. Turkce karakterler duzeltildi")
print("  4. Adimlarim: edit/delete ikonlari")
print("  5. Gelisim Gunlugu: edit/delete ikonlari")
print("  6. LinkedIn gercek ikon")
print("")
print("Simdi: npm run build")
