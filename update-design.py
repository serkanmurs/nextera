import sys

filepath = 'src/app/page.tsx'
content = open(filepath, 'r').read()

print("🎨 Tasarım İyileştirmeleri başlıyor...")

# ============================================================
# 1. HEADER İYİLEŞTİRME - Daha temiz, glassmorphism efekti
# ============================================================

old_header = '''        <header style={{ background: "linear-gradient(135deg, #0891B2, #0EA5E9)", padding: "16px 20px", display: "flex", justifyContent: "space-between", alignItems: "center", position: "sticky", top: 0, zIndex: 50, boxShadow: "0 2px 10px rgba(8,145,178,0.3)" }}>'''

new_header = '''        <header style={{ background: "linear-gradient(135deg, #0891B2 0%, #0EA5E9 50%, #06B6D4 100%)", padding: "14px 20px", display: "flex", justifyContent: "space-between", alignItems: "center", position: "sticky", top: 0, zIndex: 50, boxShadow: "0 4px 20px rgba(8,145,178,0.25)", backdropFilter: "blur(10px)" }}>'''

content = content.replace(old_header, new_header)
print("  ✅ 1. Header iyileştirildi")

# ============================================================
# 2. CARD STYLE İYİLEŞTİRME - Daha soft gölgeler
# ============================================================

old_card = '''const cardStyle: React.CSSProperties = {
  background: "#fff", borderRadius: 16, padding: 20, marginBottom: 16,
  boxShadow: "0 2px 8px rgba(0,0,0,0.06)", border: `1px solid ${COLORS.border}`,
};'''

new_card = '''const cardStyle: React.CSSProperties = {
  background: "#fff", borderRadius: 18, padding: 20, marginBottom: 14,
  boxShadow: "0 1px 3px rgba(0,0,0,0.04), 0 4px 16px rgba(0,0,0,0.04)", border: "1px solid rgba(226,232,240,0.6)",
};'''

content = content.replace(old_card, new_card)
print("  ✅ 2. Kart stilleri iyileştirildi")

# ============================================================
# 3. BOTTOM NAV İYİLEŞTİRME - Daha modern
# ============================================================

old_bottom_nav_style = '''style={{ position: "fixed", bottom: 0, left: 0, right: 0, background: "#fff", padding: "8px 0 20px", borderTop: `1px solid ${COLORS.border}`, display: "flex", justifyContent: "space-around", zIndex: 50, boxShadow: "0 -2px 10px rgba(0,0,0,0.05)" }}'''

new_bottom_nav_style = '''style={{ position: "fixed", bottom: 0, left: 0, right: 0, background: "rgba(255,255,255,0.95)", padding: "8px 0 20px", borderTop: "1px solid rgba(226,232,240,0.5)", display: "flex", justifyContent: "space-around", zIndex: 50, boxShadow: "0 -4px 20px rgba(0,0,0,0.06)", backdropFilter: "blur(12px)" }}'''

content = content.replace(old_bottom_nav_style, new_bottom_nav_style)
print("  ✅ 3. Alt navigasyon iyileştirildi")

# ============================================================
# 4. GİRİŞ EKRANI İYİLEŞTİRME
# ============================================================

# Login card style
old_login_card = '''      <div style={{ background: "rgba(255,255,255,0.97)", borderRadius: 28, padding: 32, width: "100%", maxWidth: 380, boxShadow: "0 20px 60px rgba(0,0,0,0.12)" }}>'''

new_login_card = '''      <div style={{ background: "rgba(255,255,255,0.98)", borderRadius: 28, padding: 32, width: "100%", maxWidth: 380, boxShadow: "0 8px 40px rgba(0,0,0,0.08), 0 20px 60px rgba(8,145,178,0.12)" }}>'''

content = content.replace(old_login_card, new_login_card)

# Login button
old_login_btn = '''style={{ background: "linear-gradient(135deg, #0891B2, #0EA5E9)", color: "#fff", border: "none", borderRadius: 12, padding: "12px 24px", fontSize: 15, fontWeight: 700, cursor: "pointer", width: "100%", boxShadow: "0 4px 14px rgba(8,145,178,0.3)", opacity: loading ? 0.7 : 1 }}>
          {loading ? "Giriş yapılıyor..." : "Giriş Yap"}'''

new_login_btn = '''style={{ background: "linear-gradient(135deg, #0891B2, #0EA5E9)", color: "#fff", border: "none", borderRadius: 14, padding: "13px 24px", fontSize: 15, fontWeight: 700, cursor: "pointer", width: "100%", boxShadow: "0 4px 14px rgba(8,145,178,0.3)", opacity: loading ? 0.7 : 1, transition: "all 0.2s", letterSpacing: "0.3px" }}>
          {loading ? "Giriş yapılıyor..." : "Giriş Yap"}'''

