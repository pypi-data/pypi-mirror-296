import{d as M,W as V,al as B,b as n,am as L,b5 as W,bk as f,b7 as X,c as r,e as a,a as c,f as i,u as $,ar as j,o as p,g as u,h as e,bl as E,bm as b,y as G,x as m,bn as H,m as J,A as O,bo as P,bp as Q,bi as U,a5 as q,aX as z}from"./index-BjFilUfY.js";import{u as K}from"./usePageTitle-J4-vayug.js";const at=M({__name:"TaskRun",setup(Y){const R=$(),k=V("taskRunId"),d=B(),g=n(()=>[{label:"Details",hidden:j.xl},{label:"Logs"},{label:"Artifacts"},{label:"Task Inputs"}]),l=L("tab","Logs"),{tabs:y}=W(g,l),T=n(()=>k.value?[k.value]:null),h=f(d.taskRuns.getTaskRun,T,{interval:3e4}),t=n(()=>h.response),o=n(()=>{var s;return(s=t.value)==null?void 0:s.flowRunId}),w=n(()=>o.value?[o.value]:null),I=f(d.flowRuns.getFlowRun,w),v=n(()=>{var s;return(s=t.value)!=null&&s.taskInputs?JSON.stringify(t.value.taskInputs,void 0,2):"{}"});function x(){I.refresh(),R.push(z.flowRun(o.value))}const C=n(()=>{var s;return(s=t.value)==null?void 0:s.stateType});X(C);const D=n(()=>t.value?`Task Run: ${t.value.name}`:"Task Run");return K(D),(s,_)=>{const S=i("p-code-highlight"),A=i("p-tabs"),N=i("p-layout-well");return t.value?(p(),r(N,{key:0,class:"task-run"},{header:a(()=>[u(e(E),{"task-run-id":t.value.id,onDelete:x},null,8,["task-run-id"])]),well:a(()=>[u(e(b),{alternate:"","task-run":t.value},null,8,["task-run"])]),default:a(()=>[u(A,{selected:e(l),"onUpdate:selected":_[0]||(_[0]=F=>q(l)?l.value=F:null),tabs:e(y)},G({details:a(()=>[u(e(b),{"task-run":t.value},null,8,["task-run"])]),logs:a(()=>[u(e(P),{"task-run":t.value},null,8,["task-run"])]),artifacts:a(()=>[t.value?(p(),r(e(Q),{key:0,"task-run":t.value},null,8,["task-run"])):c("",!0)]),"task-inputs":a(()=>[t.value?(p(),r(e(U),{key:0,"text-to-copy":v.value},{default:a(()=>[u(S,{lang:"json",text:v.value,class:"task-run__inputs"},null,8,["text"])]),_:1},8,["text-to-copy"])):c("",!0)]),_:2},[t.value?{name:"task-inputs-heading",fn:a(()=>[m(" Task inputs "),u(e(H),{title:"Task Inputs"},{default:a(()=>[m(J(e(O).info.taskInput),1)]),_:1})]),key:"0"}:void 0]),1032,["selected","tabs"])]),_:1})):c("",!0)}}});export{at as default};
//# sourceMappingURL=TaskRun-BgW0wXvy.js.map
