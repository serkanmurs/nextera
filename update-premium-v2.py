filepath = 'src/app/page.tsx'
content = open(filepath, 'r').read()

print("🚀 NextERA Premium Dönüşüm v2 başlıyor...")
changes = 0

# ============================================================
# 1. RENK PALETİ
# ============================================================
old = 'primary: "#0891B2"'
new = 'primary: "#0E7490"'
if old in content:
    content = content.replace(old, new)
    changes += 1
    print("  ✅ 1a. Primary renk → #0E7490")

old = 'primaryLight: "#06B6D4"'
new = 'primaryLight: "#0891B2"'
if old in content:
    content = content.replace(old, new)

old = 'accent: "#3B82F6"'
new = 'accent: "#1E40AF"'
if old in content:
    content = content.replace(old, new)

old = 'text: "#1E293B"'
new = 'text: "#0F172A"'
if old in content:
    content = content.replace(old, new)

old = 'success: "#10B981"'
new = 'success: "#059669"'
if old in content:
    content = content.replace(old, new)

old = 'danger: "#EF4444"'
new = 'danger: "#DC2626"'
if old in content:
    content = content.replace(old, new)

old = 'warning: "#F59E0B"'
new = 'warning: "#D97706"'
if old in content:
    content = content.replace(old, new)

print("  ✅ 1b. Tüm renkler güncellendi")

# ============================================================
# 2. HEADER - Koyu turkuaz, flat
# ============================================================
old = 'background: "linear-gradient(135deg, #0891B2 0%, #0EA5E9 50%, #06B6D4 100%)"'
if old in content:
    content = content.replace(old, 'background: "linear-gradient(135deg, #0E7490, #155E75)"')
    changes += 1
    print("  ✅ 2. Header koyu turkuaz")
else:
    old2 = 'background: "linear-gradient(135deg, #0891B2, #0EA5E9)"'
    if old2 in content:
        content = content.replace(old2, 'background: "linear-gradient(135deg, #0E7490, #155E75)"', 1)
        print("  ✅ 2. Header koyu turkuaz (alt)")

# ============================================================
# 3. LOGIN - Premium dönüşüm
# ============================================================
# Background
old = 'background: "linear-gradient(180deg, #0891B2 0%, #0EA5E9 40%, #F8FAFC 100%)"'
if old in content:
    content = content.replace(old, 'background: "linear-gradient(180deg, #0E7490 0%, #155E75 40%, #F0F9FF 100%)"')
    print("  ✅ 3a. Login arka plan")

# Value proposition
old = '<div style={{ marginBottom: 40, textAlign: "center" }}>'
if old in content:
    content = content.replace(old, '<div style={{ marginBottom: 32, textAlign: "center" }}>\n        <div style={{ fontSize: 13, color: "rgba(255,255,255,0.8)", fontWeight: 500, marginBottom: 16, letterSpacing: "0.3px" }}>Potansiyelini Netleştir. Stratejik Koçluk Yolculuğuna Başla.</div>', 1)
    print("  ✅ 3b. Değer önerisi eklendi")

# Button text
old = '{loading ? "Giriş yapılıyor..." : "Giriş Yap"}'
if old in content:
    content = content.replace(old, '{loading ? "Giriş yapılıyor..." : "Platforma Gir"}')
    print("  ✅ 3c. Buton: Platforma Gir")

# ICF badge - find "Şifremi Unuttum" link
old = '        <div style={{ textAlign: "center", marginTop: 8 }}>\n          <span onClick={async () => {'
if old in content:
    content = content.replace(old, '        <div style={{ textAlign: "center", marginTop: 12, paddingTop: 12, borderTop: "1px solid rgba(255,255,255,0.15)" }}>\n          <span style={{ fontSize: 11, color: "rgba(255,255,255,0.7)" }}>🏅 ICF Akredite Koç · Güvenli Platform</span>\n        </div>\n        <div style={{ textAlign: "center", marginTop: 8 }}>\n          <span onClick={async () => {')
    print("  ✅ 3d. ICF badge eklendi")

# ============================================================
# 4. REGISTER BUTTON - Flat
# ============================================================
content = content.replace('background: "linear-gradient(135deg, #F97316, #FB923C)"', 'background: "#F97316"')
print("  ✅ 4. Kayıt butonu flat")

# ============================================================
# 5. BOTTOM NAV - Clean + büyük touch targets
# ============================================================
old = 'background: "rgba(255,255,255,0.95)", padding: "8px 0 20px", borderTop: "1px solid rgba(226,232,240,0.5)", display: "flex", justifyContent: "space-around", zIndex: 50, boxShadow: "0 -4px 20px rgba(0,0,0,0.06)", backdropFilter: "blur(12px)"'
if old in content:
    content = content.replace(old, 'background: "#fff", padding: "10px 0 22px", borderTop: "1px solid #E2E8F0", display: "flex", justifyContent: "space-around", zIndex: 50')
    print("  ✅ 5. Bottom nav clean")

