"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[2850],{33312:function(e,t,n){var i=n(24246),o=n(13054);t.Z=e=>{let{search:t,onChange:n,withIcon:r,onClear:l,placeholder:s,...a}=e;return(0,i.jsxs)(o.BZy,{size:"sm",minWidth:"308px",children:[r?(0,i.jsx)(o.Z8_,{pointerEvents:"none",children:(0,i.jsx)(o.PTu,{color:"gray.300",w:"17px",h:"17px"})}):null,(0,i.jsx)(o.IIB,{autoComplete:"off",type:"search",minWidth:200,size:"sm",borderRadius:"md",value:t,name:"search",onChange:e=>n(e.target.value),placeholder:s||"",...a}),l?(0,i.jsx)(o.xHT,{children:(0,i.jsx)(o.zxk,{borderLeftRadius:0,height:"95%",right:"14px",flexShrink:0,fontWeight:"light",size:"sm",onClick:l,children:"Clear"})}):null]})}},60136:function(e,t,n){n.d(t,{D4:function(){return r.D4},MM:function(){return h},Ot:function(){return c},c6:function(){return o},cj:function(){return x},e$:function(){return s},fn:function(){return a},iC:function(){return g},nU:function(){return u},tB:function(){return d}});var i,o,r=n(41164);let l="An unexpected error occurred. Please try again.",s=function(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:l;if((0,r.Bw)(e)){if((0,r.hE)(e.data))return e.data.detail;if((0,r.cz)(e.data)){var n;let t=null===(n=e.data.detail)||void 0===n?void 0:n[0];return"".concat(null==t?void 0:t.msg,": ").concat(null==t?void 0:t.loc)}if(409===e.status&&(0,r.Dy)(e.data)||404===e.status&&(0,r.XD)(e.data))return"".concat(e.data.detail.error," (").concat(e.data.detail.fides_key,")")}return t};function a(e){return"object"==typeof e&&null!=e&&"status"in e}function c(e){return"object"==typeof e&&null!=e&&"data"in e&&"string"==typeof e.data.detail}function d(e){return"object"==typeof e&&null!=e&&"data"in e&&Array.isArray(e.data.detail)}let u=function(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{status:500,message:l};if((0,r.oK)(e))return{status:e.originalStatus,message:e.data};if((0,r.Bw)(e)){let{status:n}=e;return{status:n,message:s(e,t.message)}}return t},h=e=>Object.entries(e).map(e=>({value:e[1],label:e[1]}));(i=o||(o={})).GVL="gvl",i.AC="gacp",i.COMPASS="compass";let g={gvl:{label:"GVL",fullName:"Global Vendor List"},gacp:{label:"AC",fullName:"Google Additional Consent List"},compass:{label:"",fullName:""}},x=e=>{let t=e.split(".")[0];return"gacp"===t?"gacp":"gvl"===t?"gvl":"compass"}},56721:function(e,t,n){n.d(t,{_:function(){return o}});var i=n(27378);function o(e,t){let[n,o]=(0,i.useState)(()=>{if(!e)return t;try{let n=window.localStorage.getItem(e);return n?JSON.parse(n):t}catch(e){return console.error(e),t}});return[n,t=>{try{let i=t instanceof Function?t(n):t;o(i),e&&window.localStorage.setItem(e,JSON.stringify(i))}catch(e){console.error(e)}}]}},77650:function(e,t,n){var i=n(24246),o=n(13054);t.Z=e=>{let{isOpen:t,onClose:n,onConfirm:r,onCancel:l,title:s,message:a,cancelButtonText:c,cancelButtonThemingProps:d,continueButtonText:u,continueButtonThemingProps:h,isLoading:g,returnFocusOnClose:x,isCentered:m,testId:p="confirmation-modal",icon:f}=e;return(0,i.jsxs)(o.u_l,{isOpen:t,onClose:n,size:"lg",returnFocusOnClose:null==x||x,isCentered:m,children:[(0,i.jsx)(o.ZAr,{}),(0,i.jsxs)(o.hzk,{textAlign:"center",p:6,"data-testid":p,children:[f?(0,i.jsx)(o.M5Y,{mb:2,children:f}):null,s?(0,i.jsx)(o.xBx,{fontWeight:"medium",pb:0,children:s}):null,a?(0,i.jsx)(o.fef,{children:a}):null,(0,i.jsx)(o.mzw,{children:(0,i.jsxs)(o.MIq,{columns:2,width:"100%",children:[(0,i.jsx)(o.zxk,{variant:"outline",mr:3,onClick:()=>{l&&l(),n()},"data-testid":"cancel-btn",isDisabled:g,...d,children:c||"Cancel"}),(0,i.jsx)(o.zxk,{colorScheme:"primary",onClick:r,"data-testid":"continue-btn",isLoading:g,...h,children:u||"Continue"})]})})]})]})}},54249:function(e,t,n){n.d(t,{W3:function(){return l},bX:function(){return s},oi:function(){return a},s8:function(){return c}});var i=n(24246),o=n(13054),r=n(27378);let l=[25,50,100],s=e=>{let t=e.getFilteredRowModel().rows.length,{pageIndex:n}=e.getState().pagination,{pageSize:i}=e.getState().pagination,o=e.previousPage,r=!e.getCanPreviousPage(),l=e.nextPage,s=!e.getCanNextPage(),{setPageSize:a}=e;return{totalRows:t,onPreviousPageClick:o,isPreviousPageDisabled:r,onNextPageClick:l,isNextPageDisabled:s,setPageSize:a,startRange:n*i==0?1:n*i,endRange:n*i+i}},a=()=>{let[e,t]=(0,r.useState)(l[0]),[n,i]=(0,r.useState)(1),[o,s]=(0,r.useState)(),a=(0,r.useCallback)(()=>{i(e=>e-1)},[i]),c=(0,r.useMemo)(()=>1===n,[n]),d=(0,r.useCallback)(()=>{i(e=>e+1)},[i]),u=(0,r.useMemo)(()=>n===o,[n,o]),h=(n-1)*e==0?1:(n-1)*e,g=(n-1)*e+e,x=(0,r.useCallback)(()=>{i(1)},[]);return{onPreviousPageClick:a,isPreviousPageDisabled:c,onNextPageClick:d,isNextPageDisabled:u,pageSize:e,setPageSize:e=>{t(e),x()},PAGE_SIZES:l,startRange:h,endRange:g,pageIndex:n,resetPageIndexToDefault:x,setTotalPages:s}},c=e=>{let{pageSizes:t,totalRows:n,onPreviousPageClick:r,isPreviousPageDisabled:l,onNextPageClick:s,isNextPageDisabled:a,setPageSize:c,startRange:d,endRange:u}=e;return(0,i.jsxs)(o.Ugi,{ml:1,mt:3,mb:1,children:[(0,i.jsxs)(o.v2r,{children:[(0,i.jsx)(o.j2t,{as:o.zxk,size:"xs",variant:"ghost","data-testid":"pagination-btn",children:(0,i.jsxs)(o.xvT,{fontSize:"xs",lineHeight:4,fontWeight:"semibold",userSelect:"none",style:{fontVariantNumeric:"tabular-nums"},children:[d.toLocaleString("en"),"-",u<=n?u.toLocaleString("en"):n.toLocaleString("en")," ","of ",n.toLocaleString("en")]})}),(0,i.jsx)(o.qyq,{minWidth:"0",children:t.map(e=>(0,i.jsxs)(o.sNh,{onClick:()=>{c(e)},"data-testid":"pageSize-".concat(e),fontSize:"xs",children:[e," per view"]},e))})]}),(0,i.jsx)(o.hU,{icon:(0,i.jsx)(o.wyc,{}),size:"xs",variant:"outline","aria-label":"previous page",onClick:r,isDisabled:l,children:"previous"}),(0,i.jsx)(o.hU,{icon:(0,i.jsx)(o.XCv,{}),size:"xs",variant:"outline","aria-label":"next page",onClick:s,isDisabled:a,children:"next"})]})}},98320:function(e,t,n){n.d(t,{A4:function(){return m},CI:function(){return p},Cy:function(){return g},G3:function(){return u},Rr:function(){return j},S1:function(){return C},WP:function(){return v},k:function(){return b},mb:function(){return f}});var i=n(24246),o=n(8615),r=n(13054),l=n(27378),s=n(60136),a=n(77650),c=n(16781),d=n(94167);let u=e=>{let{value:t,...n}=e;return(0,i.jsx)(r.kCb,{alignItems:"center",height:"100%",children:(0,i.jsx)(r.xvT,{fontSize:"xs",lineHeight:4,fontWeight:"normal",overflow:"hidden",textOverflow:"ellipsis",...n,children:null!=t?t.toString():t})})},h=e=>{let{children:t,...n}=e;return(0,i.jsx)(r.Cts,{textTransform:"none",fontWeight:"400",fontSize:"xs",lineHeight:4,color:"gray.600",px:2,py:1,boxShadow:"outline"===n.variant?"inset 0 0 0px 1px var(--chakra-colors-gray-100)":void 0,...n,children:t})},g=e=>{let{time:t}=e;if(!t)return(0,i.jsx)(u,{value:"N/A"});let n=(0,o.Z)(new Date(t),new Date,{addSuffix:!0}),l=(0,d.p6)(new Date(t));return(0,i.jsx)(r.kCb,{alignItems:"center",height:"100%",children:(0,i.jsx)(r.ua7,{label:l,hasArrow:!0,children:(0,i.jsx)(r.xvT,{fontSize:"xs",lineHeight:4,fontWeight:"normal",overflow:"hidden",textOverflow:"ellipsis",children:(0,d.G8)(n)})})})},x=e=>{let{children:t,...n}=e;return(0,i.jsx)(r.kCb,{alignItems:"center",height:"100%",mr:2,...n,children:t})},m=e=>{let{value:t,suffix:n,...o}=e;return(0,i.jsx)(x,{children:(0,i.jsxs)(h,{...o,children:[t,n]})})},p=e=>{let{count:t,singSuffix:n,plSuffix:o,...r}=e,l=null;return l=1===t?(0,i.jsxs)(h,{...r,children:[t,n?" ".concat(n):null]}):(0,i.jsxs)(h,{...r,children:[t,o?" ".concat(o):null]}),(0,i.jsx)(x,{children:l})},f=e=>{let{values:t,cellProps:n,...o}=e,{isExpanded:s,isWrapped:a,version:c}=(null==n?void 0:n.cellState)||{},[d,u]=(0,l.useState)(!s),[g,x]=(0,l.useState)(!!a),[m,p]=(0,l.useState)(s?t:null==t?void 0:t.slice(0,2));return(0,l.useEffect)(()=>{u(!s)},[s,c]),(0,l.useEffect)(()=>{x(!!a)},[a]),(0,l.useEffect)(()=>{(null==t?void 0:t.length)&&p(d?t.slice(0,2):t)},[d,t]),(0,l.useMemo)(()=>(null==m?void 0:m.length)?(0,i.jsxs)(r.kCb,{alignItems:d?"center":"flex-start",flexDirection:d||g?"row":"column",flexWrap:g?"wrap":"nowrap",gap:1.5,pt:2,pb:2,onClick:e=>{d||(e.stopPropagation(),u(!0))},cursor:d?void 0:"pointer",children:[m.map(e=>(0,i.jsx)(h,{"data-testid":e.key,...o,children:e.label},e.key)),d&&t&&t.length>2&&(0,i.jsxs)(r.zxk,{variant:"link",size:"xs",fontWeight:400,onClick:()=>u(!1),display:"inline-block",children:["+",t.length-2," more"]})]}):null,[m,d,g,t,o])},v=e=>{let{value:t,suffix:n,cellState:o,ignoreZero:l,badgeProps:s}=e,a=null;return t?(a=Array.isArray(t)?1===t.length?(0,i.jsx)(h,{...s,children:t}):(null==o?void 0:o.isExpanded)&&t.length>0?t.map((e,t)=>(0,i.jsx)(r.xuv,{mr:2,children:(0,i.jsx)(h,{...s,children:e})},(null==e?void 0:e.toString())||t)):(0,i.jsxs)(h,{...s,children:[t.length,n?" ".concat(n):null]}):(0,i.jsx)(h,{...s,children:t}),(0,i.jsx)(r.kCb,{alignItems:"center",height:"100%",mr:"2",overflowX:"hidden",children:a})):l?null:(0,i.jsxs)(h,{...s,children:["0",n?" ".concat(n):""]})},b=e=>{let{dataTestId:t,...n}=e;return(0,i.jsx)(r.kCb,{alignItems:"center",justifyContent:"center",onClick:e=>e.stopPropagation(),children:(0,i.jsx)(r.XZJ,{"data-testid":t||void 0,...n,colorScheme:"purple"})})},j=e=>{let{value:t,...n}=e;return(0,i.jsx)(r.xvT,{fontSize:"xs",lineHeight:9,fontWeight:"medium",flex:1,...n,children:t})},C=e=>{let{enabled:t,onToggle:n,title:o,message:l,isDisabled:d,...u}=e,h=(0,r.qY0)(),g=(0,r.pmc)(),x=async e=>{let{enable:t}=e,i=await n(t);(0,s.D4)(i)&&g((0,c.Vo)((0,s.e$)(i.error)))},m=async e=>{let{checked:t}=e.target;t?await x({enable:!0}):h.onOpen()};return(0,i.jsxs)(i.Fragment,{children:[(0,i.jsx)(r.rsf,{colorScheme:"complimentary",isChecked:t,"data-testid":"toggle-switch",isDisabled:d,onChange:m,...u}),(0,i.jsx)(a.Z,{isOpen:h.isOpen,onClose:h.onClose,onConfirm:()=>{x({enable:!1}),h.onClose()},title:o,message:(0,i.jsx)(r.xvT,{color:"gray.500",children:l}),continueButtonText:"Confirm",isCentered:!0,icon:(0,i.jsx)(r.aNP,{color:"orange.100"})})]})}},52850:function(e,t,n){n.d(t,{A4:function(){return i.A4},CI:function(){return i.CI},F1:function(){return m},G3:function(){return i.G3},Rr:function(){return i.Rr},vr:function(){return I},ZK:function(){return R},HO:function(){return A},WP:function(){return i.WP},k:function(){return i.k},W3:function(){return O.W3},s8:function(){return O.s8},AA:function(){return _},Q$:function(){return L},I4:function(){return N},bX:function(){return O.bX},oi:function(){return O.oi}});var i=n(98320),o=n(24246),r=n(13054),l=n(27378),s=n(65201),a=n(75383),c=n(52202);let d="DraggableColumnListItem",u=e=>{let{id:t,index:n,moveColumn:i,setColumnVisible:o}=e,r=(0,l.useRef)(null),[{handlerId:s},u]=(0,a.L)({accept:d,collect:e=>({handlerId:e.getHandlerId()}),hover(e,t){var o;if(!r.current)return;let l=e.index;if(l===n)return;let s=null===(o=r.current)||void 0===o?void 0:o.getBoundingClientRect(),a=(s.bottom-s.top)/2,c=t.getClientOffset().y-s.top;l<n&&c<a||l>n&&c>a||(i(l,n),Object.assign(e,{index:n}))}}),[{isDragging:h},g,x]=(0,c.c)({type:d,item:()=>({id:t,index:n}),collect:e=>({isDragging:!!e.isDragging()})});return g(u(r)),{isDragging:h,ref:r,handlerId:s,preview:x,handleColumnVisibleToggle:e=>{o(n,e.target.checked)}}},h=e=>{let{id:t,index:n,isVisible:i,moveColumn:l,setColumnVisible:s,text:a}=e,{ref:c,isDragging:d,handlerId:h,preview:g,handleColumnVisibleToggle:x}=u({index:n,id:t,moveColumn:l,setColumnVisible:s});return(0,o.jsxs)(r.HCh,{alignItems:"center",display:"flex",minWidth:0,ref:e=>{g(e)},"data-handler-id":h,opacity:d?.2:1,children:[(0,o.jsx)(r.xuv,{ref:c,cursor:d?"grabbing":"grab",children:(0,o.jsx)(r.DE2,{as:r.zGR,color:"gray.300",flexShrink:0,height:"20px",width:"20px",_hover:{color:"gray.700"}})}),(0,o.jsxs)(r.NIc,{alignItems:"center",display:"flex",minWidth:0,title:a,children:[(0,o.jsx)(r.lXp,{color:"gray.700",fontSize:"normal",fontWeight:400,htmlFor:"".concat(t),mb:"0",minWidth:0,overflow:"hidden",textOverflow:"ellipsis",whiteSpace:"nowrap",flexGrow:1,children:a}),(0,o.jsx)(r.rsf,{colorScheme:"complimentary",id:"".concat(t),mr:2,isChecked:i,onChange:x})]})]})},g=e=>{let{columns:t}=e,[n,i]=(0,l.useState)(null!=t?t:[]);return(0,l.useEffect)(()=>{i((null==t?void 0:t.map(e=>({...e})))||[])},[t]),{columns:n,moveColumn:(0,l.useCallback)((e,t)=>{i(n=>(0,s.ZP)(n,n=>{let i=n[e];n.splice(e,1),n.splice(t,0,i)}))},[]),setColumnVisible:(0,l.useCallback)((e,t)=>{i(n=>(0,s.ZP)(n,n=>{n[e]&&(n[e].isVisible=t)}))},[])}},x=e=>{let{columns:t,columnEditor:n}=e;return(0,o.jsx)(r.aVo,{spacing:4,children:t.map((e,t)=>(0,o.jsx)(h,{id:e.id,index:t,isVisible:e.isVisible,moveColumn:n.moveColumn,setColumnVisible:n.setColumnVisible,text:e.displayText},e.id))})},m=e=>{let{isOpen:t,onClose:n,headerText:i,tableInstance:s,prefixColumns:a,onColumnOrderChange:c}=e,d=g({columns:(0,l.useMemo)(()=>s.getAllColumns().filter(e=>!a.includes(e.id)).map(e=>{var t,n,i;return{id:e.id,displayText:(null===(n=e.columnDef)||void 0===n?void 0:null===(t=n.meta)||void 0===t?void 0:t.displayText)||e.id,isVisible:null!==(i=s.getState().columnVisibility[e.id])&&void 0!==i?i:e.getIsVisible()}}).sort((e,t)=>{let{columnOrder:n}=s.getState(),i=n.indexOf(e.id),o=n.indexOf(t.id);return -1===i&&-1===o?0:-1===i?1:-1===o?-1:i-o}),[])}),u=(0,l.useCallback)(()=>{c([...a,...d.columns.map(e=>e.id)]),s.setColumnVisibility(d.columns.reduce((e,t)=>(e[t.id]=t.isVisible,e),{})),n()},[n,a,s,d.columns,c]);return(0,o.jsxs)(r.u_l,{isOpen:t,onClose:n,isCentered:!0,size:"2xl",children:[(0,o.jsx)(r.ZAr,{}),(0,o.jsxs)(r.hzk,{children:[(0,o.jsx)(r.xBx,{pb:0,children:i}),(0,o.jsx)(r.olH,{}),(0,o.jsxs)(r.fef,{children:[(0,o.jsx)(r.xvT,{fontSize:"sm",color:"gray.500",mb:2,children:"You can toggle columns on and off to hide or show them in the table. Additionally, you can drag columns up or down to change the order"}),(0,o.jsxs)(r.mQc,{colorScheme:"complimentary",children:[(0,o.jsx)(r.tdY,{children:(0,o.jsx)(r.OK9,{color:"complimentary.500",children:"Columns"})}),(0,o.jsx)(r.nPR,{children:(0,o.jsx)(r.x45,{p:0,pt:4,maxHeight:"270px",overflowY:"scroll",children:(0,o.jsx)(x,{columns:d.columns,columnEditor:d})})})]})]}),(0,o.jsx)(r.mzw,{children:(0,o.jsxs)(r.xuv,{display:"flex",justifyContent:"space-between",width:"100%",children:[(0,o.jsx)(r.zxk,{variant:"outline",size:"sm",mr:3,onClick:n,flexGrow:1,children:"Cancel"}),(0,o.jsx)(r.zxk,{"data-testid":"save-button",colorScheme:"primary",size:"sm",onClick:u,flexGrow:1,children:"Save"})]})})]})]})};var p=n(59003),f=n(56721),v=n(62528);let b=e=>"select"===e?{padding:"0px"}:{paddingLeft:r.rSc.space[3],paddingRight:"calc(".concat(r.rSc.space[3]," - 5px)"),paddingTop:"0px",paddingBottom:"0px",borderRadius:"0px"},j=(e,t)=>{let n=t.find(t=>t.startsWith(e));return n?parseInt(n.split("::")[1],10):void 0},C=e=>{var t,n,i,l,s,a;let c,{cell:d,onRowClick:u,cellState:h}=e,g=d.getContext().table.getState().grouping.length>0,x=g?d.getContext().table.getState().grouping[0]:void 0,m=d.column.id===x,f=!1,v=!1,j=!1,C=d.getContext().table.getRowModel().rows.filter(e=>!e.id.includes(":")),w=C[0].id===d.row.id,S=C[C.length-1].id===d.row.id;if(d.getValue()&&m){let e=d.getContext().table.getRow("".concat(d.column.id,":").concat(d.getValue()));j=1===e.subRows.length,f=e.subRows[0].id===d.row.id,v=e.subRows[e.subRows.length-1].id===d.row.id}let y=(!m||f)&&!!(null===(t=d.column.columnDef.meta)||void 0===t?void 0:t.onCellClick);return(null===(n=d.column.columnDef.meta)||void 0===n?void 0:n.disableRowClick)||!u?y&&(c=()=>{var e,t;null===(t=d.column.columnDef.meta)||void 0===t||null===(e=t.onCellClick)||void 0===e||e.call(t,d.row.original)}):c=e=>{u(d.row.original,e)},(0,o.jsx)(r.Td,{width:(null===(i=d.column.columnDef.meta)||void 0===i?void 0:i.width)?d.column.columnDef.meta.width:"unset",overflowX:(null===(l=d.column.columnDef.meta)||void 0===l?void 0:l.overflow)?null===(s=d.column.columnDef.meta)||void 0===s?void 0:s.overflow:"auto",borderBottomWidth:S||m?"0px":"1px",borderBottomColor:"gray.200",borderRightWidth:"1px",borderRightColor:"gray.200",sx:{article:{borderTopWidth:"2x",borderTopColor:"red"},...b(d.column.id),maxWidth:"calc(var(--col-".concat(d.column.id,"-size) * 1px)"),minWidth:"calc(var(--col-".concat(d.column.id,"-size) * 1px)"),"&:hover":{backgroundColor:y?"gray.50":void 0,cursor:y?"pointer":void 0}},_hover:!u||(null===(a=d.column.columnDef.meta)||void 0===a?void 0:a.disableRowClick)?void 0:{cursor:"pointer"},_first:{borderBottomWidth:!g&&!S||v&&!w||f&&j?"1px":"0px"},_last:{borderRightWidth:0},height:"inherit",onClick:c,"data-testid":"row-".concat(d.row.id,"-col-").concat(d.column.id),children:!d.getIsPlaceholder()||f?(0,p.ie)(d.column.columnDef.cell,{...d.getContext(),cellState:h}):null})},w=e=>{let{row:t,renderRowTooltipLabel:n,onRowClick:i,expandedColumns:l,wrappedColumns:s}=e;if(t.getIsGrouped())return null;let a=(0,o.jsx)(r.Tr,{height:"36px",_hover:i?{backgroundColor:"gray.50"}:void 0,"data-testid":"row-".concat(t.id),backgroundColor:t.getCanSelect()?void 0:"gray.50",children:t.getVisibleCells().map(e=>{let t=j(e.column.id,l),n={isExpanded:!!t&&t>0,isWrapped:!!s.find(t=>t===e.column.id),version:t};return(0,o.jsx)(C,{cell:e,onRowClick:i,cellState:n},e.id)})},t.id);return n?(0,o.jsx)(r.ua7,{label:n?n(t):void 0,hasArrow:!0,placement:"top",children:a}):a},S={asc:{icon:(0,o.jsx)(r.Hf3,{}),title:"Sort ascending"},desc:{icon:(0,o.jsx)(r.veu,{}),title:"Sort descending"}},y={height:r.rSc.space[9],width:"100%",textAlign:"start","&:focus-visible":{backgroundColor:"gray.100"},"&:focus":{outline:"none"}},k=e=>{var t,n,i,l,s,a,c,d;let{header:u,onGroupAll:h,onExpandAll:g,onWrapToggle:x,isExpandAll:m,isWrapped:f,enableSorting:j}=e,{meta:C}=u.column.columnDef;return(null==C?void 0:C.showHeaderMenu)?(0,o.jsxs)(r.v2r,{placement:"bottom-end",closeOnSelect:!C.showHeaderMenuWrapOption,children:[(0,o.jsx)(r.j2t,{as:r.zxk,rightIcon:(0,o.jsxs)(r.Ugi,{children:[null===(t=S[u.column.getIsSorted()])||void 0===t?void 0:t.icon,(0,o.jsx)(r.nXP,{transform:"rotate(90deg)"})]}),title:"Column options",variant:"ghost",size:"sm",sx:{...b(u.column.id),...y},"data-testid":"".concat(u.id,"-header-menu"),children:(0,p.ie)(u.column.columnDef.header,u.getContext())}),(0,o.jsx)(r.h_i,{children:(0,o.jsxs)(r.qyq,{fontSize:"xs",minW:"0",w:"158px","data-testid":"".concat(u.id,"-header-menu-list"),children:[(0,o.jsxs)(r.sNh,{gap:2,color:m?"complimentary.500":void 0,onClick:()=>g(u.id),children:[(0,o.jsx)(v.oq,{})," Expand all"]}),(0,o.jsxs)(r.sNh,{gap:2,color:m?void 0:"complimentary.500",onClick:()=>h(u.id),children:[(0,o.jsx)(v.Kc,{})," Collapse all"]}),j&&u.column.getCanSort()&&(0,o.jsxs)(r.sNh,{gap:2,onClick:u.column.getToggleSortingHandler(),children:[null!==(c=null===(n=S[u.column.getNextSortingOrder()])||void 0===n?void 0:n.icon)&&void 0!==c?c:(0,o.jsx)(r.Dbz,{}),null!==(d=null===(i=S[u.column.getNextSortingOrder()])||void 0===i?void 0:i.title)&&void 0!==d?d:"Clear sort"]}),C.showHeaderMenuWrapOption&&(0,o.jsxs)(o.Fragment,{children:[(0,o.jsx)(r.RaW,{}),(0,o.jsx)(r.xuv,{px:3,children:(0,o.jsx)(r.XZJ,{size:"sm",isChecked:f,onChange:()=>x(u.id,!f),colorScheme:"complimentary",children:(0,o.jsx)(r.xvT,{fontSize:"xs",children:"Wrap results"})})})]})]})})]}):j&&u.column.getCanSort()?(0,o.jsx)(r.zxk,{"data-testid":"".concat(u.id,"-header-sort"),onClick:u.column.getToggleSortingHandler(),rightIcon:null===(l=S[u.column.getIsSorted()])||void 0===l?void 0:l.icon,title:null!==(a=null===(s=S[u.column.getNextSortingOrder()])||void 0===s?void 0:s.title)&&void 0!==a?a:"Clear sort",variant:"ghost",size:"sm",sx:{...b(u.column.id),...y},children:(0,p.ie)(u.column.columnDef.header,u.getContext())}):(0,o.jsx)(r.xuv,{"data-testid":"".concat(u.id,"-header"),sx:{...b(u.column.id)},fontSize:"xs",lineHeight:9,fontWeight:"medium",children:(0,p.ie)(u.column.columnDef.header,u.getContext())})},z=e=>{var t;let{tableInstance:n,rowActionBar:i,onRowClick:l,getRowIsClickable:s,renderRowTooltipLabel:a,expandedColumns:c,wrappedColumns:d,emptyTableNotice:u}=e,h=e=>s?s(e)?l:void 0:l;return(0,o.jsxs)(r.p3B,{"data-testid":"fidesTable-body",children:[i,n.getRowModel().rows.map(e=>(0,o.jsx)(w,{row:e,onRowClick:h(e.original),renderRowTooltipLabel:a,expandedColumns:c,wrappedColumns:d},e.id)),0===n.getRowModel().rows.length&&!(null===(t=n.getState())||void 0===t?void 0:t.globalFilter)&&u&&(0,o.jsx)(r.Tr,{children:(0,o.jsx)(r.Td,{colSpan:100,children:u})})]})},W=l.memo(z,(e,t)=>e.tableInstance.options.data===t.tableInstance.options.data),R=e=>{let{tableInstance:t,rowActionBar:n,footer:i,onRowClick:s,getRowIsClickable:a,renderRowTooltipLabel:c,emptyTableNotice:d,overflow:u="auto",onSort:h,enableSorting:g=!!h,columnExpandStorageKey:x,columnWrapStorageKey:m}=e,[p,v]=(0,l.useState)(1),[b,C]=(0,f._)(x,[]),[w,S]=(0,f._)(m,[]),y=e=>{C([...b.filter(t=>t.split("::")[0]!==e),"".concat(e).concat("::").concat(p)]),v(p+1)},R=e=>{C([...b.filter(t=>t.split("::")[0]!==e),"".concat(e).concat("::").concat(-1*p)]),v(p+1)},I=(e,t)=>{S(t?[...w,e]:w.filter(t=>t!==e))},T=(0,l.useMemo)(()=>{let e=t.getFlatHeaders(),n={};for(let r=0;r<e.length;r+=1){var i,o;let l=e[r],s=!!(null===(i=t.getState().columnSizing)||void 0===i?void 0:i[l.id]),a="auto"===(null===(o=l.column.columnDef.meta)||void 0===o?void 0:o.width);!s&&a?setTimeout(()=>{var e;let i=null===(e=document.getElementById("column-".concat(l.id)))||void 0===e?void 0:e.offsetWidth;i&&(t.setColumnSizing(e=>({...e,[l.id]:i})),n["--header-".concat(l.id,"-size")]=i,n["--col-".concat(l.column.id,"-size")]=i)}):(n["--header-".concat(l.id,"-size")]=l.getSize(),n["--col-".concat(l.column.id,"-size")]=l.column.getSize())}return n},[t.getState().columnSizingInfo]);return(0,l.useEffect)(()=>{h&&h(t.getState().sorting[0])},[t.getState().sorting]),(0,o.jsx)(r.xJi,{"data-testid":"fidesTable",overflowY:u,overflowX:u,borderColor:"gray.200",borderBottomWidth:"1px",borderRightWidth:"1px",borderLeftWidth:"1px",children:(0,o.jsxs)(r.iA_,{variant:"unstyled",style:{borderCollapse:"separate",borderSpacing:0,...T,minWidth:"100%"},children:[(0,o.jsx)(r.hrZ,{position:"sticky",top:"0",height:"36px",zIndex:10,backgroundColor:"gray.50",children:t.getHeaderGroups().map(e=>(0,o.jsx)(r.Tr,{height:"inherit",children:e.headers.map(e=>{let t=j(e.id,b);return(0,o.jsxs)(r.Th,{borderColor:"gray.200",borderTopWidth:"1px",borderBottomWidth:"1px",borderRightWidth:"1px",_last:{borderRightWidth:0},colSpan:e.colSpan,"data-testid":"column-".concat(e.id),id:"column-".concat(e.id),sx:{padding:0,width:"calc(var(--header-".concat(e.id,"-size) * 1px)"),overflowX:"auto"},textTransform:"unset",position:"relative",_hover:{"& .resizer":{opacity:1}},children:[(0,o.jsx)(k,{header:e,onGroupAll:R,onExpandAll:y,onWrapToggle:I,isExpandAll:!!t&&t>0,isWrapped:!!w.find(t=>e.id===t),enableSorting:g}),e.column.getCanResize()?(0,o.jsx)(r.xuv,{onDoubleClick:()=>e.column.resetSize(),onMouseDown:e.getResizeHandler(),position:"absolute",height:"100%",top:"0",right:"0",width:"5px",cursor:"col-resize",userSelect:"none",className:"resizer",opacity:0,backgroundColor:e.column.getIsResizing()?"complimentary.500":"gray.200"}):null]},e.id)})},e.id))}),t.getState().columnSizingInfo.isResizingColumn?(0,o.jsx)(W,{tableInstance:t,rowActionBar:n,onRowClick:s,getRowIsClickable:a,renderRowTooltipLabel:c,expandedColumns:b,wrappedColumns:w,emptyTableNotice:d}):(0,o.jsx)(z,{tableInstance:t,rowActionBar:n,onRowClick:s,getRowIsClickable:a,renderRowTooltipLabel:c,expandedColumns:b,wrappedColumns:w,emptyTableNotice:d}),i]})})},I=e=>{let{totalColumns:t,children:n}=e;return(0,o.jsx)(r.$RU,{backgroundColor:"gray.50",children:(0,o.jsx)(r.Tr,{children:(0,o.jsx)(r.Td,{colSpan:t,px:4,py:2,borderTop:"1px solid",borderColor:"gray.200",children:n})})})};var T=n(33312),D=n(94167);let A=e=>{let{globalFilter:t,setGlobalFilter:n,placeholder:i,testid:s="global-text-filter"}=e,[a,c]=(0,l.useState)(t),d=(0,l.useMemo)(()=>(0,D.Ds)(n,200),[n]),u=(0,l.useCallback)(()=>{c(void 0),n(void 0)},[c,n]);return(0,l.useEffect)(()=>{a||u()},[a,u]),(0,o.jsx)(r.xuv,{maxWidth:"510px",width:"100%",children:(0,o.jsx)(T.Z,{onChange:e=>{c(e),d(e)},onClear:u,search:a||"",placeholder:i,"data-testid":s})})};var O=n(54249);let _=e=>{let{tableInstance:t,selectedRows:n,isOpen:i}=e;return i?(0,o.jsx)(r.Tr,{position:"sticky",zIndex:"10",top:"36px",backgroundColor:"purple.100",height:"36px",p:0,boxShadow:"0px 4px 6px -1px rgba(0, 0, 0, 0.05)",children:(0,o.jsx)(r.Td,{borderWidth:"1px",borderColor:"gray.200",height:"inherit",pl:4,pr:2,py:0,colSpan:t.getAllColumns().length,children:(0,o.jsxs)(r.Ugi,{children:[(0,o.jsxs)(r.xvT,{"data-testid":"selected-row-count",fontSize:"xs",children:[n.toLocaleString("en")," row(s) selected."]}),t.getIsAllRowsSelected()?null:(0,o.jsxs)(r.zxk,{"data-testid":"select-all-rows-btn",onClick:()=>{t.toggleAllRowsSelected()},variant:"link",color:"black",fontSize:"xs",fontWeight:"400",textDecoration:"underline",children:["Select all ",t.getFilteredRowModel().rows.length," rows."]})]})})}):null},L=e=>{let{children:t,...n}=e;return(0,o.jsx)(r.Ugi,{justifyContent:"space-between",alignItems:"center",p:2,borderWidth:"1px",borderBottomWidth:"0px",borderColor:"gray.200",zIndex:11,...n,children:t})},N=e=>{let{rowHeight:t,numRows:n}=e,i=[];for(let e=0;e<n;e+=1)i.push((0,o.jsx)(r.OdW,{height:"".concat(t,"px")},e));return(0,o.jsx)(r.Kqy,{children:i})}},16781:function(e,t,n){n.d(t,{MA:function(){return s},Vo:function(){return c},t5:function(){return a}});var i=n(24246),o=n(13054);let r=e=>{let{children:t}=e;return(0,i.jsxs)(o.xvT,{"data-testid":"toast-success-msg",children:[(0,i.jsx)("strong",{children:"Success:"})," ",t]})},l=e=>{let{children:t}=e;return(0,i.jsxs)(o.xvT,{"data-testid":"toast-error-msg",children:[(0,i.jsx)("strong",{children:"Error:"})," ",t]})},s={variant:"subtle",position:"top",description:"",duration:5e3,status:"success",isClosable:!0},a=e=>{let t=(0,i.jsx)(r,{children:e});return{...s,description:t}},c=e=>{let t=(0,i.jsx)(l,{children:e});return{...s,description:t,status:"error"}}},41164:function(e,t,n){n.d(t,{Bw:function(){return l},D4:function(){return o},Dy:function(){return a},XD:function(){return c},cz:function(){return d},hE:function(){return s},oK:function(){return r}});var i=n(76649);let o=e=>"error"in e,r=e=>(0,i.Ln)({status:"string"},e)&&"PARSING_ERROR"===e.status,l=e=>(0,i.Ln)({status:"number",data:{}},e),s=e=>(0,i.Ln)({detail:"string"},e),a=e=>(0,i.Ln)({detail:{error:"string",resource_type:"string",fides_key:"string"}},e),c=e=>(0,i.Ln)({detail:{error:"string",resource_type:"string",fides_key:"string"}},e),d=e=>(0,i.Ln)({detail:[{loc:["string","number"],msg:"string",type:"string"}]},e)}}]);