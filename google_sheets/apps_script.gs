/** Consolidate plan sources to 'Plans' sheet (last 90 days) */
const SOURCES=[
  {name:'Starter Sheet',type:'csv',url:'https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/export?format=csv',enabled:false},
  {name:'Sample CSV',type:'csv',url:'https://raw.githubusercontent.com/YOUR_USER/YOUR_REPO/main/data/sources/sample_plans.csv',enabled:true}
];
function dailyPull(){
  const ss=SpreadsheetApp.getActive(); const sh=ss.getSheetByName('Plans')||ss.insertSheet('Plans'); sh.clear();
  const header=["provider","plan_name","region","country","data_gb","validity_days","price_usd","product_url","timestamp"]; sh.appendRow(header);
  SOURCES.filter(s=>s.enabled).forEach(src=>{
    const res=UrlFetchApp.fetch(src.url,{muteHttpExceptions:true});
    const csv=Utilities.parseCsv(res.getContentText()); const hdr=csv[0].map(h=>h.toLowerCase()); const idx=header.map(h=>hdr.indexOf(h));
    for(let i=1;i<csv.length;i++){ sh.appendRow(idx.map(j=>j>=0?csv[i][j]:"")); }
  });
  const data=sh.getDataRange().getValues(); const now=new Date(); const keep=[header];
  for(let i=1;i<data.length;i++){ const ts=new Date(data[i][8]||now); if((now-ts)/(1000*60*60*24)<=90) keep.push(data[i]); }
  sh.clear(); sh.getRange(1,1,keep.length,keep[0].length).setValues(keep);
}
function createTrigger(){ ScriptApp.newTrigger('dailyPull').timeBased().everyDays(1).atHour(6).create(); }
