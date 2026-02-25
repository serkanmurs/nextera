import sys

filepath = sys.argv[1]
content = open(filepath, 'r').read()

# 1. Update SessionsPage to include Google Calendar events display and connection status
old_sessions_sig = 'function SessionsPage({ user, sessions, users, onBook, isAdmin }: { user: UserType; sessions: SessionType[]; users: UserType[]; onBook: (d: string, t: string) => void; isAdmin: boolean }) {'
new_sessions_sig = '''function SessionsPage({ user, sessions, users, onBook, isAdmin }: { user: UserType; sessions: SessionType[]; users: UserType[]; onBook: (d: string, t: string) => void; isAdmin: boolean }) {
  const [calendarEvents, setCalendarEvents] = useState<any[]>([]);
  const [calendarConnected, setCalendarConnected] = useState(false);
  const [loadingCal, setLoadingCal] = useState(false);

  useEffect(() => {
    const checkCalendar = async () => {
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
    checkCalendar();
    // Check URL for google=connected param
    if (typeof window !== "undefined" && window.location.search.includes("google=connected")) {
      setCalendarConnected(true);
      window.history.replaceState({}, "", window.location.pathname);
    }
  }, []);'''

content = content.replace(old_sessions_sig, new_sessions_sig)

# 2. Replace the Google Calendar section at the bottom of SessionsPage
old_cal_section = '''      <div style={{ ...cardStyle, background: "linear-gradient(135deg, #EFF6FF, #F0FDFA)", border: "2px dashed #93C5FD", textAlign: "center", padding: 24 }}>
        <Icons.Calendar />
        <h4 style={{ margin: "8px 0 4px", fontSize: 15, fontWeight: 700 }}>Google Takvim Entegrasyonu</h4>
        <p style={{ fontSize: 13, color: COLORS.textLight, margin: 0 }}>Seanslarınız otomatik olarak Google Takvim&apos;e eklenir.</p>
      </div>'''

new_cal_section = '''      {/* Google Calendar Section */}
      <div style={cardStyle}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
          <h3 style={{ margin: 0, fontSize: 15, fontWeight: 700 }}>📆 Google Takvim</h3>
          {calendarConnected ? (
            <span style={{ background: "#10B98115", color: "#10B981", borderRadius: 20, padding: "4px 12px", fontSize: 12, fontWeight: 700 }}>✅ Bağlı</span>
          ) : (
            <button onClick={() => window.location.href = "/api/auth/google"} style={{ background: "#fff", color: "#0891B2", border: "2px solid #0891B2", borderRadius: 10, padding: "6px 14px", fontSize: 12, fontWeight: 700, cursor: "pointer" }}>🔗 Bağla</button>
          )}
        </div>
        
        {loadingCal ? (
          <p style={{ color: "#64748B", fontSize: 14, textAlign: "center", padding: 16 }}>Takvim yükleniyor...</p>
        ) : calendarConnected && calendarEvents.length > 0 ? (
          <div>
            {calendarEvents.slice(0, 5).map((event: any, idx: number) => {
              const start = event.start?.dateTime || event.start?.date || "";
              const startDate = start ? new Date(start) : null;
              const timeStr = startDate ? startDate.toLocaleTimeString("tr-TR", { hour: "2-digit", minute: "2-digit" }) : "";
              const dateStr = startDate ? startDate.toLocaleDateString("tr-TR", { day: "numeric", month: "short" }) : "";
              return (
                <div key={event.id || idx} style={{ display: "flex", alignItems: "center", gap: 12, padding: "10px 0", borderBottom: "1px solid #E2E8F0" }}>
                  <div style={{ width: 42, height: 42, borderRadius: 10, background: "#3B82F612", display: "flex", flexDirection: "column" as const, alignItems: "center", justifyContent: "center", color: "#3B82F6" }}>
                    <div style={{ fontSize: 10, fontWeight: 600 }}>{dateStr}</div>
                    <div style={{ fontSize: 13, fontWeight: 800 }}>{timeStr}</div>
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 600, fontSize: 13 }}>{event.summary || "Etkinlik"}</div>
                    {event.conferenceData?.entryPoints?.[0]?.uri && (
                      <div style={{ fontSize: 11, color: "#0891B2", marginTop: 2 }}>🎥 Google Meet linki mevcut</div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        ) : calendarConnected ? (
          <p style={{ color: "#64748B", fontSize: 13, textAlign: "center", padding: 16 }}>Yaklaşan takvim etkinliği yok.</p>
        ) : (
          <div style={{ textAlign: "center", padding: 16 }}>
            <p style={{ color: "#64748B", fontSize: 13, margin: "0 0 12px" }}>Google Takvim&apos;inizi bağlayarak seanslarınızı otomatik takviminize ekleyin.</p>
            <button onClick={() => window.location.href = "/api/auth/google"} style={{ background: "linear-gradient(135deg, #0891B2, #0EA5E9)", color: "#fff", border: "none", borderRadius: 12, padding: "10px 20px", fontSize: 14, fontWeight: 700, cursor: "pointer", boxShadow: "0 4px 14px rgba(8,145,178,0.3)" }}>🔗 Google Takvim Bağla</button>
          </div>
        )}
      </div>'''

content = content.replace(old_cal_section, new_cal_section)

open(filepath, 'w').write(content)
print("Done! Page updated with Google Calendar display.")
