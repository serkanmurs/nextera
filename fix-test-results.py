filepath = 'src/app/page.tsx'
content = open(filepath, 'r').read()

print("Kisilik testi fix basliyor...")

# 1. PersonalityTestScreen'e initialResults prop ekle
# Boylece sonuc varsa direkt sonucu gosterir
old_func = 'function PersonalityTestScreen({onClose,onSave}:{onClose:()=>void;onSave:(r:any)=>void}) {'
new_func = 'function PersonalityTestScreen({onClose,onSave,initialResults}:{onClose:()=>void;onSave:(r:any)=>void;initialResults?:any}) {'

if old_func in content:
    content = content.replace(old_func, new_func)
    print("  OK 1. initialResults prop eklendi")

# 2. State'leri initialResults'a gore baslat
old_state = '''  const [step,setStep]=useState(0);
  const [ans,setAns]=useState<Record<number,number>>({});
  const [done,setDone]=useState(false);
  const [res,setRes]=useState({P:0,K:0,M:0,B:0});'''

new_state = '''  const [step,setStep]=useState(0);
  const [ans,setAns]=useState<Record<number,number>>({});
  const [done,setDone]=useState(!!initialResults);
  const [res,setRes]=useState(initialResults ? {P:initialResults.popular_optimist||0,K:initialResults.strong_choleric||0,M:initialResults.perfectionist_melancholic||0,B:initialResults.peaceful_phlegmatic||0} : {P:0,K:0,M:0,B:0});
  const [showRetake,setShowRetake]=useState(false);'''

if old_state in content:
    content = content.replace(old_state, new_state)
    print("  OK 2. State guncellendi")

# 3. Sonuc ekranina "Testi Tekrarla" butonu ekle - Kapat butonundan once
# Ve PDF butonunun dogru calismasini sagla
old_kapat = '''<button onClick={onClose} style={{width:"100%",padding:"14px",borderRadius:12,background:"#0E7490",color:"#fff",border:"none",fontSize:15,fontWeight:700,cursor:"pointer",marginTop:12}}>Kapat</button>'''

# Eger PDF butonu zaten eklendiyse farkli marker ara
old_kapat2 = '''<button onClick={onClose} style={{width:"100%",padding:"14px",borderRadius:12,background:"#0E7490",color:"#fff",border:"none",fontSize:15,fontWeight:700,cursor:"pointer",marginTop:8}}>Kapat</button>'''

# Yeni butonlar: Testi Tekrarla + Kapat
new_buttons = '''<button onClick={()=>{setDone(false);setAns({});setStep(0);setRes({P:0,K:0,M:0,B:0});}} style={{width:"100%",padding:"14px",borderRadius:12,background:"#F97316",color:"#fff",border:"none",fontSize:15,fontWeight:700,cursor:"pointer",marginTop:12}}>🔄 Testi Tekrarla</button>
        <button onClick={onClose} style={{width:"100%",padding:"14px",borderRadius:12,border:"1.5px solid #E2E8F0",background:"#fff",color:"#64748B",fontSize:15,fontWeight:700,cursor:"pointer",marginTop:8}}>Kapat</button>'''

if old_kapat2 in content:
    content = content.replace(old_kapat2, new_buttons)
    print("  OK 3a. Butonlar guncellendi (v2)")
elif old_kapat in content:
    content = content.replace(old_kapat, new_buttons)
    print("  OK 3b. Butonlar guncellendi (v1)")

# 4. Kart tiklamasini guncelle - sonuc varsa sonucu goster
old_card_click = 'onClick={() => setShowPersonalityTest(true)}'
# Bu iki kez olabilir, sadece ilk tiklamada sonucu gosterecek
# Aslinda showPersonalityTest zaten true yapiyoruz ve 
# PersonalityTestScreen initialResults ile acilacak
# Yani kart tiklamasi dogru, sadece initialResults gecmemiz lazim

# 5. PersonalityTestScreen'e initialResults gec
old_screen_call = '<PersonalityTestScreen onClose={() => setShowPersonalityTest(false)} onSave={(r: any) => { onSaveTest(r); setShowPersonalityTest(false); }} />'
new_screen_call = '<PersonalityTestScreen onClose={() => setShowPersonalityTest(false)} onSave={(r: any) => { onSaveTest(r); setShowPersonalityTest(false); }} initialResults={personalityTest} />'

if old_screen_call in content:
    content = content.replace(old_screen_call, new_screen_call)
    print("  OK 5. initialResults prop gecildi")

# 6. PDF import kontrolu - zaten eklenmis mi?
if 'import jsPDF' not in content:
    old_imp = 'import { supabase } from "@/lib/supabase";'
    new_imp = '''import { supabase } from "@/lib/supabase";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";'''
    if old_imp in content:
        content = content.replace(old_imp, new_imp)
        print("  OK 6. jsPDF import eklendi")
else:
    print("  OK 6. jsPDF import zaten var")

# 7. PDF indirme butonu - Kaynak satirindan sonra ekle
old_kaynak = '''<div style={{fontSize:11,color:"#94A3B8",textAlign:"center",marginTop:16}}>Kaynak: Florence Littauer'''

