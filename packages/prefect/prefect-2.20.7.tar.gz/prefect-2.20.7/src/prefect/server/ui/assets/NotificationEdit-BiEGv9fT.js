import{d as N,al as h,W as v,ae as C,B as w,c,e as r,f as g,o as u,g as x,h as f,cq as b,cp as k,a as B,bN as l,aX as p,_ as E}from"./index-BjFilUfY.js";import{u as V}from"./usePageTitle-J4-vayug.js";const A=N({__name:"NotificationEdit",async setup(I){let t,n;const i=h(),e=v("notificationId"),a=C({...([t,n]=w(()=>i.notifications.getNotification(e.value)),t=await t,n(),t)});async function _(s){try{await i.notifications.updateNotification(e.value,s),l.push(p.notifications())}catch(o){E("Error updating notification","error"),console.warn(o)}}function d(){l.push(p.notifications())}return V("Edit Notification"),(s,o)=>{const m=g("p-layout-default");return u(),c(m,null,{header:r(()=>[x(f(b))]),default:r(()=>[a.value?(u(),c(f(k),{key:0,notification:a.value,"onUpdate:notification":o[0]||(o[0]=y=>a.value=y),onSubmit:_,onCancel:d},null,8,["notification"])):B("",!0)]),_:1})}}});export{A as default};
//# sourceMappingURL=NotificationEdit-BiEGv9fT.js.map
