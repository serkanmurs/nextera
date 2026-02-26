import sys

filepath = 'src/app/page.tsx'
content = open(filepath, 'r').read()

print("🔄 V3 Güncellemeler başlıyor...")

# ============================================================
# 1. PAGE PERSISTENCE (Pull-to-refresh fix)
# Save current page in URL hash so refresh stays on same page
# ============================================================

# Update page state to read from hash
old_page_state = '  const [page, setPage] = useState("home");'
new_page_state = '''  const [page, setPageState] = useState(() => {
    if (typeof window !== "undefined") {
      const hash = window.location.hash.replace("#", "");
      return ["home", "sessions", "messages", "profile"].includes(hash) ? hash : "home";
    }
    return "home";
  });
  const setPage = (p: string) => {
    setPageState(p);
    if (typeof window !== "undefined") window.location.hash = p;
  };'''

content = content.replace(old_page_state, new_page_state)
print("  ✅ 1. Pull-to-refresh fix (sayfa hatırlanıyor)")

# ============================================================
# 2. REAL FILE UPLOAD IN MESSAGES
# Replace mock attachment with real Supabase Storage upload
# ============================================================

old_file_attach = '''  const handleFileAttach = () => {
    if (!activeChat) return;
    const types = ["📄 Rapor.pdf", "📸 Fotoğraf.jpg", "📋 Döküman.docx"];
    onSend(activeChat, types[Math.floor(Math.random() * types.length)], "file");
  };'''

new_file_attach = '''  const handleFileAttach = () => {
    if (!activeChat) return;
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "image/png,image/jpeg,image/jpg,application/pdf";
    input.onchange = async (e: any) => {
      const file = e.target.files?.[0];
      if (!file) return;
      if (file.size > 10 * 1024 * 1024) {
        alert("Dosya boyutu en fazla 10MB olabilir.");
        return;
      }
      try {
        const fileName = `${Date.now()}_${file.name}`;
        const { data, error } = await supabase.storage.from("uploads").upload(`messages/${fileName}`, file);
        if (error) throw error;
        const { data: urlData } = supabase.storage.from("uploads").getPublicUrl(`messages/${fileName}`);
        const fileUrl = urlData.publicUrl;
        const isImage = file.type.startsWith("image/");
        onSend(activeChat, fileUrl, isImage ? "image" : "file");
      } catch (err: any) {
        alert("Dosya yüklenemedi: " + err.message);
      }
    };
    input.click();
  };'''

content = content.replace(old_file_attach, new_file_attach)

# Update message display to show images and file links
old_msg_display = '''{m.msg_type === "file" ? <div style={{ display: "flex", alignItems: "center", gap: 6 }}><Icons.Attach /><span style={{ fontWeight: 600 }}>{m.text}</span></div> : m.text}'''

new_msg_display = '''{m.msg_type === "image" ? (
                  <a href={m.text} target="_blank" rel="noopener noreferrer"><img src={m.text} alt="Fotoğraf" style={{ maxWidth: "100%", maxHeight: 200, borderRadius: 8, display: "block" }} /></a>
                ) : m.msg_type === "file" ? (
                  <a href={m.text} target="_blank" rel="noopener noreferrer" style={{ display: "flex", alignItems: "center", gap: 6, color: isMine ? "#fff" : "#0891B2", textDecoration: "none" }}><Icons.Attach /><span style={{ fontWeight: 600 }}>📄 Dosya Görüntüle</span></a>
                ) : m.text}'''

content = content.replace(old_msg_display, new_msg_display)
print("  ✅ 2. Gerçek dosya/fotoğraf yükleme (mesajlaşma)")

# ============================================================
# 3. PROFILE PHOTO UPLOAD
# ============================================================

# Add profile photo upload to ProfilePage
old_profile_avatar = '''        <div style={{ width: 80, height: 80, borderRadius: "50%", background: "linear-gradient(135deg, #0891B2, #F97316)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 800, fontSize: 28, margin: "0 auto 14px" }}>{getInitials(user.name)}</div>'''

new_profile_avatar = '''        <div style={{ position: "relative", display: "inline-block" }}>
          {user.avatar && user.avatar.startsWith("http") ? (
            <img src={user.avatar} alt={user.name} style={{ width: 80, height: 80, borderRadius: "50%", objectFit: "cover", margin: "0 auto 14px", display: "block" }} />
          ) : (
            <div style={{ width: 80, height: 80, borderRadius: "50%", background: "linear-gradient(135deg, #0891B2, #F97316)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 800, fontSize: 28, margin: "0 auto 14px" }}>{getInitials(user.name)}</div>
          )}
          {editing && (
            <button onClick={async () => {
              const input = document.createElement("input");
              input.type = "file";
              input.accept = "image/png,image/jpeg,image/jpg";
              input.onchange = async (e: any) => {
                const file = e.target.files?.[0];
                if (!file) return;
                if (file.size > 5 * 1024 * 1024) { alert("Fotoğraf en fazla 5MB olabilir."); return; }
                try {
                  const fileName = `avatar_${user.id}_${Date.now()}`;
                  const { error: upErr } = await supabase.storage.from("uploads").upload(`avatars/${fileName}`, file, { upsert: true });
                  if (upErr) throw upErr;
                  const { data: urlData } = supabase.storage.from("uploads").getPublicUrl(`avatars/${fileName}`);
                  const avatarUrl = urlData.publicUrl;
                  setForm((p: any) => ({ ...p, avatar: avatarUrl }));
                } catch (err: any) {
                  alert("Fotoğraf yüklenemedi: " + err.message);
                }
              };
              input.click();
            }} style={{ position: "absolute", bottom: 14, right: -4, width: 28, height: 28, borderRadius: "50%", background: "#0891B2", color: "#fff", border: "2px solid #fff", display: "flex", alignItems: "center", justifyContent: "center", cursor: "pointer", fontSize: 14, padding: 0 }}>📷</button>
          )}
        </div>'''

