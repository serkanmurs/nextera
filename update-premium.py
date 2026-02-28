import sys

filepath = 'src/app/page.tsx'
content = open(filepath, 'r').read()

print("🚀 NextERA Premium Dönüşüm başlıyor...")

# 1. RENK PALETİ
old_colors = """const COLORS = {
  primary: "#0891B2",
  primaryLight: "#06B6D4",
  secondary: "#F97316",
  secondaryLight: "#FB923C",
  accent: "#3B82F6",
  white: "#FFFFFF",
  bg: "#F8FAFC",
  text: "#1E293B",
  textLight: "#64748B",
  border: "#E2E8F0",
  success: "#10B981",
  danger: "#EF4444",
  warning: "#F59E0B",
};"""

new_colors = """const COLORS = {
  primary: "#0E7490",
  primaryLight: "#0891B2",
  secondary: "#F97316",
  secondaryLight: "#FB923C",
  accent: "#1E40AF",
  white: "#FFFFFF",
  bg: "#F8FAFC",
  text: "#0F172A",
  textLight: "#64748B",
  border: "#E2E8F0",
  success: "#059669",
  danger: "#DC2626",
  warning: "#D97706",
};"""

if old_colors in content:
    content = content.replace(old_colors, new_colors)
    print("  ✅ 1. Renk paleti güncellendi")
else:
    print("  ⚠️ 1. Renk paleti bulunamadı, atlanıyor")

# 2. CARD STYLE
content = content.replace(
    'boxShadow: "0 1px 3px rgba(0,0,0,0.04), 0 4px 16px rgba(0,0,0,0.04)", border: "1px solid rgba(226,232,240,0.6)"',
    'boxShadow: "0 1px 2px rgba(0,0,0,0.03)", border: "1px solid #E2E8F0"'
)
print("  ✅ 2. Kart stili flat/minimal")

# 3. HEADER
content = content.replace(
    'background: "linear-gradient(135deg, #0891B2 0%, #0EA5E9 50%, #06B6D4 100%)"',
    'background: "linear-gradient(135deg, #0E7490, #155E75)"'
)
content = content.replace(
    'boxShadow: "0 4px 20px rgba(8,145,178,0.25)", backdropFilter: "blur(10px)"',
    'boxShadow: "0 1px 3px rgba(0,0,0,0.1)"'
)
print("  ✅ 3. Header koyu turkuaz")

# 4. LOGIN BACKGROUND
content = content.replace(
    'background: "linear-gradient(180deg, #0891B2 0%, #0EA5E9 40%, #F8FAFC 100%)"',
    'background: "linear-gradient(180deg, #0E7490 0%, #155E75 40%, #F0F9FF 100%)"'
)
# Value proposition above login
old_login_logo = '<div style={{ marginBottom: 40, textAlign: "center" }}>'
new_login_logo = '<div style={{ marginBottom: 32, textAlign: "center" }}>\n        <div style={{ fontSize: 13, color: "rgba(255,255,255,0.8)", fontWeight: 500, marginBottom: 16, letterSpacing: "0.3px" }}>Potansiyelini Netleştir. Stratejik Koçluk Yolculuğuna Başla.</div>'
content = content.replace(old_login_logo, new_login_logo, 1)
# Button text
content = content.replace('{loading ? "Giriş yapılıyor..." : "Giriş Yap"}', '{loading ? "Giriş yapılıyor..." : "Platforma Gir"}')
# ICF badge
old_forgot = '        <div style={{ textAlign: "center", marginTop: 8 }}>\n          <span onClick={async () => {'
new_forgot = '        <div style={{ textAlign: "center", marginTop: 12, paddingTop: 12, borderTop: "1px solid #E2E8F0" }}>\n          <span style={{ fontSize: 11, color: "#64748B" }}>🏅 ICF Akredite Koç · Güvenli Platform</span>\n        </div>\n        <div style={{ textAlign: "center", marginTop: 8 }}>\n          <span onClick={async () => {'
content = content.replace(old_forgot, new_forgot)
print("  ✅ 4. Login premium + ICF badge")

# 5. REGISTER BUTTON - flat orange
content = content.replace('background: "linear-gradient(135deg, #F97316, #FB923C)"', 'background: "#F97316"')
print("  ✅ 5. Kayıt butonu flat")

# 6. BOTTOM NAV - clean
content = content.replace(
    'background: "rgba(255,255,255,0.95)", padding: "8px 0 20px", borderTop: "1px solid rgba(226,232,240,0.5)", display: "flex", justifyContent: "space-around", zIndex: 50, boxShadow: "0 -4px 20px rgba(0,0,0,0.06)", backdropFilter: "blur(12px)"',
    'background: "#fff", padding: "10px 0 22px", borderTop: "1px solid #E2E8F0", display: "flex", justifyContent: "space-around", zIndex: 50'
)
# Touch targets
content = content.replace(
    'padding: "4px 12px", borderRadius: 12, position: "relative" as const }}',
    'padding: "6px 16px", borderRadius: 12, position: "relative" as const, minWidth: 56, minHeight: 44 }}'
)
print("  ✅ 6. Nav: Clean + büyük touch targets")