content = content.replace(old_login_btn, new_login_btn)

# Input fields - make more consistent
content = content.replace(
    'style={{ width: "100%", padding: "12px 16px", borderRadius: 12, border: `1.5px solid ${COLORS.border}`, fontSize: 15, outline: "none", boxSizing: "border-box" as const }}',
    'style={{ width: "100%", padding: "12px 16px", borderRadius: 12, border: "1.5px solid #E2E8F0", fontSize: 15, outline: "none", boxSizing: "border-box" as const, transition: "border-color 0.2s" }}'
)

print("  ✅ 4. Giriş ekranı iyileştirildi")

# ============================================================
# 5. KAYIT EKRANI İYİLEŞTİRME
# ============================================================

old_register_card = '''      <div style={{ background: "rgba(255,255,255,0.97)", borderRadius: 28, padding: 28, width: "100%", maxWidth: 400, boxShadow: "0 20px 60px rgba(0,0,0,0.12)", maxHeight: "80vh", overflowY: "auto" }}>'''

new_register_card = '''      <div style={{ background: "rgba(255,255,255,0.98)", borderRadius: 28, padding: 28, width: "100%", maxWidth: 400, boxShadow: "0 8px 40px rgba(0,0,0,0.08), 0 20px 60px rgba(249,115,22,0.1)", maxHeight: "80vh", overflowY: "auto" }}>'''

content = content.replace(old_register_card, new_register_card)
print("  ✅ 5. Kayıt ekranı iyileştirildi")

# ============================================================
# 6. ANA SAYFA / DASHBOARD İYİLEŞTİRME
# ============================================================

# Welcome section improvement for client
old_welcome = '<h2 style={{ margin: "0 0 4px", fontSize: 20, fontWeight: 800 }}>Merhaba, {user.name.split(" ")[0]}! 👋</h2>'
new_welcome = '<h2 style={{ margin: "0 0 4px", fontSize: 22, fontWeight: 800, letterSpacing: "-0.3px" }}>Merhaba, {user.name.split(" ")[0]}! 👋</h2>'
content = content.replace(old_welcome, new_welcome)

# Admin dashboard title
old_admin_title = '<h2 style={{ margin: "0 0 16px", fontSize: 20, fontWeight: 800 }}>📊 Admin Dashboard</h2>'
new_admin_title = '<h2 style={{ margin: "0 0 16px", fontSize: 22, fontWeight: 800, letterSpacing: "-0.3px" }}>📊 Admin Dashboard</h2>'
content = content.replace(old_admin_title, new_admin_title)

# Admin stat cards - better grid
old_stat_grid_start = '<div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>'
# There might be multiple - replace first occurrence only
if old_stat_grid_start in content:
    content = content.replace(old_stat_grid_start, '<div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>', 1)

print("  ✅ 6. Ana sayfa/Dashboard iyileştirildi")

# ============================================================
# 7. SEANSLAR SAYFASI İYİLEŞTİRME
# ============================================================

old_sessions_title = '<h2 style={{ margin: "0 0 16px", fontSize: 20, fontWeight: 800 }}>📅 Seanslar</h2>'
new_sessions_title = '<h2 style={{ margin: "0 0 16px", fontSize: 22, fontWeight: 800, letterSpacing: "-0.3px" }}>📅 Seanslar</h2>'
content = content.replace(old_sessions_title, new_sessions_title)

# Calendar day items - better styling
old_day_style = '''style={{ minWidth: 52, padding: "8px 4px", borderRadius: 12, textAlign: "center", cursor: "pointer", background: isSelected ? COLORS.primary : d.isWeekend ? "#F1F5F9" : "#fff", color: isSelected ? "#fff" : COLORS.text, border: `2px solid ${isSelected ? COLORS.primary : "transparent"}`, transition: "all 0.2s" }}'''

new_day_style = '''style={{ minWidth: 52, padding: "10px 4px", borderRadius: 14, textAlign: "center", cursor: "pointer", background: isSelected ? "linear-gradient(135deg, #0891B2, #0EA5E9)" : d.isWeekend ? "#F8FAFC" : "#fff", color: isSelected ? "#fff" : COLORS.text, border: isSelected ? "none" : "1.5px solid #E2E8F0", transition: "all 0.2s", boxShadow: isSelected ? "0 4px 12px rgba(8,145,178,0.3)" : "none" }}'''

