(()=>{"use strict";var e,t={7314:(e,t,r)=>{var a=r(434),n=r(9408);document.addEventListener("DOMContentLoaded",(()=>{!function(){const e=document.querySelector('[data-side-panel="preview"]');if(!e)return;const t=e.querySelector("[data-preview-panel]"),r=t.querySelectorAll("[data-device-width]"),o=t.querySelector("[data-default-size]"),i=e=>{const a=e.target.value;(e=>{const r=t.classList.contains("preview-panel--unavailable");let a=e;e&&!r||(a=o.dataset.deviceWidth),t.style.setProperty("--preview-device-width",a)})(e.target.dataset.deviceWidth);try{localStorage.setItem("wagtail:preview-panel-device",a)}catch(e){}r.forEach((e=>{t.classList.toggle(`preview-panel--${e.value}`,e.value===a)}))};r.forEach((e=>e.addEventListener("change",i))),new ResizeObserver((e=>t.style.setProperty("--preview-panel-width",e[0].contentRect.width))).observe(t);const l=t.querySelector("[data-preview-new-tab]"),s=t.querySelector("[data-refresh-preview]"),c=t.querySelector("[data-preview-spinner]"),d=document.querySelector("[data-edit-form]"),v=t.dataset.action,u=document.querySelector("[data-preview-mode-select]");let h,w=t.querySelector("[data-preview-iframe]"),p=!1;const f=()=>{clearTimeout(h),c.classList.add("w-hidden"),p=!1},m=()=>{const e=document.createElement("iframe");e.style.width=0,e.style.height=0,e.style.opacity=0,e.style.position="absolute",e.src=w.src,w.insertAdjacentElement("afterend",e);const t=()=>{Array.from(w.attributes).forEach((t=>{"src"!==t.nodeName&&e.setAttribute(t.nodeName,t.nodeValue)})),e.contentWindow.scroll(w.contentWindow.scrollX,w.contentWindow.scrollY),w.remove(),w=e,e.style=null,f(),e.removeEventListener("load",t)};e.addEventListener("load",t)},g=()=>p?Promise.resolve():(p=!0,h=setTimeout((()=>c.classList.remove("w-hidden")),2e3),fetch(v,{method:"POST",body:new FormData(d)}).then((e=>e.json())).then((e=>(t.classList.toggle("preview-panel--has-errors",!e.is_valid),t.classList.toggle("preview-panel--unavailable",!e.is_available),e.is_valid?m():f(),e.is_valid))).catch((e=>{throw f(),e}))),y=()=>g().catch((()=>{window.alert((0,n.ih)("Error while sending preview data."))}));if(l.addEventListener("click",(e=>{e.preventDefault();const t=window.open("",v);t.focus(),y().then((e=>{if(e){const e=new URL(l.href);t.document.location=e.toString()}else window.focus(),t.close()}))})),s&&s.addEventListener("click",y),a.QF.WAGTAIL_AUTO_UPDATE_PREVIEW){let t,r=new URLSearchParams(new FormData(d)).toString();const n=()=>{const e=new URLSearchParams(new FormData(d)).toString(),t=r!==e;return r=e,t},o=()=>{!p&&n()&&g()};e.addEventListener("show",(()=>{o(),t=setInterval(o,a.QF.WAGTAIL_AUTO_UPDATE_PREVIEW_INTERVAL)})),e.addEventListener("hide",(()=>{clearInterval(t)}))}u&&u.addEventListener("change",(e=>{const t=e.target.value,r=new URL(w.src);r.searchParams.set("mode",t),w.src=r.toString(),r.searchParams.delete("in_preview_panel"),l.href=r.toString(),y()})),fetch(v,{headers:{[a.QF.CSRF_HEADER_NAME]:a.QF.CSRF_TOKEN},method:"DELETE"}).then((()=>g())).then((()=>m()));let b=null;try{b=localStorage.getItem("wagtail:preview-panel-device")}catch(e){}(t.querySelector(`[data-device-width][value="${b}"]`)||o).click()}()}))}},r={};function a(e){var n=r[e];if(void 0!==n)return n.exports;var o=r[e]={exports:{}};return t[e](o,o.exports,a),o.exports}a.m=t,e=[],a.O=(t,r,n,o)=>{if(!r){var i=1/0;for(d=0;d<e.length;d++){for(var[r,n,o]=e[d],l=!0,s=0;s<r.length;s++)(!1&o||i>=o)&&Object.keys(a.O).every((e=>a.O[e](r[s])))?r.splice(s--,1):(l=!1,o<i&&(i=o));if(l){e.splice(d--,1);var c=n();void 0!==c&&(t=c)}}return t}o=o||0;for(var d=e.length;d>0&&e[d-1][2]>o;d--)e[d]=e[d-1];e[d]=[r,n,o]},a.n=e=>{var t=e&&e.__esModule?()=>e.default:()=>e;return a.d(t,{a:t}),t},a.d=(e,t)=>{for(var r in t)a.o(t,r)&&!a.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:t[r]})},a.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),a.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),a.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},a.j=673,(()=>{var e={673:0};a.O.j=t=>0===e[t];var t=(t,r)=>{var n,o,[i,l,s]=r,c=0;if(i.some((t=>0!==e[t]))){for(n in l)a.o(l,n)&&(a.m[n]=l[n]);if(s)var d=s(a)}for(t&&t(r);c<i.length;c++)o=i[c],a.o(e,o)&&e[o]&&e[o][0](),e[o]=0;return a.O(d)},r=globalThis.webpackChunkwagtail=globalThis.webpackChunkwagtail||[];r.forEach(t.bind(null,0)),r.push=t.bind(null,r.push.bind(r))})();var n=a.O(void 0,[751],(()=>a(7314)));n=a.O(n)})();