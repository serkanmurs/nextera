filepath = 'src/app/page.tsx'
content = open(filepath, 'r').read()

print("PDF sistemi degistiriliyor (window.print yontemi)...")

# Mevcut PDF butonunu bul ve degistir
# PDF butonun baslangici
old_pdf_start = '<button onClick={async()=>{'
old_pdf_marker = 'PDF Rapor'

# Tum PDF butonunu bul
pdf_idx = content.find('PDF Rapor İndir</button>')
if pdf_idx == -1:
    pdf_idx = content.find('PDF Rapor')

if pdf_idx > -1:
    # Butonun basini bul
    btn_start = content.rfind('<button', 0, pdf_idx)
    # Butonun sonunu bul
    btn_end = content.find('</button>', pdf_idx) + len('</button>')
    
    if btn_start > -1 and btn_end > btn_start:
        # Yeni PDF butonu - window.print() ile
        new_pdf_btn = '''<button onClick={()=>{
          const printWin=window.open("","_blank");
          if(!printWin)return;
          const pP2=Math.round(res.P/tot*100);
          const pK2=Math.round(res.K/tot*100);
          const pM2=Math.round(res.M/tot*100);
          const pB2=Math.round(res.B/tot*100);
          const dInfo=PD[dom];
          printWin.document.write(\`<!DOCTYPE html><html><head><meta charset="utf-8"><title>NextERA Kişilik Raporu</title>
          <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
            *{margin:0;padding:0;box-sizing:border-box}
            body{font-family:'Inter',sans-serif;padding:40px;color:#0F172A;max-width:800px;margin:0 auto}
            @media print{body{padding:20px}@page{margin:15mm}}
            .header{display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #0E7490;padding-bottom:16px;margin-bottom:24px}
            .logo{font-size:28px;font-weight:800;color:#0E7490}
            .logo span{color:#F97316}
            .subtitle{font-size:12px;color:#64748B;margin-top:2px}
            .client-info{text-align:right;font-size:12px;color:#64748B}
            .client-name{font-size:14px;font-weight:700;color:#0F172A}
            .dominant{text-align:center;margin:24px 0}
            .dominant-emoji{font-size:48px}
            .dominant-title{font-size:22px;font-weight:800;margin-top:8px}
            .dominant-sub{font-size:13px;color:#64748B;margin-top:4px}
            .chart-container{display:flex;justify-content:center;margin:20px 0}
            .pie{width:180px;height:180px;border-radius:50%;box-shadow:0 2px 8px rgba(0,0,0,0.1)}
            .legend{display:flex;justify-content:center;gap:16px;margin:16px 0;flex-wrap:wrap}
            .legend-item{font-size:12px;font-weight:700;display:flex;align-items:center;gap:4px}
            .legend-dot{width:12px;height:12px;border-radius:3px}
            .bar-section{margin:20px 0}
            .bar-row{margin-bottom:12px}
            .bar-label{display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px}
            .bar-name{font-weight:700}
            .bar-track{height:8px;border-radius:4px;background:#E2E8F0;overflow:hidden}
            .bar-fill{height:100%;border-radius:4px}
            .section{margin:20px 0;padding:20px;border-radius:12px}
            .section h3{font-size:16px;font-weight:800;margin-bottom:10px}
            .section p{font-size:13px;line-height:1.7;margin-bottom:8px}
            .list-item{font-size:13px;padding:3px 0}
            .footer{margin-top:24px;padding-top:16px;border-top:1px solid #E2E8F0;font-size:10px;color:#94A3B8;text-align:center}
            .no-print{margin-top:20px;text-align:center}
            @media print{.no-print{display:none}}
          </style></head><body>
          <div class="header">
            <div><div class="logo">Next<span>ERA</span></div><div class="subtitle">Kişilik Analiz Raporu</div></div>
            <div class="client-info"><div class="client-name">\${userName || ""}</div><div>\${new Date().toLocaleDateString("tr-TR",{day:"numeric",month:"long",year:"numeric"})}</div></div>
          </div>
          <div class="dominant">
            <div class="dominant-emoji">\${dInfo.e}</div>
            <div class="dominant-title" style="color:\${dInfo.c}">\${dInfo.t}</div>
            <div class="dominant-sub">Baskın kişilik tipin</div>
          </div>
          <div class="chart-container">
            <div class="pie" style="background:conic-gradient(#D97706 0% \${pP2}%, #DC2626 \${pP2}% \${pP2+pK2}%, #1E40AF \${pP2+pK2}% \${pP2+pK2+pM2}%, #059669 \${pP2+pK2+pM2}% 100%)"></div>
          </div>
          <div class="legend">
            <div class="legend-item"><div class="legend-dot" style="background:#D97706"></div>Optimist %\${pP2}</div>
            <div class="legend-item"><div class="legend-dot" style="background:#DC2626"></div>Kolerik %\${pK2}</div>
            <div class="legend-item"><div class="legend-dot" style="background:#1E40AF"></div>Melankolik %\${pM2}</div>
            <div class="legend-item"><div class="legend-dot" style="background:#059669"></div>Soğukkanlı %\${pB2}</div>
          </div>
          <div class="bar-section">
            \${[{k:"P",n:"Popüler Optimist",c:"#D97706"},{k:"K",n:"Güçlü Kolerik",c:"#DC2626"},{k:"M",n:"Mükemmeliyetçi Melankolik",c:"#1E40AF"},{k:"B",n:"Barışçıl Soğukkanlı",c:"#059669"}].map(t=>{
              const v2=res[t.k as "P"|"K"|"M"|"B"];const p2=Math.round(v2/tot*100);
              return '<div class="bar-row"><div class="bar-label"><span class="bar-name" style="color:'+t.c+'">'+t.n+'</span><span style="color:'+t.c+'">'+v2+'/'+tot+' (%'+p2+')</span></div><div class="bar-track"><div class="bar-fill" style="background:'+t.c+';width:'+p2+'%"></div></div></div>';
            }).join("")}
          </div>
          <div class="section" style="background:\${dInfo.bg}">
            <h3 style="color:\${dInfo.c}">Güçlü Yönlerin</h3>
            \${dInfo.s.map((s2: string)=>'<div class="list-item">✅ '+s2+'</div>').join("")}
            <h3 style="color:\${dInfo.c};margin-top:14px">Gelişim Alanların</h3>
            \${dInfo.w.map((w2: string)=>'<div class="list-item">💡 '+w2+'</div>').join("")}
          </div>
          <div class="section" style="background:#F8FAFC;border:1px solid #E2E8F0">
            <h3>Kişilik Profilin Hakkında</h3>
            \${dInfo.summary.split("\\n\\n").map((p2: string)=>'<p>'+p2+'</p>').join("")}
          </div>
          <div class="footer">Kaynak: Florence Littauer - Kişiliğinizi Tanıyın (Personality Plus) | NextERA Danışmanlık Platformu</div>
          <div class="no-print"><button onclick="window.print()" style="padding:12px 32px;border-radius:10px;background:#0E7490;color:#fff;border:none;font-size:15px;font-weight:700;cursor:pointer">Yazdır / PDF Kaydet</button></div>
          </body></html>\`);
          printWin.document.close();
        }} style={{width:"100%",padding:"14px",borderRadius:12,background:"#155E75",color:"#fff",border:"none",fontSize:15,fontWeight:700,cursor:"pointer",marginTop:12}}>📄 PDF Rapor İndir</button>'''
        
        content = content[:btn_start] + new_pdf_btn + content[btn_end:]
        print("  OK 1. PDF butonu window.print ile degistirildi")
    else:
        print("  SKIP 1. Buton siniri bulunamadi")
