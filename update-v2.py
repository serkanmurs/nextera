import sys

filepath = 'src/app/page.tsx'
content = open(filepath, 'r').read()

print("🔄 Güncellemeler başlıyor...")

# ============================================================
# 1. SEANS SAATLERİ: 19:00 - 21:00 (son seans 21:00-22:00)
# ============================================================
old_time_slots = '''const TIME_SLOTS = [
  "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"
];'''

new_time_slots = '''const TIME_SLOTS = [
  "19:00", "20:00", "21:00"
];'''

content = content.replace(old_time_slots, new_time_slots)
print("  ✅ 1. Seans saatleri 19:00-21:00 olarak güncellendi")

# ============================================================
# 2. GOOGLE TAKVİM DOLU SAAT KONTROLÜ + MEET LİNKİ
# SessionsPage'e busy check ve meet link gösterimi ekle
# ============================================================

# SessionsPage state'lerine busySlots ekle
old_sessions_states = '''  const [calendarEvents, setCalendarEvents] = useState<any[]>([]);
  const [calendarConnected, setCalendarConnected] = useState(false);
  const [loadingCal, setLoadingCal] = useState(false);'''

new_sessions_states = '''  const [calendarEvents, setCalendarEvents] = useState<any[]>([]);
  const [calendarConnected, setCalendarConnected] = useState(false);
  const [loadingCal, setLoadingCal] = useState(false);
  const [busySlots, setBusySlots] = useState<Record<string, string[]>>({});'''

content = content.replace(old_sessions_states, new_sessions_states)

# Update checkCalendar to also extract busy slots
old_check_cal = '''    const checkCalendar = async () => {
      try {
        setLoadingCal(true);
        const res = await fetch("/api/calendar");
        const data = await res.json();
        if (data.success && data.events) {
          setCalendarConnected(true);
          setCalendarEvents(data.events);
        }
      } catch (e) {
        console.log("Calendar not connected");
      } finally {
        setLoadingCal(false);
      }
    };
    checkCalendar();'''

new_check_cal = '''    const checkCalendar = async () => {
      try {
        setLoadingCal(true);
        const res = await fetch("/api/calendar");
        const data = await res.json();
        if (data.success && data.events) {
          setCalendarConnected(true);
          setCalendarEvents(data.events);
          // Extract busy slots per date
          const busy: Record<string, string[]> = {};
          data.events.forEach((ev: any) => {
            const start = ev.start?.dateTime;
            if (start) {
              const d = new Date(start);
              const dateKey = d.toISOString().split("T")[0];
              const hour = d.getHours().toString().padStart(2, "0") + ":00";
              if (!busy[dateKey]) busy[dateKey] = [];
              busy[dateKey].push(hour);
            }
          });
          setBusySlots(busy);
        }
      } catch (e) {
        console.log("Calendar not connected");
      } finally {
        setLoadingCal(false);
      }
    };
    checkCalendar();'''

content = content.replace(old_check_cal, new_check_cal)

# Update time slot rendering to check busy slots from Google Calendar
old_booked_times = '  const bookedTimes = sessions.filter(s => s.date === selectedDate).map(s => s.time);'
new_booked_times = '''  const bookedTimes = sessions.filter(s => s.date === selectedDate && s.status !== "cancelled").map(s => s.time);
  const calBusyTimes = busySlots[selectedDate] || [];
  const allBusyTimes = [...new Set([...bookedTimes, ...calBusyTimes])];'''

content = content.replace(old_booked_times, new_booked_times)

# Update the booked check in time slot buttons
content = content.replace(
    'const booked = bookedTimes.includes(t);',
    'const booked = allBusyTimes.includes(t);'
)

print("  ✅ 2. Google Takvim dolu saat kontrolü eklendi")