content = content.replace(old_day_style, new_day_style)

# Time slot buttons
old_time_btn = '''style={{ padding: "10px", borderRadius: 10, border: `2px solid ${selected ? COLORS.primary : COLORS.border}`, background: selected ? `${COLORS.primary}10` : booked ? "#F1F5F9" : "#fff", color: booked ? "#CBD5E1" : selected ? COLORS.primary : COLORS.text, fontWeight: 600, fontSize: 14, cursor: booked ? "not-allowed" : "pointer", textDecoration: booked ? "line-through" : "none" }}'''

new_time_btn = '''style={{ padding: "12px", borderRadius: 12, border: selected ? "2px solid #0891B2" : "1.5px solid #E2E8F0", background: selected ? "linear-gradient(135deg, #0891B210, #0EA5E910)" : booked ? "#F8FAFC" : "#fff", color: booked ? "#CBD5E1" : selected ? COLORS.primary : COLORS.text, fontWeight: 700, fontSize: 15, cursor: booked ? "not-allowed" : "pointer", textDecoration: booked ? "line-through" : "none", transition: "all 0.2s", boxShadow: selected ? "0 2px 8px rgba(8,145,178,0.15)" : "none" }}'''

content = content.replace(old_time_btn, new_time_btn)

print("  ✅ 7. Seanslar sayfası iyileştirildi")

# ============================================================
# 8. MESAJLAŞMA İYİLEŞTİRME
# ============================================================

# Message bubble - sender (me)
old_msg_bubble_mine = '''style={{ maxWidth: "80%", padding: "10px 14px", borderRadius: isMine ? "16px 16px 4px 16px" : "16px 16px 16px 4px", background: isMine ? "linear-gradient(135deg, #0891B2, #0EA5E9)" : "#F1F5F9", color: isMine ? "#fff" : COLORS.text, fontSize: 14, lineHeight: 1.5, boxShadow: isMine ? "0 2px 8px rgba(8,145,178,0.2)" : "none" }}'''

new_msg_bubble_mine = '''style={{ maxWidth: "80%", padding: "10px 14px", borderRadius: isMine ? "18px 18px 4px 18px" : "18px 18px 18px 4px", background: isMine ? "linear-gradient(135deg, #0891B2, #0EA5E9)" : "#F1F5F9", color: isMine ? "#fff" : COLORS.text, fontSize: 14, lineHeight: 1.5, boxShadow: isMine ? "0 2px 12px rgba(8,145,178,0.2)" : "0 1px 3px rgba(0,0,0,0.04)" }}'''

content = content.replace(old_msg_bubble_mine, new_msg_bubble_mine)

# Message input area
old_msg_input_area = '''style={{ display: "flex", gap: 8, padding: "12px 16px", borderTop: `1px solid ${COLORS.border}`, background: "#fff" }}'''

new_msg_input_area = '''style={{ display: "flex", gap: 8, padding: "10px 16px", borderTop: "1px solid rgba(226,232,240,0.6)", background: "rgba(255,255,255,0.95)", backdropFilter: "blur(8px)" }}'''

content = content.replace(old_msg_input_area, new_msg_input_area)

# Message input field
old_msg_input = '''style={{ flex: 1, padding: "10px 16px", borderRadius: 24, border: `1.5px solid ${COLORS.border}`, fontSize: 14, outline: "none" }}'''

new_msg_input = '''style={{ flex: 1, padding: "10px 16px", borderRadius: 24, border: "1.5px solid #E2E8F0", fontSize: 14, outline: "none", background: "#F8FAFC", transition: "border-color 0.2s" }}'''

content = content.replace(old_msg_input, new_msg_input)

# Send button
old_send_btn = '''style={{ width: 42, height: 42, borderRadius: "50%", background: "linear-gradient(135deg, #0891B2, #0EA5E9)", border: "none", color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", cursor: "pointer", boxShadow: "0 2px 8px rgba(8,145,178,0.3)" }}'''

new_send_btn = '''style={{ width: 42, height: 42, borderRadius: "50%", background: "linear-gradient(135deg, #0891B2, #0EA5E9)", border: "none", color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", cursor: "pointer", boxShadow: "0 2px 12px rgba(8,145,178,0.3)", transition: "transform 0.1s", flexShrink: 0 }}'''

content = content.replace(old_send_btn, new_send_btn)

print("  ✅ 8. Mesajlaşma sayfası iyileştirildi")

# ============================================================
# 9. PROFİL SAYFASI İYİLEŞTİRME
# ============================================================

