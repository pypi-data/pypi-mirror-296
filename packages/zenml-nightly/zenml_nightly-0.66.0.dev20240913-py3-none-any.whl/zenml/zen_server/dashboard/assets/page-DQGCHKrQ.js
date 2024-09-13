import{j as e,r as f}from"./@radix-DnFH_oo1.js";import{z as d,l as x,m as h,k as j,F as p,B as m,i as N,C as S,f as D,j as C,Z as P}from"./index-B9wVwe7u.js";import{c as E}from"./@react-router-APVeuk-U.js";import{E as _}from"./EmptyState-Cs3DEmso.js";import{a as k,b as F}from"./@tanstack-QbMbTrh5.js";import{o as T}from"./url-DwbuKk1b.js";import{E as I}from"./Error-DorJD_va.js";import{t as A}from"./zod-uFd1wBcd.js";import{u as V,C as z}from"./index.esm-BE1uqCX5.js";import{S as q}from"./check-circle-DOoS4yhF.js";import"./@reactflow-B6kq9fJZ.js";const B=d.object({device_id:d.string().optional(),user_code:d.string().optional()});function Y(){const[s]=E(),{device_id:t,user_code:i}=B.parse({device_id:s.get("device_id")||void 0,user_code:s.get("user_code")||void 0});return{user_code:i,device_id:t}}const K=d.object({trustDevice:d.boolean()});function L({deviceId:s,queryParams:t}){return["devices",s,t]}async function R({deviceId:s,queryParams:t}){const i=x(h.devices.detail(s)+"?"+T(t)),r=await j(i,{method:"GET",credentials:"include",headers:{"Content-Type":"application/json"}});if(!r.ok)throw new p({message:"Error while fetching Device details",status:r.status,statusText:r.statusText});return r.json()}function W(s,t){return k({queryKey:L(s),queryFn:async()=>R(s),...t})}function G({device:s}){var t,i,r,a,c,n;return e.jsx(m,{className:"w-full p-5",children:e.jsxs("dl",{className:"flex flex-col gap-5",children:[e.jsxs("div",{className:"flex items-center justify-between",children:[e.jsx("dt",{children:"IP Address"}),e.jsx("dd",{children:(t=s.body)==null?void 0:t.ip_address})]}),((i=s.metadata)==null?void 0:i.city)&&((r=s.metadata)==null?void 0:r.country)&&e.jsxs("div",{className:"flex items-center justify-between",children:[e.jsx("dt",{children:"Location"}),e.jsxs("dd",{children:[(a=s.metadata)==null?void 0:a.city,", ",(c=s.metadata)==null?void 0:c.country]})]}),e.jsxs("div",{className:"flex min-w-0 items-center justify-between",children:[e.jsx("dt",{children:"Hostname"}),e.jsx("dd",{className:"truncate",children:(n=s.body)==null?void 0:n.hostname})]})]})})}async function H({deviceId:s,payload:t}){const i=x(h.devices.verify(s)),r=await j(i,{method:"PUT",credentials:"include",headers:{"Content-Type":"application/json"},body:JSON.stringify(t)});if(!r.ok){const a=await r.json().then(c=>c.detail).catch(()=>["","Failed to verify device."]);throw new p({status:r.status,statusText:r.statusText,message:a[1]||"Failed to verify device."})}return r.json()}function J(s){return F({mutationFn:async t=>H(t),...s})}function M({deviceId:s,user_code:t,setSuccess:i}){const r=f.useId(),{handleSubmit:a,formState:{isValid:c},control:n}=V({resolver:A(K),defaultValues:{trustDevice:!1}}),{toast:l}=N(),{mutate:v,isPending:y}=J({onSuccess:()=>{i(!0)},onError:o=>{o instanceof Error&&l({status:"error",emphasis:"subtle",icon:e.jsx(C,{className:"h-5 w-5 shrink-0 fill-error-700"}),description:o.message,rounded:!0})}});function g(o){v({deviceId:s,payload:{user_code:t,trusted_device:o.trustDevice}})}return e.jsxs("form",{onSubmit:a(g),className:"flex flex-col gap-5",children:[e.jsxs("div",{className:"flex items-start gap-2",children:[e.jsx(z,{control:n,name:"trustDevice",render:({field:{onChange:o,value:w}})=>e.jsx(S,{checked:w,onCheckedChange:b=>o(!!b),id:r})}),e.jsxs("label",{htmlFor:r,children:[e.jsx("p",{children:"Trust this device"}),e.jsx("p",{className:"text-theme-text-secondary",children:"We won't ask you again soon on this device."})]})]}),e.jsx(D,{disabled:y||!c,size:"md",className:"flex w-full justify-center",children:"Authorize this device"})]})}function O(){return e.jsxs(m,{className:"flex min-w-[540px] flex-col items-center justify-center space-y-7 px-7 py-9",children:[e.jsx(q,{className:"h-[120px] w-[120px] fill-theme-text-success"}),e.jsxs("div",{className:"text-center",children:[e.jsx("p",{className:"text-display-xs font-semibold",children:"You successfully added your device"}),e.jsx("p",{className:"text-theme-text-secondary",children:"You may close this screen and return to your CLI."})]})]})}function ce(){const{device_id:s,user_code:t}=Y(),[i,r]=f.useState(!1),{data:a,isPending:c,isError:n,error:l}=W({deviceId:s,queryParams:{user_code:t}},{enabled:!!s&&!!t});return!s||!t?e.jsx(_,{children:e.jsx("p",{children:"Invalid device verification link."})}):n?e.jsx(u,{children:e.jsx(I,{isAlertCircle:!0,err:l})}):c?e.jsx(u,{children:e.jsx(P,{})}):i?e.jsx(O,{}):e.jsx(u,{children:e.jsxs("div",{className:"w-full space-y-7",children:[e.jsxs("div",{className:"text-center",children:[e.jsx("h1",{className:"mb-0.5 text-display-xs font-semibold",children:"Authorize a new device"}),e.jsx("p",{className:"text-theme-text-secondary",children:"You are logging in from a new device."})]}),e.jsx(G,{device:a}),e.jsx(M,{setSuccess:r,deviceId:s,user_code:t})]})})}function u({children:s}){return e.jsx(m,{className:"flex w-full min-w-[540px] flex-col items-center justify-center gap-5 p-7",children:s})}export{ce as default};