# ============================================================
# 3. MEET LİNKİ GÖSTERİMİ + SEANSA KATIL BUTONU
# Session listesinde meet linki ve katıl butonu göster
# sessions tablosuna meet_link alanı eklemek yerine, 
# calendar event'ten çekeceğiz. Ama basitlik için 
# seans kartlarına "Seansa Katıl" butonu ekleyelim
# ============================================================

# Update session item in history to show Meet link for upcoming sessions
old_session_list_item = '''              <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                <span style={{ background: `${statusColors[s.status]}15`, color: statusColors[s.status], borderRadius: 20, padding: "4px 12px", fontSize: 12, fontWeight: 700 }}>{statusLabels[s.status]}</span>
                {s.status === "upcoming" && !isAdmin && (
                  <button onClick={() => { if (confirm("Seansı iptal etmek istediğinize emin misiniz?")) onCancel(s.id); }} style={{ background: "none", border: "1px solid #EF4444", borderRadius: 8, padding: "3px 8px", fontSize: 11, color: "#EF4444", cursor: "pointer", fontWeight: 600 }}>İptal</button>
                )}
                {isAdmin && (
                  <button onClick={() => { if (confirm("Seansı silmek istediğinize emin misiniz?")) onDelete(s.id); }} style={{ background: "none", border: "1px solid #EF4444", borderRadius: 8, padding: "3px 8px", fontSize: 11, color: "#EF4444", cursor: "pointer", fontWeight: 600 }}>Sil</button>
                )}
              </div>'''

new_session_list_item = '''              <div style={{ display: "flex", alignItems: "center", gap: 6, flexWrap: "wrap" as const }}>
                <span style={{ background: `${statusColors[s.status]}15`, color: statusColors[s.status], borderRadius: 20, padding: "4px 12px", fontSize: 12, fontWeight: 700 }}>{statusLabels[s.status]}</span>
                {s.status === "upcoming" && (() => {
                  const matchingEvent = calendarEvents.find((ev: any) => {
                    const evDate = ev.start?.dateTime ? new Date(ev.start.dateTime).toISOString().split("T")[0] : "";
                    const evHour = ev.start?.dateTime ? new Date(ev.start.dateTime).getHours().toString().padStart(2, "0") + ":00" : "";
                    return evDate === s.date && evHour === s.time;
                  });
                  const meetLink = matchingEvent?.conferenceData?.entryPoints?.[0]?.uri || matchingEvent?.hangoutLink;
                  const now = new Date();
                  const sessionStart = new Date(`${s.date}T${s.time}:00+03:00`);
                  const diffMin = (sessionStart.getTime() - now.getTime()) / 60000;
                  const canJoin = diffMin <= 15 && diffMin >= -60;
                  return meetLink && canJoin ? (
                    <a href={meetLink} target="_blank" rel="noopener noreferrer" style={{ background: "linear-gradient(135deg, #10B981, #059669)", color: "#fff", borderRadius: 8, padding: "4px 10px", fontSize: 11, fontWeight: 700, textDecoration: "none", display: "inline-flex", alignItems: "center", gap: 3 }}>🎥 Seansa Katıl</a>
                  ) : meetLink ? (
                    <span style={{ fontSize: 10, color: "#64748B" }}>🎥 Meet hazır</span>
                  ) : null;
                })()}
                {s.status === "upcoming" && !isAdmin && (
                  <button onClick={() => { if (confirm("Seansı iptal etmek istediğinize emin misiniz?")) onCancel(s.id); }} style={{ background: "none", border: "1px solid #EF4444", borderRadius: 8, padding: "3px 8px", fontSize: 11, color: "#EF4444", cursor: "pointer", fontWeight: 600 }}>İptal</button>
                )}
                {isAdmin && (
                  <button onClick={() => { if (confirm("Seansı silmek istediğinize emin misiniz?")) onDelete(s.id); }} style={{ background: "none", border: "1px solid #EF4444", borderRadius: 8, padding: "3px 8px", fontSize: 11, color: "#EF4444", cursor: "pointer", fontWeight: 600 }}>Sil</button>
                )}
              </div>'''

