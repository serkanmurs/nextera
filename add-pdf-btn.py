filepath = 'src/app/page.tsx'
content = open(filepath, 'r').read()

print("PDF butonu ekleniyor...")

# Testi Tekrarla butonundan ONCE PDF butonu ekle
old_retake = '''<button onClick={()=>{setDone(false);setAns({});setStep(0);setRes({P:0,K:0,M:0,B:0});}} style={{width:"100%",padding:"14px",borderRadius:12,background:"#F97316",color:"#fff",border:"none",fontSize:15,fontWeight:700,cursor:"pointer",marginTop:12}}>🔄 Testi Tekrarla</button>'''

pdf_btn = '''<button onClick={async()=>{
          try{
            const {default:jsPDF}=await import("jspdf");
            const pdf=new jsPDF("p","mm","a4");
            const w=pdf.internal.pageSize.getWidth();
            const m=20;
            let y=20;
            
            pdf.setFontSize(24);pdf.setTextColor(14,116,144);pdf.text("NextERA",m,y);
            pdf.setFontSize(10);pdf.setTextColor(100,116,139);pdf.text("Kisilik Analiz Raporu",m,y+8);
            pdf.text(new Date().toLocaleDateString("tr-TR",{day:"numeric",month:"long",year:"numeric"}),w-m-40,y+8);
            pdf.setDrawColor(14,116,144);pdf.setLineWidth(0.5);pdf.line(m,y+12,w-m,y+12);
            y+=24;
            
            pdf.setFontSize(16);pdf.setTextColor(15,23,42);pdf.text("Baskin Kisilik Tipin:",m,y);y+=8;
            const dInfo=PD[dom];
            const cRGB=dom==="P"?[217,119,6]:dom==="K"?[220,38,38]:dom==="M"?[30,64,175]:[5,150,105];
            pdf.setFontSize(18);pdf.setTextColor(cRGB[0],cRGB[1],cRGB[2]);pdf.text(dInfo.t,m,y);y+=12;
            
            const types2=[{k:"P" as const,n:"Populer Optimist"},{k:"K" as const,n:"Guclu Kolerik"},{k:"M" as const,n:"Mukemmeliyetci Melankolik"},{k:"B" as const,n:"Bariscil Sogukkanli"}];
            pdf.setFontSize(11);
            types2.forEach(tp=>{
              const v=res[tp.k];const pct=Math.round(v/tot*100);
              pdf.setTextColor(100,116,139);pdf.text(tp.n+":",m,y);
              pdf.setTextColor(15,23,42);pdf.text(v+" puan (%"+pct+")",m+75,y);
              pdf.setFillColor(226,232,240);pdf.rect(m,y+2,w-2*m,4,"F");
              const bc=tp.k==="P"?[217,119,6]:tp.k==="K"?[220,38,38]:tp.k==="M"?[30,64,175]:[5,150,105];
              pdf.setFillColor(bc[0],bc[1],bc[2]);pdf.rect(m,y+2,(w-2*m)*pct/100,4,"F");
              y+=12;
            });
            y+=6;
            
            pdf.setFontSize(13);pdf.setTextColor(cRGB[0],cRGB[1],cRGB[2]);pdf.text("Guclu Yonlerin",m,y);y+=7;
            pdf.setFontSize(10);pdf.setTextColor(15,23,42);
            dInfo.s.forEach((s: string)=>{pdf.text("  - "+s,m,y);y+=5;});
            y+=4;
            
            pdf.setFontSize(13);pdf.setTextColor(cRGB[0],cRGB[1],cRGB[2]);pdf.text("Gelisim Alanlarin",m,y);y+=7;
            pdf.setFontSize(10);pdf.setTextColor(15,23,42);
            dInfo.w.forEach((w2: string)=>{pdf.text("  - "+w2,m,y);y+=5;});
            y+=8;
            
            if(y>240){pdf.addPage();y=20;}
            pdf.setFontSize(13);pdf.setTextColor(14,116,144);pdf.text("Kisilik Profilin Hakkinda",m,y);y+=8;
            pdf.setFontSize(10);pdf.setTextColor(15,23,42);
            const st=dInfo.summary.replace(/\\n\\n/g," ");
            const sL=pdf.splitTextToSize(st,w-2*m);
            sL.forEach((ln: string)=>{if(y>275){pdf.addPage();y=20;}pdf.text(ln,m,y);y+=5;});
            y+=8;
            
            pdf.setFontSize(8);pdf.setTextColor(148,163,184);
            pdf.text("Kaynak: Florence Littauer - Kisiliginizi Taniyin | NextERA Danismanlik Platformu",m,y);
            
            pdf.save("NextERA_Kisilik_Raporu.pdf");
          }catch(e){console.error("PDF:",e);alert("PDF olusturulamadi");}
        }} style={{width:"100%",padding:"14px",borderRadius:12,background:"#155E75",color:"#fff",border:"none",fontSize:15,fontWeight:700,cursor:"pointer",marginTop:12}}>📄 PDF Rapor İndir</button>
        ''' + old_retake

if old_retake in content:
    content = content.replace(old_retake, pdf_btn)
    print("  OK - PDF butonu eklendi")
else:
    print("  SKIP - Testi Tekrarla butonu bulunamadi")

open(filepath, 'w').write(content)
print("Kaydedildi. Simdi: npm run build")
