import sys

filepath = 'src/app/page.tsx'
content = open(filepath, 'r').read()

# ============================================================
# UPDATE 1: Add cancelSession function to main app
# ============================================================
old_book = '''  // ---- Book Session ----
  const handleBookSession = async (date: string, time: string) => {'''

new_book = '''  // ---- Cancel Session ----
  const handleCancelSession = async (sessionId: string) => {
    const { error } = await supabase.from("sessions").update({ status: "cancelled" }).eq("id", sessionId);
    if (!error) {
      setSessions(prev => prev.map(s => s.id === sessionId ? { ...s, status: "cancelled" } : s));
      showToast("Seans iptal edildi.", "info");
    } else {
      showToast("Hata: " + error.message, "error");
    }
  };

  // ---- Delete Session (Admin) ----
  const handleDeleteSession = async (sessionId: string) => {
    const { error } = await supabase.from("sessions").delete().eq("id", sessionId);
    if (!error) {
      setSessions(prev => prev.filter(s => s.id !== sessionId));
      showToast("Seans silindi.", "info");
    } else {
      showToast("Hata: " + error.message, "error");
    }
  };

  // ---- Book Session ----
  const handleBookSession = async (date: string, time: string) => {'''

content = content.replace(old_book, new_book)

# ============================================================
# UPDATE 2: Pass cancel/delete to SessionsPage
# ============================================================
old_sessions_render = '{page === "sessions" && currentUser && <SessionsPage user={currentUser} sessions={sessions} users={users} onBook={handleBookSession} isAdmin={isAdmin} />}'
new_sessions_render = '{page === "sessions" && currentUser && <SessionsPage user={currentUser} sessions={sessions} users={users} onBook={handleBookSession} onCancel={handleCancelSession} onDelete={handleDeleteSession} isAdmin={isAdmin} />}'
content = content.replace(old_sessions_render, new_sessions_render)

# ============================================================
# UPDATE 3: Update SessionsPage signature
# ============================================================
old_sessions_sig = 'function SessionsPage({ user, sessions, users, onBook, isAdmin }: { user: UserType; sessions: SessionType[]; users: UserType[]; onBook: (d: string, t: string) => void; isAdmin: boolean }) {'
new_sessions_sig = 'function SessionsPage({ user, sessions, users, onBook, onCancel, onDelete, isAdmin }: { user: UserType; sessions: SessionType[]; users: UserType[]; onBook: (d: string, t: string) => void; onCancel: (id: string) => void; onDelete: (id: string) => void; isAdmin: boolean }) {'
content = content.replace(old_sessions_sig, new_sessions_sig)

# ============================================================
# UPDATE 4: Add cancel/delete buttons in session list items
# ============================================================
old_session_item = '''              <span style={{ background: `${statusColors[s.status]}15`, color: statusColors[s.status], borderRadius: 20, padding: "4px 12px", fontSize: 12, fontWeight: 700 }}>{statusLabels[s.status]}</span>
            </div>
          );
        })}
      </div>'''

new_session_item = '''              <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                <span style={{ background: `${statusColors[s.status]}15`, color: statusColors[s.status], borderRadius: 20, padding: "4px 12px", fontSize: 12, fontWeight: 700 }}>{statusLabels[s.status]}</span>
                {s.status === "upcoming" && !isAdmin && (
                  <button onClick={() => { if (confirm("Seansı iptal etmek istediğinize emin misiniz?")) onCancel(s.id); }} style={{ background: "none", border: "1px solid #EF4444", borderRadius: 8, padding: "3px 8px", fontSize: 11, color: "#EF4444", cursor: "pointer", fontWeight: 600 }}>İptal</button>
                )}
                {isAdmin && (
                  <button onClick={() => { if (confirm("Seansı silmek istediğinize emin misiniz?")) onDelete(s.id); }} style={{ background: "none", border: "1px solid #EF4444", borderRadius: 8, padding: "3px 8px", fontSize: 11, color: "#EF4444", cursor: "pointer", fontWeight: 600 }}>Sil</button>
                )}
              </div>
            </div>
          );
        })}
      </div>'''

content = content.replace(old_session_item, new_session_item)

# ============================================================
# UPDATE 5: Add clickable client list modal in AdminDashboard
# ============================================================
old_admin_sig = 'function AdminDashboard({ users, sessions }: { users: UserType[]; sessions: SessionType[] }) {'
new_admin_sig = '''function AdminDashboard({ users, sessions }: { users: UserType[]; sessions: SessionType[] }) {
  const [showClientList, setShowClientList] = useState(false);'''
content = content.replace(old_admin_sig, new_admin_sig)

# Make the stat cards clickable - find "Toplam Danışan" stat
old_stat_grid = '''        {[
          { icon: <Icons.Users />, label: "Toplam Danışan", value: clients.length, color: COLORS.primary },'''