else:
    print("  SKIP 1. PDF butonu bulunamadi")

# 2. userName degiskenini ekle - PersonalityTestScreen'e user prop ekle
# Simdilik basit yapalim: window'dan alalim veya bos birak
# Aslinda user bilgisi ClientHome'dan gecilebilir

# PersonalityTestScreen props'a user ekle
old_screen_props = 'function PersonalityTestScreen({onClose,onSave,initialResults}:{onClose:()=>void;onSave:(r:any)=>void;initialResults?:any}) {'
new_screen_props = 'function PersonalityTestScreen({onClose,onSave,initialResults,userName}:{onClose:()=>void;onSave:(r:any)=>void;initialResults?:any;userName?:string}) {'

if old_screen_props in content:
    content = content.replace(old_screen_props, new_screen_props)
    print("  OK 2a. userName prop eklendi")

# Screen renderinda userName gec
old_screen_render = '<PersonalityTestScreen onClose={() => setShowPersonalityTest(false)}'
new_screen_render = '<PersonalityTestScreen onClose={() => setShowPersonalityTest(false)} userName={user.name}'

if old_screen_render in content:
    content = content.replace(old_screen_render, new_screen_render, 1)
    print("  OK 2b. userName gecildi")

# SAVE
open(filepath, 'w').write(content)
print("")
print("PDF SISTEMI GUNCELLENDI!")
print("  - Turkce karakter destegi (tam)")
print("  - Pasta grafik PDF'de gorunur")
print("  - NextERA logosu")
print("  - Danisan adi + tarih")
print("  - Profesyonel tasarim")
print("")
print("Simdi: npm run build")
