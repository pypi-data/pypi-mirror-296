(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[9340],{66070:function(e){e.exports=function(e,t){for(var n=-1,o=null==e?0:e.length,r=Array(o);++n<o;)r[n]=t(e[n],n,e);return r}},79867:function(e,t,n){var o=n(76747),r=n(37948);e.exports=function(e,t){t=o(t,e);for(var n=0,i=t.length;null!=e&&n<i;)e=e[r(t[n++])];return n&&n==i?e:void 0}},34282:function(e,t,n){var o=n(96539),r=n(66070),i=n(19785),l=n(55193),a=1/0,c=o?o.prototype:void 0,s=c?c.toString:void 0;e.exports=function e(t){if("string"==typeof t)return t;if(i(t))return r(t,e)+"";if(l(t))return s?s.call(t):"";var n=t+"";return"0"==n&&1/t==-a?"-0":n}},76747:function(e,t,n){var o=n(19785),r=n(40318),i=n(23419),l=n(65567);e.exports=function(e,t){return o(e)?e:r(e,t)?[e]:i(l(e))}},40318:function(e,t,n){var o=n(19785),r=n(55193),i=/\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/,l=/^\w*$/;e.exports=function(e,t){if(o(e))return!1;var n=typeof e;return!!("number"==n||"symbol"==n||"boolean"==n||null==e||r(e))||l.test(e)||!i.test(e)||null!=t&&e in Object(t)}},2941:function(e,t,n){var o=n(16651);e.exports=function(e){var t=o(e,function(e){return 500===n.size&&n.clear(),e}),n=t.cache;return t}},23419:function(e,t,n){var o=n(2941),r=/[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g,i=/\\(\\)?/g,l=o(function(e){var t=[];return 46===e.charCodeAt(0)&&t.push(""),e.replace(r,function(e,n,o,r){t.push(o?r.replace(i,"$1"):n||e)}),t});e.exports=l},37948:function(e,t,n){var o=n(55193),r=1/0;e.exports=function(e){if("string"==typeof e||o(e))return e;var t=e+"";return"0"==t&&1/e==-r?"-0":t}},99729:function(e,t,n){var o=n(79867);e.exports=function(e,t,n){var r=null==e?void 0:o(e,t);return void 0===r?n:r}},19785:function(e){var t=Array.isArray;e.exports=t},92360:function(e){e.exports=function(e){return null!=e&&"object"==typeof e}},55193:function(e,t,n){var o=n(99736),r=n(92360);e.exports=function(e){return"symbol"==typeof e||r(e)&&"[object Symbol]"==o(e)}},16651:function(e,t,n){var o=n(74554);function r(e,t){if("function"!=typeof e||null!=t&&"function"!=typeof t)throw TypeError("Expected a function");var n=function(){var o=arguments,r=t?t.apply(this,o):o[0],i=n.cache;if(i.has(r))return i.get(r);var l=e.apply(this,o);return n.cache=i.set(r,l)||i,l};return n.cache=new(r.Cache||o),n}r.Cache=o,e.exports=r},65567:function(e,t,n){var o=n(34282);e.exports=function(e){return null==e?"":o(e)}},33187:function(e,t,n){(window.__NEXT_P=window.__NEXT_P||[]).push(["/dataset/[datasetId]",function(){return n(61659)}])},61659:function(e,t,n){"use strict";n.r(t),n.d(t,{default:function(){return R}});var o=n(24246),r=n(92222),i=n(59003),l=n(13054),a=n(86677),c=n(27378),s=n(90824),u=n(81695),d=n(43124),f=n(11032),p=n(71824),x=n(52850),h=n(52987),v=n(39006),m=n(16781),j=n(57311),y=n(435),b=n(98894),g=n(5067),C=e=>{let{dataset:t,collection:n,isOpen:r,onClose:i}=e,a=null==t?void 0:t.collections.indexOf(n),[c]=(0,y.TG)(),s=(0,l.pmc)(),{isOpen:u,onOpen:d,onClose:f}=(0,l.qY0)(),p=async e=>{let o={...n,...e},r=(0,g.jC)(t,o,a);try{await c(r),s((0,m.t5)("Successfully modified collection"))}catch(e){s((0,m.Vo)(e))}i()},x=async()=>{if(t&&void 0!==a){let e=(0,g.qe)(t,a);try{await c(e),s((0,m.t5)("Successfully deleted collection"))}catch(e){s((0,m.Vo)(e))}i(),f()}};return(0,o.jsxs)(o.Fragment,{children:[(0,o.jsx)(j.ZP,{isOpen:r,onClose:i,description:"Collections are an array of objects that describe the Dataset's collections. Provide additional context to this collection by filling out the fields below.",header:(0,o.jsx)(j.zR,{title:"Collection Name: ".concat(null==n?void 0:n.name)}),footer:(0,o.jsx)(j.Gn,{onClose:i,onDelete:d,formId:b.e}),children:(0,o.jsx)(b.Z,{values:n,onSubmit:p,dataType:"collection",showDataCategories:!1})}),(0,o.jsx)(l.cVQ,{isOpen:u,onClose:f,onConfirm:x,title:"Delete Collection",message:(0,o.jsxs)(l.xvT,{children:["You are about to permanently delete the collection named"," ",(0,o.jsx)(l.xvT,{color:"complimentary.500",as:"span",fontWeight:"bold",children:null==n?void 0:n.name})," ","from this dataset. Are you sure you would like to continue?"]})})]})};let w=(0,r.Cl)(),S=()=>(0,o.jsx)(l.gCW,{mt:6,p:10,spacing:4,borderRadius:"base",maxW:"70%","data-testid":"no-results-notice",alignSelf:"center",margin:"auto",textAlign:"center",children:(0,o.jsx)(l.gCW,{children:(0,o.jsx)(l.xvT,{fontSize:"md",fontWeight:"600",children:"No collections found."})})});var R=()=>{let e=(0,a.useRouter)(),t=e.query.datasetId,{isLoading:n,data:m}=(0,h.oM)(t),j=(0,c.useMemo)(()=>(null==m?void 0:m.collections)||[],[m]),[y,b]=(0,c.useState)(!1),[g,R]=(0,c.useState)(),[_,k]=(0,c.useState)(),N=(0,c.useMemo)(()=>[w.accessor(e=>e.name,{id:"name",cell:e=>(0,o.jsx)(x.G3,{value:e.getValue(),fontWeight:"semibold"}),header:e=>(0,o.jsx)(x.Rr,{value:"Collection Name",...e}),size:180}),w.accessor(e=>e.description,{id:"description",cell:e=>(0,o.jsx)(x.G3,{value:e.getValue()}),header:e=>(0,o.jsx)(x.Rr,{value:"Description",...e}),size:300}),w.display({id:"actions",header:"Actions",cell:e=>{let{row:t}=e,n=t.original;return(0,o.jsx)(l.Ugi,{spacing:0,"data-testid":"collection-".concat(n.name),children:(0,o.jsx)(l.zxk,{variant:"outline",size:"xs",leftIcon:(0,o.jsx)(l.dY8,{}),onClick:()=>{R(n),b(!0)},children:"Edit"})})},meta:{disableRowClick:!0}})],[]),O=(0,c.useMemo)(()=>_?j.filter(e=>e.name.toLowerCase().includes(_.toLowerCase())):j,[j,_]),T=(0,i.b7)({getCoreRowModel:(0,r.sC)(),getFilteredRowModel:(0,r.vL)(),getSortedRowModel:(0,r.tj)(),columns:N,data:O});return(0,o.jsxs)(d.Z,{title:"Dataset - ".concat(t),mainProps:{paddingTop:0},children:[(0,o.jsx)(p.Z,{breadcrumbs:[{title:"Datasets"}],children:(0,o.jsx)(v.Z,{breadcrumbs:[{title:"All datasets",icon:(0,o.jsx)(s.V,{boxSize:4}),link:f.$m},{title:t,icon:(0,o.jsx)(u.l,{boxSize:5})}]})}),n?(0,o.jsx)(x.I4,{rowHeight:36,numRows:15}):(0,o.jsxs)(l.xuv,{"data-testid":"collections-table",children:[(0,o.jsx)(x.Q$,{children:(0,o.jsx)(x.HO,{globalFilter:_,setGlobalFilter:k,placeholder:"Search",testid:"collections-search"})}),(0,o.jsx)(x.ZK,{tableInstance:T,emptyTableNotice:(0,o.jsx)(S,{}),onRowClick:n=>{e.push({pathname:f.RF,query:{datasetId:t,collectionName:n.name}})}})]}),(0,o.jsx)(C,{dataset:m,collection:g,isOpen:y,onClose:()=>b(!1)})]})}}},function(e){e.O(0,[6451,4554,2850,7096,2888,9774,179],function(){return e(e.s=33187)}),_N_E=e.O()}]);