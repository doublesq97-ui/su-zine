const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {execFileSync}=require('node:child_process');
const {pathToFileURL}=require('node:url');
const {chromium}=require('playwright');
const {render}=require('../scripts/render.cjs');
const root=path.resolve(__dirname,'..');

test('light and dark preserve layout for every module and palette',async()=>{
 const temp=fs.mkdtempSync(path.join(os.tmpdir(),'su-zine-themes-'));
 let browser;
 try {
  const data=JSON.parse(fs.readFileSync(path.join(root,'assets/example.json')));
  const p=data.pages[0], sample=p.blocks[0];
  p.blocks=Array.from({length:6},(_,color)=>({...sample,color,kind:['flow','stack','tags','papers'][color%4],
   title:'中文长标题与自然换行检查',paras:['中文长段落用于检查自然换行与留白。'.repeat(6),'末行也必须完整保留。'],
   items:['核实来源','组织内容','逐图检查'],panel:'概念示意',rows:[['补充说明','右侧内容保持白字。']]}));
  const source=path.join(temp,'content.json');fs.writeFileSync(source,JSON.stringify(data));
  for(const theme of ['light','dark']) {
   const out=path.join(temp,theme);
   execFileSync('python3',[path.join(root,'scripts/build.py'),source,'--out',out,'--theme',theme]);
   const report=await render(out,{scale:1});
   assert.equal(report[0].width,1200);assert.deepEqual(report[0].overflow,[]);
   assert(!fs.readdirSync(out).some(f=>f.endsWith('.pdf')));
  }
  browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_PATH?{executablePath:process.env.CHROMIUM_PATH}:{})});
  const page=await browser.newPage({viewport:{width:1200,height:900}}),snapshots=[];
  for(const theme of ['light','dark']) {
   await page.goto(pathToFileURL(path.join(temp,theme,'page-01.html')).href);
   await page.evaluate(()=>document.fonts.ready);
   snapshots.push(await page.evaluate(()=>({
    geometry:[...document.querySelectorAll('.sheet,.sheet *')].map(el=>{const r=el.getBoundingClientRect();return [el.className,el.textContent,r.x,r.y,r.width,r.height]}),
    body:getComputedStyle(document.body).backgroundColor,
    cards:[...document.querySelectorAll('.item,.row-body,.row-label')].map(el=>getComputedStyle(el).color),
   })));
  }
  assert.deepEqual(snapshots[0].geometry,snapshots[1].geometry);
  assert.equal(snapshots[0].body,'rgb(255, 255, 255)');
  assert.equal(snapshots[1].body,'rgb(16, 17, 20)');
  assert(snapshots[1].cards.every(color=>color==='rgb(236, 238, 241)'));
 } finally {if(browser)await browser.close();fs.rmSync(temp,{recursive:true,force:true});}
});
