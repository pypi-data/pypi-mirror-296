import{j as e}from"./@radix-DnFH_oo1.js";import{u as m,S as o,A as x,a as d,g as f,b as u,r,c as h,d as p,ar as v,aq as g}from"./index-B9wVwe7u.js";import{a as j,h as N,O as b}from"./@react-router-APVeuk-U.js";import{I as w}from"./InlineAvatar-Ds2ZFHPc.js";import"./@tanstack-QbMbTrh5.js";import"./@reactflow-B6kq9fJZ.js";function y({children:s,isActiveOverride:t,...a}){const n=j(),i=t?t(n.pathname):!1;return e.jsx(N,{...a,className:({isActive:l})=>` ${i||l?"bg-primary-50 text-theme-text-brand":"hover:bg-neutral-200"} block rounded-md px-4 py-1 text-text-sm font-semibold `,children:s})}function c({items:s}){return e.jsx("nav",{className:"flex w-full flex-col items-center",children:e.jsx("ul",{className:"flex w-full flex-row flex-wrap items-center gap-1 lg:flex-col lg:items-start",children:s.map(t=>e.jsx("li",{className:"lg:w-full",children:e.jsx(y,{end:!0,to:t.href,isActiveOverride:t.isActiveOverride,children:t.name})},t.name))})})}function S(){var n,i,l;const{data:s,isError:t,isPending:a}=m({throwOnError:!0});return a?e.jsx(o,{className:"h-9 w-full"}):t?null:e.jsxs("div",{className:"flex w-full items-center gap-2 rounded-md border border-theme-border-moderate bg-theme-surface-primary p-2",children:[e.jsxs(x,{size:"md",type:"square",children:[e.jsx(d,{src:f(((n=s.body)==null?void 0:n.server_name)||"default")}),e.jsx(u,{size:"md",children:((i=s.body)==null?void 0:i.server_name[0])||"D"})]}),e.jsx("p",{className:"truncate text-text-sm font-semibold",children:(l=s.body)==null?void 0:l.server_name})]})}function I(){function s(){return[{name:"General",href:r.settings.general},{name:"Members",href:r.settings.members},{name:"Repositories",href:r.settings.repositories.overview},{name:"Secrets",href:r.settings.secrets.overview,isActiveOverride:a=>a.startsWith(r.settings.secrets.overview)},{name:"Connectors",href:r.settings.connectors.overview},{name:"Notifications",href:r.settings.notifications}]}const t=s();return e.jsx(c,{items:t})}function A(){function s(){return[{name:"Profile",href:r.settings.profile}]}const t=s();return e.jsx(c,{items:t})}function k(){const{data:s,isPending:t,isError:a}=h();return t?e.jsx(o,{className:"h-[70px] w-full"}):a?null:e.jsxs("div",{className:"rounded-md border border-theme-border-moderate bg-theme-surface-primary p-3",children:[e.jsxs("div",{className:"mb-2 flex items-center",children:[e.jsx(p,{className:"h-4 w-4 fill-theme-text-brand"}),e.jsx("p",{className:"ml-2 text-text-sm  font-semibold",children:"Open source"})]}),e.jsxs("p",{className:"mb-1 text-text-sm text-theme-text-tertiary",children:["ZenML v",s.version]}),e.jsxs("p",{className:"text-text-sm text-theme-text-tertiary",children:["UI Version ","v0.25.0"]})]})}function U(){const{data:s}=v();return e.jsxs("div",{className:"layout-container flex flex-col gap-7 pt-5 lg:flex-row lg:px-10",children:[e.jsxs("div",{className:"flex shrink-0 flex-col gap-4 lg:w-[200px]",children:[e.jsxs("div",{className:"flex flex-col gap-4",children:[e.jsx("p",{className:"text-text-xs font-semibold uppercase text-theme-text-tertiary",children:"Server"}),e.jsx(S,{}),e.jsx(I,{})]}),s?e.jsxs("div",{className:"flex flex-col gap-4",children:[e.jsx("p",{className:"text-text-xs font-semibold uppercase text-theme-text-tertiary",children:"Account"}),e.jsx(w,{username:g(s)})]}):e.jsx(o,{className:"h-[70px] w-full"}),e.jsx("div",{className:"flex flex-col gap-4",children:e.jsx(A,{})}),e.jsxs("div",{className:"flex flex-col gap-4",children:[e.jsx("p",{className:"text-text-xs font-semibold uppercase text-theme-text-tertiary",children:"Version"}),e.jsx(k,{})]})]}),e.jsx("div",{className:"w-full",children:e.jsx(b,{})})]})}export{U as default};