content = content.replace(old_session_list_item, new_session_list_item)
print("  ✅ 3. Meet linki + Seansa Katıl butonu eklendi")

# ============================================================
# 4. MESAJ BİLDİRİM ROZETİ (BADGE)
# ============================================================

# Add unread message count tracking
# In main app, add unreadMessages state and calculation
old_unread_notifs = '  const unreadNotifs = notifications.filter(n => !n.is_read).length;'
new_unread_notifs = '''  const unreadNotifs = notifications.filter(n => !n.is_read).length;

  // Unread message count
  const getUnreadMessageCount = useCallback(() => {
    if (!currentUser) return 0;
    // Count messages where receiver is current user and created_at > last read
    // Simple approach: count messages from others not yet seen
    const received = messages.filter(m => m.receiver_id === currentUser.id);
    // We'll track last seen in localStorage-like approach via state
    return received.length > 0 ? Math.min(received.filter(m => {
      const msgTime = new Date(m.created_at).getTime();
      const fiveMinAgo = Date.now() - 5 * 60 * 1000;
      return msgTime > fiveMinAgo;
    }).length, 99) : 0;
  }, [currentUser, messages]);

  const unreadMsgCount = getUnreadMessageCount();'''

content = content.replace(old_unread_notifs, new_unread_notifs)

# Add badge to Messages nav item
old_nav_items_client = '''{ id: "messages", label: "Mesajlar", Icon: Icons.Chat }'''
# This appears twice (admin and client), replace both
content = content.replace(
    '{ id: "messages", label: "Mesajlar", Icon: Icons.Chat }',
    '{ id: "messages", label: "Mesajlar", Icon: Icons.Chat, badge: unreadMsgCount }',
    2  # replace both occurrences
)

# Update nav rendering to show badge
old_nav_render = '''        {navItems.map(({ id, label, Icon }) => (
          <div key={id} onClick={() => setPage(id)} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 2, color: page === id ? COLORS.primary : COLORS.textLight, cursor: "pointer", fontSize: 11, fontWeight: page === id ? 700 : 500, padding: "4px 12px", borderRadius: 12 }}>
            <Icon />
            <span>{label}</span>
            {page === id && <div style={{ width: 5, height: 5, borderRadius: "50%", background: COLORS.primary, marginTop: 2 }} />}
          </div>'''

new_nav_render = '''        {navItems.map(({ id, label, Icon, badge }: any) => (
          <div key={id} onClick={() => setPage(id)} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 2, color: page === id ? COLORS.primary : COLORS.textLight, cursor: "pointer", fontSize: 11, fontWeight: page === id ? 700 : 500, padding: "4px 12px", borderRadius: 12, position: "relative" as const }}>
            <div style={{ position: "relative" as const }}>
              <Icon />
              {badge > 0 && <span style={{ position: "absolute", top: -4, right: -8, minWidth: 16, height: 16, borderRadius: "50%", background: "#EF4444", color: "#fff", fontSize: 9, fontWeight: 800, display: "flex", alignItems: "center", justifyContent: "center", padding: "0 3px" }}>{badge}</span>}
            </div>
            <span>{label}</span>
            {page === id && <div style={{ width: 5, height: 5, borderRadius: "50%", background: COLORS.primary, marginTop: 2 }} />}
          </div>'''

content = content.replace(old_nav_render, new_nav_render)
print("  ✅ 4. Mesaj bildirim rozeti (badge) eklendi")

# ============================================================
# 5. SEANS DEĞERLENDİRME SİSTEMİ
# Tamamlanan seanslara değerlendirme özelliği ekle
# ============================================================

# Add rating modal state to main app
old_show_notifs = '  const [showNotifications, setShowNotifications] = useState(false);'
new_show_notifs = '''  const [showNotifications, setShowNotifications] = useState(false);
  const [ratingSession, setRatingSession] = useState<string | null>(null);
  const [ratingValue, setRatingValue] = useState(0);
  const [reviewText, setReviewText] = useState("");'''

