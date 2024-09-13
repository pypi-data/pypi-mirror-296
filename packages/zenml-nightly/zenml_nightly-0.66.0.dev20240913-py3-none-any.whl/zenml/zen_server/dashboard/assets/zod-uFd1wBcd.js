import{g as d,c as p}from"./index.esm-BE1uqCX5.js";var y=function(r,t,n){if(r&&"reportValidity"in r){var e=d(n,t);r.setCustomValidity(e&&e.message||""),r.reportValidity()}},h=function(r,t){var n=function(s){var o=t.fields[s];o&&o.ref&&"reportValidity"in o.ref?y(o.ref,s,r):o.refs&&o.refs.forEach(function(i){return y(i,s,r)})};for(var e in t.fields)n(e)},m=function(r){return r instanceof Date},g=function(r){return r==null},E=function(r){return typeof r=="object"},A=function(r){return!g(r)&&!Array.isArray(r)&&E(r)&&!m(r)},V=function(r){return/^\w*$/.test(r)},v=function(r,t,n){for(var e=-1,s=V(t)?[t]:function(l){return c=l.replace(/["|']|\]/g,"").split(/\.|\[/),Array.isArray(c)?c.filter(Boolean):[];var c}(t),o=s.length,i=o-1;++e<o;){var a=s[e],f=n;if(e!==i){var u=r[a];f=A(u)||Array.isArray(u)?u:isNaN(+s[e+1])?{}:[]}r[a]=f,r=r[a]}return r},j=function(r,t){t.shouldUseNativeValidation&&h(r,t);var n={};for(var e in r){var s=d(t.fields,e),o=Object.assign(r[e]||{},{ref:s&&s.ref});if(N(t.names||Object.keys(r),e)){var i=Object.assign({},d(n,e));v(i,"root",o),v(n,e,i)}else v(n,e,o)}return n},N=function(r,t){return r.some(function(n){return n.startsWith(t+".")})},b=function(r,t){for(var n={};r.length;){var e=r[0],s=e.code,o=e.message,i=e.path.join(".");if(!n[i])if("unionErrors"in e){var a=e.unionErrors[0].errors[0];n[i]={message:a.message,type:a.code}}else n[i]={message:o,type:s};if("unionErrors"in e&&e.unionErrors.forEach(function(l){return l.errors.forEach(function(c){return r.push(c)})}),t){var f=n[i].types,u=f&&f[e.code];n[i]=p(i,t,n,s,u?[].concat(u,e.message):e.message)}r.shift()}return n},O=function(r,t,n){return n===void 0&&(n={}),function(e,s,o){try{return Promise.resolve(function(i,a){try{var f=Promise.resolve(r[n.mode==="sync"?"parse":"parseAsync"](e,t)).then(function(u){return o.shouldUseNativeValidation&&h({},o),{errors:{},values:n.raw?e:u}})}catch(u){return a(u)}return f&&f.then?f.then(void 0,a):f}(0,function(i){if(function(a){return a.errors!=null}(i))return{values:{},errors:j(b(i.errors,!o.shouldUseNativeValidation&&o.criteriaMode==="all"),o)};throw i}))}catch(i){return Promise.reject(i)}}};export{O as t};