# Logout button
old_logout_btn = '''style={{ ...cardStyle, display: "flex", alignItems: "center", justifyContent: "center", gap: 10, padding: 14, color: COLORS.danger, cursor: "pointer", fontWeight: 700, border: `1.5px solid ${COLORS.danger}20` }}'''

new_logout_btn = '''style={{ ...cardStyle, display: "flex", alignItems: "center", justifyContent: "center", gap: 10, padding: 14, color: COLORS.danger, cursor: "pointer", fontWeight: 700, border: "1.5px solid rgba(239,68,68,0.15)", background: "rgba(239,68,68,0.03)" }}'''

content = content.replace(old_logout_btn, new_logout_btn)

print("  ✅ 9. Profil sayfası iyileştirildi")

# ============================================================
# 10. TOAST / BİLDİRİM İYİLEŞTİRME
# ============================================================

old_toast = '''style={{ position: "fixed", top: 20, left: "50%", transform: "translateX(-50%)", zIndex: 200, background: toast.type === "success" ? COLORS.success : toast.type === "error" ? COLORS.danger : COLORS.accent, color: "#fff", padding: "12px 24px", borderRadius: 14, fontSize: 14, fontWeight: 600, boxShadow: "0 8px 24px rgba(0,0,0,0.15)", animation: "fadeIn 0.3s" }}'''

new_toast = '''style={{ position: "fixed", top: 20, left: "50%", transform: "translateX(-50%)", zIndex: 200, background: toast.type === "success" ? COLORS.success : toast.type === "error" ? COLORS.danger : COLORS.accent, color: "#fff", padding: "12px 24px", borderRadius: 14, fontSize: 14, fontWeight: 600, boxShadow: "0 8px 30px rgba(0,0,0,0.15), 0 2px 8px rgba(0,0,0,0.1)", animation: "fadeIn 0.3s", backdropFilter: "blur(8px)", maxWidth: "90%", textAlign: "center" as const }}'''

content = content.replace(old_toast, new_toast)

print("  ✅ 10. Toast bildirimleri iyileştirildi")

# ============================================================
# 11. NOTIFICATION PANEL İYİLEŞTİRME
# ============================================================

old_notif_panel = '''style={{ position: "fixed", top: 0, right: 0, bottom: 0, width: "85%", maxWidth: 340, background: "#fff", zIndex: 100, boxShadow: "-4px 0 20px rgba(0,0,0,0.1)", padding: 20, overflowY: "auto" }}'''

new_notif_panel = '''style={{ position: "fixed", top: 0, right: 0, bottom: 0, width: "85%", maxWidth: 340, background: "#fff", zIndex: 100, boxShadow: "-4px 0 30px rgba(0,0,0,0.12)", padding: 20, overflowY: "auto", borderTopLeftRadius: 20, borderBottomLeftRadius: 20 }}'''

content = content.replace(old_notif_panel, new_notif_panel)

print("  ✅ 11. Bildirim paneli iyileştirildi")

# ============================================================
# 12. GLOBAL SCROLL VE PADDING FIX
# ============================================================

# Content area padding bottom for bottom nav
old_content_style = '''style={{ flex: 1, overflowY: "auto", background: COLORS.bg, paddingBottom: 80 }}'''
new_content_style = '''style={{ flex: 1, overflowY: "auto", background: COLORS.bg, paddingBottom: 85 }}'''
content = content.replace(old_content_style, new_content_style)

print("  ✅ 12. Scroll ve padding düzeltmeleri")

# ============================================================
# 13. SESSION STATUS BADGE İYİLEŞTİRME
# ============================================================

# Already uses good colors, just improve border-radius consistency
content = content.replace('borderRadius: 20, padding: "4px 12px", fontSize: 12, fontWeight: 700', 'borderRadius: 10, padding: "4px 10px", fontSize: 11, fontWeight: 700, letterSpacing: "0.2px"')

print("  ✅ 13. Durum etiketleri iyileştirildi")

# ============================================================
# SAVE
# ============================================================
open(filepath, 'w').write(content)

print("")
print("🎉 TASARIM İYİLEŞTİRMELERİ TAMAMLANDI!")
print("  - Header: Glassmorphism efekt")
print("  - Kartlar: Soft gölgeler")
print("  - Alt nav: Blur efekt")
print("  - Giriş/Kayıt: Daha modern gölgeler")
print("  - Takvim günleri: Gradient seçim")
print("  - Saat slotları: Daha büyük, modern")
print("  - Mesajlaşma: Daha yuvarlak balonlar")
print("  - Input alanları: Yumuşak geçişler")
print("  - Toast/Bildirim: Blur efekt")
print("")
print("Şimdi: npm run build")
