filepath = 'src/app/page.tsx'
content = open(filepath, 'r').read()

print("PDF butonu ekleniyor...")

old_retake = '<button onClick={()=>{setDone(false);setAns({});setStep(0);setRes({P:0,K:0,M:0,B:0});}} style={{width:"100%",padding:"14px",borderRadius:12,background:"#F97316",color:"#fff",border:"none",fontSize:15,fontWeight:700,cursor:"pointer",marginTop:12}}>'

if old_retake in content:
    pdf_btn = '<button onClick={()=>{\n'
    pdf_btn += '          const dI=PD[dom];\n'
    pdf_btn += '          const pP2=Math.round(res.P/tot*100),pK2=Math.round(res.K/tot*100),pM2=Math.round(res.M/tot*100),pB2=Math.round(res.B/tot*100);\n'
    pdf_btn += '          const bars=[{n:"Pop\\u00fcler Optimist",c:"#D97706",v:res.P,p:pP2},{n:"G\\u00fc\\u00e7l\\u00fc Kolerik",c:"#DC2626",v:res.K,p:pK2},{n:"M\\u00fckemmeliyetçi Melankolik",c:"#1E40AF",v:res.M,p:pM2},{n:"Bar\\u0131\\u015f\\u00e7\\u0131l So\\u011fukkanlı",c:"#059669",v:res.B,p:pB2}];\n'
    pdf_btn += '          const bH=bars.map(function(b){return "<div style=\\"margin-bottom:12px\\"><div style=\\"display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px\\"><span style=\\"font-weight:700;color:"+b.c+"\\">"+b.n+"</span><span style=\\"color:"+b.c+"\\">"+b.v+"/"+tot+" (%"+b.p+")</span></div><div style=\\"height:8px;border-radius:4px;background:#E2E8F0;overflow:hidden\\"><div style=\\"height:100%;border-radius:4px;background:"+b.c+";width:"+b.p+"%\\"></div></div></div>";}).join("");\n'
    pdf_btn += '          const sH=dI.s.map(function(x: string){return "<div style=\\"font-size:13px;padding:3px 0\\">\\u2705 "+x+"</div>";}).join("");\n'
    pdf_btn += '          const wH=dI.w.map(function(x: string){return "<div style=\\"font-size:13px;padding:3px 0\\">\\ud83d\\udca1 "+x+"</div>";}).join("");\n'
    pdf_btn += '          const smH=dI.summary.split("\\n\\n").map(function(x: string){return "<p style=\\"margin:0 0 10px;font-size:13px;line-height:1.7\\">"+x+"</p>";}).join("");\n'
    pdf_btn += '          const dt=new Date().toLocaleDateString("tr-TR",{day:"numeric",month:"long",year:"numeric"});\n'
    pdf_btn += '          var h="<!DOCTYPE html><html><head><meta charset=\\"utf-8\\"><title>NextERA Rapor</title>";\n'
    pdf_btn += '          h+="<link href=\\"https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap\\" rel=\\"stylesheet\\">";\n'
    pdf_btn += '          h+="<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Inter,sans-serif;padding:40px;color:#0F172A;max-width:800px;margin:0 auto}@media print{body{padding:20px}@page{margin:15mm}.np{display:none!important}}</style></head><body>";\n'
    pdf_btn += '          h+="<div style=\\"display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #0E7490;padding-bottom:16px;margin-bottom:24px\\">";\n'
    pdf_btn += '          h+="<div><div style=\\"font-size:28px;font-weight:800;color:#0E7490\\">Next<span style=\\"color:#F97316\\">ERA</span></div><div style=\\"font-size:12px;color:#64748B\\">Ki\\u015filik Analiz Raporu</div></div>";\n'
    pdf_btn += '          h+="<div style=\\"text-align:right\\"><div style=\\"font-size:14px;font-weight:700\\">"+(userName||"")+"</div><div style=\\"font-size:12px;color:#64748B\\">"+dt+"</div></div></div>";\n'
    pdf_btn += '          h+="<div style=\\"text-align:center;margin:24px 0\\"><div style=\\"font-size:48px\\">"+dI.e+"</div>";\n'
    pdf_btn += '          h+="<div style=\\"font-size:22px;font-weight:800;color:"+dI.c+";margin-top:8px\\">"+dI.t+"</div>";\n'
    pdf_btn += '          h+="<div style=\\"font-size:13px;color:#64748B;margin-top:4px\\">Bask\\u0131n ki\\u015filik tipin</div></div>";\n'
    pdf_btn += '          h+="<div style=\\"display:flex;justify-content:center;margin:20px 0\\">";\n'
    pdf_btn += '          h+="<div style=\\"width:180px;height:180px;border-radius:50%;background:conic-gradient(#D97706 0% "+pP2+"%, #DC2626 "+pP2+"% "+(pP2+pK2)+"%, #1E40AF "+(pP2+pK2)+"% "+(pP2+pK2+pM2)+"%, #059669 "+(pP2+pK2+pM2)+"% 100%);box-shadow:0 2px 8px rgba(0,0,0,0.1)\\"></div></div>";\n'
    pdf_btn += '          h+="<div style=\\"display:flex;justify-content:center;gap:16px;margin:16px 0;flex-wrap:wrap\\">";\n'
    pdf_btn += '          h+="<span style=\\"font-size:12px;font-weight:700;color:#D97706\\">Optimist %"+pP2+"</span>";\n'
    pdf_btn += '          h+="<span style=\\"font-size:12px;font-weight:700;color:#DC2626\\">Kolerik %"+pK2+"</span>";\n'
    pdf_btn += '          h+="<span style=\\"font-size:12px;font-weight:700;color:#1E40AF\\">Melankolik %"+pM2+"</span>";\n'
    pdf_btn += '          h+="<span style=\\"font-size:12px;font-weight:700;color:#059669\\">So\\u011fukkanlı %"+pB2+"</span></div>";\n'
    pdf_btn += '          h+="<div style=\\"margin:20px 0\\">"+bH+"</div>";\n'
    pdf_btn += '          h+="<div style=\\"margin:20px 0;padding:20px;border-radius:12px;background:"+dI.bg+"\\">";\n'
    pdf_btn += '          h+="<h3 style=\\"font-size:16px;font-weight:800;color:"+dI.c+";margin-bottom:10px\\">G\\u00fc\\u00e7l\\u00fc Y\\u00f6nlerin</h3>"+sH;\n'
    pdf_btn += '          h+="<h3 style=\\"font-size:16px;font-weight:800;color:"+dI.c+";margin-top:14px;margin-bottom:10px\\">Geli\\u015fim Alanlar\\u0131n</h3>"+wH+"</div>";\n'
    pdf_btn += '          h+="<div style=\\"margin:20px 0;padding:20px;border-radius:12px;background:#F8FAFC;border:1px solid #E2E8F0\\">";\n'
    pdf_btn += '          h+="<h3 style=\\"font-size:16px;font-weight:800;margin-bottom:10px\\">Ki\\u015filik Profilin Hakk\\u0131nda</h3>"+smH+"</div>";\n'
    pdf_btn += '          h+="<div style=\\"margin-top:24px;padding-top:16px;border-top:1px solid #E2E8F0;font-size:10px;color:#94A3B8;text-align:center\\">Kaynak: Florence Littauer | NextERA</div>";\n'
    pdf_btn += '          h+="<div class=\\"np\\" style=\\"margin-top:20px;text-align:center\\"><button onclick=\\"window.print()\\" style=\\"padding:12px 32px;border-radius:10px;background:#0E7490;color:#fff;border:none;font-size:15px;font-weight:700;cursor:pointer\\">Yazd\\u0131r / PDF Kaydet</button></div>";\n'
    pdf_btn += '          h+="</body></html>";\n'
    pdf_btn += '          var pw=window.open("","_blank");if(pw){pw.document.write(h);pw.document.close();}\n'
    pdf_btn += '        }} style={{width:"100%",padding:"14px",borderRadius:12,background:"#155E75",color:"#fff",border:"none",fontSize:15,fontWeight:700,cursor:"pointer",marginTop:12}}>📄 PDF Rapor İndir</button>\n        '
    pdf_btn += old_retake

    content = content.replace(old_retake, pdf_btn, 1)
    print("  OK - PDF butonu eklendi")
else:
    print("  SKIP - Testi Tekrarla butonu bulunamadi")

open(filepath, 'w').write(content)
print("Kaydedildi. Simdi: npm run build")
