import{r as n,j as s}from"./@radix-DnFH_oo1.js";import{S as m}from"./check-circle-DOoS4yhF.js";import{u as p}from"./url-DwbuKk1b.js";import{B as h,f as x,r as d,z as r}from"./index-B9wVwe7u.js";import{c as f,L as g}from"./@react-router-APVeuk-U.js";import{a as S}from"./UpdatePasswordSchemas-C6Zb7ASL.js";const c=n.createContext(null);function _({children:e,initialStep:t=1}){const[a,o]=n.useState(t);return s.jsx(c.Provider,{value:{surveyStep:a,setSurveyStep:o},children:e})}function y(){const e=n.useContext(c);if(e===null)throw new Error("useSurveyContext must be used within an SurveyProvider");return e}function U({stepAmount:e}){const{surveyStep:t}=y();return t>e?null:s.jsx("ol",{className:"flex flex-wrap justify-center gap-1 pb-5","aria-label":"progress",children:Array.from({length:e},(a,o)=>s.jsx("li",{"aria-current":t===o+1?"step":void 0,className:`h-0.5 w-[90px] rounded-rounded ${t===o+1?"bg-primary-100":t>o?"bg-primary-300":"bg-neutral-200"}`},o))})}const v=e=>n.createElement("svg",{viewBox:"0 0 24 24",fill:"black",xmlns:"http://www.w3.org/2000/svg",...e},n.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M11.2929 4.29289C11.6834 3.90237 12.3166 3.90237 12.7071 4.29289L19.7071 11.2929C20.0976 11.6834 20.0976 12.3166 19.7071 12.7071L12.7071 19.7071C12.3166 20.0976 11.6834 20.0976 11.2929 19.7071C10.9024 19.3166 10.9024 18.6834 11.2929 18.2929L16.5858 13H5C4.44772 13 4 12.5523 4 12C4 11.4477 4.44772 11 5 11H16.5858L11.2929 5.70711C10.9024 5.31658 10.9024 4.68342 11.2929 4.29289Z"}));function F({username:e,subHeader:t,displayBody:a=!0}){const[o]=f(),i=o.get("redirect"),u=i&&`${window.location.origin}${i}`,l=p.safeParse(u);return s.jsxs(h,{className:"flex max-w-[540px] flex-col items-center justify-center space-y-7 px-7 py-9",children:[s.jsx(m,{className:"h-[120px] w-[120px] fill-theme-text-success"}),s.jsxs("div",{className:"space-y-3 text-center",children:[s.jsxs("p",{className:"text-display-xs font-semibold",children:["Congratulations!",s.jsx("br",{}),t]}),a&&s.jsxs("p",{className:"text-theme-text-secondary",children:["You can log in to the dashboard with your username"," ",s.jsx("span",{className:"font-semibold text-theme-text-primary",children:e})," and your password to start exploring!"]}),s.jsx(x,{className:"inline-flex",size:"md",intent:"primary",asChild:!0,children:s.jsxs(g,{to:l.success?l.data:d.home,children:[s.jsx("span",{children:"Go to Dashboard"}),s.jsx(v,{className:"h-5 w-5 fill-white"})]})})]})]})}const L=r.object({fullName:r.union([r.string(),r.literal("")]),email:r.union([r.string().email(),r.literal("")]),getUpdates:r.boolean()}).refine(e=>e.getUpdates?e.email!=="":!0),B=r.object({primaryUse:r.string().min(1)}),E=r.object({providers:r.string().array(),other:r.boolean(),otherVal:r.string().optional()}).refine(e=>e.other?e.otherVal!=="":e.providers.length>0),T=r.object({serverName:r.string().optional()});function w(e=!1){return S.extend({username:r.string()}).refine(t=>t.newPassword===t.confirmPassword,{path:["confirmPassword"],message:"Passwords do not match"}).refine(t=>e?t.username.length>0:!0)}w();const V=r.object({usageReason:r.union([r.enum(["exploring","planning_poc","comparing_tools","implementing_production_environment"]),r.literal("")]),comparison_tools:r.string().array().optional(),otherTool:r.boolean().optional(),otherToolVal:r.string().optional()}).refine(e=>{var t;return e.usageReason.length===0?!1:e.otherTool?e.otherToolVal!=="":e.usageReason==="comparing_tools"?((t=e.comparison_tools)==null?void 0:t.length)??!1:!0});export{E as I,U as S,V as U,F as a,_ as b,T as c,L as d,w as g,B as p,y as u};