# 7. CLIENT HOME - haftalık odak + motivasyon
old_hello = '<p style={{ margin: "0 0 16px", fontSize: 14, color: COLORS.textLight }}>Gelişim yolculuğunuza devam edin.</p>'
new_hello = """<p style={{ margin: "0 0 16px", fontSize: 14, color: COLORS.textLight }}>Stratejik gelişim yolculuğuna devam et.</p>

      {/* Haftalık Odak */}
      <div style={{ ...cardStyle, background: "#F0F9FF", border: "1px solid #BAE6FD" }}>
        <div style={{ fontSize: 13, fontWeight: 700, color: COLORS.primary, marginBottom: 8 }}>🎯 Bu Haftaki Odağın</div>
        <div style={{ fontSize: 14, color: COLORS.text, lineHeight: 1.5, fontStyle: "italic" }}>&ldquo;Her seans bir farkındalık, her farkındalık bir adım. Bugün hangi adımı atacaksın?&rdquo;</div>
      </div>"""
content = content.replace(old_hello, new_hello)
# Empty states
content = content.replace('Yolculuk başlıyor. İlk seansın dönüşümünü burada göreceksin. 🌱', 'Yolculuk başlıyor. İlk seansın dönüşümünü burada göreceksin. 🌱')
content = content.replace('Henüz seans yok.', 'Yolculuk başlıyor. İlk seansın dönüşümünü burada göreceksin. 🌱')
print("  ✅ 7. Client Home: Haftalık odak + motivasyon")

# 8. COACH CARD - premium
content = content.replace(
    'background: "linear-gradient(135deg, #0891B2 0%, #0EA5E9 100%)"',
    'background: "linear-gradient(135deg, #0E7490, #155E75)"'
)
# Add ICF badge to coach card - find bio line
content = content.replace(
    '<div style={{ fontSize: 13, opacity: 0.85 }}>{admin.bio}</div>',
    '<div style={{ fontSize: 12, opacity: 0.9, marginTop: 2 }}>🏅 ICF Akredite Profesyonel Koç</div>'
)
print("  ✅ 8. Koç kartı: ICF badge")

# 9. PROGRAMS + ABOUT - Add to ClientHome before closing
old_client_end = '    </div>\n  );\n}\n\n// ==================== ADMIN DASHBOARD'
new_client_end = """      {/* Programlar */}
      <div style={cardStyle}>
        <h3 style={{ margin: "0 0 14px", fontSize: 16, fontWeight: 800, color: COLORS.text }}>📋 Programlar</h3>
        <div style={{ display: "flex", flexDirection: "column" as const, gap: 12 }}>
          <div style={{ padding: 16, borderRadius: 12, border: "1px solid #E2E8F0", background: "#FAFAFA" }}>
            <div style={{ fontWeight: 700, fontSize: 14, color: COLORS.primary, marginBottom: 4 }}>NextERA Student</div>
            <div style={{ fontSize: 12, color: COLORS.textLight, lineHeight: 1.5 }}>Öğrenciler ve yeni mezunlar için. SWOT Analizi, Değerler Çalışması, Yaşam Çemberi, CV &amp; LinkedIn, Hedefler &amp; Vizyon. 4 veya 6 seanslık programlar.</div>
          </div>
          <div style={{ padding: 16, borderRadius: 12, border: "1px solid #E2E8F0", background: "#FAFAFA" }}>
            <div style={{ fontWeight: 700, fontSize: 14, color: COLORS.primary, marginBottom: 4 }}>NextERA Professional</div>
            <div style={{ fontSize: 12, color: COLORS.textLight, lineHeight: 1.5 }}>Profesyoneller için. Kariyer SWOT Analizi, Değerler Analizi, Vizyon &amp; Misyon, Gelişim Planı Takibi, CV &amp; LinkedIn Danışmanlığı. 4 veya 6 seanslık programlar.</div>
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

// ==================== ADMIN DASHBOARD"""
content = content.replace(old_client_end, new_client_end)
print("  ✅ 9. Programlar + Hakkımda eklendi")

# 10. FLAT GRADIENTS
content = content.replace('background: "linear-gradient(135deg, #0891B2, #0EA5E9)"', 'background: "#0E7490"')
content = content.replace('background: "linear-gradient(135deg, #0891B2, #F97316)"', 'background: "#0E7490"')
content = content.replace('background: "linear-gradient(135deg, #0E7490, #F97316)"', 'background: "#0E7490"')
content = content.replace('boxShadow: "0 4px 14px rgba(8,145,178,0.3)"', 'boxShadow: "none"')
print("  ✅ 10. Gradient → flat dönüşüm")

# 11. ADMIN TITLES
content = content.replace('"Admin Paneli"', '"Yönetim Paneli"')
content = content.replace('📊 Admin Dashboard', '📊 Yönetim Paneli')
print("  ✅ 11. Admin başlıkları")

# 12. FONT (layout + css güncellemesi için hatırlatma)
print("  ✅ 12. Font (Inter) → ayrıca layout.tsx ve globals.css güncellenecek")

# SAVE
open(filepath, 'w').write(content)

print("")
print("🎉 PREMIUM DÖNÜŞÜM TAMAMLANDI!")
print("  • Renk: Koyu turkuaz/lacivert (#0E7490)")
print("  • Flat/minimal tasarım")
print("  • Login: Değer önerisi + ICF badge")
print("  • Haftalık Odak kartı")
print("  • Programlar (Student + Professional)")
print("  • Hakkımda sayfası")
print("  • Motivasyonel empty states")
print("  • Büyük touch targets")
print("")
print("Şimdi: npm run build")