content = content.replace(old_show_notifs, new_show_notifs)

# Add handleRateSession function before handleBookSession
old_cancel_session = '  // ---- Cancel Session ----'
new_cancel_session = '''  // ---- Rate Session ----
  const handleRateSession = async (sessionId: string, rating: number, review: string) => {
    const { error } = await supabase.from("sessions").update({ rating, review }).eq("id", sessionId);
    if (!error) {
      setSessions(prev => prev.map(s => s.id === sessionId ? { ...s, rating, review } : s));
      setRatingSession(null);
      setRatingValue(0);
      setReviewText("");
      showToast("Değerlendirmeniz kaydedildi! ⭐", "success");
    } else {
      showToast("Hata: " + error.message, "error");
    }
  };

  // ---- Cancel Session ----'''

content = content.replace(old_cancel_session, new_cancel_session)

# Add rating modal in the main render, before bottom nav
old_bottom_nav = '''      {/* Bottom Nav */}'''
new_bottom_nav = '''      {/* Rating Modal */}
      {ratingSession && (
        <div style={{ position: "fixed", top: 0, left: 0, right: 0, bottom: 0, zIndex: 100, display: "flex", alignItems: "center", justifyContent: "center" }}>
          <div onClick={() => { setRatingSession(null); setRatingValue(0); setReviewText(""); }} style={{ position: "absolute", inset: 0, background: "rgba(0,0,0,0.4)" }} />
          <div style={{ position: "relative", background: "#fff", borderRadius: 20, padding: 28, width: "90%", maxWidth: 380, zIndex: 101 }}>
            <h3 style={{ margin: "0 0 4px", fontSize: 18, fontWeight: 800, textAlign: "center" }}>⭐ Seansı Değerlendir</h3>
            <p style={{ margin: "0 0 20px", fontSize: 13, color: "#64748B", textAlign: "center" }}>Deneyiminizi puanlayın ve yorumunuzu paylaşın.</p>
            <div style={{ display: "flex", justifyContent: "center", gap: 8, marginBottom: 16 }}>
              {[1, 2, 3, 4, 5].map(i => (
                <span key={i} onClick={() => setRatingValue(i)} style={{ cursor: "pointer", fontSize: 32 }}>{i <= ratingValue ? "⭐" : "☆"}</span>
              ))}
            </div>
            <textarea
              value={reviewText}
              onChange={e => setReviewText(e.target.value)}
              placeholder="Yorumunuzu yazın (isteğe bağlı)..."
              style={{ width: "100%", padding: "12px 16px", borderRadius: 12, border: "1.5px solid #E2E8F0", fontSize: 14, outline: "none", boxSizing: "border-box", minHeight: 80, resize: "vertical", fontFamily: "inherit" }}
            />
            <div style={{ display: "flex", gap: 8, marginTop: 16 }}>
              <button onClick={() => { setRatingSession(null); setRatingValue(0); setReviewText(""); }} style={{ flex: 1, padding: "10px", borderRadius: 12, border: "1.5px solid #E2E8F0", background: "#fff", fontSize: 14, fontWeight: 600, cursor: "pointer", color: "#64748B" }}>Vazgeç</button>
              <button onClick={() => { if (ratingValue > 0) handleRateSession(ratingSession, ratingValue, reviewText); }} disabled={ratingValue === 0} style={{ flex: 1, padding: "10px", borderRadius: 12, border: "none", background: ratingValue > 0 ? "linear-gradient(135deg, #F59E0B, #F97316)" : "#E2E8F0", color: ratingValue > 0 ? "#fff" : "#94A3B8", fontSize: 14, fontWeight: 700, cursor: ratingValue > 0 ? "pointer" : "default" }}>Gönder ⭐</button>
            </div>
          </div>
        </div>
      )}

      {/* Bottom Nav */}'''

