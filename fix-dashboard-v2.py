filepath = 'src/app/page.tsx'
content = open(filepath, 'r').read()

print("Fix v2 basliyor...")

# 1. FETCH - Promise.all icerisine tasks ve journal ekle
old_fetch = '''      const [usersRes, sessionsRes, messagesRes, notifsRes] = await Promise.all([
        supabase.from("users").select("*"),
        supabase.from("sessions").select("*"),
        supabase.from("messages").select("*").or(`sender_id.eq.${userId},receiver_id.eq.${userId}`).order("created_at", { ascending: true }),
        supabase.from("notifications").select("*").eq("user_id", userId).order("created_at", { ascending: false }),
      ]);
      if (usersRes.data) setUsers(usersRes.data);
      if (sessionsRes.data) setSessions(sessionsRes.data);
      if (messagesRes.data) setMessages(messagesRes.data);
      if (notifsRes.data) setNotifications(notifsRes.data);'''

new_fetch = '''      const [usersRes, sessionsRes, messagesRes, notifsRes, tasksRes, journalRes] = await Promise.all([
        supabase.from("users").select("*"),
        supabase.from("sessions").select("*"),
        supabase.from("messages").select("*").or(`sender_id.eq.${userId},receiver_id.eq.${userId}`).order("created_at", { ascending: true }),
        supabase.from("notifications").select("*").eq("user_id", userId).order("created_at", { ascending: false }),
        supabase.from("tasks").select("*"),
        supabase.from("journal").select("*").order("created_at", { ascending: false }),
      ]);
      if (usersRes.data) setUsers(usersRes.data);
      if (sessionsRes.data) setSessions(sessionsRes.data);
      if (messagesRes.data) setMessages(messagesRes.data);
      if (notifsRes.data) setNotifications(notifsRes.data);
      if (tasksRes.data) setTasks(tasksRes.data);
      if (journalRes.data) setJournal(journalRes.data);'''

if old_fetch in content:
    content = content.replace(old_fetch, new_fetch)
    print("  OK 1. Fetch eklendi (tasks + journal)")
else:
    print("  SKIP 1. Fetch bulunamadi")

# 2. Ilerleme kartlari - ClientHome return icine, Danismaniniz kartindan once
# Mevcut yaklasan seanslarim basligindan once ekleyelim
old_upcoming = '        <h3 style={{ margin: "0 0 14px", fontSize: 16, fontWeight: 700 }}>Yaklasan Seanslarim</h3>'

# Turkce karakterli versiyon deneyelim
if old_upcoming not in content:
    # Gercek metni bulalim
    import re
    match = re.search(r'<h3[^>]*>.*?Yakla.*?Seans.*?</h3>', content)
    if match:
        print(f"  DEBUG: Bulunan baslik: {match.group()[:60]}")

# Farkli yaklasim: cardStyle tanimlamasindan sonra return basina ekleyelim
# ClientHome'un return basini bulalim
old_return = '''  return (
    <div style={{ padding: 16 }}>
      <h2 style={{ margin: "0 0 4px", fontSize: 22, fontWeight: 800, letterSpacing: "-0.3px" }}>Merhaba, {user.name.split(" ")[0]}! '''

if old_return not in content:
    # Basit versiyon
    old_return = '      <h2 style={{ margin: "0 0 4px", fontSize: 22, fontWeight: 800'
    if old_return in content:
        # Merhaba basligini bulduk, ondan sonraki subtitle'i bulup ardindan ekleyelim
        pass

# En guvenli yol: "Aksiyon Planim" blogundan ONCE ilerleme kartlarini ekle
old_aksiyon = '      {/* Aksiyon'

