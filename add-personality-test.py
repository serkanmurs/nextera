filepath = 'src/app/page.tsx'
content = open(filepath, 'r').read()

print("Kisilik Testi entegrasyonu basliyor...")

# ============================================================
# 1. TYPE ekle
# ============================================================
old_journal_type_end = '''interface JournalType {
  id: string;
  client_id: string;
  session_id: string | null;
  note: string;
  category: string;
  created_at: string;
}'''

new_journal_type_end = '''interface JournalType {
  id: string;
  client_id: string;
  session_id: string | null;
  note: string;
  category: string;
  created_at: string;
}

interface PersonalityTestType {
  id: string;
  client_id: string;
  popular_optimist: number;
  strong_choleric: number;
  perfectionist_melancholic: number;
  peaceful_phlegmatic: number;
  answers: any;
  created_at: string;
}'''

if old_journal_type_end in content:
    content = content.replace(old_journal_type_end, new_journal_type_end)
    print("  OK 1. Type eklendi")

# ============================================================
# 2. STATE ekle
# ============================================================
old_j = '  const [journal, setJournal] = useState<JournalType[]>([]);'
new_j = '''  const [journal, setJournal] = useState<JournalType[]>([]);
  const [personalityTests, setPersonalityTests] = useState<PersonalityTestType[]>([]);'''
if old_j in content:
    content = content.replace(old_j, new_j)
    print("  OK 2. State eklendi")

# ============================================================
# 3. FETCH ekle
# ============================================================
old_f = '      if (journalRes.data) setJournal(journalRes.data);'
new_f = '''      if (journalRes.data) setJournal(journalRes.data);
      const { data: ptData } = await supabase.from("personality_tests").select("*");
      if (ptData) setPersonalityTests(ptData);'''
if old_f in content:
    content = content.replace(old_f, new_f)
    print("  OK 3. Fetch eklendi")

# ============================================================
# 4. ClientHome props
# ============================================================
old_p = 'onEditJournal: (id: string, note: string) => void; onDeleteJournal: (id: string) => void })'
new_p = 'onEditJournal: (id: string, note: string) => void; onDeleteJournal: (id: string) => void; personalityTest: PersonalityTestType | null; onSaveTest: (r: any) => void })'
if old_p in content:
    content = content.replace(old_p, new_p)
    print("  OK 4a. Props type")

old_d = 'onAddTask, onToggleTask, onAddJournal, onEditTask, onDeleteTask, onEditJournal, onDeleteJournal }'
new_d = 'onAddTask, onToggleTask, onAddJournal, onEditTask, onDeleteTask, onEditJournal, onDeleteJournal, personalityTest, onSaveTest }'
if old_d in content:
    content = content.replace(old_d, new_d)
    print("  OK 4b. Props destructure")

# ============================================================
# 5. Render props
# ============================================================
old_r = 'onDeleteJournal={async (id) => { await supabase.from("journal").delete().eq("id", id); setJournal(prev => prev.filter(j => j.id !== id)); }} />'
new_r = 'onDeleteJournal={async (id) => { await supabase.from("journal").delete().eq("id", id); setJournal(prev => prev.filter(j => j.id !== id)); }} personalityTest={personalityTests.find(pt => pt.client_id === currentUser?.id) || null} onSaveTest={async (results) => { const { data } = await supabase.from("personality_tests").upsert({ client_id: currentUser!.id, ...results }).select().single(); if (data) setPersonalityTests(prev => { const f = prev.filter(p => p.client_id !== currentUser!.id); return [...f, data]; }); }} />'
if old_r in content:
    content = content.replace(old_r, new_r)
    print("  OK 5. Render props")

# ============================================================
# 6. showPersonalityTest state
# ============================================================
old_ms = '  const mySessions = sessions.filter(s => s.client_id === user.id);'
new_ms = '''  const [showPersonalityTest, setShowPersonalityTest] = useState(false);
  const mySessions = sessions.filter(s => s.client_id === user.id);'''
if old_ms in content:
    content = content.replace(old_ms, new_ms)
    print("  OK 6. showPersonalityTest state")

# ============================================================
# 7. Kisilik Testi karti - Adimlarim'dan once
# ============================================================
old_ak = '      {/* Aksiyon'

