"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[3273],{43124:function(e,i,t){t.d(i,{Z:function(){return h}});var n=t(24246),r=t(13054),s=t(88038),a=t.n(s),l=t(86677);t(27378);var o=t(11596),c=t(72247),d=t(11032),u=()=>{let e=(0,l.useRouter)();return(0,n.jsx)(r.xuv,{bg:"gray.50",border:"1px solid",borderColor:"blue.400",borderRadius:"md",justifyContent:"space-between",p:5,mb:5,mt:5,children:(0,n.jsxs)(r.xuv,{children:[(0,n.jsxs)(r.Kqy,{direction:{base:"column",sm:"row"},justifyContent:"space-between",children:[(0,n.jsx)(r.xvT,{fontWeight:"semibold",children:"Configure your storage and messaging provider"}),(0,n.jsx)(r.zxk,{size:"sm",variant:"outline",onClick:()=>{e.push(d.fz)},children:"Configure"})]}),(0,n.jsxs)(r.xvT,{children:["Before Fides can process your privacy requests we need two simple steps to configure your storage and email client."," "]})]})})},h=e=>{let{children:i,title:t,padded:s=!0,mainProps:d}=e,h=(0,o.hz)(),x=(0,l.useRouter)(),p="/privacy-requests"===x.pathname||"/datastore-connection"===x.pathname,m=!(h.flags.privacyRequestsConfiguration&&p),{data:f}=(0,c.JE)(void 0,{skip:m}),{data:g}=(0,c.PW)(void 0,{skip:m}),v=h.flags.privacyRequestsConfiguration&&(!f||!g)&&p;return(0,n.jsxs)(r.kCb,{"data-testid":t,direction:"column",h:"100vh",children:[(0,n.jsxs)(a(),{children:[(0,n.jsxs)("title",{children:["Fides Admin UI - ",t]}),(0,n.jsx)("meta",{name:"description",content:"Privacy Engineering Platform"}),(0,n.jsx)("link",{rel:"icon",href:"/favicon.ico"})]}),(0,n.jsxs)(r.kCb,{as:"main",direction:"column",py:s?6:0,px:s?10:0,h:s?"calc(100% - 48px)":"full",flex:1,minWidth:0,overflow:"auto",...d,children:[v?(0,n.jsx)(u,{}):null,i]})]})}},65399:function(e,i,t){t.d(i,{HK:function(){return s},VY:function(){return n.V},O3:function(){return l}});var n=t(75139),r=t(60136);let s=()=>{let{errorAlert:e}=(0,n.V)();return{handleError:i=>{let t="An unexpected error occurred. Please try again.";(0,r.Ot)(i)?t=i.data.detail:(0,r.tB)(i)&&(t=i.data.detail[0].msg),e(t)}}};var a=t(27378);let l=e=>{let i=(0,a.useRef)(void 0);return(0,a.useEffect)(()=>{let t=t=>{var n;(null===(n=i.current)||void 0===n?void 0:n.contains(t.target))||e()};return document.addEventListener("mousedown",t),()=>{document.removeEventListener("mousedown",t)}},[i,e]),{ref:i}}},75139:function(e,i,t){t.d(i,{V:function(){return s}});var n=t(24246),r=t(13054);let s=()=>{let e=(0,r.pmc)();return{errorAlert:(i,t,s)=>{let a={...s,position:(null==s?void 0:s.position)||"top",render:e=>{let{onClose:s}=e;return(0,n.jsxs)(r.bZj,{alignItems:"normal",status:"error",children:[(0,n.jsx)(r.zMQ,{}),(0,n.jsxs)(r.xuv,{children:[t&&(0,n.jsx)(r.CdC,{children:t}),(0,n.jsx)(r.XaZ,{children:i})]}),(0,n.jsx)(r.PZ7,{onClick:s,position:"relative",right:0,size:"sm",top:-1})]})}};(null==s?void 0:s.id)&&e.isActive(s.id)?e.update(s.id,a):e(a)},successAlert:(i,t,s)=>{let a={...s,position:(null==s?void 0:s.position)||"top",render:e=>{let{onClose:s}=e;return(0,n.jsxs)(r.bZj,{alignItems:"normal",status:"success",variant:"subtle",children:[(0,n.jsx)(r.zMQ,{}),(0,n.jsxs)(r.xuv,{children:[t&&(0,n.jsx)(r.CdC,{children:t}),(0,n.jsx)(r.XaZ,{children:i})]}),(0,n.jsx)(r.PZ7,{onClick:s,position:"relative",right:0,size:"sm",top:-1})]})}};(null==s?void 0:s.id)&&e.isActive(s.id)?e.update(s.id,a):e(a)}}}},73485:function(e,i,t){t.d(i,{R:function(){return l}});var n=t(24246),r=t(13054),s=t(79894),a=t.n(s);let l=e=>{let{onClick:i,...t}=e;return(0,n.jsxs)(r.kCb,{alignItems:"center",mt:-4,mb:3,onClick:i,cursor:"pointer",...t,children:[(0,n.jsx)(r.hU,{"aria-label":"Back",icon:(0,n.jsx)(r.Rpv,{}),mr:2,size:"xs",variant:"outline"}),(0,n.jsx)(r.xvT,{as:"a",fontSize:"sm",fontWeight:"500",children:"Back"})]})};i.Z=e=>{let{backPath:i,...t}=e;return(0,n.jsxs)(r.kCb,{alignItems:"center",mb:6,...t,children:[(0,n.jsx)(r.hU,{as:a(),href:i,"aria-label":"Back",icon:(0,n.jsx)(r.Rpv,{}),mr:2,size:"xs",variant:"outline"}),(0,n.jsx)(r.xvT,{as:a(),href:i,fontSize:"sm",fontWeight:"500",children:"Back"})]})}},73025:function(e,i,t){var n=t(24246);t(27378);var r=t(43124);i.Z=e=>{let{children:i}=e;return(0,n.jsx)(r.Z,{title:"Connections",children:i})}},59201:function(e,i,t){t.d(i,{s:function(){return E}});var n=t(24246),r=t(69728),s=t(13054),a=t(86677),l=t(27378),o=t(44296),c=t(11032),d=t(19686),u=t(65399),h=t(75139),x=t(7564),p=t(45007),m=t(34090);let f=(e,i)=>{let t={...e};return Object.entries(i.properties).forEach(i=>{let[n,r]=i;if("integer"===r.type){let i=r.default?Number(r.default):e[n];t[n]=i||0}else{var s;let i=null!==(s=r.default)&&void 0!==s?s:e[n];t[n]=null!=i?i:null}}),t},g="#/definitions/FidesDatasetReference";var v=e=>{let{data:i,defaultValues:t,isSubmitting:a=!1,onSaveClick:c,onTestConnectionClick:h,testButtonLabel:p="Test connection"}=e,v=(0,l.useRef)(!1),{handleError:y}=(0,u.HK)(),{connection:j,connectionOption:b}=(0,o.C)(r.ZZ),[k,C]=(0,x.h2)(),_=e=>{let i;return(void 0===e||""===e)&&(i="Connection Identifier is required"),e&&(0,s.kEn)(e)&&(i="Connection Identifier must be an alphanumeric value"),i},w=(e,i,t)=>{let n;return(void 0===i||""===i)&&(n="".concat(e," is required")),t===g&&(i.includes(".")?i.split(".").length<3&&(n="Dataset reference must include at least three parts"):n="Dataset reference must be dot delimited"),n},S=(e,i)=>(0,n.jsx)(s.lXp,{color:"gray.900",fontSize:"14px",fontWeight:"semibold",htmlFor:e,minWidth:"150px",children:i}),z=e=>{var i;if((null===(i=e.allOf)||void 0===i?void 0:i[0].$ref)===g)return"Enter dataset.collection.field"},I=(e,t)=>{var r;return(0,n.jsx)(m.gN,{id:e,name:e,validate:(null!==(r=i.required)&&void 0!==r&&!!r.includes(e)||"integer"===t.type)&&(e=>{var i;return w(t.title,e,null===(i=t.allOf)||void 0===i?void 0:i[0].$ref)}),children:r=>{var a;let{field:l,form:o}=r;return(0,n.jsxs)(s.NIc,{display:"flex",isRequired:null===(a=i.required)||void 0===a?void 0:a.includes(e),isInvalid:o.errors[e]&&o.touched[e],children:[S(e,t.title),(0,n.jsxs)(s.gCW,{align:"flex-start",w:"inherit",children:["integer"!==t.type&&(0,n.jsx)(s.IIB,{...l,value:l.value||"",placeholder:z(t),autoComplete:"off",color:"gray.700",size:"sm"}),"integer"===t.type&&(0,n.jsxs)(s.Y2U,{allowMouseWheel:!0,color:"gray.700",defaultValue:0,min:0,size:"sm",children:[(0,n.jsx)(s.zuI,{...l,autoComplete:"off"}),(0,n.jsxs)(s.FiK,{children:[(0,n.jsx)(s.WQu,{}),(0,n.jsx)(s.Y_d,{})]})]}),(0,n.jsx)(s.J1D,{children:o.errors[e]})]}),(0,n.jsx)(s.ua7,{"aria-label":t.description,hasArrow:!0,label:t.description,placement:"right-start",openDelay:500,children:(0,n.jsx)(s.kCb,{alignItems:"center",h:"32px",visibility:t.description?"visible":"hidden",children:(0,n.jsx)(s.ITP,{marginLeft:"8px",_hover:{cursor:"pointer"}})})})]})}},e)},R=async()=>{try{await k(j.key).unwrap()}catch(e){y(e)}};return(0,l.useEffect)(()=>(v.current=!0,C.isSuccess&&h(C),()=>{v.current=!1}),[h,C]),(0,n.jsx)(m.J9,{enableReinitialize:!0,initialValues:(()=>{let e={...t};if(null==j?void 0:j.key){var n,r;e.name=null!==(r=j.name)&&void 0!==r?r:"",e.description=j.description,e.instance_key=j.connection_type===d.Rj.SAAS?null===(n=j.saas_config)||void 0===n?void 0:n.fides_key:j.key}return f(e,i)})(),onSubmit:(e,t)=>{let n={...e};Object.keys(i.properties).forEach(t=>{var r;if((null===(r=i.properties[t].allOf)||void 0===r?void 0:r[0].$ref)===g){let i=e[t].split(".");n[t]={dataset:i.shift(),field:i.join("."),direction:"from"}}}),c(n,t)},validateOnBlur:!1,validateOnChange:!1,children:e=>(0,n.jsx)(m.l0,{noValidate:!0,children:(0,n.jsxs)(s.gCW,{align:"stretch",gap:"16px",children:[(0,n.jsx)(m.gN,{id:"name",name:"name",validate:e=>w("Name",e),children:i=>{let{field:t}=i;return(0,n.jsxs)(s.NIc,{display:"flex",isRequired:!0,isInvalid:e.errors.name&&e.touched.name,children:[S("name","Name"),(0,n.jsxs)(s.gCW,{align:"flex-start",w:"inherit",children:[(0,n.jsx)(s.IIB,{...t,autoComplete:"off",autoFocus:!0,color:"gray.700",placeholder:"Enter a friendly name for your new ".concat(b.human_readable," connection"),size:"sm","data-testid":"input-name"}),(0,n.jsx)(s.J1D,{children:e.errors.name})]}),(0,n.jsx)(s.kCb,{alignItems:"center",h:"32px",visibility:"hidden",children:(0,n.jsx)(s.ITP,{marginLeft:"8px"})})]})}}),(0,n.jsx)(m.gN,{id:"description",name:"description",children:e=>{let{field:i}=e;return(0,n.jsxs)(s.NIc,{display:"flex",children:[S("description","Description"),(0,n.jsx)(s.gxH,{...i,color:"gray.700",placeholder:"Enter a description for your new ".concat(b.human_readable," connection"),resize:"none",size:"sm",value:i.value||""}),(0,n.jsx)(s.kCb,{alignItems:"center",h:"32px",visibility:"hidden",children:(0,n.jsx)(s.ITP,{marginLeft:"8px"})})]})}}),(0,n.jsx)(m.gN,{id:"instance_key",name:"instance_key",validate:_,children:i=>{let{field:t}=i;return(0,n.jsxs)(s.NIc,{display:"flex",isRequired:!0,isInvalid:e.errors.instance_key&&e.touched.instance_key,children:[S("instance_key","Connection Identifier"),(0,n.jsxs)(s.gCW,{align:"flex-start",w:"inherit",children:[(0,n.jsx)(s.IIB,{...t,autoComplete:"off",color:"gray.700",isDisabled:!!(null==j?void 0:j.key),placeholder:"A unique identifier for your new ".concat(b.human_readable," connection"),size:"sm"}),(0,n.jsx)(s.J1D,{children:e.errors.instance_key})]}),(0,n.jsx)(s.ua7,{"aria-label":"The fides_key will allow fidesops to associate dataset field references appropriately. Must be a unique alphanumeric value with no spaces (underscores allowed) to represent this connection.",hasArrow:!0,label:"The fides_key will allow fidesops to associate dataset field references appropriately. Must be a unique alphanumeric value with no spaces (underscores allowed) to represent this connection.",placement:"right-start",openDelay:500,children:(0,n.jsx)(s.kCb,{alignItems:"center",h:"32px",children:(0,n.jsx)(s.ITP,{marginLeft:"8px",_hover:{cursor:"pointer"}})})})]})}}),Object.entries(i.properties).map(e=>{let[i,t]=e;return"advanced_settings"===i?null:I(i,t)}),(0,n.jsxs)(s.hE2,{size:"sm",spacing:"8px",variant:"outline",children:[(0,n.jsx)(s.zxk,{colorScheme:"gray.700",isDisabled:!(null==j?void 0:j.key),isLoading:C.isLoading||C.isFetching,loadingText:"Testing",onClick:R,variant:"outline",children:p}),(0,n.jsx)(s.zxk,{bg:"primary.800",color:"white",isDisabled:a,isLoading:a,loadingText:"Submitting",size:"sm",variant:"solid",type:"submit",_active:{bg:"primary.500"},_disabled:{opacity:"inherit"},_hover:{bg:"primary.400"},children:"Save"})]})]})})})},y=t(99377);let j=e=>{let{onConnectionCreated:i,data:t}=e,s=(0,p.I0)(),{errorAlert:a,successAlert:c}=(0,h.V)(),{handleError:m}=(0,u.HK)(),[f,g]=(0,l.useState)(!1),{connection:v,connectionOption:j}=(0,o.C)(r.ZZ),[b]=(0,x.pH)(),[k]=(0,x.Du)();return{isSubmitting:f,handleSubmit:async e=>{try{var l;g(!0);let o={access:d.uv.WRITE,connection_type:null==j?void 0:j.identifier,description:e.description,disabled:!1,key:(0,y.E)(e.instance_key),name:e.name},u=await b(o).unwrap();if((null===(l=u.failed)||void 0===l?void 0:l.length)>0)a(u.failed[0].message);else{let l={connection_key:u.succeeded[0].key,secrets:{}};Object.entries(t.properties).forEach(i=>{l.secrets[i[0]]=e[i[0]]});let o=await k(l).unwrap();"failed"===o.test_status?a((0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)("b",{children:"Message:"})," ",o.msg,(0,n.jsx)("br",{}),(0,n.jsx)("b",{children:"Failure Reason:"})," ",o.failure_reason]})):(s((0,r.lm)(u.succeeded[0])),c("Connector successfully ".concat((null==v?void 0:v.key)?"updated":"added","!")),(null==v?void 0:v.key)||!i||i())}}catch(e){m(e)}finally{g(!1)}},connectionOption:j}},b=e=>{let{data:i,onConnectionCreated:t,onTestConnectionClick:r}=e,{isSubmitting:a,handleSubmit:l,connectionOption:o}=j({onConnectionCreated:t,data:i});return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsxs)(s.xuv,{color:"gray.700",fontSize:"14px",h:"80px",children:["Connect to your ",o.human_readable," environment by providing the information below. Once you have saved the form, you may test the integration to confirm that it's working correctly."]}),(0,n.jsx)(v,{data:i,defaultValues:{description:"",instance_key:"",name:""},isSubmitting:a,onSaveClick:l,onTestConnectionClick:r})]})},k={description:"",instance_key:"",name:""},C=e=>{let{data:i,onConnectionCreated:t,onTestEmail:r}=e,{connectionOption:a,isSubmitting:l,handleSubmit:o}=j({onConnectionCreated:t,data:i});return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsxs)(s.xuv,{color:"gray.700",fontSize:"14px",h:"80px",children:["Configure your ",a.human_readable," connector by providing the connector name, description and a test email address. Once you have saved the details, you can click test email to check the format of the email."]}),(0,n.jsx)(v,{data:i,defaultValues:k,isSubmitting:l,onSaveClick:e=>{o(e)},onTestConnectionClick:r,testButtonLabel:"Test email"})]})};var _=t(16310),w=t(9699),S=t(47418),z=e=>{let{defaultValues:i,isSubmitting:t=!1,onSaveClick:l}=e,d=(0,a.useRouter)(),{connection:u,connectionOption:h}=(0,o.C)(r.ZZ);return(0,n.jsx)(m.J9,{initialValues:(()=>{if(null==u?void 0:u.key){var e;i.name=null!==(e=u.name)&&void 0!==e?e:"",i.description=u.description}return i})(),onSubmit:(e,i)=>{l(e,i)},validateOnBlur:!1,validateOnChange:!1,validationSchema:_.Ry().shape({name:_.Z_().required("Name is required")}),children:(0,n.jsx)(m.l0,{noValidate:!0,children:(0,n.jsxs)(s.gCW,{align:"stretch",gap:"16px",children:[(0,n.jsx)(w.Z,{autoFocus:!0,disabled:!!(null==u?void 0:u.key),isRequired:!0,label:"Name",name:"name",placeholder:"Enter a friendly name for your new ".concat(h.human_readable," connection")}),(0,n.jsx)(w.Z,{label:"Description",name:"description",placeholder:"Enter a description for your new ".concat(h.human_readable," connection"),type:"textarea"}),(0,n.jsx)(S.h,{isSubmitting:t,onCancelClick:()=>{d.push(c.JR)}})]})})})};let I=e=>{let{onConnectionCreated:i}=e,t=(0,p.I0)(),{errorAlert:a,successAlert:c}=(0,h.V)(),{handleError:m}=(0,u.HK)(),[f,g]=(0,l.useState)(!1),{connection:v,connectionOption:y}=(0,o.C)(r.ZZ),[j]=(0,x.pH)(),b=async(e,n)=>{try{var s;g(!0);let n={access:d.uv.WRITE,connection_type:null==y?void 0:y.identifier,description:e.description,disabled:!1,name:e.name,key:null==v?void 0:v.key},l=await j(n).unwrap();(null===(s=l.failed)||void 0===s?void 0:s.length)>0?a(l.failed[0].message):(t((0,r.lm)(l.succeeded[0])),c("Connector successfully ".concat((null==v?void 0:v.key)?"updated":"added","!")),(null==v?void 0:v.key)||!i||i())}catch(e){m(e)}finally{g(!1)}};return(0,n.jsxs)(s.gCW,{align:"stretch",gap:"16px",children:[(0,n.jsxs)(s.xuv,{color:"gray.700",fontSize:"14px",children:["To begin setting up your new ",y.human_readable," ","connector you must first assign a name to the connector and a description.",(0,n.jsx)("br",{}),(0,n.jsx)("br",{}),"Once you have completed this section you can then progress onto"," ",(0,n.jsx)(s.xvT,{display:"inline-block",fontWeight:"700",children:"DSR customization"})," ","using the menu on the left hand side."]}),(0,n.jsx)(z,{defaultValues:{description:"",name:""},isSubmitting:f,onSaveClick:b})]})},R=e=>{let{data:i,onConnectionCreated:t,onTestConnectionClick:a}=e,c=(0,p.I0)(),{errorAlert:m,successAlert:f}=(0,h.V)(),{handleError:g}=(0,u.HK)(),[j,b]=(0,l.useState)(!1),{connection:k,connectionOption:C}=(0,o.C)(r.ZZ),[_]=(0,x.pL)(),[w]=(0,x.pH)(),[S]=(0,x.Du)(),z=async(e,s)=>{try{if(b(!0),k){var a;let t={access:d.uv.WRITE,connection_type:k.connection_type,description:e.description,disabled:!1,key:k.key,name:e.name},s=await w(t).unwrap();if((null===(a=s.failed)||void 0===a?void 0:a.length)>0)m(s.failed[0].message);else{c((0,r.lm)(s.succeeded[0]));let t={connection_key:k.key,secrets:{}};Object.entries(i.properties).forEach(i=>{t.secrets[i[0]]=e[i[0]]});let a=await S(t).unwrap();"failed"===a.test_status?m((0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)("b",{children:"Message:"})," ",a.msg,(0,n.jsx)("br",{}),(0,n.jsx)("b",{children:"Failure Reason:"})," ",a.failure_reason]})):f("Connector successfully updated!")}}else{let n={description:e.description,name:e.name,instance_key:(0,y.E)(e.instance_key),saas_connector_type:C.identifier,secrets:{}};Object.entries(i.properties).forEach(i=>{n.secrets[i[0]]=e[i[0]]});let s=await _(n).unwrap();c((0,r.lm)(s.connection)),f("Connector successfully added!"),null==t||t()}}catch(e){g(e)}finally{b(!1)}};return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsxs)(s.xuv,{color:"gray.700",fontSize:"14px",h:"80px",children:["Connect to your ",C.human_readable," environment by providing the information below. Once you have saved the form, you may test the integration to confirm that it's working correctly."]}),(0,n.jsx)(v,{data:i,defaultValues:{description:"",instance_key:"",name:""},isSubmitting:j,onSaveClick:z,onTestConnectionClick:a})]})};var Z=t(94167);let T=e=>{var i,t;let{response:a}=e,{connectionOption:l}=(0,o.C)(r.ZZ);return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(s.izJ,{color:"gray.100"}),(0,n.jsxs)(s.gCW,{align:"flex-start",mt:"16px",children:[(null===(i=a.data)||void 0===i?void 0:i.test_status)==="succeeded"&&(0,n.jsxs)(n.Fragment,{children:[(0,n.jsxs)(s.Ugi,{children:[(0,n.jsxs)(s.X6q,{as:"h5",color:"gray.700",size:"xs",children:["Successfully connected to ",l.human_readable]}),(0,n.jsx)(s.Vp9,{colorScheme:"green",size:"sm",variant:"solid",children:"Success"})]}),(0,n.jsx)(s.xvT,{color:"gray.500",fontSize:"sm",mt:"12px !important",children:(0,Z.p6)(a.fulfilledTimeStamp)}),(0,n.jsx)(s.xuv,{bg:"green.100",border:"1px solid",borderColor:"green.300",color:"green.700",mt:"16px",borderRadius:"6px",children:(0,n.jsxs)(s.Ugi,{alignItems:"flex-start",margin:["14px","17px","14px","17px"],children:[(0,n.jsx)(s.StI,{}),(0,n.jsxs)(s.xuv,{children:[(0,n.jsx)(s.X6q,{as:"h5",color:"green.500",fontWeight:"semibold",size:"xs",children:"Success message:"}),(0,n.jsx)(s.xvT,{color:"gray.700",fontSize:"sm",fontWeight:"400",children:a.data.msg})]})]})})]}),(null===(t=a.data)||void 0===t?void 0:t.test_status)==="failed"&&(0,n.jsxs)(n.Fragment,{children:[(0,n.jsxs)(s.Ugi,{children:[(0,n.jsxs)(s.X6q,{as:"h5",color:"gray.700",size:"xs",children:["Output error to ",l.human_readable]}),(0,n.jsx)(s.Vp9,{colorScheme:"red",size:"sm",variant:"solid",children:"Error"})]}),(0,n.jsx)(s.xvT,{color:"gray.500",fontSize:"sm",mt:"12px !important",children:(0,Z.p6)(a.fulfilledTimeStamp)}),(0,n.jsx)(s.xuv,{bg:"red.50",border:"1px solid",borderColor:"red.300",color:"red.300",mt:"16px",borderRadius:"6px",children:(0,n.jsxs)(s.Ugi,{alignItems:"flex-start",margin:["14px","17px","14px","17px"],children:[(0,n.jsx)(s.f9v,{}),(0,n.jsxs)(s.xuv,{children:[(0,n.jsx)(s.X6q,{as:"h5",color:"red.500",fontWeight:"semibold",size:"xs",children:"Error message:"}),(0,n.jsx)(s.xvT,{color:"gray.700",fontSize:"sm",fontWeight:"400",children:a.data.failure_reason}),(0,n.jsx)(s.xvT,{color:"gray.700",fontSize:"sm",fontWeight:"400",children:a.data.msg})]})]})})]})]})]})},E=e=>{let{onConnectionCreated:i}=e,t=(0,a.useRouter)(),{connectionOption:u}=(0,o.C)(r.ZZ),h=u&&u.type===d.Zi.MANUAL,{data:x,isFetching:p,isLoading:m,isSuccess:f}=(0,r.n3)(u.identifier,{skip:h}),[g,v]=(0,l.useState)(),y=e=>{v(e)},j=(0,l.useCallback)(()=>{t.push(c.JR)},[t]),k=(0,l.useCallback)(()=>{switch(null==u?void 0:u.type){case d.Zi.DATABASE:if(f&&x)return(0,n.jsx)(b,{data:x,onConnectionCreated:i,onTestConnectionClick:y});break;case d.Zi.MANUAL:return(0,n.jsx)(I,{onConnectionCreated:i});case d.Zi.SAAS:if(f&&x)return(0,n.jsx)(R,{data:x,onConnectionCreated:i,onTestConnectionClick:y});break;case d.Zi.EMAIL:if(f&&x)return(0,n.jsx)(C,{data:x,onConnectionCreated:j,onTestEmail:y})}},[null==u?void 0:u.type,x,f,i,j]);return(0,n.jsxs)(s.kCb,{gap:"97px",children:[(0,n.jsxs)(s.gCW,{w:"579px",gap:"16px",align:"stretch",children:[(p||m)&&(0,n.jsx)(s.M5Y,{children:(0,n.jsx)(s.$jN,{})}),k()]}),g&&(0,n.jsxs)(s.Rg9,{in:!0,children:[" ",(0,n.jsx)(s.xuv,{mt:"16px",maxW:"528px",w:"fit-content",children:(0,n.jsx)(T,{response:g})})]})]})}},4894:function(e,i,t){t.d(i,{Z:function(){return j}});var n=t(24246),r=t(65399),s=t(69728),a=t(7564),l=t(13054),o=t(86677),c=t(27378),d=t(44296),u=t(60136),h=t(11032),x=t(52987),p=t(75139),m=t(66527),f=t(12719),g=t(50558),v=e=>{let{data:i=[],isSubmitting:t=!1,onSubmit:r,onCancel:s,disabled:a}=e,o=(0,c.useRef)(null),{errorAlert:d}=(0,p.V)(),u=i.length>0?m.ZP.dump(i):void 0,[h,v]=(0,c.useState)(void 0),[y,j]=(0,c.useState)(!1),[b,k]=(0,c.useState)(!u),C=(0,l.qY0)(),{data:_}=(0,x.NR)(),[w,S]=(0,c.useState)([]),z=e=>{m.ZP.load(e,{json:!0}),v(void 0)},I=()=>{let e=o.current.getValue();r(m.ZP.load(e,{json:!0})),S([])};return(0,n.jsxs)(l.kCb,{gap:"97px",children:[(0,n.jsxs)(l.gCW,{align:"stretch",w:"800px",children:[(0,n.jsx)(f.M,{defaultLanguage:"yaml",defaultValue:u,height:"calc(100vh - 526px)",onChange:e=>{try{j(!0),z(e),k(!!(!e||""===e.trim()))}catch(e){(0,f.F)(e)?v(e):d("Could not parse the supplied YAML")}},onMount:(e,i)=>{o.current=e,o.current.focus()},options:{fontFamily:"Menlo",fontSize:13,minimap:{enabled:!0},readOnly:a},theme:"light"}),(0,n.jsxs)(l.hE2,{size:"sm",children:[s?(0,n.jsx)(l.zxk,{onClick:s,children:"Cancel"}):null,(0,n.jsx)(l.zxk,{colorScheme:"primary",isDisabled:a||b||!!h||t,isLoading:t,loadingText:"Saving",onClick:()=>{if(_&&_.length){let e=o.current.getValue(),i=_.filter(i=>e.includes("fides_key: ".concat(i.fides_key,"\n"))).map(e=>e.fides_key);if(S(i),i.length){C.onOpen();return}}I()},type:"submit","data-testid":"save-yaml-btn",width:"fit-content",children:"Save"})]})]}),y&&(b||h)&&(0,n.jsx)(g.Z,{isEmptyState:b,yamlError:h}),(0,n.jsx)(l.cVQ,{isOpen:C.isOpen,onClose:C.onClose,onConfirm:()=>{I(),C.onClose()},title:"Overwrite dataset",message:(0,n.jsxs)(n.Fragment,{children:[(0,n.jsxs)(l.xvT,{children:["You are about to overwrite the dataset",w.length>1?"s":""," ",w.map((e,i)=>{let t=i===w.length-1;return(0,n.jsxs)(c.Fragment,{children:[(0,n.jsx)(l.xvT,{color:"complimentary.500",as:"span",fontWeight:"bold",children:e}),t?".":", "]},e)})]}),(0,n.jsx)(l.xvT,{children:"Are you sure you would like to continue?"})]})})]})};let y=e=>{let{children:i,...t}=e;return(0,n.jsx)(l.xvT,{color:"gray.700",fontSize:"14px",...t,children:i})};var j=()=>{let e=(0,o.useRouter)(),{errorAlert:i,successAlert:t}=(0,r.VY)(),{handleError:p}=(0,r.HK)(),[m,f]=(0,c.useState)(!1),{connection:g}=(0,d.C)(s.ZZ),{data:j,isFetching:b,isLoading:k,isSuccess:C}=(0,a.Eg)(g.key),[_]=(0,a.Lz)(),[w]=(0,x.EG)(),{data:S,isLoading:z,error:I}=(0,x.NR)(),[R,Z]=(0,c.useState)(void 0);(0,c.useEffect)(()=>{j&&j.items.length&&Z(j.items[0].ctl_dataset.fides_key)},[j]);let T=()=>{e.push(h.JR)},E=async n=>{var r;let s={connection_key:null==g?void 0:g.key,dataset_pairs:n},a=await _(s).unwrap();(null===(r=a.failed)||void 0===r?void 0:r.length)>0?i(a.failed[0].message):t("Dataset successfully updated!"),e.push(h.JR)},W=async()=>{if(R)try{let e=R;j&&j.items.length&&(e=j.items[0].fides_key);let i=[{fides_key:e,ctl_dataset_fides_key:R}];E(i)}catch(e){p(e)}},F=async e=>{try{f(!0);let t=Array.isArray(e)?e:[e],n=await w(t);if("error"in n){let e=(0,u.e$)(n.error);i(e);return}let r=t.map(e=>({fides_key:e.fides_key,ctl_dataset_fides_key:e.fides_key}));if(j&&j.items.length){let{items:e}=j;r=e.map((e,i)=>({fides_key:e.fides_key,ctl_dataset_fides_key:t[i].fides_key}))}E(r)}catch(e){p(e)}finally{f(!1)}},q=""!==R&&void 0!==R;if(b||k||z&&!I)return(0,n.jsx)(l.M5Y,{children:(0,n.jsx)(l.$jN,{})});let L=S&&S.length;return(0,n.jsxs)(l.gCW,{alignItems:"left",children:[I?(0,n.jsx)(y,{mb:4,color:"red",children:"There was a problem loading existing datasets, please try again."}):null,(0,n.jsxs)(l.Ugi,{spacing:8,mb:4,children:[L?(0,n.jsxs)(n.Fragment,{children:[(0,n.jsxs)(l.gCW,{alignSelf:"start",mr:4,children:[(0,n.jsxs)(l.xuv,{"data-testid":"dataset-selector-section",mb:4,children:[(0,n.jsx)(y,{mb:4,children:"Choose a dataset to associate with this connector."}),(0,n.jsx)(l.PhF,{size:"sm",width:"fit-content",placeholder:"Select",onChange:e=>{Z(e.target.value)},value:R,"data-testid":"dataset-selector",children:S.map(e=>(0,n.jsx)("option",{value:e.fides_key,children:e.fides_key},e.fides_key))})]}),(0,n.jsx)(l.zxk,{size:"sm",colorScheme:"primary",alignSelf:"start",isDisabled:!q,onClick:W,"data-testid":"save-dataset-link-btn",children:"Save"})]}),(0,n.jsx)(y,{children:"or"})]}):null,(0,n.jsxs)(l.xuv,{"data-testid":"yaml-editor-section",children:[(0,n.jsx)(y,{mb:4,children:"View your dataset YAML below!"}),C&&(null==j?void 0:j.items)?(0,n.jsx)(v,{data:j.items.map(e=>e.ctl_dataset),isSubmitting:m,onSubmit:F,disabled:q,onCancel:L?void 0:T}):null]})]}),L?(0,n.jsx)(l.zxk,{width:"fit-content",size:"sm",variant:"outline",onClick:T,children:"Cancel"}):null]})}},99377:function(e,i,t){t.d(i,{E:function(){return n},S:function(){return r}});let n=e=>e.toLowerCase().replace(/ /g,"_"),r=(e,i)=>{let t="".concat(window.location.origin+i,"&key=").concat(e);window.location.href.toLowerCase()!==t.toLowerCase()&&window.history.replaceState(null,"",t)}},47418:function(e,i,t){t.d(i,{h:function(){return s}});var n=t(24246),r=t(13054);t(27378);let s=e=>{let{isSubmitting:i=!1,onCancelClick:t}=e;return(0,n.jsxs)(r.hE2,{size:"sm",spacing:"8px",variant:"outline",children:[(0,n.jsx)(r.zxk,{onClick:t,variant:"outline",children:"Cancel"}),(0,n.jsx)(r.zxk,{bg:"primary.800",color:"white",isDisabled:i,isLoading:i,loadingText:"Submitting",size:"sm",variant:"solid",type:"submit",_active:{bg:"primary.500"},_disabled:{opacity:"inherit"},_hover:{bg:"primary.400"},children:"Save"})]})}},89468:function(e,i,t){t.d(i,{Z:function(){return j}});var n=t(24246),r=t(65399),s=t(69728),a=t(7564),l=t(13054),o=t(86677),c=t(27378),d=t(44296),u=t(11032),h=t(34090),x=t(16310),p=t(34803),m=t(47411),f=t(35249),g=t(9699),v=t(47418),y=e=>{let{data:i=[],isSubmitting:t=!1,onSaveClick:s}=e,{isLoading:a}=(0,m.MO)(),c=(0,d.C)(f.qb),y=(0,o.useRouter)(),{errorAlert:j}=(0,r.VY)(),b=()=>{y.push(u.JR)};return a?null:(0,n.jsx)(h.J9,{enableReinitialize:!0,initialValues:{fields:i.length>0?i:[{pii_field:"",dsr_package_label:"",data_categories:[]}]},onSubmit:(e,i)=>{if(new Set(e.fields.map(e=>e.pii_field)).size<e.fields.length){j("PII Field must be unique");return}s(e,i)},validateOnBlur:!1,validateOnChange:!1,validationSchema:x.Ry({fields:x.IX().of(x.Ry().shape({pii_field:x.Z_().required("PII Field is required").min(1,"PII Field must have at least one character").max(200,"PII Field has a maximum of 200 characters").label("PII Field"),dsr_package_label:x.Z_().required("DSR Package Label is required").min(1,"DSR Package Label must have at least one character").max(200,"DSR Package Label has a maximum of 200 characters").label("DSR Package Label"),data_categories:x.IX(x.Z_()).label("Data Categories")}))}),children:e=>(0,n.jsx)(h.l0,{style:{marginTop:0},noValidate:!0,children:(0,n.jsx)(l.gCW,{align:"stretch",children:(0,n.jsx)(h.F2,{name:"fields",render:i=>{let{fields:r}=e.values;return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsxs)(l.Ugi,{color:"gray.900",flex:"1",fontSize:"14px",fontWeight:"semibold",lineHeight:"20px",mb:"6px",spacing:"24px",children:[(0,n.jsx)(l.xuv,{w:"416px",children:"PII Field"}),(0,n.jsx)(l.xuv,{w:"416px",children:"DSR Package Label"}),(0,n.jsx)(l.xuv,{w:"416px",children:"Data Categories"}),(0,n.jsx)(l.xuv,{visibility:"hidden",children:(0,n.jsx)(l.lr0,{})})]}),(0,n.jsx)(l.xuv,{children:r&&r.length>0?r.map((e,t)=>(0,n.jsxs)(l.Ugi,{mt:t>0?"12px":void 0,spacing:"24px",align:"flex-start",children:[(0,n.jsx)(l.xuv,{minH:"57px",w:"416px",children:(0,n.jsx)(g.Z,{autoFocus:0===t,displayHelpIcon:!1,isRequired:!0,name:"fields.".concat(t,".pii_field")})}),(0,n.jsx)(l.xuv,{minH:"57px",w:"416px",children:(0,n.jsx)(g.Z,{displayHelpIcon:!1,isRequired:!0,name:"fields.".concat(t,".dsr_package_label")})}),(0,n.jsx)(l.xuv,{minH:"57px",w:"416px",children:(0,n.jsx)(p.AP,{name:"fields.".concat(t,".data_categories"),options:c.map(e=>({value:e.fides_key,label:e.fides_key})),isRequired:!0,isMulti:!0})}),(0,n.jsx)(l.xuv,{h:"57px",visibility:t>0?"visible":"hidden",children:(0,n.jsx)(l.lr0,{onClick:()=>i.remove(t),_hover:{cursor:"pointer"}})})]},t)):null}),(0,n.jsx)(l.xvT,{color:"complimentary.500",fontWeight:"medium",fontSize:"sm",mb:"24px !important",mt:"24px !important",onClick:()=>{i.push({pii_field:"",dsr_package_label:"",data_categories:[]})},_hover:{cursor:"pointer"},children:"Add new PII field"}),(0,n.jsx)(v.h,{isSubmitting:t,onCancelClick:b})]})}})})})})},j=()=>{let e=(0,c.useRef)(!1),i=(0,o.useRouter)(),{successAlert:t}=(0,r.VY)(),{handleError:h}=(0,r.HK)(),[x,p]=(0,c.useState)(!1),[m,f]=(0,c.useState)([]),{connection:g}=(0,d.C)(s.ZZ),{data:v,isFetching:j,isLoading:b,isSuccess:k}=(0,a.QV)(g.key),[C]=(0,a.jF)(),[_]=(0,a._d)(),w=async(e,n)=>{try{p(!0);let n={connection_key:null==g?void 0:g.key,body:{...e}};m.length>0?await _(n).unwrap():await C(n).unwrap(),t("DSR customization ".concat(m.length>0?"updated":"added","!")),i.push(u.JR)}catch(e){h(e)}finally{p(!1)}};return(0,c.useEffect)(()=>(e.current=!0,k&&v&&f(v.fields),()=>{e.current=!1}),[v,k]),(0,n.jsxs)(l.gCW,{align:"stretch",gap:"16px",children:[(0,n.jsx)(l.xuv,{color:"gray.700",fontSize:"14px",w:"572px",children:"Customize your PII fields to create a friendly label name for your privacy request packages. This “Package Label” is the label your user will see in their downloaded package."}),(j||b)&&(0,n.jsx)(l.M5Y,{children:(0,n.jsx)(l.$jN,{})}),e.current&&!b?(0,n.jsx)(y,{data:m,isSubmitting:x,onSaveClick:w}):null]})}}}]);