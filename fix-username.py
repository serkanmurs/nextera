filepath = 'src/app/page.tsx'
content = open(filepath, 'r').read()

# 1. userName prop type ekle
old1 = 'function PersonalityTestScreen({onClose,onSave,initialResults}:{onClose:()=>void;onSave:(r:any)=>void;initialResults?:any}) {'
new1 = 'function PersonalityTestScreen({onClose,onSave,initialResults,userName}:{onClose:()=>void;onSave:(r:any)=>void;initialResults?:any;userName?:string}) {'

old1b = 'function PersonalityTestScreen({onClose,onSave,initialResults,userName}:{onClose:()=>void;onSave:(r:any)=>void;initialResults?:any;userName?:string}) {'

if old1b in content:
    print("OK - userName prop zaten var")
elif old1 in content:
    content = content.replace(old1, new1)
    print("OK 1. userName prop eklendi")
else:
    print("SKIP 1. Fonksiyon imzasi bulunamadi")

# 2. Render'da userName gec
old2 = '<PersonalityTestScreen onClose={() => setShowPersonalityTest(false)}'
new2 = '<PersonalityTestScreen onClose={() => setShowPersonalityTest(false)} userName={user.name}'

if 'userName={user.name}' in content:
    print("OK - userName zaten geciliyor")
elif old2 in content:
    content = content.replace(old2, new2, 1)
    print("OK 2. userName gecildi")
else:
    print("SKIP 2. Screen render bulunamadi")

open(filepath, 'w').write(content)
print("Kaydedildi. Simdi: npm run build")