CARD = '''      {/* Kisilik Testi */}
      {showPersonalityTest ? (
        <PersonalityTestScreen onClose={() => setShowPersonalityTest(false)} onSave={(r: any) => { onSaveTest(r); setShowPersonalityTest(false); }} />
      ) : (
        <div onClick={() => setShowPersonalityTest(true)} style={{ ...cardStyle, cursor: "pointer", background: personalityTest ? "#F0FDF4" : "linear-gradient(135deg, #FEF3C7, #FFF7ED)", border: personalityTest ? "1px solid #BBF7D0" : "1px solid #FED7AA" }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
            <div>
              <div style={{ fontSize: 15, fontWeight: 800, color: "#0F172A" }}>{personalityTest ? "Kişilik Analiz Sonucun" : "Kişilik Analizini Keşfet"}</div>
              <div style={{ fontSize: 12, color: "#64748B", marginTop: 4 }}>{personalityTest ? "Sonuçlarını görüntüle veya testi tekrarla" : "40 soruluk Florence Littauer kişilik testi"}</div>
            </div>
            <div style={{ fontSize: 28 }}>{personalityTest ? "📊" : "🧠"}</div>
          </div>
          {personalityTest && (
            <div style={{ display: "flex", gap: 6, marginTop: 10, flexWrap: "wrap" as const }}>
              <span style={{ fontSize: 11, padding: "3px 8px", borderRadius: 6, background: "#FEF3C7", color: "#92400E", fontWeight: 600 }}>Optimist: %{Math.round(personalityTest.popular_optimist / 40 * 100)}</span>
              <span style={{ fontSize: 11, padding: "3px 8px", borderRadius: 6, background: "#FEE2E2", color: "#991B1B", fontWeight: 600 }}>Kolerik: %{Math.round(personalityTest.strong_choleric / 40 * 100)}</span>
              <span style={{ fontSize: 11, padding: "3px 8px", borderRadius: 6, background: "#DBEAFE", color: "#1E40AF", fontWeight: 600 }}>Melankolik: %{Math.round(personalityTest.perfectionist_melancholic / 40 * 100)}</span>
              <span style={{ fontSize: 11, padding: "3px 8px", borderRadius: 6, background: "#D1FAE5", color: "#065F46", fontWeight: 600 }}>Soğukkanlı: %{Math.round(personalityTest.peaceful_phlegmatic / 40 * 100)}</span>
            </div>
          )}
        </div>
      )}

      {/* Aksiyon'''

if old_ak in content:
    content = content.replace(old_ak, CARD, 1)
    print("  OK 7. Kart eklendi")

# ============================================================
# 8. PersonalityTestScreen component
# ============================================================
old_toast = '// ==================== TOAST =='

# Florence Littauer testi - soru sirasi:
# Her soruda 4 secenek: sira Populer(P), Guclu Kolerik(K), Mukemmeliyetci Melankolik(M), Bariscil Sogukkanli(B)
# Ancak sira her soruda farkli - asagida dogru mapping var