new_stat_grid = '''        {[
          { icon: <Icons.Users />, label: "Toplam Danışan", value: clients.length, color: COLORS.primary, onClick: () => setShowClientList(true) },'''
content = content.replace(old_stat_grid, new_stat_grid)

# Update the stat card rendering to support onClick
old_stat_render = '''        ].map((s, i) => (
          <div key={i} style={{ ...cardStyle, padding: 16, display: "flex", alignItems: "center", gap: 14 }}>
            <div style={{ width: 50, height: 50, borderRadius: 14, background: `${s.color}12`, display: "flex", alignItems: "center", justifyContent: "center", color: s.color }}>{s.icon}</div>
            <div><div style={{ fontSize: 24, fontWeight: 800, color: s.color }}>{s.value}</div><div style={{ fontSize: 13, color: COLORS.textLight }}>{s.label}</div></div>
          </div>
        ))}'''

new_stat_render = '''        ].map((s: any, i: number) => (
          <div key={i} onClick={s.onClick} style={{ ...cardStyle, padding: 16, display: "flex", alignItems: "center", gap: 14, cursor: s.onClick ? "pointer" : "default" }}>
            <div style={{ width: 50, height: 50, borderRadius: 14, background: `${s.color}12`, display: "flex", alignItems: "center", justifyContent: "center", color: s.color }}>{s.icon}</div>
            <div><div style={{ fontSize: 24, fontWeight: 800, color: s.color }}>{s.value}</div><div style={{ fontSize: 13, color: COLORS.textLight }}>{s.label}</div></div>
          </div>
        ))}

        {/* Client List Modal */}
        {showClientList && (
          <div style={{ position: "fixed", top: 0, left: 0, right: 0, bottom: 0, zIndex: 100, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <div onClick={() => setShowClientList(false)} style={{ position: "absolute", inset: 0, background: "rgba(0,0,0,0.4)" }} />
            <div style={{ position: "relative", background: "#fff", borderRadius: 20, padding: 24, width: "90%", maxWidth: 400, maxHeight: "80vh", overflowY: "auto", zIndex: 101 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
                <h3 style={{ margin: 0, fontSize: 18, fontWeight: 800 }}>👥 Tüm Danışanlar ({clients.length})</h3>
                <span onClick={() => setShowClientList(false)} style={{ cursor: "pointer", fontSize: 20 }}>✕</span>
              </div>
              {clients.map(c => {
                const cSessions = sessions.filter(s => s.client_id === c.id);
                const cCompleted = cSessions.filter(s => s.status === "completed").length;
                const cUpcoming = cSessions.filter(s => s.status === "upcoming").length;
                return (
                  <div key={c.id} style={{ display: "flex", alignItems: "center", gap: 12, padding: "12px 0", borderBottom: "1px solid #E2E8F0" }}>
                    <div style={{ width: 44, height: 44, borderRadius: "50%", background: "linear-gradient(135deg, #0891B2, #F97316)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 800, fontSize: 15 }}>{getInitials(c.name)}</div>
                    <div style={{ flex: 1 }}>
                      <div style={{ fontWeight: 700, fontSize: 14 }}>{c.name}</div>
                      <div style={{ fontSize: 12, color: "#64748B" }}>{c.email}</div>
                      <div style={{ fontSize: 12, color: "#64748B" }}>{c.city} · {c.phone}</div>
                    </div>
                    <div style={{ textAlign: "right" }}>
                      <div style={{ fontSize: 11, color: "#10B981", fontWeight: 600 }}>✅ {cCompleted}</div>
                      <div style={{ fontSize: 11, color: "#3B82F6", fontWeight: 600 }}>🗓 {cUpcoming}</div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}'''

content = content.replace(old_stat_render, new_stat_render)

# ============================================================
# UPDATE 6: Add "Forgot Password" to Login Screen
# ============================================================
old_login_register_link = '''        <div style={{ textAlign: "center", marginTop: 20 }}>
          <span style={{ color: COLORS.textLight, fontSize: 14 }}>Hesabınız yok mu? </span>
          <span style={{ color: COLORS.primary, fontWeight: 700, cursor: "pointer", fontSize: 14 }} onClick={onGoRegister}>Kayıt Ol</span>
        </div>
      </div>
    </div>
  );
}

// ==================== REGISTER SCREEN'''

new_login_register_link = '''        <div style={{ textAlign: "center", marginTop: 16 }}>
          <span style={{ color: COLORS.textLight, fontSize: 14 }}>Hesabınız yok mu? </span>
          <span style={{ color: COLORS.primary, fontWeight: 700, cursor: "pointer", fontSize: 14 }} onClick={onGoRegister}>Kayıt Ol</span>
        </div>
        <div style={{ textAlign: "center", marginTop: 8 }}>
          <span onClick={async () => {
            const resetEmail = prompt("Şifre sıfırlama linki gönderilecek e-posta adresinizi girin:");
            if (resetEmail) {
              const { error: resetError } = await supabase.auth.resetPasswordForEmail(resetEmail, { redirectTo: window.location.origin });
              if (resetError) alert("Hata: " + resetError.message);
              else alert("Şifre sıfırlama linki e-posta adresinize gönderildi!");
            }
          }} style={{ color: COLORS.textLight, fontSize: 13, cursor: "pointer", textDecoration: "underline" }}>Şifremi Unuttum</span>
        </div>
      </div>
    </div>
  );
}

// ==================== REGISTER SCREEN'''

