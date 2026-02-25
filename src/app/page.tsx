"use client";
import { useState, useEffect, useRef, useCallback } from "react";
import { supabase } from "@/lib/supabase";

// ==================== CONSTANTS ====================
const COLORS = {
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
};

const CITIES = [
  "İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Adana", "Konya",
  "Gaziantep", "Mersin", "Diyarbakır", "Kayseri", "Eskişehir", "Samsun",
  "Denizli", "Trabzon", "Malatya", "Erzurum", "Van", "Batman", "Muğla",
];

const ADMIN_EMAIL = "serkanmursalli@gmail.com";

const TIME_SLOTS = [
  "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"
];

// ==================== ICONS ====================
const Icons = {
  Home: () => <svg width="22" height="22" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9,22 9,12 15,12 15,22"/></svg>,
  Calendar: () => <svg width="22" height="22" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>,
  Chat: () => <svg width="22" height="22" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>,
  User: () => <svg width="22" height="22" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>,
  Bell: () => <svg width="22" height="22" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24"><path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 01-3.46 0"/></svg>,
  Send: () => <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22,2 15,22 11,13 2,9"/></svg>,
  Star: ({ filled }: { filled: boolean }) => <svg width="18" height="18" fill={filled ? "#F59E0B" : "none"} stroke="#F59E0B" strokeWidth="2" viewBox="0 0 24 24"><polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/></svg>,
  LogOut: () => <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16,17 21,12 16,7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>,
  Attach: () => <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24"><path d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l9.19-9.19a4 4 0 015.66 5.66l-9.2 9.19a2 2 0 01-2.83-2.83l8.49-8.49"/></svg>,
  Check: () => <svg width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24"><polyline points="20,6 9,17 4,12"/></svg>,
  X: () => <svg width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>,
  Users: () => <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/></svg>,
  Clock: () => <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12,6 12,12 16,14"/></svg>,
  Award: () => <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24"><circle cx="12" cy="8" r="7"/><polyline points="8.21,13.89 7,23 12,20 17,23 15.79,13.88"/></svg>,
  ChevronLeft: () => <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24"><polyline points="15,18 9,12 15,6"/></svg>,
  Edit: () => <svg width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>,
  Mail: () => <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>,
  Dashboard: () => <svg width="22" height="22" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>,
};

// ==================== TYPES ====================
interface UserType {
  id: string;
  name: string;
  email: string;
  gender: string;
  phone: string;
  city: string;
  bio: string;
  role: "admin" | "client";
  avatar: string;
}

interface SessionType {
  id: string;
  client_id: string;
  date: string;
  time: string;
  duration: number;
  status: "completed" | "upcoming" | "cancelled";
  rating: number | null;
  review: string | null;
}

interface MessageType {
  id: string;
  sender_id: string;
  receiver_id: string;
  text: string;
  msg_type: string;
  created_at: string;
}

interface NotificationType {
  id: string;
  user_id: string;
  text: string;
  type: string;
  is_read: boolean;
  created_at: string;
}

// ==================== HELPER ====================
function getInitials(name: string) {
  return name.split(" ").map(w => w[0]).join("").toUpperCase().slice(0, 2);
}

function formatDate(dateStr: string) {
  const d = new Date(dateStr);
  const months = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"];
  return `${d.getDate()} ${months[d.getMonth()]} ${d.getFullYear()}`;
}

// ==================== TOAST ====================
function Toast({ message, type = "info", onClose }: { message: string; type?: string; onClose: () => void }) {
  const bgColors: Record<string, string> = { info: COLORS.primary, success: COLORS.success, error: COLORS.danger, warning: COLORS.warning };
  useEffect(() => { const t = setTimeout(onClose, 3000); return () => clearTimeout(t); }, [onClose]);
  return (
    <div style={{ position: "fixed", top: 20, left: "50%", transform: "translateX(-50%)", background: bgColors[type] || COLORS.primary, color: "#fff", padding: "12px 24px", borderRadius: 12, fontSize: 14, fontWeight: 600, zIndex: 1000, boxShadow: "0 8px 30px rgba(0,0,0,0.15)", animation: "slideDown 0.3s ease", maxWidth: "90%", textAlign: "center" }}>
      {message}
    </div>
  );
}

// ==================== STAR RATING ====================
function StarRating({ rating, onRate, readonly = false }: { rating: number; onRate?: (r: number) => void; readonly?: boolean }) {
  return (
    <div style={{ display: "flex", gap: 4 }}>
      {[1, 2, 3, 4, 5].map(i => (
        <span key={i} onClick={() => !readonly && onRate?.(i)} style={{ cursor: readonly ? "default" : "pointer" }}>
          <Icons.Star filled={i <= rating} />
        </span>
      ))}
    </div>
  );
}

// ==================== LOGIN SCREEN ====================
function LoginScreen({ onLogin, onGoRegister }: { onLogin: (email: string, password: string) => void; onGoRegister: () => void }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    if (!email || !password) { setError("Lütfen tüm alanları doldurun."); return; }
    setLoading(true);
    setError("");
    onLogin(email.trim().toLowerCase(), password);
    setLoading(false);
  };

  return (
    <div style={{ minHeight: "100vh", background: "linear-gradient(180deg, #0891B2 0%, #0EA5E9 40%, #F8FAFC 100%)", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: 24 }}>
      <div style={{ marginBottom: 40, textAlign: "center" }}>
        <div style={{ fontSize: 42, fontWeight: 900, color: "#fff", letterSpacing: "-1px" }}>Next<span style={{ color: "#FCD34D" }}>ERA</span></div>
        <div style={{ color: "rgba(255,255,255,0.85)", fontSize: 15, marginTop: 6, fontWeight: 500 }}>Danışmanlık Platformu</div>
      </div>
      <div style={{ background: "#fff", borderRadius: 24, padding: 32, width: "100%", maxWidth: 380, boxShadow: "0 20px 60px rgba(0,0,0,0.12)" }}>
        <h2 style={{ margin: "0 0 24px", fontSize: 22, fontWeight: 800, textAlign: "center" }}>Giriş Yap</h2>
        {error && <div style={{ background: "#FEF2F2", color: COLORS.danger, padding: "10px 14px", borderRadius: 10, fontSize: 13, marginBottom: 16, fontWeight: 600 }}>{error}</div>}
        <div style={{ marginBottom: 16 }}>
          <label style={{ fontSize: 13, fontWeight: 600, color: COLORS.textLight, marginBottom: 6, display: "block" }}>E-posta</label>
          <input style={{ width: "100%", padding: "12px 16px", borderRadius: 12, border: `1.5px solid ${COLORS.border}`, fontSize: 15, outline: "none", boxSizing: "border-box" }} type="email" value={email} onChange={e => { setEmail(e.target.value); setError(""); }} placeholder="ornek@email.com" />
        </div>
        <div style={{ marginBottom: 24 }}>
          <label style={{ fontSize: 13, fontWeight: 600, color: COLORS.textLight, marginBottom: 6, display: "block" }}>Şifre</label>
          <input style={{ width: "100%", padding: "12px 16px", borderRadius: 12, border: `1.5px solid ${COLORS.border}`, fontSize: 15, outline: "none", boxSizing: "border-box" }} type="password" value={password} onChange={e => { setPassword(e.target.value); setError(""); }} placeholder="••••••••" onKeyDown={e => e.key === "Enter" && handleLogin()} />
        </div>
        <button onClick={handleLogin} disabled={loading} style={{ background: "linear-gradient(135deg, #0891B2, #0EA5E9)", color: "#fff", border: "none", borderRadius: 12, padding: "12px 24px", fontSize: 15, fontWeight: 700, cursor: "pointer", width: "100%", boxShadow: "0 4px 14px rgba(8,145,178,0.3)", opacity: loading ? 0.7 : 1 }}>
          {loading ? "Giriş yapılıyor..." : "Giriş Yap"}
        </button>
        <div style={{ textAlign: "center", marginTop: 20 }}>
          <span style={{ color: COLORS.textLight, fontSize: 14 }}>Hesabınız yok mu? </span>
          <span style={{ color: COLORS.primary, fontWeight: 700, cursor: "pointer", fontSize: 14 }} onClick={onGoRegister}>Kayıt Ol</span>
        </div>
      </div>
    </div>
  );
}

