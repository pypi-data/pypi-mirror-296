var b=`<div class="pglite-app-container">

    <h1><tt>pglite</tt></h1>

    <div>Executed commands:</div>
    <div class="code-editor" title="code-editor"></div>
    <div id="pglite-timestamp"></div>
    <hr>
    <div>Result:</div>
    <div title="results"></div>
    <hr>
    <div>Raw Output:</div>
    <div title="output"></div>
</div>`;function T(){return"xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,function(e){let t=Math.random()*16|0;return(e==="x"?t:t&3|8).toString(16)})}import{PGlite as _}from"https://cdn.jsdelivr.net/npm/@electric-sql/pglite/dist/index.js";var x=new window.AudioContext,R=e=>{if(e){let t=new SpeechSynthesisUtterance(e);window.speechSynthesis.speak(t)}};function D(e=440,t=1e3,n=.1,l="sine",a=null){let i=x.createOscillator(),c=x.createGain();c.gain.value=n,i.type=l,i.frequency.value=e,i.connect(c),i.connect(x.destination),i.start(),c.gain.exponentialRampToValueAtTime(1e-5,x.currentTime+t),setTimeout(()=>{i.stop(),a&&setTimeout(()=>{R(a)},100)},t)}function v(e=null){D(500,5,.05,"sine",e)}var B=`
-- Optionally select statements to execute.

CREATE TABLE IF NOT EXISTS test  (
        id serial primary key,
        title varchar not null
      );

INSERT INTO test (title) values ('dummy');

`.trim();function M(e){let t=document.createElement("table"),n=t.insertRow();return e.fields.forEach(l=>{let a=document.createElement("th");a.textContent=l.name,n.appendChild(a)}),t}function S(e,t){e.rows.forEach(n=>{let l=t.insertRow();e.fields.forEach(a=>{let i=l.insertCell();i.textContent=String(n[a.name])})})}function C(e){if(e&&e.file_content&&e.file_info){let{file_content:t,file_info:n}=e,l=atob(t),a=new Array(l.length);for(let s=0;s<l.length;s++)a[s]=l.charCodeAt(s);let i=new Uint8Array(a),c=new Blob([i],{type:n.type});return new File([c],n.name,{type:n.type,lastModified:n.lastModified})}return null}function L({model:e,el:t}){let n=e.get("idb"),l=e.get("file_package"),a=C(l),i={};a&&(i.loadDataDir=a);let c=n?new _(n,i):new _(i),m=e.get("headless");if(!m){let s=document.createElement("div");s.innerHTML=b;let r=T();s.id=r,t.appendChild(s)}e.on("change:datadump",async()=>{if(e.get("datadump")=="generate_dump"){let r=await c.dumpDataDir(),y=new FileReader;y.onload=p=>{let g={name:r.name,size:r.size,type:r.type,lastModified:r.lastModified},h=p.target.result.split(",")[1],d={file_info:g,file_content:h};e.set("file_package",d),e.set("response",{status:"datadump_ready"}),e.save_changes(),e.get("audio")&&v()},y.readAsDataURL(r)}}),e.on("change:code_content",async()=>{function s(o){if(m)return;let u=t.querySelector('div[title="code-editor"]');u.innerHTML=u.innerHTML+"<br>"+o}function r(o){if(m)return;let u=t.querySelector('div[title="output"]'),f=t.querySelector('div[title="results"]');u.innerHTML=JSON.stringify(o);let w=M(o);S(o,w),f.innerHTML="",f.append(w)}function y(o,u){m||(s(o),r(u))}let p=e.get("code_content");if(!p)return;let g=e.get("multiline"),h=e.get("multiexec"),d={rows:[],fields:[{name:"",dataTypeID:0}]};if(h){s(p);let o=await c.exec(p);r(o[o.length-1]),e.set("response",{status:"completed",response:o,response_type:"multi"})}else if(g!=""){let o=p.split(g);for(let u of o){let f=u.trim();f!==""&&(s(`${f};`),d=await c.query(f),r(d))}e.set("response",{status:"completed",response:d,response_type:"single"})}else s(p),d=await c.query(p),r(d),e.set("response",{status:"completed",response:d,response_type:"single"});e.save_changes(),e.get("audio")&&v()}),e.set("response",{status:"ready"}),e.save_changes()}var G={render:L};export{G as default};
