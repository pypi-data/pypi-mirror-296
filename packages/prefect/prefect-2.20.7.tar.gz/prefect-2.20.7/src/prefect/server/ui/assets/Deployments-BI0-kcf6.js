import{d,al as y,t as _,b as o,c as a,e as n,f as i,o as t,g as f,h as s,bz as h,p as b,bA as k,by as g,F as v,a as x}from"./index-BjFilUfY.js";import{u as D}from"./usePageTitle-J4-vayug.js";const V=d({__name:"Deployments",setup(C){const l=y(),c={interval:3e4},e=_(l.deployments.getDeployments,[{}],c),p=o(()=>e.response??[]),r=o(()=>e.executed&&p.value.length===0),m=o(()=>e.executed);return D("Deployments"),(B,F)=>{const u=i("p-layout-default");return t(),a(u,{class:"deployments"},{header:n(()=>[f(s(h))]),default:n(()=>[m.value?(t(),b(v,{key:0},[r.value?(t(),a(s(k),{key:0})):(t(),a(s(g),{key:1,onDelete:s(e).refresh},null,8,["onDelete"]))],64)):x("",!0)]),_:1})}}});export{V as default};
//# sourceMappingURL=Deployments-BI0-kcf6.js.map