# Touch targets
old = 'padding: "4px 12px", borderRadius: 12, position: "relative" as const }}'
if old in content:
    content = content.replace(old, 'padding: "6px 16px", borderRadius: 12, position: "relative" as const, minWidth: 56, minHeight: 44 }}')
    print("  ✅ 5b. Touch targets büyütüldü")

# ============================================================
# 6. CLIENT HOME - Haftalık odak
# ============================================================
old = '<p style={{ margin: "0 0 16px", fontSize: 14, color: COLORS.textLight }}>Gelişim yolculuğunuza devam edin.</p>'
new = '''<p style={{ margin: "0 0 16px", fontSize: 14, color: COLORS.textLight }}>Stratejik gelişim yolculuğuna devam et.</p>

      {/* Haftalık Odak */}
      <div style={{ ...cardStyle, background: "#F0F9FF", border: "1px solid #BAE6FD" }}>
        <div style={{ fontSize: 13, fontWeight: 700, color: COLORS.primary, marginBottom: 8 }}>🎯 Bu Haftaki Odağın</div>
        <div style={{ fontSize: 14, color: COLORS.text, lineHeight: 1.5, fontStyle: "italic" }}>&ldquo;Her seans bir farkındalık, her farkındalık bir adım. Bugün hangi adımı atacaksın?&rdquo;</div>
      </div>'''
if old in content:
    content = content.replace(old, new)
    print("  ✅ 6. Haftalık odak eklendi")

# Empty states
content = content.replace('Henüz seans yok.', 'Yolculuk başlıyor. İlk seansın dönüşümünü burada göreceksin. 🌱')
content = content.replace('Henüz mesaj yok.', 'Koçunuzla ilk mesajınızı gönderin. 💬')
print("  ✅ 6b. Motivasyonel empty states")

# ============================================================
# 7. KOÇ KARTI - ICF badge
# ============================================================
old = 'background: "linear-gradient(135deg, #0891B2 0%, #0EA5E9 100%)"'
if old in content:
    content = content.replace(old, 'background: "linear-gradient(135deg, #0E7490, #155E75)"')
    print("  ✅ 7a. Koç kartı renk")

# ICF badge yerine bio
old = '<div style={{ fontSize: 13, opacity: 0.85 }}>{admin.bio}</div>'
if old in content:
    content = content.replace(old, '<div style={{ fontSize: 12, opacity: 0.9 }}>🏅 ICF Akredite Profesyonel Koç</div>')
    print("  ✅ 7b. Koç kartı ICF badge")

# ============================================================
# 8. PROGRAMLAR + HAKKIMDA - ClientHome sonuna DOĞRU yere ekle
# ============================================================
# ClientHome'un kapanışı: "    </div>\n  );\n}\n\n// ==================== SESSIONS PAGE"
old_client_end = '    </div>\n  );\n}\n\n// ==================== SESSIONS PAGE'

programs_about = '''      {/* Programlar */}
      <div style={cardStyle}>
        <h3 style={{ margin: "0 0 14px", fontSize: 16, fontWeight: 800, color: COLORS.text }}>📋 Programlar</h3>
        <div style={{ display: "flex", flexDirection: "column" as const, gap: 12 }}>
          <div style={{ padding: 16, borderRadius: 12, border: "1px solid #E2E8F0", background: "#FAFAFA" }}>
            <div style={{ fontWeight: 700, fontSize: 14, color: COLORS.primary, marginBottom: 4 }}>NextERA Student</div>
            <div style={{ fontSize: 12, color: COLORS.textLight, lineHeight: 1.5 }}>Öğrenciler ve yeni mezunlar için. SWOT Analizi, Değerler Çalışması, Yaşam Çemberi, CV & LinkedIn, Hedefler & Vizyon. 4 veya 6 seanslık programlar.</div>
          </div>
          <div style={{ padding: 16, borderRadius: 12, border: "1px solid #E2E8F0", background: "#FAFAFA" }}>
            <div style={{ fontWeight: 700, fontSize: 14, color: COLORS.primary, marginBottom: 4 }}>NextERA Professional</div>
            <div style={{ fontSize: 12, color: COLORS.textLight, lineHeight: 1.5 }}>Profesyoneller için. Kariyer SWOT Analizi, Değerler Analizi, Vizyon & Misyon, Gelişim Planı Takibi, CV & LinkedIn Danışmanlığı. 4 veya 6 seanslık programlar.</div>
          </div>
        </div>
        <div style={{ marginTop: 12, padding: "10px 14px", borderRadius: 10, background: "#FFF7ED", border: "1px solid #FED7AA" }}>
          <div style={{ fontSize: 12, color: "#92400E", fontWeight: 600 }}>🎁 Ücretsiz Tanışma: 40 dk Kimya Seansı ile hedef ve beklenti analizi</div>
        </div>
      </div>

      {/* Hakkımda */}
      <div style={cardStyle}>
        <h3 style={{ margin: "0 0 14px", fontSize: 16, fontWeight: 800, color: COLORS.text }}>👤 Koçunuz Hakkında</h3>
        <div style={{ fontSize: 13, color: COLORS.text, lineHeight: 1.7 }}>
          <p style={{ margin: "0 0 10px" }}>Serkan Mursallı, ICF akredite profesyonel koçluk altyapısını; veri odaklı analiz, stratejik planlama, liderlik ve değişim yönetimi uzmanlığıyla birleştirmektedir.</p>
          <p style={{ margin: "0 0 10px" }}>Süreç geliştirme, operasyonel mükemmellik ve dijital dönüşüm alanlarında Constantia Flexibles, Jotun, Vestel ve Arçelik gibi markalarda edindiği 8+ yıllık deneyimle profesyonellerin ihtiyaçlarına doğru dokunan çözümler sunmaktadır.</p>
          <p style={{ margin: 0, fontWeight: 600, color: COLORS.primary }}>Odak: Potansiyeli somut sonuçlara dönüştürmek, karar alma mekanizmalarını güçlendirmek.</p>
        </div>
        <div style={{ display: "flex", gap: 8, marginTop: 14 }}>
          <a href="https://www.linkedin.com/services/page/2800ba317abbbbb440/" target="_blank" rel="noopener noreferrer" style={{ flex: 1, textAlign: "center" as const, padding: "10px", borderRadius: 10, background: "#0E7490", color: "#fff", textDecoration: "none", fontSize: 13, fontWeight: 700 }}>LinkedIn Profili</a>
          <a href="mailto:serkanmursalli@gmail.com" style={{ flex: 1, textAlign: "center" as const, padding: "10px", borderRadius: 10, border: "1.5px solid #0E7490", color: "#0E7490", textDecoration: "none", fontSize: 13, fontWeight: 700 }}>E-posta Gönder</a>
        </div>
      </div>

    </div>
  );
}

// ==================== SESSIONS PAGE'''

