(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[9738],{53910:function(e,t,n){(window.__NEXT_P=window.__NEXT_P||[]).push(["/datamap",function(){return n(65217)}])},43124:function(e,t,n){"use strict";n.d(t,{Z:function(){return x}});var l=n(24246),i=n(13054),r=n(88038),s=n.n(r),o=n(86677);n(27378);var a=n(11596),d=n(72247),c=n(11032),u=()=>{let e=(0,o.useRouter)();return(0,l.jsx)(i.xuv,{bg:"gray.50",border:"1px solid",borderColor:"blue.400",borderRadius:"md",justifyContent:"space-between",p:5,mb:5,mt:5,children:(0,l.jsxs)(i.xuv,{children:[(0,l.jsxs)(i.Kqy,{direction:{base:"column",sm:"row"},justifyContent:"space-between",children:[(0,l.jsx)(i.xvT,{fontWeight:"semibold",children:"Configure your storage and messaging provider"}),(0,l.jsx)(i.zxk,{size:"sm",variant:"outline",onClick:()=>{e.push(c.fz)},children:"Configure"})]}),(0,l.jsxs)(i.xvT,{children:["Before Fides can process your privacy requests we need two simple steps to configure your storage and email client."," "]})]})})},x=e=>{let{children:t,title:n,padded:r=!0,mainProps:c}=e,x=(0,a.hz)(),h=(0,o.useRouter)(),m="/privacy-requests"===h.pathname||"/datastore-connection"===h.pathname,f=!(x.flags.privacyRequestsConfiguration&&m),{data:g}=(0,d.JE)(void 0,{skip:f}),{data:p}=(0,d.PW)(void 0,{skip:f}),j=x.flags.privacyRequestsConfiguration&&(!g||!p)&&m;return(0,l.jsxs)(i.kCb,{"data-testid":n,direction:"column",h:"100vh",children:[(0,l.jsxs)(s(),{children:[(0,l.jsxs)("title",{children:["Fides Admin UI - ",n]}),(0,l.jsx)("meta",{name:"description",content:"Privacy Engineering Platform"}),(0,l.jsx)("link",{rel:"icon",href:"/favicon.ico"})]}),(0,l.jsxs)(i.kCb,{as:"main",direction:"column",py:r?6:0,px:r?10:0,h:r?"calc(100% - 48px)":"full",flex:1,minWidth:0,overflow:"auto",...c,children:[j?(0,l.jsx)(u,{}):null,t]})]})}},78622:function(e,t,n){"use strict";n.d(t,{Y:function(){return s}});var l=n(24246),i=n(27378);let r=(0,i.createRef)(),s=(0,i.createContext)(r);t.Z=e=>{let{children:t}=e;return(0,l.jsx)(s.Provider,{value:r,children:t})}},28401:function(e,t,n){"use strict";n.d(t,{m:function(){return i}});var l=n(27378);class i{updateTableInstance(e){this.tableInstance=e}constructor(e=null){this.tableInstance=e,this.updateTableInstance=this.updateTableInstance.bind(this)}}let r=l.createContext(new i);t.Z=r},65217:function(e,t,n){"use strict";n.r(t),n.d(t,{default:function(){return H}});var l=n(24246),i=n(27378),r=n(73269),s=n(43124),o=n(13054),a=n(65218),d=n.n(a),c=n(44296),u=n(54321),x=n(78622),h=n(92222),m=n(59003),f=n(91650),g=n(79851),p=n(5445),j=n(28401);let v=e=>{var t;let{column:n}=e,{tableInstance:l}=(0,i.useContext)(j.Z),r=i.useMemo(()=>Array.from(n.getFacetedUniqueValues().keys()),[n]),s=i.useMemo(()=>{let e={};return r.forEach(t=>{e[t]=!1}),e},[r]);return{filterValue:null!==(t=n.getFilterValue())&&void 0!==t?t:s,clearFilterOptions:()=>{let e={};r.forEach(t=>{e[t]=!1}),n.setFilterValue(e)},toggleFilterOption:(e,t)=>{var i;let r={...null!==(i=n.getFilterValue())&&void 0!==i?i:s,[e]:t};Object.values(r).every(e=>!e)?null==l||l.setColumnFilters(null==l?void 0:l.getState().columnFilters.filter(e=>e.id!==n.id)):n.setFilterValue(r)},options:r,header:n.columnDef.header}};var b=n(47411);let y=(0,h.Cl)(),C={multifield:(e,t,n)=>n[e.original[t]]},w=()=>{let e=(0,c.T)(),{updateTableInstance:t}=(0,i.useContext)(j.Z),n=(0,c.C)(p.eo),{data:l,isLoading:r}=(0,p.Ex)({organizationName:"default_organization"});(0,b.MO)(),(0,g.fd)(),(0,f.te)();let s=(0,i.useRef)(!1);(0,i.useEffect)(()=>{if(l){let{columns:t,rows:n}=l;e((0,p.dd)(t)),s.current||(s.current=!0,0===n.length?e((0,p.ym)(!0)):e((0,p.ym)(!1)))}},[l,e]);let o=(0,i.useMemo)(()=>l?l.rows:[],[l]),a=(0,i.useMemo)(()=>(n||[]).map(e=>{let{text:t,value:n}=e;return y.accessor(e=>e[n],{id:n,header:t,cell:e=>{let{getValue:t}=e,n=t();return Array.isArray(n)?n.join(", "):n},filterFn:C.multifield})}),[n]),d=(0,m.b7)({columns:a,data:o,filterFns:C,getCoreRowModel:(0,h.sC)(),getFilteredRowModel:(0,h.vL)(),getFacetedRowModel:(0,h.o6)(),getFacetedUniqueValues:(0,h.JG)(),manualPagination:!0});return(0,i.useEffect)(()=>t(d),[d,t]),{...d,isLoading:r}};var k=n(83766),F=n.n(k),z=n(11596),S=n(39514),I=n(52850),O=n(31404);let R=e=>{var t,n,i;let{option:r,columnId:s,filterValue:a,toggleFilterOption:d}=e,u=(0,c.C)(b.L5),x=s===O.Ux&&null!==(n=null===(t=u.get(r))||void 0===t?void 0:t.name)&&void 0!==n?n:r;return(0,l.jsx)(o.XZJ,{value:r,width:"193px",height:"20px",mb:"25px",isChecked:null!==(i=a[r])&&void 0!==i&&i,onChange:e=>{let{target:t}=e;d(r,t.checked)},_focusWithin:{bg:"gray.100"},colorScheme:"complimentary",children:(0,l.jsx)(o.xvT,{fontSize:"sm",lineHeight:5,height:"20px",width:"170px",textOverflow:"ellipsis",overflow:"hidden",whiteSpace:"nowrap",children:x})},r)};var M=e=>{let{column:t}=e,{filterValue:n,toggleFilterOption:r,options:s}=v({column:t}),[a,d]=(0,i.useState)(!1),c=a?s:s.slice(0,15),u=s.length>15;return(0,l.jsx)(o.UQy,{width:"100%",allowToggle:!0,children:(0,l.jsxs)(o.Qdk,{border:"0px",children:[(0,l.jsx)(o.X6q,{height:"56px",children:(0,l.jsxs)(o.KFZ,{height:"100%",children:[(0,l.jsx)(o.xuv,{flex:"1",alignItems:"center",justifyContent:"center",textAlign:"left",children:t.columnDef.header}),(0,l.jsx)(o.XEm,{})]})}),(0,l.jsxs)(o.Hk3,{children:[(0,l.jsx)(o.MIq,{columns:3,children:c.map(e=>(0,l.jsx)(R,{columnId:t.id,option:e,filterValue:n,toggleFilterOption:r},e))}),!a&&u?(0,l.jsx)(o.zxk,{size:"sm",variant:"ghost",onClick:()=>{d(!0)},children:"View more"}):null,a&&u?(0,l.jsx)(o.zxk,{size:"sm",variant:"ghost",onClick:()=>{d(!1)},children:"View less"}):null]})]})},t.id)};let _=e=>{let{heading:t,children:n}=e;return(0,l.jsxs)(o.xuv,{padding:"24px 8px 8px 24px",children:[(0,l.jsx)(o.X6q,{size:"md",lineHeight:6,fontWeight:"bold",mb:2,children:t}),n]})};var T=e=>{let t,{isOpen:n,onClose:r}=e,{tableInstance:s}=(0,i.useContext)(j.Z),a=null==s?void 0:s.getHeaderGroups(),d=(e,t)=>e.filter(e=>e.id===t).map(e=>(0,l.jsx)(M,{column:e.column},t)),c=(0,i.useMemo)(()=>(null==a?void 0:a[0].headers)||[],[a]);return(0,l.jsxs)(o.u_l,{isOpen:n,onClose:r,isCentered:!0,size:"2xl",children:[(0,l.jsx)(o.ZAr,{}),(0,l.jsxs)(o.hzk,{children:[(0,l.jsx)(o.xBx,{children:"Filters"}),(0,l.jsx)(o.olH,{}),(0,l.jsx)(o.izJ,{}),(0,l.jsx)(o.fef,{maxH:"85vh",padding:"0px",overflowX:"auto",children:(t=[O.vy,O.Ux,O.OL],c.some(e=>t.indexOf(e.id)>-1))?(0,l.jsxs)(_,{heading:"Privacy attributes",children:[d(c,O.vy),d(c,O.Ux),d(c,O.OL)]}):null}),(0,l.jsx)(o.mzw,{children:(0,l.jsxs)(o.xuv,{display:"flex",justifyContent:"space-between",width:"100%",children:[(0,l.jsx)(o.zxk,{variant:"outline",size:"sm",mr:3,onClick:()=>{null==s||s.resetColumnFilters()},flexGrow:1,children:"Reset Filters"}),(0,l.jsx)(o.zxk,{colorScheme:"primary",size:"sm",onClick:r,flexGrow:1,children:"Done"})]})})]})]})};let Z=()=>{let{isOpen:e,onOpen:t,onClose:n}=(0,o.qY0)();return{isFilterModalOpen:e,onFilterModalOpen:t,onFilterModalClose:n}};var V=()=>{let{isFilterModalOpen:e,onFilterModalOpen:t,onFilterModalClose:n}=Z(),{tableInstance:r}=(0,i.useContext)(j.Z),{systemsCount:s,dictionaryService:a}=(0,z.hz)(),d=null==r?void 0:r.getRowModel(),c=(0,i.useMemo)(()=>{let e=(null==d?void 0:d.rows)||[];return F()(null==e?void 0:e.map(e=>e.original["system.fides_key"]))},[d]);if(!r)return null;let u=c.length,x=r.getState().columnFilters.length;return(0,l.jsxs)(l.Fragment,{children:[(0,l.jsxs)(o.kCb,{justifyContent:"flex-end",flexDirection:"row",alignItems:"center",flexWrap:"wrap",rowGap:4,columnGap:4,children:[(0,l.jsx)(o.kCb,{flexGrow:1,children:(0,l.jsx)(I.HO,{globalFilter:r.getState().globalFilter,setGlobalFilter:r.setGlobalFilter})}),(0,l.jsxs)(o.kCb,{children:[s>0?(0,l.jsxs)(o.kCb,{alignItems:"center",borderRadius:"md",gap:1,marginRight:4,children:[(0,l.jsxs)(o.xvT,{fontSize:"xs",children:[u," of ",s," systems displayed"]}),a?(0,l.jsx)(S.Z,{label:"Note that Global Vendor List (GVL) and Additional Consent (AC) systems are not currently included in these reports"}):null]}):null,(0,l.jsxs)(o.zxk,{"aria-label":"Open Filter Settings",variant:"outline",size:"xs",onClick:t,children:["Filter",x>0?(0,l.jsx)(o.Vp9,{ml:2,borderRadius:"full",size:"sm",children:x}):null]})]})]}),(0,l.jsx)(T,{isOpen:e,onClose:n})]})},E=n(12003),P=n(11032),q=()=>(0,l.jsx)(o.M5Y,{flex:1,"data-testid":"get-started-modal",backgroundColor:"gray.100",children:(0,l.jsx)(o.xuv,{backgroundColor:"white",p:10,borderRadius:"6px",boxShadow:"0px 1px 3px rgba(0, 0, 0, 0.1), 0px 1px 2px rgba(0, 0, 0, 0.06)",maxWidth:{base:"80%",lg:"60%",xl:"50%"},maxHeight:"90%",textAlign:"center",children:(0,l.jsxs)(o.Kqy,{spacing:4,children:[(0,l.jsx)(o.xvT,{color:"gray.700",fontWeight:"600",children:"Privacy engineering can seem like an endlessly complex confluence of legal and data engineering terminology—fear not—Fides is here to simplify this."}),(0,l.jsx)(o.xvT,{children:"Start by scanning your infrastructure. The scanner will connect to your infrastructure to automatically scan and create a list of all systems available and then classify each system containing PII."}),(0,l.jsx)(o.xvT,{children:"Let's get started!"}),(0,l.jsx)(o.xuv,{children:(0,l.jsx)(o.zxk,{as:"a",href:P.xo,width:"fit-content",colorScheme:"primary","data-testid":"add-systems-btn",children:"Add Systems"})})]})})});let G=d()(()=>Promise.all([n.e(5199),n.e(4804),n.e(2800)]).then(n.bind(n,2800)),{loadableGenerated:{webpack:()=>[2800]},ssr:!1}),W=()=>{let e=(0,c.C)(E.Xt),t=(0,i.useContext)(x.Y),{attemptAction:n}=(0,r.oI)(),[l,s]=(0,i.useState)(),o=(0,i.useCallback)(e=>{n().then(t=>{t&&s(e)})},[n,s]),a=(0,i.useCallback)(()=>{n().then(e=>{if(e&&l){if(t.current){var n;null===(n=t.current)||void 0===n||n.$id(l).unselect()}s(void 0)}})},[n,t,l]);return{isGettingStarted:e,selectedSystemId:l,setSelectedSystemId:o,resetSelectedSystemId:a}};var A=()=>{let{isGettingStarted:e,setSelectedSystemId:t,selectedSystemId:n,resetSelectedSystemId:i}=W(),{isLoading:r}=w();return r?(0,l.jsx)(o.M5Y,{width:"100%",flex:"1",children:(0,l.jsx)(o.$jN,{})}):e?(0,l.jsx)(q,{}):(0,l.jsxs)(o.kCb,{direction:"column",height:"100%",children:[(0,l.jsx)(o.xuv,{marginBottom:3,marginRight:10,children:(0,l.jsx)(V,{})}),(0,l.jsxs)(o.kCb,{position:"relative",flex:1,direction:"row",overflow:"auto",borderWidth:"1px",borderStyle:"solid",borderColor:"gray.200",children:[(0,l.jsx)(o.xuv,{flex:1,minWidth:"50%",maxWidth:"100%",children:(0,l.jsx)(G,{setSelectedSystemId:t})}),(0,l.jsx)(u.Z,{selectedSystemId:n,resetSelectedSystemId:i})]})]})},H=()=>{let e=(0,i.useMemo)(()=>new j.m,[]);return(0,l.jsx)(s.Z,{title:"View Map",mainProps:{padding:"40px 0 0 40px"},children:(0,l.jsx)(j.Z.Provider,{value:e,children:(0,l.jsxs)(x.Z,{children:[(0,l.jsx)(A,{}),(0,l.jsx)(r.eB,{})]})})})}}},function(e){e.O(0,[6451,4554,255,2850,8454,2017,4321,2888,9774,179],function(){return e(e.s=53910)}),_N_E=e.O()}]);