// ==================== REGISTER SCREEN ====================
function RegisterScreen({ onRegister, onGoLogin }: { onRegister: (form: any) => void; onGoLogin: () => void }) {
  const [form, setForm] = useState({ name: "", email: "", password: "", gender: "", phone: "", city: "", bio: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleRegister = () => {
    if (!form.name || !form.email || !form.password || !form.gender || !form.phone || !form.city) {
      setError("Lütfen zorunlu alanları doldurun."); return;
    }
    setLoading(true);
    onRegister(form);
  };

  const update = (key: string, val: string) => { setForm(p => ({ ...p, [key]: val })); setError(""); };

  const inputStyle = { width: "100%", padding: "12px 16px", borderRadius: 12, border: `1.5px solid ${COLORS.border}`, fontSize: 15, outline: "none", boxSizing: "border-box" as const };
  const labelStyle = { fontSize: 13, fontWeight: 600, color: COLORS.textLight, marginBottom: 6, display: "block" as const };

  return (
    <div style={{ minHeight: "100vh", background: "linear-gradient(180deg, #F97316 0%, #FB923C 30%, #F8FAFC 100%)", display: "flex", flexDirection: "column", alignItems: "center", padding: "40px 24px" }}>
      <div style={{ marginBottom: 30, textAlign: "center" }}>
        <div style={{ fontSize: 36, fontWeight: 900, color: "#fff" }}>Next<span style={{ color: "#FCD34D" }}>ERA</span></div>
        <div style={{ color: "rgba(255,255,255,0.85)", fontSize: 14, marginTop: 4 }}>Hesap Oluştur</div>
      </div>
      <div style={{ background: "#fff", borderRadius: 24, padding: 28, width: "100%", maxWidth: 380, boxShadow: "0 20px 60px rgba(0,0,0,0.12)" }}>
        {error && <div style={{ background: "#FEF2F2", color: COLORS.danger, padding: "10px 14px", borderRadius: 10, fontSize: 13, marginBottom: 16, fontWeight: 600 }}>{error}</div>}
        
        {[
          { key: "name", label: "Ad Soyad *", placeholder: "Adınız Soyadınız", type: "text" },
          { key: "email", label: "E-posta *", placeholder: "ornek@email.com", type: "email" },
          { key: "password", label: "Şifre *", placeholder: "En az 6 karakter", type: "password" },
          { key: "phone", label: "Telefon *", placeholder: "0532 000 0000", type: "tel" },
        ].map(f => (
          <div key={f.key} style={{ marginBottom: 14 }}>
            <label style={labelStyle}>{f.label}</label>
            <input style={inputStyle} type={f.type} value={(form as any)[f.key]} onChange={e => update(f.key, e.target.value)} placeholder={f.placeholder} />
          </div>
        ))}
        
        <div style={{ marginBottom: 14 }}>
          <label style={labelStyle}>Cinsiyet *</label>
          <div style={{ display: "flex", gap: 8 }}>
            {["Kadın", "Erkek", "Diğer"].map(g => (
              <button key={g} onClick={() => update("gender", g)} style={{ flex: 1, padding: "10px", borderRadius: 10, border: `2px solid ${form.gender === g ? COLORS.primary : COLORS.border}`, background: form.gender === g ? `${COLORS.primary}10` : "#fff", color: form.gender === g ? COLORS.primary : COLORS.textLight, fontWeight: 600, fontSize: 13, cursor: "pointer" }}>
                {g}
              </button>
            ))}
          </div>
        </div>
        
        <div style={{ marginBottom: 14 }}>
          <label style={labelStyle}>Şehir *</label>
          <select style={{ ...inputStyle, appearance: "auto" as const }} value={form.city} onChange={e => update("city", e.target.value)}>
            <option value="">Şehir Seçin</option>
            {CITIES.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>
        
        <div style={{ marginBottom: 20 }}>
          <label style={labelStyle}>Biyografi</label>
          <textarea style={{ ...inputStyle, minHeight: 80, resize: "vertical" }} value={form.bio} onChange={e => update("bio", e.target.value)} placeholder="Kendinizden kısaca bahsedin..." />
        </div>
        
        <button onClick={handleRegister} disabled={loading} style={{ background: "linear-gradient(135deg, #F97316, #FB923C)", color: "#fff", border: "none", borderRadius: 12, padding: "12px 24px", fontSize: 15, fontWeight: 700, cursor: "pointer", width: "100%", boxShadow: "0 4px 14px rgba(249,115,22,0.3)", opacity: loading ? 0.7 : 1 }}>
          {loading ? "Kayıt yapılıyor..." : "Kayıt Ol"}
        </button>
        
        <div style={{ textAlign: "center", marginTop: 16 }}>
          <span style={{ color: COLORS.textLight, fontSize: 14 }}>Zaten hesabınız var mı? </span>
          <span style={{ color: COLORS.secondary, fontWeight: 700, cursor: "pointer", fontSize: 14 }} onClick={onGoLogin}>Giriş Yap</span>
        </div>
      </div>
    </div>
  );
}

// ==================== ADMIN DASHBOARD ====================
function AdminDashboard({ users, sessions }: { users: UserType[]; sessions: SessionType[] }) {
  const clients = users.filter(u => u.role === "client");
  const completed = sessions.filter(s => s.status === "completed");
  const upcoming = sessions.filter(s => s.status === "upcoming");
  const totalHours = Math.round(completed.length * 50 / 60 * 10) / 10;
  const ratedSessions = completed.filter(s => s.rating);
  const avgRating = ratedSessions.length > 0 ? ratedSessions.reduce((a, s) => a + (s.rating || 0), 0) / ratedSessions.length : 0;

  const cardStyle = { background: "#fff", borderRadius: 16, padding: 20, marginBottom: 12, boxShadow: "0 1px 3px rgba(0,0,0,0.06)", border: `1px solid ${COLORS.border}` };

  return (
    <div style={{ padding: 16 }}>
      <div style={{ marginBottom: 20 }}>
        <h2 style={{ margin: 0, fontSize: 20, fontWeight: 800 }}>Dashboard</h2>
        <p style={{ margin: "4px 0 0", fontSize: 13, color: COLORS.textLight }}>Hoş geldin, Serkan 👋</p>
      </div>
      
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginBottom: 16 }}>
        {[
          { icon: <Icons.Users />, label: "Toplam Danışan", value: clients.length, color: COLORS.primary },
          { icon: <Icons.Clock />, label: "Toplam Saat", value: totalHours, color: COLORS.secondary },
          { icon: <Icons.Check />, label: "Tamamlanan", value: completed.length, color: COLORS.success },
          { icon: <Icons.Award />, label: "Ort. Puan", value: avgRating.toFixed(1), color: COLORS.warning },
        ].map((s, i) => (
          <div key={i} style={{ ...cardStyle, padding: 16, display: "flex", alignItems: "center", gap: 14 }}>
            <div style={{ width: 50, height: 50, borderRadius: 14, background: `${s.color}12`, display: "flex", alignItems: "center", justifyContent: "center", color: s.color }}>{s.icon}</div>
            <div><div style={{ fontSize: 24, fontWeight: 800, color: s.color }}>{s.value}</div><div style={{ fontSize: 13, color: COLORS.textLight }}>{s.label}</div></div>
          </div>
        ))}
      </div>
      
      <div style={cardStyle}>
        <h3 style={{ margin: "0 0 14px", fontSize: 16, fontWeight: 700 }}>📅 Yaklaşan Seanslar</h3>
        {upcoming.length === 0 ? <p style={{ color: COLORS.textLight, fontSize: 14, textAlign: "center", padding: 20 }}>Yaklaşan seans yok</p> : upcoming.slice(0, 5).map(s => {
          const client = users.find(u => u.id === s.client_id);
          return (
            <div key={s.id} style={{ display: "flex", alignItems: "center", gap: 12, padding: "10px 0", borderBottom: `1px solid ${COLORS.border}` }}>
              <div style={{ width: 36, height: 36, borderRadius: "50%", background: "linear-gradient(135deg, #0891B2, #F97316)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 800, fontSize: 13 }}>{client ? getInitials(client.name) : "?"}</div>
              <div style={{ flex: 1 }}><div style={{ fontWeight: 700, fontSize: 14 }}>{client?.name || "Danışan"}</div><div style={{ fontSize: 12, color: COLORS.textLight }}>{formatDate(s.date)} · {s.time}</div></div>
              <span style={{ background: `${COLORS.accent}15`, color: COLORS.accent, borderRadius: 20, padding: "4px 12px", fontSize: 12, fontWeight: 700 }}>Yaklaşan</span>
            </div>
          );
        })}
      </div>
      
      <div style={cardStyle}>
        <h3 style={{ margin: "0 0 14px", fontSize: 16, fontWeight: 700 }}>👥 Danışanlar</h3>
        {clients.map(c => {
          const clientSessions = sessions.filter(s => s.client_id === c.id);
          const completedCount = clientSessions.filter(s => s.status === "completed").length;
          return (
            <div key={c.id} style={{ display: "flex", alignItems: "center", gap: 12, padding: "10px 0", borderBottom: `1px solid ${COLORS.border}` }}>
              <div style={{ width: 40, height: 40, borderRadius: "50%", background: "linear-gradient(135deg, #0891B2, #F97316)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 800, fontSize: 14 }}>{getInitials(c.name)}</div>
              <div style={{ flex: 1 }}><div style={{ fontWeight: 700, fontSize: 14 }}>{c.name}</div><div style={{ fontSize: 12, color: COLORS.textLight }}>{c.city} · {c.phone}</div></div>
              <div style={{ textAlign: "right" }}><div style={{ fontSize: 16, fontWeight: 800, color: COLORS.primary }}>{completedCount}</div><div style={{ fontSize: 11, color: COLORS.textLight }}>seans</div></div>
            </div>
          );
        })}
      </div>

      <div style={cardStyle}>
        <h3 style={{ margin: "0 0 14px", fontSize: 16, fontWeight: 700 }}>⭐ Son Değerlendirmeler</h3>
        {sessions.filter(s => s.review).length === 0 ? <p style={{ color: COLORS.textLight, fontSize: 14, textAlign: "center", padding: 20 }}>Henüz değerlendirme yok</p> : sessions.filter(s => s.review).slice(0, 5).map(s => {
          const client = users.find(u => u.id === s.client_id);
          return (
            <div key={s.id} style={{ padding: "12px 0", borderBottom: `1px solid ${COLORS.border}` }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6 }}>
                <div style={{ width: 28, height: 28, borderRadius: "50%", background: "linear-gradient(135deg, #0891B2, #F97316)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 800, fontSize: 10 }}>{client ? getInitials(client.name) : "?"}</div>
                <span style={{ fontWeight: 700, fontSize: 13 }}>{client?.name}</span>
                <StarRating rating={s.rating || 0} readonly />
              </div>
              <p style={{ margin: 0, fontSize: 13, color: COLORS.textLight, fontStyle: "italic" }}>&ldquo;{s.review}&rdquo;</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ==================== CLIENT HOME ====================
function ClientHome({ user, sessions, users }: { user: UserType; sessions: SessionType[]; users: UserType[] }) {
  const mySessions = sessions.filter(s => s.client_id === user.id);
  const completed = mySessions.filter(s => s.status === "completed");
  const upcoming = mySessions.filter(s => s.status === "upcoming");
  const admin = users.find(u => u.role === "admin");
  const cardStyle = { background: "#fff", borderRadius: 16, padding: 20, marginBottom: 12, boxShadow: "0 1px 3px rgba(0,0,0,0.06)", border: `1px solid ${COLORS.border}` };

  return (
    <div style={{ padding: 16 }}>
      <div style={{ marginBottom: 20 }}>
        <h2 style={{ margin: 0, fontSize: 20, fontWeight: 800 }}>Merhaba, {user.name.split(" ")[0]} 👋</h2>
        <p style={{ margin: "4px 0 0", fontSize: 13, color: COLORS.textLight }}>Seans özetiniz aşağıda</p>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10, marginBottom: 16 }}>
        {[
          { value: mySessions.length, label: "Toplam", color: COLORS.primary },
          { value: completed.length, label: "Tamamlanan", color: COLORS.success },
          { value: upcoming.length, label: "Yaklaşan", color: COLORS.accent },
        ].map((s, i) => (
          <div key={i} style={{ ...cardStyle, padding: 14, textAlign: "center" }}>
            <div style={{ fontSize: 28, fontWeight: 800, color: s.color }}>{s.value}</div>
            <div style={{ fontSize: 11, color: COLORS.textLight }}>{s.label}</div>
          </div>
        ))}
      </div>

      {admin && (
        <div style={{ ...cardStyle, background: "linear-gradient(135deg, #0891B2 0%, #0EA5E9 100%)", color: "#fff", border: "none" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
            <div style={{ width: 56, height: 56, borderRadius: "50%", background: "rgba(255,255,255,0.2)", border: "3px solid rgba(255,255,255,0.4)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 800, fontSize: 20 }}>{getInitials(admin.name)}</div>
            <div><div style={{ fontWeight: 800, fontSize: 17 }}>{admin.name}</div><div style={{ fontSize: 13, opacity: 0.85 }}>{admin.bio}</div><div style={{ fontSize: 12, opacity: 0.7, marginTop: 2 }}>{admin.city}</div></div>
          </div>
        </div>
      )}

      <div style={cardStyle}>
        <h3 style={{ margin: "0 0 14px", fontSize: 16, fontWeight: 700 }}>🗓 Yaklaşan Seanslarım</h3>
        {upcoming.length === 0 ? <p style={{ fontSize: 14, color: COLORS.textLight, textAlign: "center", padding: 20 }}>Yaklaşan seansınız yok.</p> : upcoming.map(s => (
          <div key={s.id} style={{ display: "flex", alignItems: "center", gap: 12, padding: "10px 0", borderBottom: `1px solid ${COLORS.border}` }}>
            <div style={{ width: 44, height: 44, borderRadius: 12, background: `${COLORS.accent}12`, display: "flex", alignItems: "center", justifyContent: "center", color: COLORS.accent, fontSize: 18, fontWeight: 800 }}>{new Date(s.date).getDate()}</div>
            <div style={{ flex: 1 }}><div style={{ fontWeight: 700, fontSize: 14 }}>Online Seans</div><div style={{ fontSize: 12, color: COLORS.textLight }}>{formatDate(s.date)} · {s.time} · {s.duration} dk</div></div>
            <span style={{ background: `${COLORS.accent}15`, color: COLORS.accent, borderRadius: 20, padding: "4px 12px", fontSize: 12, fontWeight: 700 }}>Yaklaşan</span>
          </div>
        ))}
      </div>

      <div style={cardStyle}>
        <h3 style={{ margin: "0 0 14px", fontSize: 16, fontWeight: 700 }}>✅ Tamamlanan Seanslarım</h3>
        {completed.length === 0 ? <p style={{ fontSize: 14, color: COLORS.textLight, textAlign: "center", padding: 20 }}>Tamamlanan seansınız yok.</p> : completed.map(s => (
          <div key={s.id} style={{ padding: "12px 0", borderBottom: `1px solid ${COLORS.border}` }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <div><div style={{ fontWeight: 700, fontSize: 14 }}>Online Seans</div><div style={{ fontSize: 12, color: COLORS.textLight }}>{formatDate(s.date)} · {s.time}</div></div>
              <span style={{ background: `${COLORS.success}15`, color: COLORS.success, borderRadius: 20, padding: "4px 12px", fontSize: 12, fontWeight: 700 }}>Tamamlandı</span>
            </div>
            {s.rating ? (
              <div style={{ marginTop: 8 }}>
                <StarRating rating={s.rating} readonly />
                {s.review && <p style={{ margin: "4px 0 0", fontSize: 12, color: COLORS.textLight, fontStyle: "italic" }}>&ldquo;{s.review}&rdquo;</p>}
              </div>
            ) : <div style={{ marginTop: 6, fontSize: 12, color: COLORS.secondary, fontWeight: 600 }}>⭐ Değerlendir</div>}
          </div>
        ))}
      </div>
    </div>
  );
}

// ==================== SESSIONS PAGE ====================
function SessionsPage({ user, sessions, users, onBook, isAdmin }: { user: UserType; sessions: SessionType[]; users: UserType[]; onBook: (d: string, t: string) => void; isAdmin: boolean }) {
  const [selectedDate, setSelectedDate] = useState(() => { const d = new Date(); d.setDate(d.getDate() + 1); return d.toISOString().split("T")[0]; });
  const [selectedTime, setSelectedTime] = useState("");
  const [showBooking, setShowBooking] = useState(false);

  const mySessions = isAdmin ? sessions : sessions.filter(s => s.client_id === user.id);
  const bookedTimes = sessions.filter(s => s.date === selectedDate).map(s => s.time);
  const cardStyle = { background: "#fff", borderRadius: 16, padding: 20, marginBottom: 12, boxShadow: "0 1px 3px rgba(0,0,0,0.06)", border: `1px solid ${COLORS.border}` };

  const handleBook = () => {
    if (!selectedTime) return;
    onBook(selectedDate, selectedTime);
    setSelectedTime("");
    setShowBooking(false);
  };

  const getDays = () => {
    const days = [];
    const today = new Date();
    const dayNames = ["Paz", "Pzt", "Sal", "Çar", "Per", "Cum", "Cmt"];
    for (let i = 0; i < 14; i++) {
      const d = new Date(today);
      d.setDate(today.getDate() + i);
      days.push({ date: d.toISOString().split("T")[0], day: d.getDate(), dayName: dayNames[d.getDay()], isWeekend: d.getDay() === 0 || d.getDay() === 6 });
    }
    return days;
  };

  return (
    <div style={{ padding: 16 }}>
      <h2 style={{ margin: "0 0 16px", fontSize: 20, fontWeight: 800 }}>📅 Seanslar</h2>
      <div style={{ ...cardStyle, padding: 14 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
          <h3 style={{ margin: 0, fontSize: 15, fontWeight: 700 }}>Tarih Seçin</h3>
          <div style={{ display: "flex", gap: 4 }}>
            <span style={{ padding: "4px 8px", background: `${COLORS.success}15`, color: COLORS.success, borderRadius: 6, fontSize: 11, fontWeight: 600 }}>● Müsait</span>
            <span style={{ padding: "4px 8px", background: `${COLORS.danger}15`, color: COLORS.danger, borderRadius: 6, fontSize: 11, fontWeight: 600 }}>● Dolu</span>
          </div>
        </div>
        <div style={{ display: "flex", gap: 6, overflowX: "auto", paddingBottom: 4 }}>
          {getDays().map(d => {
            const hasSession = sessions.some(s => s.date === d.date);
            const isSelected = d.date === selectedDate;
            return (
              <div key={d.date} onClick={() => { setSelectedDate(d.date); setShowBooking(true); }}
                style={{ minWidth: 52, padding: "8px 4px", borderRadius: 12, textAlign: "center", cursor: "pointer", background: isSelected ? COLORS.primary : d.isWeekend ? "#F1F5F9" : "#fff", color: isSelected ? "#fff" : COLORS.text, border: `2px solid ${isSelected ? COLORS.primary : "transparent"}`, transition: "all 0.2s" }}>
                <div style={{ fontSize: 11, fontWeight: 500, opacity: 0.7 }}>{d.dayName}</div>
                <div style={{ fontSize: 18, fontWeight: 800, margin: "2px 0" }}>{d.day}</div>
                {hasSession && <div style={{ width: 6, height: 6, borderRadius: "50%", background: isSelected ? "#fff" : COLORS.secondary, margin: "0 auto" }} />}
              </div>
            );
          })}
        </div>
      </div>

      {showBooking && !isAdmin && (
        <div style={cardStyle}>
          <h3 style={{ margin: "0 0 12px", fontSize: 15, fontWeight: 700 }}>🕐 Müsait Saatler - {formatDate(selectedDate)}</h3>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 8, marginBottom: 16 }}>
            {TIME_SLOTS.map(t => {
              const booked = bookedTimes.includes(t);
              const selected = selectedTime === t;
              return (
                <button key={t} disabled={booked} onClick={() => setSelectedTime(t)}
                  style={{ padding: "10px", borderRadius: 10, border: `2px solid ${selected ? COLORS.primary : COLORS.border}`, background: selected ? `${COLORS.primary}10` : booked ? "#F1F5F9" : "#fff", color: booked ? "#CBD5E1" : selected ? COLORS.primary : COLORS.text, fontWeight: 600, fontSize: 14, cursor: booked ? "not-allowed" : "pointer", textDecoration: booked ? "line-through" : "none" }}>
                  {t}
                </button>
              );
            })}
          </div>
          {selectedTime && (
            <button onClick={handleBook} style={{ background: "linear-gradient(135deg, #0891B2, #0EA5E9)", color: "#fff", border: "none", borderRadius: 12, padding: "12px 24px", fontSize: 15, fontWeight: 700, cursor: "pointer", width: "100%", boxShadow: "0 4px 14px rgba(8,145,178,0.3)" }}>
              {formatDate(selectedDate)} - {selectedTime} Randevu Al
            </button>
          )}
        </div>
      )}

      <div style={cardStyle}>
        <h3 style={{ margin: "0 0 14px", fontSize: 15, fontWeight: 700 }}>Seans Geçmişi</h3>
        {mySessions.length === 0 ? <p style={{ color: COLORS.textLight, fontSize: 14, textAlign: "center", padding: 20 }}>Henüz seans yok.</p> : [...mySessions].sort((a, b) => b.date.localeCompare(a.date)).map(s => {
          const client = users.find(u => u.id === s.client_id);
          const statusColors: Record<string, string> = { completed: COLORS.success, upcoming: COLORS.accent, cancelled: COLORS.danger };
          const statusLabels: Record<string, string> = { completed: "Tamamlandı", upcoming: "Yaklaşan", cancelled: "İptal" };
          return (
            <div key={s.id} style={{ display: "flex", alignItems: "center", gap: 12, padding: "10px 0", borderBottom: `1px solid ${COLORS.border}` }}>
              {isAdmin && <div style={{ width: 34, height: 34, borderRadius: "50%", background: "linear-gradient(135deg, #0891B2, #F97316)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 800, fontSize: 12 }}>{client ? getInitials(client.name) : "?"}</div>}
              <div style={{ flex: 1 }}>
                {isAdmin && <div style={{ fontWeight: 700, fontSize: 13 }}>{client?.name}</div>}
                <div style={{ fontSize: 13, fontWeight: isAdmin ? 400 : 600 }}>{formatDate(s.date)} · {s.time}</div>
                <div style={{ fontSize: 12, color: COLORS.textLight }}>{s.duration} dakika</div>
              </div>
              <span style={{ background: `${statusColors[s.status]}15`, color: statusColors[s.status], borderRadius: 20, padding: "4px 12px", fontSize: 12, fontWeight: 700 }}>{statusLabels[s.status]}</span>
            </div>
          );
        })}
      </div>

      <div style={{ ...cardStyle, background: "linear-gradient(135deg, #EFF6FF, #F0FDFA)", border: "2px dashed #93C5FD", textAlign: "center", padding: 24 }}>
        <Icons.Calendar />
        <h4 style={{ margin: "8px 0 4px", fontSize: 15, fontWeight: 700 }}>Google Takvim Entegrasyonu</h4>
        <p style={{ fontSize: 13, color: COLORS.textLight, margin: 0 }}>Seanslarınız otomatik olarak Google Takvim&apos;e eklenir.</p>
        <button onClick={() => window.location.href = "/api/auth/google"} style={{ background: "#fff", color: "#0891B2", border: "2px solid #0891B2", borderRadius: 12, padding: "8px 20px", fontSize: 13, fontWeight: 700, cursor: "pointer", marginTop: 12 }}>🔗 Google Takvim Bağla</button>
      </div>
    </div>
  );
}

// ==================== MESSAGES PAGE ====================
function MessagesPage({ user, messages, users, onSend, isAdmin }: { user: UserType; messages: MessageType[]; users: UserType[]; onSend: (receiverId: string, text: string, type: string) => void; isAdmin: boolean }) {
  const [activeChat, setActiveChat] = useState<string | null>(null);
  const [msgText, setMsgText] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const chatPartners = isAdmin ? users.filter(u => u.role === "client") : users.filter(u => u.role === "admin");

  const getConversation = (partnerId: string) => {
    return messages.filter(m =>
      (m.sender_id === user.id && m.receiver_id === partnerId) ||
      (m.sender_id === partnerId && m.receiver_id === user.id)
    ).sort((a, b) => a.created_at.localeCompare(b.created_at));
  };

  const getLastMessage = (partnerId: string) => {
    const conv = getConversation(partnerId);
    return conv[conv.length - 1];
  };

  const handleSend = () => {
    if (!msgText.trim() || !activeChat) return;
    onSend(activeChat, msgText.trim(), "text");
    setMsgText("");
  };

  const handleFileAttach = () => {
    if (!activeChat) return;
    const types = ["📄 Rapor.pdf", "📸 Fotoğraf.jpg", "📋 Döküman.docx"];
    onSend(activeChat, types[Math.floor(Math.random() * types.length)], "file");
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, activeChat]);

  const cardStyle = { background: "#fff", borderRadius: 16, padding: 14, marginBottom: 12, boxShadow: "0 1px 3px rgba(0,0,0,0.06)", border: `1px solid ${COLORS.border}` };

  if (!activeChat) {
    return (
      <div style={{ padding: 16 }}>
        <h2 style={{ margin: "0 0 16px", fontSize: 20, fontWeight: 800 }}>💬 Mesajlar</h2>
        {chatPartners.length === 0 ? <p style={{ color: COLORS.textLight, textAlign: "center", padding: 40 }}>Henüz mesaj yok</p> : chatPartners.map(partner => {
          const lastMsg = getLastMessage(partner.id);
          return (
            <div key={partner.id} onClick={() => setActiveChat(partner.id)}
              style={{ ...cardStyle, display: "flex", alignItems: "center", gap: 12, cursor: "pointer" }}>
              <div style={{ width: 48, height: 48, borderRadius: "50%", background: "linear-gradient(135deg, #0891B2, #F97316)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 800, fontSize: 17, flexShrink: 0 }}>{getInitials(partner.name)}</div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ display: "flex", justifyContent: "space-between" }}>
                  <span style={{ fontWeight: 700, fontSize: 15 }}>{partner.name}</span>
                  {lastMsg && <span style={{ fontSize: 11, color: COLORS.textLight }}>{lastMsg.created_at.split("T")[1]?.slice(0, 5)}</span>}
                </div>
                <div style={{ fontSize: 13, color: COLORS.textLight, marginTop: 2, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                  {lastMsg?.text || "Henüz mesaj yok"}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    );
  }

  const partner = users.find(u => u.id === activeChat);
  const conversation = getConversation(activeChat);

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "calc(100vh - 130px)" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 12, padding: "12px 16px", background: "#fff", borderBottom: `1px solid ${COLORS.border}` }}>
        <span onClick={() => setActiveChat(null)} style={{ cursor: "pointer", color: COLORS.primary }}><Icons.ChevronLeft /></span>
        <div style={{ width: 38, height: 38, borderRadius: "50%", background: "linear-gradient(135deg, #0891B2, #F97316)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 800, fontSize: 14 }}>{partner ? getInitials(partner.name) : "?"}</div>
        <div><div style={{ fontWeight: 700, fontSize: 15 }}>{partner?.name}</div><div style={{ fontSize: 12, color: COLORS.success }}>● Çevrimiçi</div></div>
      </div>
      <div style={{ flex: 1, overflowY: "auto", padding: 16, background: "#F8FAFC" }}>
        {conversation.map(m => {
          const isMine = m.sender_id === user.id;
          return (
            <div key={m.id} style={{ display: "flex", justifyContent: isMine ? "flex-end" : "flex-start", marginBottom: 8 }}>
              <div style={{ maxWidth: "75%", padding: "10px 14px", borderRadius: isMine ? "16px 16px 4px 16px" : "16px 16px 16px 4px", background: isMine ? "linear-gradient(135deg, #0891B2, #0EA5E9)" : "#fff", color: isMine ? "#fff" : COLORS.text, fontSize: 14, boxShadow: "0 1px 3px rgba(0,0,0,0.08)" }}>
                {m.msg_type === "file" ? <div style={{ display: "flex", alignItems: "center", gap: 6 }}><Icons.Attach /><span style={{ fontWeight: 600 }}>{m.text}</span></div> : m.text}
                <div style={{ fontSize: 10, opacity: 0.7, marginTop: 4, textAlign: "right" }}>{m.created_at.split("T")[1]?.slice(0, 5)}</div>
              </div>
            </div>
          );
        })}
        <div ref={messagesEndRef} />
      </div>
      <div style={{ display: "flex", gap: 8, padding: "10px 16px", background: "#fff", borderTop: `1px solid ${COLORS.border}`, alignItems: "center" }}>
        <button onClick={handleFileAttach} style={{ background: "none", border: "none", color: COLORS.textLight, cursor: "pointer", padding: 4 }}><Icons.Attach /></button>
        <input style={{ flex: 1, padding: "10px 16px", borderRadius: 20, border: `1.5px solid ${COLORS.border}`, fontSize: 15, outline: "none", boxSizing: "border-box" }} placeholder="Mesaj yazın..." value={msgText} onChange={e => setMsgText(e.target.value)} onKeyDown={e => e.key === "Enter" && handleSend()} />
        <button onClick={handleSend} style={{ background: COLORS.primary, border: "none", borderRadius: "50%", width: 40, height: 40, display: "flex", alignItems: "center", justifyContent: "center", cursor: "pointer", color: "#fff" }}><Icons.Send /></button>
      </div>
    </div>
  );
}

// ==================== PROFILE PAGE ====================
function ProfilePage({ user, sessions, onLogout, onUpdate }: { user: UserType; sessions: SessionType[]; onLogout: () => void; onUpdate: (u: UserType) => void }) {
  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({ ...user });
  const mySessions = user.role === "admin" ? sessions : sessions.filter(s => s.client_id === user.id);
  const completed = mySessions.filter(s => s.status === "completed").length;
  const cardStyle = { background: "#fff", borderRadius: 16, padding: 20, marginBottom: 12, boxShadow: "0 1px 3px rgba(0,0,0,0.06)", border: `1px solid ${COLORS.border}` };
  const inputStyle = { width: "100%", padding: "12px 16px", borderRadius: 12, border: `1.5px solid ${COLORS.border}`, fontSize: 15, outline: "none", boxSizing: "border-box" as const };
  const labelStyle = { fontSize: 13, fontWeight: 600, color: COLORS.textLight, marginBottom: 6, display: "flex" as const, alignItems: "center" as const, gap: 4 };

  const handleSave = () => { onUpdate(form as UserType); setEditing(false); };

  return (
    <div style={{ padding: 16 }}>
      <div style={{ ...cardStyle, textAlign: "center", padding: 28, background: "linear-gradient(135deg, #F0FDFA 0%, #EFF6FF 100%)" }}>
        <div style={{ width: 80, height: 80, borderRadius: "50%", background: "linear-gradient(135deg, #0891B2, #F97316)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 800, fontSize: 28, margin: "0 auto 14px" }}>{getInitials(user.name)}</div>
        <h2 style={{ margin: "0 0 4px", fontSize: 22, fontWeight: 800 }}>{user.name}</h2>
        <p style={{ margin: 0, fontSize: 14, color: COLORS.textLight }}>{user.email}</p>
        {user.role === "admin" && <span style={{ background: COLORS.secondary, color: "#fff", borderRadius: 20, padding: "3px 10px", fontSize: 11, fontWeight: 700, display: "inline-block", marginTop: 8 }}>Admin</span>}
        <div style={{ display: "flex", justifyContent: "center", gap: 24, marginTop: 16 }}>
          <div><div style={{ fontSize: 22, fontWeight: 800, color: COLORS.primary }}>{mySessions.length}</div><div style={{ fontSize: 11, color: COLORS.textLight }}>Toplam</div></div>
          <div><div style={{ fontSize: 22, fontWeight: 800, color: COLORS.success }}>{completed}</div><div style={{ fontSize: 11, color: COLORS.textLight }}>Tamamlanan</div></div>
        </div>
      </div>

      <div style={cardStyle}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
          <h3 style={{ margin: 0, fontSize: 16, fontWeight: 700 }}>Profil Bilgileri</h3>
          <button onClick={() => editing ? handleSave() : setEditing(true)} style={{ background: "none", border: "none", color: COLORS.primary, cursor: "pointer", fontWeight: 700, fontSize: 13, display: "flex", alignItems: "center", gap: 4 }}>
            {editing ? <><Icons.Check /> Kaydet</> : <><Icons.Edit /> Düzenle</>}
          </button>
        </div>
        {[
          { key: "name", label: "Ad Soyad", icon: "👤" },
          { key: "email", label: "E-posta", icon: "📧" },
          { key: "phone", label: "Telefon", icon: "📱" },
          { key: "gender", label: "Cinsiyet", icon: "⚧" },
          { key: "city", label: "Şehir", icon: "📍" },
        ].map(f => (
          <div key={f.key} style={{ marginBottom: 14 }}>
            <label style={labelStyle}>{f.icon} {f.label}</label>
            {editing ? (
              f.key === "city" ? <select style={{ ...inputStyle, appearance: "auto" as const }} value={(form as any)[f.key]} onChange={e => setForm(p => ({ ...p, [f.key]: e.target.value }))}>{CITIES.map(c => <option key={c}>{c}</option>)}</select>
              : f.key === "gender" ? <div style={{ display: "flex", gap: 8 }}>{["Kadın", "Erkek", "Diğer"].map(g => <button key={g} onClick={() => setForm(p => ({ ...p, gender: g }))} style={{ flex: 1, padding: 8, borderRadius: 8, border: `2px solid ${form.gender === g ? COLORS.primary : COLORS.border}`, background: form.gender === g ? `${COLORS.primary}10` : "#fff", fontWeight: 600, fontSize: 13, cursor: "pointer", color: form.gender === g ? COLORS.primary : COLORS.textLight }}>{g}</button>)}</div>
              : <input style={inputStyle} value={(form as any)[f.key]} onChange={e => setForm(p => ({ ...p, [f.key]: e.target.value }))} />
            ) : <div style={{ fontSize: 15, fontWeight: 600, padding: "8px 0" }}>{(user as any)[f.key]}</div>}
          </div>
        ))}
        <div style={{ marginBottom: 14 }}>
          <label style={labelStyle}>📝 Biyografi</label>
          {editing ? <textarea style={{ ...inputStyle, minHeight: 80, resize: "vertical" }} value={form.bio} onChange={e => setForm(p => ({ ...p, bio: e.target.value }))} />
          : <div style={{ fontSize: 14, color: COLORS.textLight, padding: "8px 0", fontStyle: "italic" }}>{user.bio || "Henüz biyografi eklenmemiş."}</div>}
        </div>
      </div>

      <div style={{ ...cardStyle, display: "flex", alignItems: "center", gap: 12 }}>
        <div style={{ width: 44, height: 44, borderRadius: 12, background: `${COLORS.accent}12`, display: "flex", alignItems: "center", justifyContent: "center", color: COLORS.accent }}><Icons.Mail /></div>
        <div style={{ flex: 1 }}><div style={{ fontWeight: 700, fontSize: 14 }}>E-posta Bildirimleri</div><div style={{ fontSize: 12, color: COLORS.textLight }}>Seans hatırlatmaları aktif ✅</div></div>
      </div>

      <button onClick={onLogout} style={{ background: "#fff", color: COLORS.danger, border: `2px solid ${COLORS.danger}`, borderRadius: 12, padding: "12px 24px", fontSize: 15, fontWeight: 700, cursor: "pointer", width: "100%", display: "flex", alignItems: "center", justifyContent: "center", gap: 8, marginTop: 8 }}>
        <Icons.LogOut /> Çıkış Yap
      </button>
    </div>
  );
}

// ==================== NOTIFICATIONS PANEL ====================
function NotificationsPanel({ notifications, onClose, onMarkRead }: { notifications: NotificationType[]; onClose: () => void; onMarkRead: (id: string) => void }) {
  return (
    <div style={{ position: "fixed", top: 0, left: 0, right: 0, bottom: 0, zIndex: 100 }}>
      <div onClick={onClose} style={{ position: "absolute", inset: 0, background: "rgba(0,0,0,0.3)" }} />
      <div style={{ position: "absolute", top: 0, right: 0, width: "100%", maxWidth: 400, height: "100%", background: "#fff", boxShadow: "-10px 0 40px rgba(0,0,0,0.1)", overflowY: "auto", animation: "slideRight 0.3s ease" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "16px 20px", borderBottom: `1px solid ${COLORS.border}`, position: "sticky", top: 0, background: "#fff", zIndex: 1 }}>
          <h3 style={{ margin: 0, fontSize: 18, fontWeight: 800 }}>🔔 Bildirimler</h3>
          <span onClick={onClose} style={{ cursor: "pointer", color: COLORS.textLight }}><Icons.X /></span>
        </div>
        <div style={{ padding: 16 }}>
          {notifications.length === 0 ? <p style={{ color: COLORS.textLight, textAlign: "center", padding: 40 }}>Bildirim yok</p> : notifications.map(n => {
            const typeIcons: Record<string, string> = { reminder: "🗓", review: "⭐", message: "💬", system: "🔔" };
            return (
              <div key={n.id} onClick={() => onMarkRead(n.id)} style={{ display: "flex", gap: 12, padding: "14px 0", borderBottom: `1px solid ${COLORS.border}`, opacity: n.is_read ? 0.6 : 1, cursor: "pointer" }}>
                <div style={{ fontSize: 22, lineHeight: 1 }}>{typeIcons[n.type] || "🔔"}</div>
                <div style={{ flex: 1 }}>
                  <p style={{ margin: 0, fontSize: 14, fontWeight: n.is_read ? 400 : 600 }}>{n.text}</p>
                  <p style={{ margin: "4px 0 0", fontSize: 12, color: COLORS.textLight }}>{n.created_at?.split("T")[0]}</p>
                </div>
                {!n.is_read && <div style={{ width: 8, height: 8, borderRadius: "50%", background: COLORS.secondary, marginTop: 4 }} />}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

// ==================== MAIN APP ====================
export default function NextERAApp() {
  const [currentUser, setCurrentUser] = useState<UserType | null>(null);
  const [screen, setScreen] = useState<"login" | "register" | "app">("login");
  const [page, setPage] = useState("home");
  const [users, setUsers] = useState<UserType[]>([]);
  const [sessions, setSessions] = useState<SessionType[]>([]);
  const [messages, setMessages] = useState<MessageType[]>([]);
  const [notifications, setNotifications] = useState<NotificationType[]>([]);
  const [showNotifications, setShowNotifications] = useState(false);
  const [toast, setToast] = useState<{ message: string; type: string } | null>(null);
  const [loading, setLoading] = useState(true);

  const isAdmin = currentUser?.role === "admin";
  const unreadNotifs = notifications.filter(n => !n.is_read).length;

  const showToast = useCallback((message: string, type: string = "info") => {
    setToast({ message, type });
  }, []);

  // ---- Fetch data from Supabase ----
  const fetchData = useCallback(async (userId: string) => {
    try {
      const [usersRes, sessionsRes, messagesRes, notifsRes] = await Promise.all([
        supabase.from("users").select("*"),
        supabase.from("sessions").select("*"),
        supabase.from("messages").select("*").or(`sender_id.eq.${userId},receiver_id.eq.${userId}`).order("created_at", { ascending: true }),
        supabase.from("notifications").select("*").eq("user_id", userId).order("created_at", { ascending: false }),
      ]);
      if (usersRes.data) setUsers(usersRes.data);
      if (sessionsRes.data) setSessions(sessionsRes.data);
      if (messagesRes.data) setMessages(messagesRes.data);
      if (notifsRes.data) setNotifications(notifsRes.data);
    } catch (err) {
      console.error("Data fetch error:", err);
    }
  }, []);

  // ---- Auth state ----
  useEffect(() => {
    const checkAuth = async () => {
      const { data: { session } } = await supabase.auth.getSession();
      if (session?.user) {
        const { data: userData } = await supabase.from("users").select("*").eq("email", session.user.email).single();
        if (userData) {
          setCurrentUser(userData);
          setScreen("app");
          await fetchData(userData.id);
        }
      }
      setLoading(false);
    };
    checkAuth();

    const { data: { subscription } } = supabase.auth.onAuthStateChange(async (event, session) => {
      if (event === "SIGNED_OUT") {
        setCurrentUser(null);
        setScreen("login");
      }
    });

    return () => subscription.unsubscribe();
  }, [fetchData]);

  // ---- Login ----
  const handleLogin = async (email: string, password: string) => {
    const { data, error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) {
      showToast("Giriş başarısız: " + error.message, "error");
      return;
    }
    if (data.user) {
      const { data: userData } = await supabase.from("users").select("*").eq("email", data.user.email).single();
      if (userData) {
        setCurrentUser(userData);
        setScreen("app");
        await fetchData(userData.id);
        showToast(`Hoş geldiniz, ${userData.name}!`, "success");
      }
    }
  };

  // ---- Register ----
  const handleRegister = async (form: any) => {
    const { data, error } = await supabase.auth.signUp({ email: form.email, password: form.password });
    if (error) {
      showToast("Kayıt başarısız: " + error.message, "error");
      return;
    }
    if (data.user) {
      const initials = form.name.split(" ").map((w: string) => w[0]).join("").toUpperCase().slice(0, 2);
      const newUser = {
        id: data.user.id,
        name: form.name,
        email: form.email,
        gender: form.gender,
        phone: form.phone,
        city: form.city,
        bio: form.bio || "",
        role: form.email === ADMIN_EMAIL ? "admin" : "client",
        avatar: initials,
      };
      await supabase.from("users").insert(newUser);
      setCurrentUser(newUser as UserType);
      setScreen("app");
      await fetchData(newUser.id);
      showToast("Hesabınız oluşturuldu! 🎉", "success");
    }
  };

  // ---- Logout ----
  const handleLogout = async () => {
    await supabase.auth.signOut();
    setCurrentUser(null);
    setScreen("login");
    setPage("home");
  };

  // ---- Book Session ----
  const handleBookSession = async (date: string, time: string) => {
    if (!currentUser) return;
    const newSession = {
      client_id: currentUser.id,
      date, time, duration: 50,
      status: "upcoming",
      rating: null, review: null,
    };
    const { data, error } = await supabase.from("sessions").insert(newSession).select().single();
    if (data) {
      setSessions(prev => [...prev, data]);
      // Add notification
      const notif = { user_id: currentUser.id, text: `${formatDate(date)} ${time} tarihine yeni seans eklendi.`, type: "reminder", is_read: false };
      const { data: nData } = await supabase.from("notifications").insert(notif).select().single();
      if (nData) setNotifications(prev => [nData, ...prev]);
      // Google Takvim entegrasyonu
      try {
        const client = users.find(u => u.id === currentUser.id);
        await fetch("/api/calendar", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            date, time, duration: 50,
            clientName: client?.name || "Danışan",
            clientEmail: client?.email || "",
          }),
        });
        showToast("Seans oluşturuldu ve takvime eklendi! 📅", "success");
      } catch (e) {
        showToast("Seans oluşturuldu! (Takvim bağlantısı kontrol edin)", "success");
      }
    }
    if (error) showToast("Hata: " + error.message, "error");
  };

  // ---- Send Message ----
  const handleSendMessage = async (receiverId: string, text: string, type: string) => {
    if (!currentUser) return;
    const newMsg = { sender_id: currentUser.id, receiver_id: receiverId, text, msg_type: type };
    const { data, error } = await supabase.from("messages").insert(newMsg).select().single();
    if (data) setMessages(prev => [...prev, data]);
    if (error) console.error(error);
  };

  // ---- Update Profile ----
  const handleUpdateProfile = async (updatedUser: UserType) => {
    const { error } = await supabase.from("users").update({
      name: updatedUser.name, phone: updatedUser.phone, gender: updatedUser.gender,
      city: updatedUser.city, bio: updatedUser.bio,
    }).eq("id", updatedUser.id);
    if (!error) {
      setCurrentUser(updatedUser);
      setUsers(prev => prev.map(u => u.id === updatedUser.id ? updatedUser : u));
      showToast("Profil güncellendi! ✅", "success");
    }
  };

  // ---- Mark Notification Read ----
  const handleMarkNotifRead = async (id: string) => {
    await supabase.from("notifications").update({ is_read: true }).eq("id", id);
    setNotifications(prev => prev.map(n => n.id === id ? { ...n, is_read: true } : n));
  };

  // ---- Loading ----
  if (loading) {
    return (
      <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", background: "linear-gradient(135deg, #0891B2, #0EA5E9)" }}>
        <div style={{ textAlign: "center", color: "#fff" }}>
          <div style={{ fontSize: 42, fontWeight: 900, marginBottom: 12 }}>Next<span style={{ color: "#FCD34D" }}>ERA</span></div>
          <div style={{ fontSize: 16, opacity: 0.8 }}>Yükleniyor...</div>
        </div>
      </div>
    );
  }

  // ---- Auth Screens ----
  if (screen === "login") return <LoginScreen onLogin={handleLogin} onGoRegister={() => setScreen("register")} />;
  if (screen === "register") return <RegisterScreen onRegister={handleRegister} onGoLogin={() => setScreen("login")} />;

  // ---- Main App ----
  const navItems = isAdmin
    ? [{ id: "home", label: "Dashboard", Icon: Icons.Dashboard }, { id: "sessions", label: "Seanslar", Icon: Icons.Calendar }, { id: "messages", label: "Mesajlar", Icon: Icons.Chat }, { id: "profile", label: "Profil", Icon: Icons.User }]
    : [{ id: "home", label: "Ana Sayfa", Icon: Icons.Home }, { id: "sessions", label: "Seanslar", Icon: Icons.Calendar }, { id: "messages", label: "Mesajlar", Icon: Icons.Chat }, { id: "profile", label: "Profil", Icon: Icons.User }];

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { margin: 0; background: #E2E8F0; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }
        input:focus, textarea:focus, select:focus { border-color: #0891B2 !important; box-shadow: 0 0 0 3px rgba(8,145,178,0.12); outline: none; }
        button:active { transform: scale(0.97); }
        @keyframes slideDown { from { transform: translateX(-50%) translateY(-20px); opacity: 0; } to { transform: translateX(-50%) translateY(0); opacity: 1; } }
        @keyframes slideRight { from { transform: translateX(100%); } to { transform: translateX(0); } }
      `}</style>

      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
      {showNotifications && <NotificationsPanel notifications={notifications} onClose={() => setShowNotifications(false)} onMarkRead={handleMarkNotifRead} />}

      {/* Header */}
      <div style={{ background: "linear-gradient(135deg, #0891B2, #0EA5E9)", padding: "16px 20px", display: "flex", alignItems: "center", justifyContent: "space-between", position: "sticky", top: 0, zIndex: 50 }}>
        <div>
          <div style={{ color: "#fff", fontSize: 22, fontWeight: 800, letterSpacing: "-0.5px" }}>Next<span style={{ color: "#FCD34D" }}>ERA</span></div>
          <div style={{ color: "rgba(255,255,255,0.8)", fontSize: 12, fontWeight: 500 }}>{isAdmin ? "Admin Paneli" : "Danışmanlık Platformu"}</div>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div onClick={() => setShowNotifications(true)} style={{ position: "relative", cursor: "pointer", color: "#fff" }}>
            <Icons.Bell />
            {unreadNotifs > 0 && <span style={{ position: "absolute", top: -4, right: -4, width: 18, height: 18, borderRadius: "50%", background: COLORS.secondary, color: "#fff", fontSize: 10, fontWeight: 800, display: "flex", alignItems: "center", justifyContent: "center" }}>{unreadNotifs}</span>}
          </div>
          <div style={{ width: 34, height: 34, borderRadius: "50%", background: "linear-gradient(135deg, #0891B2, #F97316)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 800, fontSize: 12, border: "2px solid rgba(255,255,255,0.4)" }}>{currentUser ? getInitials(currentUser.name) : "?"}</div>
        </div>
      </div>

      {/* Page Content */}
      <div style={{ paddingBottom: 80, minHeight: "calc(100vh - 130px)" }}>
        {page === "home" && (isAdmin ? <AdminDashboard users={users} sessions={sessions} /> : currentUser && <ClientHome user={currentUser} sessions={sessions} users={users} />)}
        {page === "sessions" && currentUser && <SessionsPage user={currentUser} sessions={sessions} users={users} onBook={handleBookSession} isAdmin={isAdmin} />}
        {page === "messages" && currentUser && <MessagesPage user={currentUser} messages={messages} users={users} onSend={handleSendMessage} isAdmin={isAdmin} />}
        {page === "profile" && currentUser && <ProfilePage user={currentUser} sessions={sessions} onLogout={handleLogout} onUpdate={handleUpdateProfile} />}
      </div>

      {/* Bottom Nav */}
      <div style={{ display: "flex", justifyContent: "space-around", background: "#fff", borderTop: `1px solid ${COLORS.border}`, padding: "8px 0 12px", position: "sticky", bottom: 0, zIndex: 50 }}>
        {navItems.map(({ id, label, Icon }) => (
          <div key={id} onClick={() => setPage(id)} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 2, color: page === id ? COLORS.primary : COLORS.textLight, cursor: "pointer", fontSize: 11, fontWeight: page === id ? 700 : 500, padding: "4px 12px", borderRadius: 12 }}>
            <Icon />
            <span>{label}</span>
            {page === id && <div style={{ width: 5, height: 5, borderRadius: "50%", background: COLORS.primary, marginTop: 2 }} />}
          </div>
        ))}
      </div>
    </>
  );
}