COMP = '''// ==================== PERSONALITY TEST ====================
const PQ = [
  {o:["Maceraperest","Uyumlu","Canlı","Analitik"],t:["K","B","P","M"]},
  {o:["Israrcı","Şakacı","İkna edici","Barışçıl"],t:["K","P","K","B"]},
  {o:["Uysal","Özverili","Sosyal","Azimli"],t:["B","M","P","K"]},
  {o:["Düşünceli","Kontrollü","Rekabetçi","İnandırıcı"],t:["M","B","K","P"]},
  {o:["Hayat veren","Saygılı","İhtiyatlı","Becerili"],t:["P","B","M","K"]},
  {o:["Halinden Memnun","Duyarlı","Kendine Güvenli","Hayat Dolu"],t:["B","M","K","P"]},
  {o:["Planlayıcı","Sabırlı","Olumlu","Yönlendirici"],t:["M","B","P","K"]},
  {o:["Kendinden Emin","Günü Yaşayan","Programlı","Utangaç"],t:["K","P","M","B"]},
  {o:["Düzenli","Nazik","Açık sözlü","İyimser"],t:["M","B","K","P"]},
  {o:["Dostça Davranan","Sadık","Eğlenceli","Etkili"],t:["B","M","P","K"]},
  {o:["Cesur","Hoş","Diplomatik","Ayrıntıcı"],t:["K","P","B","M"]},
  {o:["Neşeli","Tutarlı","Kültürlü","Güvenli"],t:["P","B","M","K"]},
  {o:["İdealist","Bağımsız","Kendi Halinde","Esin Kaynağı"],t:["M","K","B","P"]},
  {o:["Sıcakkanlı","Kararlı","İnce Esprili","Derin"],t:["P","K","B","M"]},
  {o:["Arabulucu","Müziksever","Harekete Geçiren","Kolay Kaynaşan"],t:["B","M","K","P"]},
  {o:["İnce düşünceli","Azimli","Konuşkan","Hoşgörülü"],t:["M","K","P","B"]},
  {o:["İyi Dinleyici","Vefalı","Lider","Enerjik"],t:["B","M","K","P"]},
  {o:["Kanaatkar","Şef","Organizatör","Şirin"],t:["B","K","M","P"]},
  {o:["Mükemmeliyetçi","Tatlı","Üretken","Popüler"],t:["M","B","K","P"]},
  {o:["Hareketli","Gözü pek","Terbiyeli","Dengeli"],t:["P","K","M","B"]},
  {o:["İfadesiz","Sıkılgan","Arsız","Zorba"],t:["B","M","P","K"]},
  {o:["Disiplinsiz","Anlayışsız","Coşkusuz","Affetmeyen"],t:["P","K","B","M"]},
  {o:["Suskun","Kinci","Karşı Gelen","Kendini Tekrarlayan"],t:["B","M","K","P"]},
  {o:["Telaşlı","Korkak","Unutkan","Dobra"],t:["M","B","P","K"]},
  {o:["Laf Kesen","Sabırsız","Güvensiz","Kararsız"],t:["P","K","M","B"]},
  {o:["Popüler Olmayan","Bulaşmayan","Ne Yapacağı Belirsiz","Şevkatsiz"],t:["M","B","P","K"]},
  {o:["Dik Kafalı","Gelişigüzel","Zor Beğenen","Tereddütlü"],t:["K","P","M","B"]},
  {o:["Renksiz","Kötümser","Kibirli","Göz Yuman"],t:["B","M","K","P"]},
  {o:["Kolay Sinirlenen","Amaçsız","İddiacı","Yabancılaşmış"],t:["M","B","K","P"]},
  {o:["Ahmak","Negatif davranan","Küstah","Kayıtsız"],t:["P","M","K","B"]},
  {o:["Endişeli","Yalnızlığa Sığınan","İş Delisi","Tanınmak İsteyen"],t:["M","B","K","P"]},
  {o:["Aşırı Hassas","Patavatsız","Ürkek","Geveze"],t:["M","K","B","P"]},
  {o:["Şüpheci","Düzensiz","Otoriter","Bunalımlı"],t:["M","P","K","B"]},
  {o:["Tutarsız","İçe Dönük","Hoşgörüsüz","Umursamaz"],t:["P","M","K","B"]},
  {o:["Dağınık","Karamsar","Sızlanan","İnsan Kullanan"],t:["P","M","B","K"]},
  {o:["Uyuşuk","İnatçı","Hava Atan","Kuşkucu"],t:["B","K","P","M"]},
  {o:["Yalnızlığı Seven","Güdmeye Çalışan","Tembel","Gürültücü"],t:["M","K","B","P"]},
  {o:["Ağırkanlı","Şüpheci","Çabuk Sinirlenen","Kafası Dağınık"],t:["B","M","K","P"]},
  {o:["Huzursuz","Aceleci","İntikamcı","Gönülsüz"],t:["P","K","M","B"]},
  {o:["Ödün Veren","Tenkitçi","Kurnaz","Değişken"],t:["B","M","K","P"]},
];

const PD: Record<string,{t:string;c:string;bg:string;e:string;s:string[];w:string[]}> = {
  P:{t:"Popüler Optimist",c:"#D97706",bg:"#FEF3C7",e:"🌟",
    s:["Eğlenceli ve enerjik","Kolay arkadaşlık kurar","İyimser ve coşkulu","İlham verici","Yaratıcı fikirler üretir"],
    w:["Odaklanma süresi kısa olabilir","Dağınık olabilir","Detayları atlayabilir","Abartıya kaçabilir"]},
  K:{t:"Güçlü Kolerik",c:"#DC2626",bg:"#FEE2E2",e:"🔥",
    s:["Doğal lider","Kararlı ve hedef odaklı","Hızlı karar verir","Organize ve üretken","Cesur ve risk alır"],
    w:["Sabırsız olabilir","Otoriter davranabilir","Başkalarının duygularını göz ardı edebilir","İnatçı olabilir"]},
  M:{t:"Mükemmeliyetçi Melankolik",c:"#1E40AF",bg:"#DBEAFE",e:"💎",
    s:["Detaycı ve analitik","Planlı ve düzenli","Derin düşünür","Yaratıcı ve yetenekli","Sadık ve özverili"],
    w:["Aşırı eleştirici olabilir","Karamsarlığa yatkın","Karar vermekte zorlanabilir","Aşırı hassas olabilir"]},
  B:{t:"Barışçıl Soğukkanlı",c:"#059669",bg:"#D1FAE5",e:"🌿",
    s:["Sakin ve dengeli","İyi dinleyici","Uyumlu ve barışçıl","Sabırlı ve hoşgörülü","Güvenilir ve tutarlı"],
    w:["Kararsız olabilir","Motivasyon eksikliği","Değişime dirençli","Pasif kalabilir"]},
};

function PersonalityTestScreen({onClose,onSave}:{onClose:()=>void;onSave:(r:any)=>void}) {
  const [step,setStep]=useState(0);
  const [ans,setAns]=useState<Record<number,number>>({});
  const [done,setDone]=useState(false);
  const [res,setRes]=useState({P:0,K:0,M:0,B:0});

  const calc=()=>{
    const sc={P:0,K:0,M:0,B:0};
    PQ.forEach((q,i)=>{const s=ans[i];if(s!==undefined){const tp=q.t[s] as "P"|"K"|"M"|"B";sc[tp]++;}});
    setRes(sc);setDone(true);
    onSave({popular_optimist:sc.P,strong_choleric:sc.K,perfectionist_melancholic:sc.M,peaceful_phlegmatic:sc.B,answers:ans});
  };

  const tot=res.P+res.K+res.M+res.B||1;
  const dom=(Object.entries(res).sort((a,b)=>b[1]-a[1])[0]||["P"])[0];

  if(done){
    const pP=res.P/tot*100,pK=res.K/tot*100,pM=res.M/tot*100;
    return(
      <div style={{position:"fixed",top:0,left:0,right:0,bottom:0,background:"#fff",zIndex:200,overflowY:"auto",padding:16}}>
        <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:20}}>
          <h2 style={{margin:0,fontSize:20,fontWeight:800}}>Kişilik Analiz Sonucun</h2>
          <button onClick={onClose} style={{background:"none",border:"none",fontSize:24,cursor:"pointer",color:"#64748B"}}>✕</button>
        </div>
        <div style={{textAlign:"center",marginBottom:20}}>
          <div style={{fontSize:48}}>{PD[dom].e}</div>
          <div style={{fontSize:20,fontWeight:800,color:PD[dom].c,marginTop:8}}>{PD[dom].t}</div>
          <div style={{fontSize:13,color:"#64748B",marginTop:4}}>Baskın kişilik tipin</div>
        </div>
        <div style={{display:"flex",justifyContent:"center",marginBottom:24}}>
          <div style={{width:180,height:180,borderRadius:"50%",background:`conic-gradient(#D97706 0% ${pP}%, #DC2626 ${pP}% ${pP+pK}%, #1E40AF ${pP+pK}% ${pP+pK+pM}%, #059669 ${pP+pK+pM}% 100%)`,boxShadow:"0 2px 8px rgba(0,0,0,0.1)"}}/>
        </div>
        <div style={{display:"flex",justifyContent:"center",gap:8,flexWrap:"wrap" as const,marginBottom:20}}>
          {(["P","K","M","B"] as const).map(k=>(
            <span key={k} style={{fontSize:11,padding:"4px 8px",borderRadius:6,background:PD[k].bg,color:PD[k].c,fontWeight:700}}>{PD[k].e} {Math.round(res[k]/tot*100)}%</span>
          ))}
        </div>
        {(["P","K","M","B"] as const).map(k=>{
          const d=PD[k];const pct=Math.round(res[k]/tot*100);
          return(<div key={k} style={{marginBottom:14}}>
            <div style={{display:"flex",justifyContent:"space-between",marginBottom:4}}>
              <span style={{fontSize:13,fontWeight:700,color:d.c}}>{d.e} {d.t}</span>
              <span style={{fontSize:13,fontWeight:800,color:d.c}}>{res[k]}/{tot} (%{pct})</span>
            </div>
            <div style={{height:8,borderRadius:4,background:"#E2E8F0",overflow:"hidden"}}>
              <div style={{height:"100%",borderRadius:4,background:d.c,width:pct+"%",transition:"width 0.5s"}}/>
            </div>
          </div>);
        })}
        <div style={{background:PD[dom].bg,borderRadius:16,padding:20,marginTop:16}}>
          <h3 style={{margin:"0 0 10px",fontSize:16,fontWeight:800,color:PD[dom].c}}>Güçlü Yönlerin</h3>
          {PD[dom].s.map((s,i)=>(<div key={i} style={{fontSize:13,color:"#0F172A",padding:"3px 0"}}>✅ {s}</div>))}
          <h3 style={{margin:"14px 0 10px",fontSize:16,fontWeight:800,color:PD[dom].c}}>Gelişim Alanların</h3>
          {PD[dom].w.map((w,i)=>(<div key={i} style={{fontSize:13,color:"#0F172A",padding:"3px 0"}}>💡 {w}</div>))}
        </div>
        <div style={{fontSize:11,color:"#94A3B8",textAlign:"center",marginTop:16}}>Kaynak: Florence Littauer - Kişiliğinizi Tanıyın</div>
        <button onClick={onClose} style={{width:"100%",padding:"14px",borderRadius:12,background:"#0E7490",color:"#fff",border:"none",fontSize:15,fontWeight:700,cursor:"pointer",marginTop:12}}>Kapat</button>
      </div>
    );
  }

  const cq=PQ[step];const ac=Object.keys(ans).length;
  return(
    <div style={{position:"fixed",top:0,left:0,right:0,bottom:0,background:"#fff",zIndex:200,overflowY:"auto",display:"flex",flexDirection:"column"}}>
      <div style={{padding:"14px 16px",borderBottom:"1px solid #E2E8F0",display:"flex",justifyContent:"space-between",alignItems:"center"}}>
        <button onClick={onClose} style={{background:"none",border:"none",fontSize:14,cursor:"pointer",color:"#64748B",fontWeight:600}}>✕ Kapat</button>
        <span style={{fontSize:13,fontWeight:700,color:"#0E7490"}}>{step+1} / 40</span>
      </div>
      <div style={{height:4,background:"#E2E8F0"}}><div style={{height:"100%",background:"#0E7490",width:((step+1)/40*100)+"%",transition:"width 0.3s"}}/></div>
      <div style={{flex:1,display:"flex",flexDirection:"column",justifyContent:"center",padding:24}}>
        <div style={{fontSize:14,color:"#64748B",marginBottom:8,fontWeight:600}}>Soru {step+1}</div>
        <div style={{fontSize:16,fontWeight:700,color:"#0F172A",marginBottom:24}}>Aşağıdakilerden hangisi sizi en iyi tanımlar?</div>
        <div style={{display:"flex",flexDirection:"column",gap:10}}>
          {cq.o.map((opt,i)=>{const sel=ans[step]===i;return(
            <div key={i} onClick={()=>setAns(p=>({...p,[step]:i}))} style={{padding:"14px 16px",borderRadius:12,border:sel?"2px solid #0E7490":"1.5px solid #E2E8F0",background:sel?"#F0F9FF":"#fff",cursor:"pointer",fontSize:15,fontWeight:sel?700:500,color:sel?"#0E7490":"#0F172A",transition:"all 0.2s"}}>{opt}</div>
          );})}
        </div>
      </div>
      <div style={{padding:"16px",borderTop:"1px solid #E2E8F0",display:"flex",gap:10}}>
        <button onClick={()=>setStep(Math.max(0,step-1))} disabled={step===0} style={{flex:1,padding:"12px",borderRadius:12,border:"1.5px solid #E2E8F0",background:"#fff",fontSize:14,fontWeight:600,cursor:step===0?"default":"pointer",color:step===0?"#CBD5E1":"#64748B"}}>Geri</button>
        {step<39?(
          <button onClick={()=>{if(ans[step]!==undefined)setStep(step+1);}} style={{flex:1,padding:"12px",borderRadius:12,border:"none",background:ans[step]!==undefined?"#0E7490":"#CBD5E1",color:"#fff",fontSize:14,fontWeight:700,cursor:ans[step]!==undefined?"pointer":"default"}}>İleri</button>
        ):(
          <button onClick={()=>{if(ac>=40)calc();}} style={{flex:1,padding:"12px",borderRadius:12,border:"none",background:ac>=40?"#059669":"#CBD5E1",color:"#fff",fontSize:14,fontWeight:700,cursor:ac>=40?"pointer":"default"}}>Testi Bitir</button>
        )}
      </div>
    </div>
  );
}

// ==================== TOAST =='''

if old_toast in content:
    content = content.replace(old_toast, COMP)
    print("  OK 8. Component eklendi")

# SAVE
open(filepath, 'w').write(content)
print("")
print("KISILIK TESTI TAMAMLANDI!")
print("  - 40 soru (dogru siralamayla)")
print("  - Pasta grafik")
print("  - Guclu yonler / gelisim alanlari")
print("  - Supabase kayit")
print("")
print("Simdi: npm run build")