progress_and_focus = '''      {/* Haftalik Odak */}
      <div style={{ ...cardStyle, background: "#F0F9FF", border: "1px solid #BAE6FD" }}>
        <div style={{ fontSize: 13, fontWeight: 700, color: COLORS.primary, marginBottom: 8 }}>Bu Haftaki Odagin</div>
        <div style={{ fontSize: 14, color: COLORS.text, lineHeight: 1.5, fontStyle: "italic" }}>Her seans bir farkindalik, her farkindalik bir adim. Bugun hangi adimi atacaksin?</div>
      </div>

      {/* Ilerleme + Milestone */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
        <div style={cardStyle}>
          <div style={{ fontSize: 12, fontWeight: 700, color: COLORS.textLight, marginBottom: 8 }}>Ilerleme</div>
          <div style={{ fontSize: 24, fontWeight: 800, color: COLORS.primary }}>{completed.length}/{mySessions.length}</div>
          <div style={{ fontSize: 11, color: COLORS.textLight, marginBottom: 8 }}>Seans Tamamlandi</div>
          <div style={{ height: 6, borderRadius: 3, background: "#E2E8F0", overflow: "hidden" }}>
            <div style={{ height: "100%", borderRadius: 3, background: COLORS.primary, width: mySessions.length > 0 ? String(Math.round(completed.length / mySessions.length * 100)) + "%" : "0%", transition: "width 0.5s" }} />
          </div>
          <div style={{ fontSize: 11, color: COLORS.textLight, marginTop: 4 }}>{mySessions.length > 0 ? Math.round(completed.length / mySessions.length * 100) : 0}% tamamlandi</div>
        </div>
        <div style={cardStyle}>
          <div style={{ fontSize: 12, fontWeight: 700, color: COLORS.textLight, marginBottom: 8 }}>Sonraki Hedef</div>
          {upcoming.length > 0 ? (<><div style={{ fontSize: 14, fontWeight: 700, color: COLORS.text }}>{formatDate(upcoming[0].date)}</div><div style={{ fontSize: 12, color: COLORS.textLight, marginTop: 2 }}>{upcoming[0].time} - Online Seans</div><div style={{ marginTop: 8, fontSize: 11, color: COLORS.primary, fontWeight: 600 }}>Hazirlan ve Odaklan</div></>) : (<div style={{ fontSize: 13, color: COLORS.textLight }}>Yeni seans planla</div>)}
        </div>
      </div>

      {/* Siradaki Seans */}
      {upcoming.length > 0 && (
        <div style={{ ...cardStyle, background: "linear-gradient(135deg, #0E7490, #155E75)", color: "#fff", border: "none" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
            <div>
              <div style={{ fontSize: 12, opacity: 0.8, fontWeight: 600, marginBottom: 4 }}>Siradaki Seansin</div>
              <div style={{ fontSize: 20, fontWeight: 800 }}>{formatDate(upcoming[0].date)}</div>
              <div style={{ fontSize: 14, opacity: 0.9, marginTop: 2 }}>{upcoming[0].time} - {upcoming[0].duration} dk</div>
            </div>
            <div style={{ background: "rgba(255,255,255,0.15)", borderRadius: 12, padding: "8px 12px", fontSize: 13, fontWeight: 700 }}>
              {(() => { const now = new Date(); const s = new Date(upcoming[0].date + "T" + upcoming[0].time + ":00+03:00"); const diff = Math.round((s.getTime() - now.getTime()) / 86400000); return diff === 0 ? "Bugun" : diff === 1 ? "Yarin" : diff + " gun"; })()}
            </div>
          </div>
          <div style={{ marginTop: 12, padding: "10px", borderRadius: 10, background: "rgba(255,255,255,0.15)", textAlign: "center" as const, fontSize: 13, fontWeight: 700, cursor: "pointer" }}>Seansa Katil</div>
        </div>
      )}

      {/* Aksiyon'''

if old_aksiyon in content:
    content = content.replace(old_aksiyon, progress_and_focus, 1)
    print("  OK 2. Haftalik Odak + Ilerleme + Siradaki Seans eklendi")
else:
    print("  SKIP 2. Aksiyon blogu bulunamadi")

# SAVE
open(filepath, 'w').write(content)
print("Dosya kaydedildi. Simdi: npm run build")
