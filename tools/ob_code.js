// Usage: node tools/ob_code.js <topicIndex> DA PS MG CK critMissed harmful
const T=['Abnormal Uterine Bleeding','Diabetes in Pregnancy','First Trimester Bleeding','Fetal Growth Restriction','Multiple Gestation','Ovarian / Pelvic Mass','Postmenopausal Bleeding','Postpartum Hemorrhage','Preeclampsia–Eclampsia / Hypertension','Preterm Labor / PPROM','Third Trimester Bleeding','UTI / Renal Disease in Pregnancy','Abnormal Pap Test','Amenorrhea','Contraception','Endometriosis','Infertility','Menopause Management','PCOS / Hirsutism','Pelvic Pain / STI','Prenatal Evaluation and Care','Vulvovaginitis'];
const B='0123456789ABCDEFGHJKMNPQRSTVWXYZ';
function fnv(s){ let h=2166136261; for(let i=0;i<s.length;i++){ h^=s.charCodeAt(i); h=Math.imul(h,16777619)>>>0; } return h; }
const [t,DA,PS,MG,CK,cm,hm]=process.argv.slice(2).map(Number); const nonce=Math.floor(Math.random()*256);
let p=0; for(const [v,b] of [[t,5],[DA,4],[PS,4],[MG,4],[CK,4],[Math.min(7,cm),3],[Math.min(7,hm),3],[nonce,8]]) p=p*2**b+v;
let n=p*1024+(fnv(p+'|ob-orals')&1023), s=''; for(let i=0;i<9;i++){ s=B[n%32]+s; n=Math.floor(n/32); }
console.log(`OB-${s.slice(0,4)}-${s.slice(4)}  (${T[t]}: DA ${DA} PS ${PS} MG ${MG} CK ${CK}, ${cm} crit missed, ${hm} harmful)`);