content = content.replace(old_bottom_nav, new_bottom_nav)

# In ClientHome, add "Değerlendir" button for completed sessions without rating
old_client_rating = '''            {s.rating ? (
              <div style={{ marginTop: 8 }}>
                <StarRating rating={s.rating} readonly />
                {s.review && <p style={{ margin: "4px 0 0", fontSize: 12, color: COLORS.textLight, fontStyle: "italic" }}>&ldquo;{s.review}&rdquo;</p>}
              </div>
            ) : <div style={{ marginTop: 6, fontSize: 12, color: COLORS.secondary, fontWeight: 600 }}>⭐ Değerlendir</div>}'''

new_client_rating = '''            {s.rating ? (
              <div style={{ marginTop: 8 }}>
                <StarRating rating={s.rating} readonly />
                {s.review && <p style={{ margin: "4px 0 0", fontSize: 12, color: COLORS.textLight, fontStyle: "italic" }}>&ldquo;{s.review}&rdquo;</p>}
              </div>
            ) : <div onClick={() => { setRatingSession(s.id); setRatingValue(0); setReviewText(""); }} style={{ marginTop: 6, fontSize: 12, color: COLORS.secondary, fontWeight: 600, cursor: "pointer" }}>⭐ Değerlendir</div>}'''

# This won't work directly because ClientHome doesn't have access to setRatingSession
# We need to pass it as a prop. Let's update ClientHome.

# First update ClientHome signature
old_client_home_sig = 'function ClientHome({ user, sessions, users }: { user: UserType; sessions: SessionType[]; users: UserType[] }) {'
new_client_home_sig = 'function ClientHome({ user, sessions, users, onRate }: { user: UserType; sessions: SessionType[]; users: UserType[]; onRate: (id: string) => void }) {'
content = content.replace(old_client_home_sig, new_client_home_sig)

# Update the rating click in ClientHome
content = content.replace(
    ') : <div style={{ marginTop: 6, fontSize: 12, color: COLORS.secondary, fontWeight: 600 }}>⭐ Değerlendir</div>}',
    ') : <div onClick={() => onRate(s.id)} style={{ marginTop: 6, fontSize: 12, color: COLORS.secondary, fontWeight: 600, cursor: "pointer" }}>⭐ Değerlendir</div>}'
)

# Update ClientHome rendering to pass onRate
old_client_home_render = '{page === "home" && (isAdmin ? <AdminDashboard users={users} sessions={sessions} /> : currentUser && <ClientHome user={currentUser} sessions={sessions} users={users} />)}'
new_client_home_render = '{page === "home" && (isAdmin ? <AdminDashboard users={users} sessions={sessions} /> : currentUser && <ClientHome user={currentUser} sessions={sessions} users={users} onRate={(id) => { setRatingSession(id); setRatingValue(0); setReviewText(""); }} />)}'
content = content.replace(old_client_home_render, new_client_home_render)

print("  ✅ 5. Seans değerlendirme sistemi (1-5 yıldız + yorum) eklendi")

# ============================================================
# 6. SEANS SÜRESİNİ 60 DK YAP (tekrar kontrol)
# ============================================================
content = content.replace('duration: 50,', 'duration: 60,')
content = content.replace('duration: 50', 'duration: 60')
print("  ✅ 6. Seans süresi 60 dakika olarak güncellendi")

# ============================================================
# SAVE
# ============================================================
open(filepath, 'w').write(content)

print("")
print("🎉 TÜM GÜNCELLEMELER TAMAMLANDI!")
print("  1. Seans saatleri: 19:00, 20:00, 21:00")
print("  2. Google Takvim dolu saat kontrolü")
print("  3. Meet linki + Seansa Katıl butonu")
print("  4. Mesaj bildirim rozeti (badge)")
print("  5. Seans değerlendirme (1-5 yıldız + yorum)")
print("  6. Seans süresi 60 dakika")
print("")
print("Şimdi: npm run build")