content = content.replace(old_login_register_link, new_login_register_link)

# We need to add supabase import to LoginScreen - it uses supabase now
# LoginScreen doesn't have direct access, let's pass it as prop or use inline
# Actually supabase is already imported at top level and LoginScreen is in same file, so it works.

# ============================================================
# UPDATE 7: Add KVKK checkbox to Register Screen
# ============================================================
old_register_button = '''        <button onClick={handleRegister} disabled={loading} style={{ background: "linear-gradient(135deg, #F97316, #FB923C)", color: "#fff", border: "none", borderRadius: 12, padding: "12px 24px", fontSize: 15, fontWeight: 700, cursor: "pointer", width: "100%", boxShadow: "0 4px 14px rgba(249,115,22,0.3)", opacity: loading ? 0.7 : 1 }}>
          {loading ? "Kayıt yapılıyor..." : "Kayıt Ol"}
        </button>'''

new_register_button = '''        <div style={{ marginBottom: 16 }}>
          <label style={{ display: "flex", alignItems: "flex-start", gap: 8, cursor: "pointer" }}>
            <input type="checkbox" checked={form.kvkk || false} onChange={e => update("kvkk", e.target.checked ? "yes" : "")} style={{ marginTop: 3, width: 18, height: 18, accentColor: "#0891B2" }} />
            <span style={{ fontSize: 12, color: "#64748B", lineHeight: 1.4 }}>
              <strong>KVKK Aydınlatma Metni</strong>&apos;ni okudum ve kişisel verilerimin işlenmesini kabul ediyorum. Verileriniz güvenli şekilde saklanır ve üçüncü taraflarla paylaşılmaz.
            </span>
          </label>
        </div>

        <button onClick={handleRegister} disabled={loading} style={{ background: "linear-gradient(135deg, #F97316, #FB923C)", color: "#fff", border: "none", borderRadius: 12, padding: "12px 24px", fontSize: 15, fontWeight: 700, cursor: "pointer", width: "100%", boxShadow: "0 4px 14px rgba(249,115,22,0.3)", opacity: loading ? 0.7 : 1 }}>
          {loading ? "Kayıt yapılıyor..." : "Kayıt Ol"}
        </button>'''

content = content.replace(old_register_button, new_register_button)

# Update register validation to check KVKK
old_register_validation = '''    if (!form.name || !form.email || !form.password || !form.gender || !form.phone || !form.city) {
      setError("Lütfen zorunlu alanları doldurun."); return;
    }'''

new_register_validation = '''    if (!form.name || !form.email || !form.password || !form.gender || !form.phone || !form.city) {
      setError("Lütfen zorunlu alanları doldurun."); return;
    }
    if (!form.kvkk) {
      setError("KVKK Aydınlatma Metni\\'ni kabul etmeniz gerekiyor."); return;
    }'''

content = content.replace(old_register_validation, new_register_validation)

# Update register form state to include kvkk
old_register_state = 'const [form, setForm] = useState({ name: "", email: "", password: "", gender: "", phone: "", city: "", bio: "" });'
new_register_state = 'const [form, setForm] = useState<any>({ name: "", email: "", password: "", gender: "", phone: "", city: "", bio: "", kvkk: false });'
content = content.replace(old_register_state, new_register_state)

# Update the update function to handle boolean
old_update_fn = '  const update = (key: string, val: string) => { setForm((p: any) => ({ ...p, [key]: val })); setError(""); };'
if old_update_fn not in content:
    old_update_fn = '  const update = (key: string, val: string) => { setForm(p => ({ ...p, [key]: val })); setError(""); };'

new_update_fn = '  const update = (key: string, val: any) => { setForm((p: any) => ({ ...p, [key]: val })); setError(""); };'
content = content.replace(old_update_fn, new_update_fn)

# ============================================================
# UPDATE 8: Add "cancelled" status label/color to ClientHome upcoming
# ============================================================
# Already exists in statusLabels, just make sure cancelled shows properly

# ============================================================
# SAVE
# ============================================================
open(filepath, 'w').write(content)
print("✅ TÜM GÜNCELLEMELER TAMAMLANDI!")
print("  1. Seans iptal (danışan)")
print("  2. Seans silme (admin)")
print("  3. Danışan listesi modal (dashboard'da tıklanabilir)")
print("  4. Şifremi unuttum (giriş ekranı)")
print("  5. KVKK onay checkbox (kayıt ekranı)")
