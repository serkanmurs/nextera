"use client";
import { useState, useEffect } from "react";
import { supabase } from "@/lib/supabase";

export default function ResetPasswordPage() {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    // Supabase handles the token from URL automatically
    const { data: { subscription } } = supabase.auth.onAuthStateChange((event) => {
      if (event === "PASSWORD_RECOVERY") {
        setReady(true);
      }
    });
    // Also check if already in recovery state
    supabase.auth.getSession().then(({ data: { session } }) => {
      if (session) setReady(true);
    });
    return () => subscription.unsubscribe();
  }, []);

  const handleReset = async () => {
    setError("");
    setMessage("");
    if (!password || !confirmPassword) {
      setError("Lütfen tüm alanları doldurun.");
      return;
    }
    if (password.length < 6) {
      setError("Şifre en az 6 karakter olmalıdır.");
      return;
    }
    if (password !== confirmPassword) {
      setError("Şifreler eşleşmiyor.");
      return;
    }
    setLoading(true);
    const { error: updateError } = await supabase.auth.updateUser({ password });
    setLoading(false);
    if (updateError) {
      setError("Hata: " + updateError.message);
    } else {
      setMessage("Şifreniz başarıyla güncellendi! Giriş sayfasına yönlendiriliyorsunuz...");
      setTimeout(() => {
        window.location.href = "/";
      }, 2500);
    }
  };

  return (
    <div style={{ minHeight: "100vh", background: "linear-gradient(180deg, #0891B2 0%, #0EA5E9 40%, #F8FAFC 100%)", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: 24, fontFamily: "'Nunito', sans-serif" }}>
      <div style={{ marginBottom: 40, textAlign: "center" }}>
        <div style={{ fontSize: 42, fontWeight: 900, color: "#fff", letterSpacing: "-1px" }}>Next<span style={{ color: "#FCD34D" }}>ERA</span></div>
        <div style={{ color: "rgba(255,255,255,0.85)", fontSize: 15, marginTop: 6, fontWeight: 500 }}>Şifre Sıfırlama</div>
      </div>
      <div style={{ background: "#fff", borderRadius: 24, padding: 32, width: "100%", maxWidth: 380, boxShadow: "0 20px 60px rgba(0,0,0,0.12)" }}>
        <h2 style={{ margin: "0 0 8px", fontSize: 22, fontWeight: 800, textAlign: "center" }}>Yeni Şifre Belirle</h2>
        <p style={{ margin: "0 0 24px", fontSize: 13, color: "#64748B", textAlign: "center" }}>Hesabınız için yeni bir şifre belirleyin.</p>

        {error && <div style={{ background: "#FEF2F2", color: "#EF4444", padding: "10px 14px", borderRadius: 10, fontSize: 13, marginBottom: 16, fontWeight: 600 }}>{error}</div>}
        {message && <div style={{ background: "#F0FDF4", color: "#10B981", padding: "10px 14px", borderRadius: 10, fontSize: 13, marginBottom: 16, fontWeight: 600 }}>{message}</div>}

        {!ready && !message ? (
          <div style={{ textAlign: "center", padding: 20 }}>
            <p style={{ color: "#64748B", fontSize: 14 }}>Oturum doğrulanıyor...</p>
            <p style={{ color: "#64748B", fontSize: 12, marginTop: 8 }}>Bu sayfa e-postanızdaki şifre sıfırlama linkinden açılmalıdır.</p>
            <a href="/" style={{ color: "#0891B2", fontSize: 14, fontWeight: 700, marginTop: 16, display: "inline-block" }}>← Giriş Sayfasına Dön</a>
          </div>
        ) : !message ? (
          <>
            <div style={{ marginBottom: 16 }}>
              <label style={{ fontSize: 13, fontWeight: 600, color: "#64748B", marginBottom: 6, display: "block" }}>Yeni Şifre</label>
              <input
                style={{ width: "100%", padding: "12px 16px", borderRadius: 12, border: "1.5px solid #E2E8F0", fontSize: 15, outline: "none", boxSizing: "border-box" }}
                type="password"
                value={password}
                onChange={e => { setPassword(e.target.value); setError(""); }}
                placeholder="En az 6 karakter"
              />
            </div>
            <div style={{ marginBottom: 24 }}>
              <label style={{ fontSize: 13, fontWeight: 600, color: "#64748B", marginBottom: 6, display: "block" }}>Yeni Şifre (Tekrar)</label>
              <input
                style={{ width: "100%", padding: "12px 16px", borderRadius: 12, border: "1.5px solid #E2E8F0", fontSize: 15, outline: "none", boxSizing: "border-box" }}
                type="password"
                value={confirmPassword}
                onChange={e => { setConfirmPassword(e.target.value); setError(""); }}
                placeholder="Şifrenizi tekrar girin"
                onKeyDown={e => e.key === "Enter" && handleReset()}
              />
            </div>
            <button
              onClick={handleReset}
              disabled={loading}
              style={{ background: "linear-gradient(135deg, #0891B2, #0EA5E9)", color: "#fff", border: "none", borderRadius: 12, padding: "12px 24px", fontSize: 15, fontWeight: 700, cursor: "pointer", width: "100%", boxShadow: "0 4px 14px rgba(8,145,178,0.3)", opacity: loading ? 0.7 : 1 }}
            >
              {loading ? "Güncelleniyor..." : "Şifreyi Güncelle"}
            </button>
          </>
        ) : null}
      </div>
    </div>
  );
}