# PDF butonu zaten var mi kontrol et
if 'PDF Rapor' not in content:
    new_kaynak = '''<div style={{fontSize:11,color:"#94A3B8",textAlign:"center",marginTop:16}}>Kaynak: Florence Littauer'''
    
    # Kaynak satirindan sonraki </div> dan sonra PDF butonunu ekle
    kaynak_idx = content.find(old_kaynak)
    if kaynak_idx > -1:
        # Kaynak div'inin sonunu bul
        end_div = content.find('</div>', kaynak_idx + len(old_kaynak))
        if end_div > -1:
            insert_point = end_div + 6
            pdf_button = '''
        <button onClick={async()=>{
          try{
            const pdf=new jsPDF("p","mm","a4");
            const w=pdf.internal.pageSize.getWidth();
            const margin=20;
            let y=20;
            
            // Header
            pdf.setFontSize(24);pdf.setTextColor(14,116,144);pdf.text("NextERA",margin,y);
            pdf.setFontSize(10);pdf.setTextColor(100,116,139);pdf.text("Kisilik Analiz Raporu",margin,y+8);
            pdf.text(new Date().toLocaleDateString("tr-TR",{day:"numeric",month:"long",year:"numeric"}),w-margin-40,y+8);
            pdf.setDrawColor(14,116,144);pdf.setLineWidth(0.5);pdf.line(margin,y+12,w-margin,y+12);
            y+=24;
            
            // Baskin tip
            pdf.setFontSize(18);pdf.setTextColor(15,23,42);pdf.text("Baskin Kisilik Tipin:",margin,y);y+=8;
            const domTitle=PD[dom].t;
            pdf.setFontSize(16);pdf.setTextColor(PD[dom].c==="#D97706"?217:PD[dom].c==="#DC2626"?220:PD[dom].c==="#1E40AF"?30:5,PD[dom].c==="#D97706"?119:PD[dom].c==="#DC2626"?38:PD[dom].c==="#1E40AF"?64:150,PD[dom].c==="#D97706"?6:PD[dom].c==="#DC2626"?38:PD[dom].c==="#1E40AF"?175:105);
            pdf.text(domTitle,margin,y);y+=14;
            
            // Skorlar
            pdf.setFontSize(12);pdf.setTextColor(15,23,42);
            const types=[{k:"P",n:"Populer Optimist"},{k:"K",n:"Guclu Kolerik"},{k:"M",n:"Mukemmeliyetci Melankolik"},{k:"B",n:"Bariscil Sogukkanli"}];
            types.forEach(tp=>{
              const v=res[tp.k as "P"|"K"|"M"|"B"];
              const pct=Math.round(v/tot*100);
              pdf.setTextColor(100,116,139);pdf.text(tp.n+":",margin,y);
              pdf.setTextColor(15,23,42);pdf.text(v+" puan (%"+pct+")",margin+80,y);
              // Bar
              pdf.setFillColor(226,232,240);pdf.rect(margin,y+2,w-2*margin,4,"F");
              const barColor=tp.k==="P"?[217,119,6]:tp.k==="K"?[220,38,38]:tp.k==="M"?[30,64,175]:[5,150,105];
              pdf.setFillColor(barColor[0],barColor[1],barColor[2]);pdf.rect(margin,y+2,(w-2*margin)*pct/100,4,"F");
              y+=12;
            });
            y+=8;
            
            // Guclu yonler
            pdf.setFontSize(14);pdf.setTextColor(14,116,144);pdf.text("Guclu Yonlerin",margin,y);y+=8;
            pdf.setFontSize(11);pdf.setTextColor(15,23,42);
            PD[dom].s.forEach(s=>{pdf.text("  - "+s,margin,y);y+=6;});
            y+=6;
            
            // Gelisim alanlari
            pdf.setFontSize(14);pdf.setTextColor(14,116,144);pdf.text("Gelisim Alanlarin",margin,y);y+=8;
            pdf.setFontSize(11);pdf.setTextColor(15,23,42);
            PD[dom].w.forEach(w2=>{pdf.text("  - "+w2,margin,y);y+=6;});
            y+=10;
            
            // Footer
            pdf.setFontSize(9);pdf.setTextColor(148,163,184);
            pdf.text("Kaynak: Florence Littauer - Kisiliginizi Taniyin | NextERA Danismanlik Platformu",margin,y);
            
            pdf.save("NextERA_Kisilik_Raporu.pdf");
          }catch(e){console.error("PDF error:",e);alert("PDF olusturulurken hata olustu");}
        }} style={{width:"100%",padding:"14px",borderRadius:12,background:"#155E75",color:"#fff",border:"none",fontSize:15,fontWeight:700,cursor:"pointer",marginTop:12}}>PDF Rapor Indir</button>'''
            
            content = content[:insert_point] + pdf_button + content[insert_point:]
            print("  OK 7. PDF butonu eklendi")
    else:
        print("  SKIP 7. Kaynak satiri bulunamadi")
else:
    print("  OK 7. PDF butonu zaten var")

# 8. Eski PDF div varsa kaldir (html2canvas yontemi)
if 'id="pdfReport"' in content:
    start = content.find('{/* Hidden PDF report div */}')
    if start > -1:
        end = content.find("</div>\n\n        <button", start)
        if end > -1:
            content = content[:start] + content[end+6:]
            print("  OK 8. Eski PDF div kaldirildi")

# SAVE
open(filepath, 'w').write(content)
print("")
print("FIX TAMAMLANDI!")
print("  - Sonuc varsa direkt gosterir")
print("  - Testi Tekrarla butonu")  
print("  - PDF Rapor Indir butonu")
print("")
print("Simdi: npm run build")