content = content.replace(old_profile_avatar, new_profile_avatar)

# Update handleUpdateProfile to include avatar
old_update_profile = '''  const handleUpdateProfile = async (updatedUser: UserType) => {
    const { error } = await supabase.from("users").update({
      name: updatedUser.name, phone: updatedUser.phone, gender: updatedUser.gender,
      city: updatedUser.city, bio: updatedUser.bio,
    }).eq("id", updatedUser.id);'''

new_update_profile = '''  const handleUpdateProfile = async (updatedUser: UserType) => {
    const { error } = await supabase.from("users").update({
      name: updatedUser.name, phone: updatedUser.phone, gender: updatedUser.gender,
      city: updatedUser.city, bio: updatedUser.bio, avatar: updatedUser.avatar,
    }).eq("id", updatedUser.id);'''

content = content.replace(old_update_profile, new_update_profile)

# Update avatar displays throughout the app to use photo if available
# Header avatar
old_header_avatar = '''<div style={{ width: 34, height: 34, borderRadius: "50%", background: "linear-gradient(135deg, #0891B2, #F97316)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 800, fontSize: 12, border: "2px solid rgba(255,255,255,0.4)" }}>{currentUser ? getInitials(currentUser.name) : "?"}</div>'''

new_header_avatar = '''{currentUser?.avatar?.startsWith("http") ? (
              <img src={currentUser.avatar} alt="" style={{ width: 34, height: 34, borderRadius: "50%", objectFit: "cover", border: "2px solid rgba(255,255,255,0.4)" }} />
            ) : (
              <div style={{ width: 34, height: 34, borderRadius: "50%", background: "linear-gradient(135deg, #0891B2, #F97316)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 800, fontSize: 12, border: "2px solid rgba(255,255,255,0.4)" }}>{currentUser ? getInitials(currentUser.name) : "?"}</div>
            )}'''

content = content.replace(old_header_avatar, new_header_avatar)

print("  ✅ 3. Profil fotoğrafı yükleme/değiştirme")

# ============================================================
# 4. COACH PROFILE CARD - LinkedIn + Email
# ============================================================

old_coach_card = '''      {admin && (
        <div style={{ ...cardStyle, background: "linear-gradient(135deg, #0891B2 0%, #0EA5E9 100%)", color: "#fff", border: "none" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
            <div style={{ width: 56, height: 56, borderRadius: "50%", background: "rgba(255,255,255,0.2)", border: "3px solid rgba(255,255,255,0.4)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 800, fontSize: 20 }}>{getInitials(admin.name)}</div>
            <div><div style={{ fontWeight: 800, fontSize: 17 }}>{admin.name}</div><div style={{ fontSize: 13, opacity: 0.85 }}>{admin.bio}</div><div style={{ fontSize: 12, opacity: 0.7, marginTop: 2 }}>{admin.city}</div></div>
          </div>
        </div>
      )}'''

new_coach_card = '''      {admin && (
        <div style={{ ...cardStyle, background: "linear-gradient(135deg, #0891B2 0%, #0EA5E9 100%)", color: "#fff", border: "none" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
            {admin.avatar?.startsWith("http") ? (
              <img src={admin.avatar} alt={admin.name} style={{ width: 56, height: 56, borderRadius: "50%", objectFit: "cover", border: "3px solid rgba(255,255,255,0.4)", flexShrink: 0 }} />
            ) : (
              <div style={{ width: 56, height: 56, borderRadius: "50%", background: "rgba(255,255,255,0.2)", border: "3px solid rgba(255,255,255,0.4)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 800, fontSize: 20, flexShrink: 0 }}>{getInitials(admin.name)}</div>
            )}
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: 800, fontSize: 17 }}>{admin.name}</div>
              <div style={{ fontSize: 13, opacity: 0.85 }}>{admin.bio}</div>
              <div style={{ fontSize: 12, opacity: 0.7, marginTop: 2 }}>{admin.city}</div>
              <div style={{ display: "flex", gap: 10, marginTop: 8 }}>
                <a href="https://www.linkedin.com/services/page/2800ba317abbbbb440/" target="_blank" rel="noopener noreferrer" style={{ width: 32, height: 32, borderRadius: 8, background: "rgba(255,255,255,0.2)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", textDecoration: "none", fontSize: 16 }}>💼</a>
                <a href="mailto:serkanmursalli@gmail.com" style={{ width: 32, height: 32, borderRadius: 8, background: "rgba(255,255,255,0.2)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", textDecoration: "none", fontSize: 16 }}>✉️</a>
              </div>
            </div>
          </div>
        </div>
      )}'''

content = content.replace(old_coach_card, new_coach_card)
print("  ✅ 4. Koç profil kartı - LinkedIn + Email butonları")

# ============================================================
# 5. Supabase import for storage (already imported at top)
# Just verify it's there
# ============================================================
if 'from "@/lib/supabase"' in content:
    print("  ✅ 5. Supabase import zaten mevcut")
else:
    print("  ⚠️ 5. Supabase import eksik!")

# ============================================================
# SAVE
# ============================================================
open(filepath, 'w').write(content)

print("")
print("🎉 V3 TÜM GÜNCELLEMELER TAMAMLANDI!")
print("  1. Pull-to-refresh fix (sayfa hatırlanıyor)")
print("  2. Gerçek dosya/fotoğraf yükleme (mesajlaşma)")
print("  3. Profil fotoğrafı yükleme/değiştirme")
print("  4. Koç profil kartı - LinkedIn + Email")
print("")
print("Şimdi: npm run build")