if old_client_end in content:
    content = content.replace(old_client_end, programs_about)
    print("  ✅ 8. Programlar + Hakkımda doğru yere eklendi (ClientHome sonu)")
else:
    print("  ❌ 8. ClientHome sonu bulunamadı!")

# ============================================================
# 9. KALAN GRADİENTLER - Flat dönüşüm
# ============================================================
content = content.replace('background: "linear-gradient(135deg, #0891B2, #0EA5E9)"', 'background: "#0E7490"')
content = content.replace('background: "linear-gradient(135deg, #0891B2, #F97316)"', 'background: "#0E7490"')
content = content.replace('boxShadow: "0 4px 14px rgba(8,145,178,0.3)"', 'boxShadow: "none"')
content = content.replace('boxShadow: "0 4px 20px rgba(8,145,178,0.25)", backdropFilter: "blur(10px)"', 'boxShadow: "0 1px 3px rgba(0,0,0,0.1)"')
print("  ✅ 9. Gradient → flat dönüşüm")

# ============================================================
# 10. CARD STYLE - Flat gölge (tüm occurrences)
# ============================================================
content = content.replace(
    'boxShadow: "0 1px 3px rgba(0,0,0,0.04), 0 4px 16px rgba(0,0,0,0.04)", border: "1px solid rgba(226,232,240,0.6)"',
    'boxShadow: "0 1px 2px rgba(0,0,0,0.03)", border: "1px solid #E2E8F0"'
)
print("  ✅ 10. Kart gölgeleri flat")

# ============================================================
# 11. ADMIN BAŞLIKLARI
# ============================================================
content = content.replace('"Admin Paneli"', '"Yönetim Paneli"')
content = content.replace('📊 Admin Dashboard', '📊 Yönetim Paneli')
print("  ✅ 11. Admin başlıkları Türkçe")

# ============================================================
# 12. MESAJ BALONU - Flat
# ============================================================
old = 'boxShadow: isMine ? "0 2px 12px rgba(8,145,178,0.2)" : "0 1px 3px rgba(0,0,0,0.04)"'
if old in content:
    content = content.replace(old, 'boxShadow: "none"')
    print("  ✅ 12. Mesaj baloncukları flat")

# ============================================================
# 13. TOAST - Minimal
# ============================================================
old = 'boxShadow: "0 8px 30px rgba(0,0,0,0.15), 0 2px 8px rgba(0,0,0,0.1)", animation: "fadeIn 0.3s", backdropFilter: "blur(8px)", maxWidth: "90%", textAlign: "center" as const'
if old in content:
    content = content.replace(old, 'boxShadow: "0 4px 12px rgba(0,0,0,0.1)", animation: "fadeIn 0.3s", maxWidth: "90%", textAlign: "center" as const')
    print("  ✅ 13. Toast minimal")

# SAVE
open(filepath, 'w').write(content)

print("")
print("🎉 PREMIUM DÖNÜŞÜM v2 TAMAMLANDI!")
print(f"   Toplam ana değişiklik: {changes}+")
print("")
print("Şimdi: npm run build")
