filepath = 'src/app/page.tsx'
content = open(filepath, 'r').read()

print("PDF Rapor ozellligi ekleniyor...")

# 1. Import ekle
old_import = 'import { supabase } from "@/lib/supabase";'
new_import = '''import { supabase } from "@/lib/supabase";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";'''

if old_import in content:
    content = content.replace(old_import, new_import)
    print("  OK 1. Import eklendi")

# 2. Test sonuc ekranina PDF butonu ve rapor divi ekle
# "Kapat" butonundan once PDF indir butonu ekle
old_close_btn = '''<button onClick={onClose} style={{width:"100%",padding:"14px",borderRadius:12,background:"#0E7490",color:"#fff",border:"none",fontSize:15,fontWeight:700,cursor:"pointer",marginTop:12}}>Kapat</button>'''

new_close_btn = '''<button onClick={async ()=>{
          const el=document.getElementById("pdfReport");
          if(!el)return;
          el.style.display="block";
          try{
            const canvas=await html2canvas(el,{scale:2,useCORS:true,backgroundColor:"#fff"});
            const imgData=canvas.toDataURL("image/png");
            const pdf=new jsPDF("p","mm","a4");
            const w=pdf.internal.pageSize.getWidth();
            const h=(canvas.height*w)/canvas.width;
            pdf.addImage(imgData,"PNG",0,0,w,h);
            pdf.save("NextERA_Kisilik_Raporu.pdf");
          }catch(e){console.error(e);}
          el.style.display="none";
        }} style={{width:"100%",padding:"14px",borderRadius:12,background:"#155E75",color:"#fff",border:"none",fontSize:15,fontWeight:700,cursor:"pointer",marginTop:12}}>📄 PDF Rapor İndir</button>

        {/* Hidden PDF report div */}
        <div id="pdfReport" style={{display:"none",position:"absolute",left:"-9999px",top:0,width:794,background:"#fff",padding:40,fontFamily:"Inter,sans-serif"}}>
          <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",borderBottom:"2px solid #0E7490",paddingBottom:16,marginBottom:24}}>
            <div>
              <div style={{fontSize:28,fontWeight:800,color:"#0E7490"}}>Next<span style={{color:"#F97316"}}>ERA</span></div>
              <div style={{fontSize:12,color:"#64748B"}}>Kişilik Analiz Raporu</div>
            </div>
            <div style={{textAlign:"right"}}>
              <div style={{fontSize:12,color:"#64748B"}}>{new Date().toLocaleDateString("tr-TR",{day:"numeric",month:"long",year:"numeric"})}</div>
            </div>
          </div>

          <div style={{marginBottom:24}}>
            <div style={{fontSize:18,fontWeight:800,color:"#0F172A",marginBottom:4}}>Kişilik Profil Raporu</div>
            <div style={{fontSize:13,color:"#64748B"}}>Florence Littauer Kişilik Analizi Sonuçları</div>
          </div>

          <div style={{textAlign:"center",marginBottom:24}}>
            <div style={{fontSize:36,marginBottom:8}}>{PD[dom].e}</div>
            <div style={{fontSize:22,fontWeight:800,color:PD[dom].c}}>Baskın Tip: {PD[dom].t}</div>
          </div>

          <div style={{display:"flex",justifyContent:"center",marginBottom:24}}>
            <div style={{width:160,height:160,borderRadius:"50%",background:"conic-gradient(#D97706 0% "+String(pP)+"%, #DC2626 "+String(pP)+"% "+String(pP+pK)+"%, #1E40AF "+String(pP+pK)+"% "+String(pP+pK+pM)+"%, #059669 "+String(pP+pK+pM)+"% 100%)"}}/>
          </div>

          <div style={{display:"flex",justifyContent:"center",gap:16,marginBottom:24}}>
            {(["P","K","M","B"] as const).map(k=>(<div key={k} style={{textAlign:"center"}}><div style={{fontSize:18,fontWeight:800,color:PD[k].c}}>{Math.round(res[k]/tot*100)}%</div><div style={{fontSize:11,color:"#64748B"}}>{PD[k].t}</div></div>))}
          </div>

          {(["P","K","M","B"] as const).map(k=>{const d=PD[k];const pct=Math.round(res[k]/tot*100);return(
            <div key={k} style={{marginBottom:12}}>
              <div style={{display:"flex",justifyContent:"space-between",marginBottom:4}}>
                <span style={{fontSize:12,fontWeight:700,color:d.c}}>{d.t}</span>
                <span style={{fontSize:12,fontWeight:700,color:d.c}}>{res[k]} puan (%{pct})</span>
              </div>
              <div style={{height:10,borderRadius:5,background:"#E2E8F0",overflow:"hidden"}}>
                <div style={{height:"100%",borderRadius:5,background:d.c,width:pct+"%"}}/>
              </div>
            </div>
          );})}

          <div style={{marginTop:24,padding:20,background:PD[dom].bg,borderRadius:12}}>
            <div style={{fontSize:14,fontWeight:800,color:PD[dom].c,marginBottom:8}}>Güçlü Yönleriniz</div>
            {PD[dom].s.map((s,i)=>(<div key={i} style={{fontSize:12,color:"#0F172A",padding:"2px 0"}}>• {s}</div>))}
            <div style={{fontSize:14,fontWeight:800,color:PD[dom].c,marginTop:12,marginBottom:8}}>Gelişim Alanlarınız</div>
            {PD[dom].w.map((w,i)=>(<div key={i} style={{fontSize:12,color:"#0F172A",padding:"2px 0"}}>• {w}</div>))}
          </div>

          <div style={{marginTop:24,paddingTop:16,borderTop:"1px solid #E2E8F0",fontSize:10,color:"#94A3B8",textAlign:"center"}}>
            Kaynak: Florence Littauer - Kişiliğinizi Tanıyın (Personality Plus) | NextERA Danışmanlık Platformu
          </div>
        </div>

        <button onClick={onClose} style={{width:"100%",padding:"14px",borderRadius:12,background:"#0E7490",color:"#fff",border:"none",fontSize:15,fontWeight:700,cursor:"pointer",marginTop:8}}>Kapat</button>'''

if old_close_btn in content:
    content = content.replace(old_close_btn, new_close_btn)
    print("  OK 2. PDF butonu ve rapor divi eklendi")
else:
    print("  SKIP 2. Kapat butonu bulunamadi")

# SAVE
open(filepath, 'w').write(content)
print("")
print("PDF RAPOR TAMAMLANDI!")
print("Simdi: npm run build")
